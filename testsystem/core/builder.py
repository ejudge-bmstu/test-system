import os
from subprocess import Popen, PIPE
import settings

class AppBuilder(object):
    def __init__(self, code_type):
        self.type_set = set(("py, c, cpp"))

        if code_type not in self.type_set:
            raise Exception("Unknown type of file")

        self.docker_test_folder = "data/testdir/"
        self.code_filename = self.docker_test_folder + "source."

    def __create_temp_folder(self):
        if not os.path.exists(self.docker_test_folder):
            os.mkdir(self.docker_test_folder)

    def __delete_file(self, filename):
        if os.path.exists(filename):
            os.unlink(filename)

    def __create_source(self, filename, text = ""):
        with open(filename, "w") as f:
            f.write(text)

    def __get_lang_setting(self, programming_language):
        for setting in settings.settings_list:
            if programming_language == setting.lang:
                return setting
        return None



    def compile(self, settings):
        process = Popen(settings.parameters, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        return (output, error)
    
    def assembly(self, source_text, programming_language):
        setting = self.__get_lang_setting(programming_language)
        fsource = self.code_filename + setting.source_type
        fbinary = self.code_filename + setting.exe_type
        self.__create_source(fsource, source_text)

        if setting.is_compiled:
            command = setting.get_command(fsource, fbinary)
            output, error = self.compile(command)
            if len(error) != 0:
                return (True, error)

        return (False, fbinary)
        
        





        


        

    

