from flask import Flask, Response
from .settings import GET_PATH, PARAM_NAME
from .validator import validate_uuid
import server.settings

app = Flask(__name__)


@app.route(GET_PATH + "<%s>" % PARAM_NAME, methods=['GET'])
def get_solution_id(solution_id):
    if validate_uuid(solution_id):
        resp = Response(status=200)
        server.settings.queue.put(solution_id)
    else:
        resp = Response(status=400)

    return resp
