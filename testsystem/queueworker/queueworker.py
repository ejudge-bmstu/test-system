
from threading import Thread
from queue import Queue
import psycopg2
import time


class QueueRetriever(Thread):
    def __init__(self, db_settings):
        super().__init__()
        self.connection = psycopg2.connect(**db_settings)
        self.queue = Queue()

        self.debug = False

    def __make_request(self, request, params = {}, delete = False):
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
            if not delete:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = None
        return result


    def __del_element(self, queue_id):
        request = "DELETE FROM queue WHERE id=%(queue_id)s"
        param = {"queue_id": queue_id}
        self.__make_request(request, param, True)



    def __get(self):
        request = "SELECT id, solution_id, min(unixtime) FROM queue GROUP BY id"
        result = self.__make_request(request)
        if len(result) == 0:
            return None, None
        result = result[0]
        return result[0], result[1]

    def __get_solution_id(self):
        queue_id, solution_id = self.__get()
        if queue_id is None:
            return None
        if not self.debug:
            self.__del_element(queue_id)
        else:
            print(solution_id)
        return solution_id

    def run(self):
        while True:
            solution_id = self.__get_solution_id()
            if solution_id is not None:
                self.queue.put(solution_id)
            else:
                time.sleep(3)

            if self.debug:
                return


            
if  __name__ == "__main__":
    QR = QueueRetriever()
    QR.debug = True
    QR.start()
    while 1:
        print(QR.queue.get())
    b= 0