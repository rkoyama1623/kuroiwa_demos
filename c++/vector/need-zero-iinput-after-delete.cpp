#include <iostream>
#include <vector>
#include <map>

int main(){
  int *a = new int();
  std::cout << a << std::endl;
  delete a;
  std::cout << a << std::endl;

  int *b = new int();
  std::cout << b << std::endl;
  *b = 0;
  std::cout << *b << std::endl;
  *a = 100;
  std::cout << *b << std::endl;
  delete b;

  enum leg_type {RLEG, LLEG, RARM, LARM, BOTH};
  std::vector<leg_type> d{RLEG};
  if (d == std::vector<leg_type>{LLEG}) {
    std::cout << "RLEG" << std::endl;
  } else if (d == std::vector<leg_type>{RLEG}) {
    std::cout << "RLEG" << std::endl;
  }
  std::vector<int>no1_list{1,2,3,4};
  std::vector<double>no2_list{0.1,0.2,0.3,0.4};
  std::vector<int>no3_list{1,2,3,4};
  std::vector<double>no4_list{0.1,0.2};


  for ( int i = 2, j = 3, k = i + j; i < 5; ++i, --j, k = k + i + j)
    {
      std::cout << "i,j,k: " << j << (k / 5) << std::endl;
    }

  for (std::vector<int>::iterator it1 = no1_list.begin(), it3 = no3_list.begin(); it1 != no1_list.end(); it1++, it3++) {
    std::cout << *it1 << ", " << *it3 << std::endl;
  }

  for (auto it1 = no1_list.begin(), it3 = no3_list.begin(); it1 != no1_list.end(); it1++, it3++) {
    std::cout << *it1 << ", " << *it3 << std::endl;
  }

  std::vector<int>::iterator it1 = no1_list.begin();
  std::vector<double>::iterator it2 = no2_list.begin();
  for (; it1 != no1_list.end(); it1++, it2++) {
    std::cout << *it1 << ", " << *it2 << std::endl;
  }

  std::vector<int>::iterator it1_new = no1_list.begin();
  std::vector<double>::iterator it4_new = no4_list.begin();
  for (; it1_new != no1_list.end() && it4_new != no4_list.end(); it1_new++, it4_new++) {
    std::cout << *it1_new << ", " << *it4_new << std::endl;
  }

  std::vector<int> test1{1, 2, 3};
  std::vector<int> test2{4, 5, 6};
  test1.insert(test1.end(), test2.begin(), test2.end());
  for (int t1 : test1) {
    std::cout << t1 << ", ";
  }
  std::cout << std::endl;

  return 0;
}
