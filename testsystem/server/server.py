from server.controller import app
from server.sender import QueueSender
import server.settings

if __name__ == '__main__':
    pipe_sender = QueueSender()
    queue = server.settings.init_queue(pipe_sender.queue)
    pipe_sender.start()
    app.run(host="localhost", port = 8080)