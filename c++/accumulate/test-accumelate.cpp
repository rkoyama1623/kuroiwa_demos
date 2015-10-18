#include "coordinates.h"
#include <vector>
#include <numeric>

int main(){
  std::vector<Eigen::Vector3d> vec;
  Eigen::Vector3d qqq = Eigen::Vector3d::Zero();
  vec.push_back(Eigen::Vector3d(1,2,3));
  vec.push_back(Eigen::Vector3d(3,4,1));
  vec.push_back(Eigen::Vector3d(4,2,-2));
  std::cout << "sum = " << std::accumulate(vec.begin(), vec.end(), qqq) << std::endl;
  std::cout << "avg = " << std::accumulate(vec.begin(), vec.end(), qqq) / vec.size() << std::endl;

  coordinates a(Eigen::Vector3d(1,2,3), Eigen::Matrix3d::Identity());
  coordinates b(Eigen::Vector3d(4,3,0), Eigen::Matrix3d::Identity());
  coordinates c(Eigen::Vector3d(4,3,0), Eigen::Matrix3d::Identity());
  std::cout << a.pos << std::endl;

  std::vector<coordinates> vec_cdt;
  vec_cdt.push_back(a);
  vec_cdt.push_back(b);
  vec_cdt.push_back(c);
  /* std::cout << "sum = " << std::accumulate(vec.begin(), vec.end(), new coordinates()) << std::endl; */
  /* std::cout << "avg = " << std::accumulate(vec.begin(), vec.end(), 0) / vec.size() << std::endl; */

  std::cout << "koko" << std::endl;
  for (std::vector<coordinates>::iterator it = vec_cdt.begin(); it != vec_cdt.end(); it++) {
    std::cout << it->pos << std::endl;
  }

  std::vector<Eigen::Vector3d> test_vec;
  test_vec.push_back(Eigen::Vector3d(1,2,3));
  test_vec.push_back(Eigen::Vector3d(2,1,0));
  for (std::vector<Eigen::Vector3d>::iterator it = test_vec.begin(); it != test_vec.end(); it++)
    (*it)(0) = 100;
  for (std::vector<Eigen::Vector3d>::iterator it = test_vec.begin(); it != test_vec.end(); it++)
    std::cerr << 5*(*it)(0) << ", " << std::endl;

  Eigen::Vector3f ex, ey, ez;
  ez = Eigen::Vector3f(1, 0, 0).normalized();
  ex = Eigen::Vector3f::UnitY().cross(ez).normalized();
  ey = ez.cross(ex).normalized();
  Eigen::Matrix3f m;
  m << ex, ey, ez;
  std::cerr << "m : " << m << std::endl;
  // http://www.wolframalpha.com/input/?i=RotationMatrix%5B0%2C%7B0%2C0%2C1%7D%5D+.+RotationMatrix%5Bpi%2F2%2C%7B0%2C1%2C0%7D%5D+.+RotationMatrix%5B0%2C%7B1%2C0%2C0%7D%5D

  Eigen::Vector3d aa = Eigen::Vector3d(1,2,3);
  std::cout << "vector" << aa << std::endl;
  aa * aa.transpose();
  std::cout << aa * aa.transpose() << std::endl;
}
