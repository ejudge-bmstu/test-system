
from threading import Thread
from queue import Queue
import psycopg2
import uuid
import time
from .validator import validate_uuid

class QueueSender(Thread):
    def __init__(self,dbname = "ejudge_queue",usr = "postgres",psw = "0000",host = "localhost"):
        super().__init__()
        self.connection = psycopg2.connect(database=dbname, user=usr, host=host, password=psw)
        self.connection.autocommit = True
        self.queue = Queue()
        
        
    def __make_request(self, request, params):
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
        


    def __put(self, solution_id):
        request = "INSERT INTO queue(id, solution_id, unixtime) VALUES(%(id)s, %(solution_id)s, %(unixtime)s)"
        params = {"id": str(uuid.uuid4()), "solution_id":solution_id, "unixtime": int(time.time())}
        self.__make_request(request, params)
        


    def run(self):
        while True:
            solution_id = self.queue.get()
            if validate_uuid(solution_id):
                self.__put(solution_id)


