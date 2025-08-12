# C++ Learning

## Namespaces

Using names: `std::cout`, `std::endl`, etc. is common in C++. To avoid typing `std::` every time, you can use the `using` directive.

```cpp
#include <iostream>
using namespace std;

int main(){
  int file_size = 100;
  double sales = 1234.56;

  cout << file_size << "int" << endl;
  cout << sales << "bold "<< endl;

  return 0;
}
```
## Random

```cpp
# include <cstdlib> 
# include <iostream>
# include <ctime>

using namespace std;

int main(){
  long elapsed_time = time(0);
  srand(elapsed_time);

  int number = rand() % 100;
```
