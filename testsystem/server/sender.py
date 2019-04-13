
from threading import Thread
import psycopg2
import uuid
import time
from .validator import validate_uuid


class QueueSender(Thread):
    """
    FrontServer is needed to transfer information from the webback to database .
    """

    def __init__(self, db_settings):
        """
   Initialisation of FrontServer.
    :param db_settings: setting of database to connect.
    :return: None
    """
        super().__init__()
        self.connection = psycopg2.connect(**db_settings)
        self.connection.autocommit = True
        self.queue = None

    def init_queue(self, queue):
        """
   Initialisation of Queue.
    :param db_settings: setting of database to connect.
    :return: None
    """
        self.queue = queue

    def __make_request(self, request, params):
        """
    Method to make custom request to database.
    :param request: body of SQL-request without parameters.
    :param params: parameters for SQL-request.
    :return: None
    """
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)

    def __put(self, solution_id):
        """
    Method to create SQL request to add solution_id.
    :param solution_id: id of users solution.
    :return: None
    """
        request = "INSERT INTO queue(id, solution_id, unixtime) VALUES(%(id)s, %(solution_id)s, %(unixtime)s)"
        params = {
            "id": str(
                uuid.uuid4()),
            "solution_id": solution_id,
            "unixtime": int(
                time.time())}
        self.__make_request(request, params)

    def run(self):
        """
    Method to run QueueSender.
    :return: None
    """
        while True:
            solution_id = self.queue.get()
            if validate_uuid(solution_id):
                self.__put(solution_id)
