from threading import Thread
from .sender import QueueSender
from .controller import app, queue


class FrontServer(Thread):
    def __init__(self, db_settings, rest_settings):
        super().__init__()
        self.sender = QueueSender(db_settings)
        self.sender.init_queue(queue)
        self.rest_settings = rest_settings
    def run(self):
        self.sender.start()
        app.run(**self.rest_settings)




if __name__ == '__main__':
    sender = QueueSender()
    sender.start()
    app.run(host="localhost", port=8080)
