#include <iostream>
#include <vector>
#include <string>
#include <boost/lambda/lambda.hpp>

enum leg_type {RLEG, LLEG, RARM, LARM, BOTH, ALL};
struct step_node
{
  leg_type l_r;
  std::string name;
  step_node (const leg_type _l_r, const std::string _name)
    : l_r(_l_r), name(_name) {};
};

int main() {
  std::vector<step_node> v1{step_node(RARM, "RARM"), step_node(LLEG, "LLEG")};
  std::cout << "v1 : ";
  for (auto sn : v1) {
    std::cout << sn.l_r << " + " << sn.name << ", ";
  }
  std::cout << std::endl;

  /* 
   * std::sort(v1.begin(), v1.end(),
   *           [](step_node x, step_node y) {
   *             return (x.l_r < y.l_r);
   *           });
   */

  std::sort(v1.begin(), v1.end(),
            ((&boost::lambda::_1->* &step_node::l_r) < (&boost::lambda::_2->* &step_node::l_r)));

  std::cout << "sorted v1 : ";
  for (auto sn : v1) {
    std::cout << sn.l_r << " + " << sn.name << ", ";
  }
  std::cout << std::endl;
}
