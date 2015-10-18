#include <iostream>
#include <vector>

int main(){
  std::vector<int> a;
  a.push_back(5);
  a.push_back(4);
  a.push_back(3);
  for (std::vector<int>::iterator it = a.begin(); it != a.end(); it++) {
    std::cout << *it << ", ";
  }
  std::cout << std::endl;

  std::cout << "size : " << a.size() << std::endl;
  std::cout << "front : " << a.front() << std::endl;
  std::cout << "at(2) : " << a.at(2) << std::endl;

  return 0;
}
