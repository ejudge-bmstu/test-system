import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import testcore, settings, builder
import unittest
import shutil
class TestAppBuilder(unittest.TestCase):
    def setUp(self):
        self.docker = testcore.DockerManager()    
 
    def test_run_python_container_ok(self):
        source = """import sys
print(sys.argv[1:])"""

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit="20M", mem_swappiness=0, timeout=10)
        self.docker.rm_image("test:test")

        self.assertEqual(result[1], "['1', '2', '3']\n")
        
    
    def test_run_python_container_timeout(self):
        source = """while 1:
    pass """

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit="20M", mem_swappiness=0, timeout=3)
        self.docker.rm_image("test:test")

        self.assertIsNone(result)   


    
    def test_run_python_container_error(self):
        source = """while 1g:
    pass """

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit="20M", mem_swappiness=0, timeout=3)
        self.docker.rm_image("test:test")

        self.assertEqual('  File "source.py", line 1\n    while 1g:\n           ^\nSyntaxError: invalid syntax\n', result[1])



    @unittest.skip
    def test_run_c_container_ok(self):
        source = """#include <iostream> 
using namespace std; 
  
int main(int argc, char** argv) 
{ 
    cout << "You have entered " << argc 
         << " arguments:" << " "; 
  
    for (int i = 0; i < argc; ++i) 
        cout << argv[i] << " "; 
  
    return 0; 
} """
        self.docker.rm_image("test:test")
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "cpp")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit="40M", mem_swappiness=0, timeout=10)
        









if __name__ == "__main__":
    unittest.main(exit=False)

    