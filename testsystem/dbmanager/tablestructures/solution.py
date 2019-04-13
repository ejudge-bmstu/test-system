from .tasklimits import TaskLimits


class Solution(object):
    def __init__(self, user_solution_id, answer, tests, limits):
        self.answer = answer
        self.tests = tests
        self.limits = limits
        self.user_solution_id = user_solution_id
        self.__status = None
        self.passed = 0

    status = property()

    @status.getter
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def get_limit(self, lang):
        return self.limits
