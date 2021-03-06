class CompileSettings(object):
    def __init__(self):
        self.parameters = None
        self.lang = None
        self.is_compiled = True
        self.exe_type = None
        self.source_type = None

    def get_command(self, fin, fout):
        return self.parameters + " %s -o %s " % (fin, fout)


class CompileSettingsC(CompileSettings):
    def __init__(self):
        super().__init__()
        self.parameters = "gcc -O0 -w "
        self.lang = "c"
        self.exe_type = "out"
        self.source_type = "c"


class CompileSettingsCpp(CompileSettings):
    def __init__(self):
        super().__init__()
        self.parameters = "g++ -O0 -w "
        self.lang = "cpp"
        self.exe_type = "out"
        self.source_type = "cpp"


class CompileSettingsPython(CompileSettings):
    def __init__(self):
        super().__init__()
        self.parameters = ""
        self.lang = "python"
        self.source_type = "py"
        self.exe_type = "py"
        self.is_compiled = False


settings_list = (
    CompileSettingsC(),
    CompileSettingsCpp(),
    CompileSettingsPython())
docker_test_folder = "data/testdir/"
docker_file_folder = "data/"
docker_tag = "test:test"

out_file = "source."
answer_dir = "data/map_folder/"
answer_filename = answer_dir + "/" + "out.txt"
answer_len = 256
