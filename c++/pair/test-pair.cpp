#include <iostream>
#include <vector>
#include <string>
#include <map>

int main(){
  std::map<std::string, int> aaa;
  aaa.insert(std::pair<std::string, int>("rleg", 100));
  aaa.insert(std::pair<std::string, int>("lleg", 120));
  aaa.insert(std::pair<std::string, int>("rarm", 130));
  aaa.insert(std::pair<std::string, int>("larm", 140));
  for (std::map<std::string, int>::const_iterator it = aaa.begin(); it != aaa.end(); it++) {
    std::cout << it->first << std::endl;
  }
}
