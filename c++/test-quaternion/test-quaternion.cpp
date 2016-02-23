#include <Eigen/Dense>
#include <iostream>

int main() {
  Eigen::Vector3d axis;
  axis << 0,1,0;
  Eigen::Quaternion<double> q(Eigen::AngleAxisd(M_PI/3*2, axis));
  Eigen::Vector3d v, v2, v3;
  v << 5, 0, 0;
  /* rotate vector */
  v2 = q._transformVector(v);
  /* rotate coordinate */
  v3 = q.conjugate()._transformVector(v);
  std::cout << "q.w : " << q.w() << std::endl;
  std::cout << "q.vec : " << std::endl << q.vec() << std::endl;
  std::cout << "v : " << v << std::endl;
  std::cout << "v2 : " << v2 << std::endl;
  std::cout << "v3 : " << v3 << std::endl;
  std::cout << "R * v : " << q.toRotationMatrix() * v << std::endl;
  std::cout << "R^{T} * v : " << q.toRotationMatrix().transpose() * v << std::endl;
}
