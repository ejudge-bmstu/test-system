from server.front_server import FrontServer
from dbmanager.dbmanager import BDManager
from queueworker.queueworker import QueueRetriever
from core.testcore import DockerManager
from core.builder import AppBuilder
from core.settings import docker_file_folder, docker_tag, out_file
from server_settings import db_settings, rest_settings
from threading import Thread


class MainServer(object):
    """
    Organizes the interaction of all modules of the test system.
    """

    def __init__(self):
        """
   Initialisation of MainServer.
    :return: None
    """
        self.db_manager = BDManager(db_settings)
        self.queue_worker = QueueRetriever(db_settings)
        self.queue = self.queue_worker.queue
        self.docker = DockerManager()
        self.builder = AppBuilder()

        self.queue_worker.start()

    def _get_solution(self):
        """
    Method to get solution struct from BDManager.
    :return: solution struct.
    """
        solution_id = self.queue.get()
        solution = self.db_manager.get_solution(solution_id)
        return solution

    def _assembly_files(self, solution):
        """
    Method prepare user solution to containerization.
    :param solution: user solution struct.
    :return: existing of error and ext information.
    """
        code = solution.answer.program_text
        lang = solution.answer.programming_language
        result = self.builder.assembly(code, lang)
        return result

    def _build_image(self):
        """
   Build image with users source code.
    :param dockerfile: name of file with container settings.
    :return: None.
    """
        self.docker.build_image(self.builder.docker_file_folder, docker_tag)

    def _rm_image(self):
        """
   Delete docker image after tests.
    :param tag: tag of container.
    :return: None
    """
        self.docker.rm_image(docker_tag)

    def _run_container(self, solution, command):
        """
   Run the container for test.
    :param solution: user solution struct.
    :param command: docker command to run image.
    :return: error code and ext information.
    """
        limit = solution.get_limit(solution.answer.programming_language)
        mem_swappiness = 0
        memory_limit = limit.memory_limit
        timeout = limit.time_limit

        err_res = self.docker.run_time_container(
            docker_tag, command, memory_limit, mem_swappiness, timeout)
        return err_res

    def _command_formatter(self, lang):
        """
    Method to create command that run docker image.
    :param lang: programming language.
    :return: command that run docker image.
    """
        if lang == "python":
            return "python3 %s " % (out_file + "py")
        elif lang == "c" or lang == "cpp":
            return "./%s " % (out_file + "out")

    def answer_validation(self, test, answer):
        """
    Method compare user answer and right answer.
    :param test: test struct with right answer.
    :param answer: user answer.
    :return: True if user answer is right else return False.
    """
        
        answer = "" if answer is None else answer.strip()
        test_str = "" if test.output_data is None else test.output_data.strip()
        return answer == test_str

    def err_code_validation(self, err_res, test, solution):
        """
    Method compare error code from test with patterns and save result
    in database if error code != 0.
    :param err_res: error code.
    :param test: test struct with test id.
    :param solution: user solution struct.
    :return: 0 if no errors (err_res == 0) else return -1.
    """
        status = "Error"
        err_code, info = err_res if err_res is not None else [None] * 2
        user_solution_id = solution.user_solution_id
        test_id = test.test_id
        ext_info = None

        if err_code is None:
            status = "Прохождение теста превысило максимальное время для задания."
        elif err_code == 0:
            if self.answer_validation(test, info):
                return 0
            else:
                status = "Неверный ответ."

        elif err_code == 137:
            status = "Прохождение теста превысило максимальный объем памяти задания."

        elif err_code == -137:
            ext_info = "Minimal memory error. Docker error."
            test_id = None

        else:
            status = "Ошибка времени выполнения."
            ext_info = "{}".format(info)

        self.db_manager.add_status(
            user_solution_id,
            status,
            solution.passed,
            test_id,
            ext_info)

        return -1

    def _run_tests(self, solution):
        """
   Run the tests for users solution and save result to database.
    :param solution: user solution struct.
    :return: None
    """
        base_command = self._command_formatter(
            solution.answer.programming_language)
        for test in solution.tests:
            cin = test.input_data
            command = base_command + cin
            err_res = self._run_container(solution, command)
            test_result = self.err_code_validation(err_res, test, solution)
            if test_result == -1:
                return
            solution.passed += 1

        self.db_manager.add_status(
            solution.user_solution_id,
            "Задание выполнено.",
            solution.passed,
            None,
            None)
        return

    def _build_err_handler(self, information, solution):
        """
   Add error compile to user solution status in database.
    :param information: extended information.
    :param solution: user solution struct.
    :return: None
    """
        user_solution_id = solution.user_solution_id
        status = "Ошибка компиляции."
        err_test_id = None
        ext_info = information
        passed = 0

        self.db_manager.add_status(
            user_solution_id,
            status,
            passed,
            err_test_id,
            ext_info)

    def worker(self):
        """
   Get, compile and test one user solution from queue.
    :return: None
    """
        solution = self._get_solution()
        assembly_err, assembly_info = self._assembly_files(solution)
        if assembly_err:
            self._build_err_handler(assembly_info, solution)
            return

        self._build_image()

        self._run_tests(solution)

        self._rm_image()

    def start(self):
        """
   Start the MainServer in infinite loop.
    :return: None.
    """
        try:
            while True:
                self.worker()
        except KeyboardInterrupt:
            pass


def init():
    FS = FrontServer(db_settings, rest_settings)
    FS.start()

    MS = MainServer()
    MS.start()


if __name__ == "__main__":
    init()
