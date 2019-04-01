
from threading import Thread
from queue import Queue
import psycopg2



class QueueSender(Thread):
    def __init__(
            self,
            dbname="ejudge_queue",
            usr="postgres",
            psw="0000",
            host="localhost"):
        super().__init__()
        self.connection = psycopg2.connect(
            database=dbname, user=usr, host=host, password=psw)
        self.queue = Queue()

    def __make_request(self, request, params = {}):
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
            result = cursor.fetchall()
        return result


    def __get(self):
        request = "SELECT solution_id, min(unixtime) FROM queue"
        result = self.__make_request(request)
        if len(result) == 0:
            return None
        return result[0]

    def __get_solution_id(self):
        result = self.__get()
        return result[0]

    def run(self):
        while True:
            solution_id = self.__get_solution_id()
            self.queue.put(solution_id)

            
            