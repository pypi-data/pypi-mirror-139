import random, atexit, time, threading
from uuid import UUID, uuid4
from typing import Awaitable, NamedTuple
from signal import SIGTERM, SIGINT
from asyncio import run, get_event_loop, create_task
from asyncio import wait, Event, Queue, Task, sleep
from asyncio import FIRST_COMPLETED
from websockets import serve
from websockets.legacy.protocol import WebSocketCommonProtocol 
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from argparse import ArgumentParser

from .common import Message, Connection

class QueuedItem(NamedTuple):
    msg: Message
    timestamp: int
    def __repr__(self):
        elements = [
            str(self.msg),
            self.timestamp
        ]
        return f"<QueuedItem({', '.join([str(e) for e in elements])})>"

class Endpoint(NamedTuple):
    name: str
    queue: Queue
    size: int = None
    def __repr__(self):
        elements = [
            self.name,
            str(self.queue.qsize()),
            str(self.size)
        ]
        return f"<Endpoint({', '.join([str(e) for e in elements])})>"

class Channel(NamedTuple):
    name: str
    queue: Queue
    priority: int = 0
    size: int = None
    def __repr__(self):
        elements = [
            self.name + ":" + str(self.priority),
            str(self.queue.qsize()),
            str(self.size)
        ]
        return f"<Channel({', '.join([str(e) for e in elements])})>"


class Router(object):

    def __init__(self, debug: bool = False):
        self._debug = debug
        self.qsize = 100000
        self.channels: dict[str, Channel] = {}
        self.endpoints: dict[str, Endpoint] = {}
        self.forwarders: dict[str, Task] = {}
        self.routes: dict[Channel, set[Endpoint]] = {}
        self.replies: dict[bytes, Endpoint] = {}
        atexit.register(self._cleanup)

    def _cleanup(self):
        for _, task in self.forwarders.items():
            if not task.cancelled():
                task.cancel()

    async def _forwarder(self, channel: str, hook: Awaitable = None):
        print(f"* Starting message forwarder for '{channel}'")
        src = self.channels[channel]
        # if src.name == 'system':
        #     system = System(self, self._debug)
        # else:
        #     system = None
        while True:
            # get next message in src Queue
            item: QueuedItem = await src.queue.get()
            if self._debug:
                print(f"Pulled message {UUID(bytes=item.msg.uid).hex} from '{src}")
            forward = True
            # process hook
            if hook:
                try:
                    forward = await hook(item.msg)
                except Exception as e:
                    print(f"Exception in '{channel}' hook: {e}")
                    pass
            # put message in dests Queues
            # if self._debug:
            #     print(f"{dests} {forward}")
            if forward:
                dests = set(self.route(src))
                if item.msg.reference and item.msg.reference in self.replies:
                    endpoint = self.replies.pop(item.msg.reference)
                    dests.add(endpoint)
                    if self._debug:
                        print(f"Adding endpoint {endpoint} to {channel} for {UUID(bytes=item.msg.reference).hex}")
                for endpoint in dests:
                    if self._debug:
                        print(f"Forwarding {UUID(bytes=item.msg.uid).hex} from '{channel}' to '{endpoint.name}'")
                    if endpoint.queue.full():
                        await endpoint.queue.get()
                        endpoint.queue.task_done()
                    await endpoint.queue.put(item)
                    # if self._debug:
                    #     print([UUID(bytes=m.uid).hex for m in list(endpoint.queue._queue)])
    
    def forward(self, channel: str, hook: Awaitable = None):
        task = create_task(self._forwarder(channel, hook))
        task.set_name(f"Forwarder:{channel}")
        self.forwarders[channel] = task

    def channel(self, name: str, create: bool = False, hook: Awaitable = None) -> Channel:
        '''
        Get channel by name, optionally creating if needed
        '''
        if name in self.channels:
            return self.channels[name]
        else:
            if create:
                print(f"Creating channel '{name}'")
                self.channels[name] = Channel(name, Queue(self.qsize))
                self.forward(name, hook)
                return self.channels[name]
            else:
                return None

    def endpoint(self, name: str, create: bool = False) -> Endpoint:
        '''
        Get endpoint by name, optionally creating if needed
        '''
        if name in self.endpoints:
            return self.endpoints[name]
        else:
            if create:
                print(f"Creating endpoint '{name}'")
                self.endpoints[name] = Endpoint(name, Queue(self.qsize))
                return self.endpoints[name]
            else:
                return None

    def route(self, src: Channel, dest: Endpoint = None) -> set[Endpoint]:
        '''
        Get route or add dest to route
        '''
        if src not in self.routes:
            self.routes[src] = set()
        if not dest:
            return self.routes[src]
        else:
            dests = self.routes[src]
            dests.add(dest)
            print(f"Added '{src.name}' -> '{dest.name}' route")

    def unroute(self, src: Channel, dest: Endpoint):
        '''
        Remove dest from route
        '''
        if src in self.routes and dest in self.routes[src]:
            self.routes[src].remove(dest)
            print(f"Removed '{src.name}' -> '{dest.name}' route")

