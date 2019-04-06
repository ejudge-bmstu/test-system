from server.controller import app
from server.sender import QueueSender
import server.settings

if __name__ == '__main__':
    sender = QueueSender()
    queue = server.settings.init_queue(sender.queue)
    sender.start()
    app.run(host="localhost", port=8080)
