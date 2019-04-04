import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import builder, settings
import unittest
import shutil
class TestAppBuilder(unittest.TestCase):
    def setUp(self):
        self.app_builder = builder.AppBuilder()

    def tearDown(self):
        filename = self.app_builder.docker_test_folder
        if os.path.exists(filename):
            shutil.rmtree(filename)



    def test_get_lang_setting_python(self):
        result = self.app_builder._get_lang_setting("python")
        self.assertIsInstance(result, settings.CompileSettingsPython)

    def test_get_lang_setting_c(self):
        result = self.app_builder._get_lang_setting("c")
        self.assertIsInstance(result, settings.CompileSettingsC)

    def test_get_lang_setting_cpp(self):
        result = self.app_builder._get_lang_setting("cpp")
        self.assertIsInstance(result, settings.CompileSettingsCpp)

   
    def test_assembly_python(self):
        source = """for _ in range(2):
     print("Hello, world!")
                    """
        self.app_builder.assembly(source, "python")
        fout = self.app_builder.code_filename + self.app_builder._get_lang_setting("python").exe_type
        with open(fout, "r") as f:
            result =  f.read()
        
        self.assertEqual(source, result)

    def test_assembly_c_success(self):
        source = """#include <stdio.h>
int main (void) {puts ("Hello, World!");return 0;}
                    """
        result = self.app_builder.assembly(source, "c")
        fout = self.app_builder.code_filename + self.app_builder._get_lang_setting("c").exe_type
        
        path_ex = os.path.exists(fout)
        self.assertTrue(path_ex)
        self.assertFalse(result[0])
        
    def test_assembly_c_failed(self):
        source = """#include <stdio.h>
itn main (void) {puts ("Hello, World!");return 0;}
                    """
        result = self.app_builder.assembly(source, "c")
        self.assertTrue(result[0]) 
              


    def test_assembly_cpp_success(self):
        source = """#include <iostream>
int main (void) {std::cout << "Hello, World!";return 0;}
                    """
        result = self.app_builder.assembly(source, "cpp")
        fout = self.app_builder.code_filename + self.app_builder._get_lang_setting("c").exe_type
        
        path_ex = os.path.exists(fout)
        self.assertTrue(path_ex)
        self.assertFalse(result[0])
        
    def test_assembly_cpp_failed(self):
        source = """#include <iostream>
int main (void) {cout << "Hello, World!";return 0;}
                    """
        result = self.app_builder.assembly(source, "cpp")
        self.assertTrue(result[0])  


if __name__ == "__main__":
    unittest.main(exit=False)