class System(object):

    def __init__(self, router: Router, debug: bool = False):
        self._debug = debug
        self._router = router
        router.channel('system', create=True, hook=self._on_forward)
    
    async def _on_forward(self, msg: Message) -> bool:
        if self._debug:
            print(f"System message {msg} {msg.data}")
        if msg.subject == 'subscribe.channel':
            if len(msg.data) == 3:
                endpoint, channel, subject = msg.data
                # lookup or create src and dest
                src = self._router.channel(channel, create=True)
                dest = self._router.endpoint(endpoint, create=True)
                # add src -> dest route
                self._router.route(src, dest)
        elif msg.subject == 'subscribe.message':
            if len(msg.data) == 2:
                endpoint, uid = msg.data
                # lookup dest
                dest = self._router.endpoint(endpoint, create=True)
                # add src -> dest route for uid
                self._router.replies[uid] = dest
                if self._debug:
                    print(f"Added {dest} for {UUID(bytes=uid).hex}")
        elif msg.subject == 'unsubscribe.channel':
            if len(msg.data) == 2:
                endpoint, channel = msg.data
                # lookup src and dest
                src = self._router.channel(channel, create=True)
                dest = self._router.endpoint(endpoint, create=True)
                # remove dest from map for src
                if src and dest:
                    self._router.unroute(src, dest)
        return True


class Server(object):

    def __init__(self, host: str, port: int, key: str, stats = False, debug=False):
        self.host = host
        self.port = port
        self.key = key
        self._stats = stats
        self._debug = debug
        self._stop = None
        self._threaded = None
    
    async def _handler(self, conn: Connection, name: str, router: Router):
        print(f"* Starting {conn.id} handler for '{name}'")
        endpoint = router.endpoint(name, create=True)
        async def ingress():
            while True:
                # get next inbound message
                msg: Message = await conn.recv()
                # lookup channel by name
                # creating channel if needed
                # put message into channel queue
                channel = router.channel(msg.channel, create=True)
                if channel.queue.full():
                    await channel.queue.get()
                await channel.queue.put(QueuedItem(msg, int(time.time())))
                if self._debug:
                    print(f"Message {UUID(bytes=msg.uid).hex} queued into {router.channel(msg.channel)}")
        async def egress():
            try:
                while True:
                    # get next outbound message
                    item: QueuedItem = await endpoint.queue.get()
                    # send to remote node
                    await conn.send(item.msg)
                    endpoint.queue.task_done()
            except Exception as e:
                print(e)
                raise
        # start communcation tasks and wait until finished
        pending = []
        try:
            done, pending = await wait({
                create_task(ingress()),
                create_task(egress())
            }, return_when=FIRST_COMPLETED)
            for task in done:
                exc = task.exception()
                if exc and not isinstance(exc, ConnectionClosedOK):
                    print(f"* Exception: {exc}")
        finally: 
            for task in pending:
                task.cancel()
            await conn.close()

        print(f"* Stopping {conn.id} handler for '{name}'")

    async def main(self):
        
        self._loop = get_event_loop()
        self._stop = Event()
        if not self._threaded:
            self._loop.add_signal_handler(SIGINT, self._stop.set)
            self._loop.add_signal_handler(SIGTERM, self._stop.set)
        
        random.seed()
        router = Router(self._debug)
        System(router, self._debug)

        async def dispatch(ws: WebSocketCommonProtocol, uri: str):
            print(f"* New connection for {uri} using {router}")
            _, name = uri.split('/')
            if len(name):
                await self._handler(Connection(ws, self._debug), name, router)
                await sleep(0.1)

        async def stat_task(interval: int):
            while True:
                await sleep(interval)
                print("- Channels ------")
                for _, channel in router.channels.items():
                    print(f"{channel}")
                    if channel.name == 'system':
                        for m in list(channel.queue._queue):
                            print(f"- {m}")
                print("- Endpoints -----")
                for _, endpoint in router.endpoints.items():
                    print(f"{endpoint}")
                print("=================")

        async def expire_task(interval: int, maxage: int):
            print(f"* Starting message expiration of {maxage} seconds...")
            while True:
                await sleep(interval)
                now = int(time.time())
                if self._debug:
                    print(f"Starting expiration check for {now}")
                for _, endpoint in router.endpoints.items():
                    for item in list(endpoint.queue._queue):
                        if (now - item.timestamp) > maxage:
                            try:
                                endpoint.queue._queue.remove(item)
                                endpoint.queue.task_done()
                                if self._debug:
                                    print(f"Expiring {UUID(bytes=item.msg.uid).hex}")
                            except:
                                pass

        create_task(expire_task(1, 60))
        if self._stats:
            create_task(stat_task(10))
        
        # dispatch any incoming connections
        async with serve(dispatch, self.host, self.port):
            print(f"** Listening on {self.host}:{self.port}")
            try:
                print("* Waiting for shutdown signal...")
                await self._stop.wait()
                print("* Shutdown signal!")
                await sleep(0.1)
            except Exception as e:
                print(f"Exception: {e}")
            print(f"** Server shutdown!")

    def run(self):
        if threading.current_thread() is threading.main_thread():
            self._threaded = False
        else:
            self._threaded = True
        run(self.main())

    def stop(self):
        self._stop.set()


class ServerThread(threading.Thread):

    def __init__(self, host: str = 'localhost', port: int = 1234, key: str = None, debug=False):
        super().__init__(None, None, 'MessageServer')
        self.name = 'MessageServer'
        self.daemon = True
        self.host = host
        self.port = port
        self.key = key
        self.debug = debug

    def run(self):
        self._server = Server(self.host, self.port, self.key, self.debug)
        self._server.run()

    def stop(self):
        self._server._loop.call_soon_threadsafe(self._server.stop)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--key', type=str, default='abc123')
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=1234)
    parser.add_argument('--stats', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    Server(args.host, args.port, args.key, args.stats, args.debug).run()
    # server = ServerThread(args.host, args.port, args.key, args.debug)
    # server.start()
    # def cleanup():
    #     server.stop()
    #     server.join()
    # atexit.register(cleanup)
    # while True:
    #     time.sleep(10)
