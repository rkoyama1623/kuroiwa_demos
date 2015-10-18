#include <iostream>
#include <vector>
#include <boost/range/algorithm/count.hpp>
#include <boost/range/algorithm/count_if.hpp>
#include <boost/range/adaptor/filtered.hpp>
#include <boost/range/algorithm/copy.hpp>
#include <boost/range/algorithm/transform.hpp>
#include <boost/assign.hpp>
#include <boost/lambda/lambda.hpp>
#include <boost/range/algorithm.hpp>
#include <algorithm>
#include <boost/range/algorithm_ext/erase.hpp>
#include <set>

int main()
{
  std::vector<int> v = boost::assign::list_of<int>(1)(2)(3)(4)(5);

  std::cout << "the number of 3 is " << boost::count(v, 3) << std::endl;
  std::cout << "the number of even is " << boost::count_if(v, (boost::lambda::_1 % 2 == 0)) << std::endl;
  std::vector<int> ret;
  boost::copy(boost::adaptors::filter(v, (boost::lambda::_1 % 2 == 0)), std::back_inserter(ret));
  std::cout << "v.size() is " << v.size() << std::endl;
  std::cout << "ret.size() is " << ret.size() << std::endl;
  for (size_t i = 0; i < ret.size(); i++)  std::cout << ret.at(i) << ","; std::cout << std::endl;
  std::transform(v.begin(), v.end(),
                 v.begin(),
                 (boost::lambda::_1 * 2));
  for (size_t i = 0; i < v.size(); i++)  std::cout << v.at(i) << ","; std::cout << std::endl;

  std::vector<std::string> all = boost::assign::list_of<std::string>("RLEG")("LLEG")("RARM")("LARM");
  std::vector<std::string> sup = boost::assign::list_of<std::string>("LLEG")("RARM");
  std::vector<std::string> swg;
  std::sort(all.begin(), all.end());
  std::sort(sup.begin(), sup.end());
  std::set_difference(all.begin(), all.end(), sup.begin(), sup.end(), std::back_inserter(swg));
  std::cout << "all : "; for (size_t i = 0; i < all.size(); i++)  std::cout << all.at(i) << ","; std::cout << std::endl;
  std::cout << "sup : "; for (size_t i = 0; i < sup.size(); i++)  std::cout << sup.at(i) << ","; std::cout << std::endl;
  std::cout << "swg : "; for (size_t i = 0; i < swg.size(); i++)  std::cout << swg.at(i) << ","; std::cout << std::endl;
}
