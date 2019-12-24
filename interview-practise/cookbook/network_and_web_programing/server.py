from threading import Thread
from socketserver import BaseRequestHandler, TCPServer

NWORKERS = 16

def EchoHandler(BaseRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(5120)
            if not msg:
                break
        self.request.send(b'recv finished')


# if __name__ == '__main__':
#     sevrer = TCPServer(('localhost', 20000), EchoHandler)
#     for n in range(NWORKERS):
#         t = Thread(target=server.serve_forever)
#         t.daemon = True
#         t.start()
#     server.serve_forever()

if __name__ == '__main__':
    server = TCPServer(('', 20000), EchoHandler, bind_and_activate=False)
    # set up various socket options
    serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # bind and activate
    server.server_bind()
    server.server_activate()
    server.serve_forever()

