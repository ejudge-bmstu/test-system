from threading import Thread
#from tools.controller import app
#from tools.server.controller import app
from .sender import QueueSender
from .controller import app
from .settings import init_queue


class FrontServer(Thread):
    def __init__(self):
        super().__init__()
        self.sender = QueueSender()
        self.queue = init_queue(self.sender.queue)
    def run(self, server_host = "localhost", server_port = 8080):
        self.sender.start()
        app.run(host=server_host, port=server_port)




if __name__ == '__main__':
    sender = QueueSender()
    queue = init_queue(sender.queue)
    sender.start()
    app.run(host="localhost", port=8080)
