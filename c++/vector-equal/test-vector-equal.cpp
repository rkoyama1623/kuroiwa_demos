#include <iostream>
#include <vector>
#include <string>
#include <boost/range/algorithm_ext/erase.hpp>
#include <boost/lambda/lambda.hpp>

int main() {
  /* v1 + v2 - v3 = {"a", "c", "d"} */
  std::vector<std::string> v1{"a", "b", "c"};
  std::vector<std::string> v2{"a", "b", "c"};
  std::vector<std::string> v3{"a", "c", "b"};
  std::vector<std::string> v4{"b", "c", "b"};

  std::cout << "v1 : ";
  for (auto str : v1) {
    std::cout << str << ", ";
  }
  std::cout << std::endl;
  std::cout << "v2 : ";
  for (auto str : v2) {
    std::cout << str << ", ";
  }
  std::cout << std::endl;
  std::cout << "v3 : ";
  for (auto str : v3) {
    std::cout << str << ", ";
  }
  std::cout << std::endl;
  std::cout << "v4 : ";
  for (auto str : v4) {
    std::cout << str << ", ";
  }
  std::cout << std::endl;

  std::cout << "v1 == v2 : " << (v1 == v2) << std::endl;
  std::cout << "v1 == v3 : " << (v1 == v3) << std::endl;
  std::cout << "v1 == v4 : " << (v1 == v4) << std::endl;
}
