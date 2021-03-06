from flask import Flask, Response
from queue import Queue
from .settings import GET_PATH, PARAM_NAME
from .validator import validate_uuid

"""
Flask instance.
"""
app = Flask(__name__)

"""
Queue to transfer the solution_id to the database.
"""
queue = Queue()


@app.route(GET_PATH + "<%s>" % PARAM_NAME, methods=['GET'])
def get_solution_id(solution_id):
    """
   GET request handler for web backend.
    :param solution_id: id of user solution
    :return: returns 200 if solution_id is valid else 400
    """
    if validate_uuid(solution_id):
        resp = Response(status=200)
        queue.put(solution_id)
    else:
        resp = Response(status=400)

    return resp
