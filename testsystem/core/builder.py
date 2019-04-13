import os
import glob
from subprocess import Popen, PIPE
from .settings import docker_file_folder, docker_test_folder, out_file, settings_list


class AppBuilder(object):
    """
    AppBuilder is needed for the interaction with source codes of solutions.
    """

    def __init__(self):
        """
   Initialisation of AppBuilder.
    :return: None
    """
        self.docker_test_folder = os.path.dirname(
            os.path.realpath(__file__)) + "/" + docker_test_folder
        self.code_filename = self.docker_test_folder + out_file
        self.docker_file_folder = os.path.dirname(
            os.path.realpath(__file__)) + "/" + docker_file_folder

    def _create_temp_folder(self):
        """
   Create folder for users source code.
    :return: None
    """
        if not os.path.exists(self.docker_test_folder):
            os.mkdir(self.docker_test_folder)

    def _delete_file(self, filename):
        """
   Delete certain file.
    :param filename: name of file.
    :return: None
    """
        if os.path.exists(filename):
            os.unlink(filename)

    def _create_source(self, filename, text=""):
        """
   Create file with users source code.
    :param filename: name of file.
    :param text: users source code.
    :return: None
    """
        with open(filename, "w") as f:
            f.write(text)

    def _get_lang_setting(self, programming_language):
        """
    Method to get settings for programming language.
    :param programming_language: programming language.
    :return: None if no results else return setting.
    """
        for setting in settings_list:
            if programming_language == setting.lang:
                return setting
        return None

    def compile(self, settings):
        """
   Compile file with users source code.
    :param setting: settings for programming language.
    :return: stdout of compiler and error code
    """
        process = Popen(settings.split(), stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        return (output, error.decode("utf-8"))

    def assembly(self, source_text, programming_language):
        """
    Method prepare users code to containerization.
    :param programming_language: programming language.
    :param source_text: users source code.
    :return: existing of error and ext information.
    """
        self._create_temp_folder()
        setting = self._get_lang_setting(programming_language)
        fsource = self.code_filename + setting.source_type
        fbinary = self.code_filename + setting.exe_type
        self._create_source(fsource, source_text)
        result = (False, fbinary)
        if setting.is_compiled:
            command = setting.get_command(fsource, fbinary)
            output, error = self.compile(command)
            if len(error) != 0:
                result = (True, error)
        return result

    def clean_folder(self):
        """
   Delete all temporary files in docker folder.
    :return: None
    """
        listfiles = [os.path.abspath(f)
                     for f in os.listdir(docker_test_folder)]
        for f in listfiles:
            self._delete_file(f)


if __name__ == "__main__":
    app_builder = AppBuilder()
    source = """#include <stdio.h>
int main (void) {puts ("Hello, World!");return 0;}
                    """
    app_builder.assembly(source, "c")
    fout = app_builder.code_filename + \
        app_builder._get_lang_setting("c").exe_type

    result = os.path.exists(fout)
