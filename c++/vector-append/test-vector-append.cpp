#include <iostream>
#include <vector>
#include <string>
#include <boost/range/algorithm_ext/erase.hpp>
#include <boost/lambda/lambda.hpp>

int main() {
  /* v1 + v2 - v3 = {"a", "c", "d"} */
  std::vector<std::string> v1{"a", "b", "c"};
  std::vector<std::string> v2{"d", "e"};
  std::vector<std::string> v3{"e", "b", "z"};

  std::vector<std::string> ret = v1;
  std::copy(v2.begin(), v2.end(), std::back_inserter(ret));
  for (size_t i = 0; i < v3.size(); i++) {
    std::vector<std::string>::iterator it = std::remove_if(ret.begin(), ret.end(), (boost::lambda::_1 == v3.at(i)));
    ret.erase(it, ret.end());
  }
  /* 
   * boost::remove_erase_if(ret, [v3](std::string el)
   *                        { return std::find(v3.begin(),
   *                                           v3.end(),
   *                                           el) != v3.end(); });
   */
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

  std::cout << "v1 + v2 : ";
  for (auto str : ret) {
    std::cout << str << ", ";
  }
  std::cout << std::endl;
}
