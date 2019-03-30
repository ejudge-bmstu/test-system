class CompileSettings(object):
    def __init__(self):
        self.parameters = None
        self.lang = None
        self.is_compiled = True
        self.exe_type = None
        self.source_type = None

    def get_command(self, fin, fout):
        return self.parameters + " %s %s " % (fin ,fout)
    

class CompileSettingsC(CompileSettings):
    def __init__(self):
        super().__init__()
        self.parameters = "gcc -O0 -o"
        self.lang = "c"
        self.exe_type = "out"
        self.source_type = "c"

class CompileSettingsCpp(CompileSettings):
    def __init__(self):
        super().__init__()
        self.parameters = "g++ -O0 -o" 
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


settings_list = (CompileSettingsC, CompileSettingsCpp, CompileSettingsPython)