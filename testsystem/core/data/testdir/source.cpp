#include <iostream> 
using namespace std; 
  
int main(int argc, char** argv) 
{ 
    cout << "You have entered " << argc 
         << " arguments:" << " "; 
  
    for (int i = 0; i < argc; ++i) 
        cout << argv[i] << " "; 
  
    return 0; 
} 