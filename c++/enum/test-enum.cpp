#include <iostream>
#include <vector>
#include <map>
#include <boost/assign.hpp>
#include <string>
#include <boost/lambda/lambda.hpp>
enum leg_type {RLEG, LLEG, RARM, LARM, BOTH, ALL};

int main(){
  std::map<leg_type, std::string> leg_type_map = boost::assign::map_list_of<leg_type, std::string>(RLEG, "rleg")(LLEG, "lleg")(RARM, "rarm")(LARM, "larm");

  std::vector<leg_type> test_enum = boost::assign::list_of(RARM)(LARM);
  std::vector<std::string> test_string = boost::assign::list_of("larm")("rleg");

  std::cout << "test_enum -> string : ";
  for (std::vector<leg_type>::const_iterator it = test_enum.begin(); it != test_enum.end(); it++) {
    std::cout << leg_type_map.find(*it)->second << ", ";
  }
  std::cout << std::endl;


  std::cout << "test_string -> enum : ";
  for (std::vector<std::string>::iterator it = test_string.begin(); it != test_string.end(); it++) {
    std::map<leg_type, std::string>::iterator it2 = std::find_if(leg_type_map.begin(), leg_type_map.end(), (&boost::lambda::_1->* &std::map<leg_type, std::string>::value_type::second == *it));
    std::cout << it2->first << ", ";
  }
  std::cout << std::endl;
}
