#include <iostream>
#include <vector>
#include <string>
#include <map>

std::vector<std::string> hoge () {
  std::vector<std::string> ans;
  ans.push_back("a");
  ans.push_back("i");
  ans.push_back("u");
  return ans;
}

int& fuga () {
  int i;
  i = 5;
  return i;
}

int main(){
  std::vector<std::string> tmp = hoge();
  int tmp2 = fuga();
  for (size_t i = 0; i < tmp.size(); i++) {
    std::cout << tmp.at(i) << std::endl;
  }
  std::cout << "fuga : " << tmp2 << std::endl;
}
