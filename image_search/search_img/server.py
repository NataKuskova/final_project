from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import asyncio
import asyncio_redis
import logging
import json


FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
         u'[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)  # filename=u'../logs.log'


# tags = {}


class WebSocketFactory(WebSocketServerFactory):
    """
    Class for asyncio-based WebSocket server factories.
    """

    _tags = {}

    def register_client(self, tag, id_connection, instance):
        """
        Adds a client to a list.

        Args:
            id_connection: Address of the client.
            instance: Instance of the class Server Protocol.
        """
        # self._tags[tag].setdefault(id_connection, instance)
        # self._tags.setdefault(tag, {id_connection: instance})
        if tag not in self._tags:
            self._tags[tag] = [{id_connection: instance}]
        else:
            tags = self._tags[tag]
            self._tags[tag] = []
            self._tags[tag] = tags
            self._tags[tag] += [{id_connection: instance}]
        print(self._tags)

    def get_client(self, tag):
        """
        Receives the client instance.

        Args:
            id_connection: Address of the client.

        Returns:
            The client instance.
        """
        return self._tags[tag]

    def unregister_client(self, id_connection):
        """
        Removes the client from the list when a connection is closed.

        Args:
             id_connection: Address of the client.
        """
        # self._tags = {k: v for k, v in self._tags.items() if not v}
        for tag, client in self._tags.items():
            if id_connection in client:
                del(self._tags[tag][id_connection])

        logging.info('Connection {0} is closed.'.format(id_connection))


class ServerProtocol(WebSocketServerProtocol):
    """
    Class for asyncio-based WebSocket server protocols.
    """

    def onConnect(self, request):
        """
        Callback fired during WebSocket opening handshake when a client
        connects (to a server with request from client) or when server
        connection established (by a client with response from server).
        This method may run asynchronous code.

        Adds a client to a list.

        Args:
            request: WebSocket connection request information.
        """
        logging.info("Client connecting: {0}".format(request.peer))
        # self.factory.register_client(request.peer, self)
        # global tags
        # tags = request.peer

    def onOpen(self):
        """
        Callback fired when the initial WebSocket opening handshake was
        completed.

        Sends a WebSocket message to the client with its address.
        """
        logging.info("WebSocket connection open.")
        # self.sendMessage(clients.encode('utf8'), False)

    def onMessage(self, payload, isBinary):
        """
        Callback fired when a complete WebSocket message was received.

        Saved the client address.

        Args:
            payload: The WebSocket message received.
            isBinary: `True` if payload is binary, else the payload
            is UTF-8 encoded text.
        """
        logging.info("Message received: {0}".format(payload.decode('utf8')))

        # self.sendMessage(payload, isBinary)
        # global clients
        # clients = payload.decode('utf8')
        self.factory.register_client(payload.decode('utf8'), self.peer, self)

    def onClose(self, wasClean, code, reason):
        """
        Callback fired when the WebSocket connection has been closed
        (WebSocket closing handshake has been finished or the connection
        was closed uncleanly).

        Removes the client from the list.

        Args:
            wasClean: `True` if the WebSocket connection was closed cleanly.
            code: Close status code as sent by the WebSocket peer.
            reason: Close reason as sent by the WebSocket peer.
        """
        factory.unregister_client(self.peer)
        logging.info("WebSocket connection closed: {0}".format(reason))


@asyncio.coroutine
def run_subscriber():
    """
    Asynchronous Redis client. Start a pubsub listener.
    It receives signals from the spiders and sends a message to the client.
    """

    # Create connection
    connection = yield from asyncio_redis.Connection.create(
        host='localhost', port=6379)

    # Create subscriber.
    subscriber = yield from connection.start_subscribe()

    # Subscribe to channel.
    yield from subscriber.subscribe(['spiders'])

    spiders = []
    # Inside a while loop, wait for incoming events.
    while True:
        reply = yield from subscriber.next_published()
        # print(reply.value)
        # print(json.loads(reply.value))
        spiders.append(json.loads(reply.value))
        if spiders:
            # if clients is not None:
            for spider in spiders:
            # print(spiders[0]['tag'])
                # for tag in spider['tag']:
                    # print('tag')
                    # print(tag)
                tags = factory.get_client(spider['tag'])
                for clients in tags:
                    for client in clients:
                        clients[client].sendMessage('ok'.encode('utf8'), False)

            # tags.clear()
            # spiders.clear()
            """
                try:
                    if 'google' in spiders:
                        # and 'yandex' in spiders \
                        # and 'instagram' in spiders:
                        factory.get_client(clients).sendMessage(
                            'ok'.encode('utf8'), False)
                        spiders.clear()
                    # elif 'google' in spiders:
                    #     factory.get_client(client_id).sendMessage(
                    #         'google'.encode('utf8'), False)
                    # elif 'yandex' in spiders:
                    #     factory.get_client(client_id).sendMessage(
                    #         'yandex'.encode('utf8'), False)
                    # elif 'instagram' in spiders:
                    #     factory.get_client(client_id).sendMessage(
                    #         'instagram'.encode('utf8'), False)
                except:
                    factory.get_client(clients).sendMessage(
                        'error'.encode('utf8'), False)
            """

        logging.info('Received: ' + repr(reply.value) + ' on channel ' +
                     reply.channel)


    # When finished, close the connection.
    connection.close()


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        import trollius as asyncio

    factory = WebSocketFactory(u"ws://127.0.0.1:9000")
    factory.protocol = ServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    web_socket_server = loop.run_until_complete(coro)
    subscriber_server = loop.run_until_complete(run_subscriber())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        web_socket_server.close()
        subscriber_server.close()
        loop.close()

