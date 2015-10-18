#include <iostream>
#include <vector>
#include <algorithm>
#include <boost/range/algorithm_ext/erase.hpp>

int main()
{
  std::vector<int> v = { 1, 2, 3, 4, 5 };

  std::vector<int>::iterator it =
    std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });

  std::cout << "after remove_if" << std::endl;
  for (int x : v) {
    std::cout << x << " ,";
  }
  std::cout << std::endl;

  v.erase(it, v.end());

  std::cout << "after remove_if and erase" << std::endl;
  for (int x : v) {
    std::cout << x << ", ";
  }
  std::cout << std::endl;

  std::cout << "use remove_erase_if" << std::endl;
  std::vector<int> v2 = { 1, 2, 3, 4, 5 };
  boost::remove_erase_if(v2, [](int x) { return x % 2 == 0; });
  for (int x : v2) {
    std::cout << x << ", ";
  }
  std::cout << std::endl;
}
