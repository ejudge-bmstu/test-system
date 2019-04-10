from threading import Thread
from .sender import QueueSender
from .controller import app, queue


class FrontServer(Thread):
    """
    FrontServer is needed to transfer information from the webback to QueueSender.
    """
    def __init__(self, db_settings, rest_settings):
        """
   Initialisation of FrontServer.
    :param db_settings: setting of database to connect.
    :param rest_settings: setting of REST-api server.
    :return: None
    """
        super().__init__()
        self.sender = QueueSender(db_settings)
        self.sender.init_queue(queue)
        self.rest_settings = rest_settings
    def run(self):
        """
    Method run FrontServer.
    :return: None
    """
        self.sender.start()
        app.run(**self.rest_settings)




if __name__ == '__main__':
    sender = QueueSender()
    sender.start()
    app.run(host="localhost", port=8080)
