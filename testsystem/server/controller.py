from flask import Flask, Response
from queue import Queue
from .settings import GET_PATH, PARAM_NAME
from .validator import validate_uuid


app = Flask(__name__)
queue = Queue()

@app.route(GET_PATH + "<%s>" % PARAM_NAME, methods=['GET'])
def get_solution_id(solution_id):
    if validate_uuid(solution_id):
        resp = Response(status=200)
        queue.put(solution_id)
    else:
        resp = Response(status=400)

    return resp
