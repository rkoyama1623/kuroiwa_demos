#ifndef RATSMATRIX_H
#define RATSMATRIX_H

#include <iostream>
#include <math.h>
#include <Eigen/Dense>

inline bool eps_eq(const double a, const double b, const double eps = 0.001)
{
  return fabs((a)-(b)) <= eps;
};

struct coordinates {
  Eigen::Vector3d pos;
  Eigen::Matrix3d rot;
  coordinates() : pos(Eigen::Vector3d::Zero()), rot(Eigen::Matrix3d::Identity()) {};
  coordinates(const Eigen::Vector3d& p, const Eigen::Matrix3d& r) : pos(p), rot(r) {};
  coordinates(const coordinates& c) : pos(c.pos), rot(c.rot) {};
  virtual ~coordinates() {
  }

  Eigen::Vector3d matrix_log(const Eigen::Matrix3d& m);
  void rotm3times (Eigen::Matrix3d& m12, const Eigen::Matrix3d& m1, const Eigen::Matrix3d& m2);
  void mid_rot(Eigen::Matrix3d& mid_rot, const double p, const Eigen::Matrix3d& rot1, const Eigen::Matrix3d& rot2);
  void mid_coords(coordinates& mid_coords, const double p, const coordinates& c1, const coordinates& c2);
};


void calcRodrigues(Eigen::Matrix3d& out_R, const Eigen::Vector3d& axis, double q)
{

  const double sth = sin(q);
  const double vth = 1.0 - cos(q);

  double ax = axis(0);
  double ay = axis(1);
  double az = axis(2);

  const double axx = ax*ax*vth;
  const double ayy = ay*ay*vth;
  const double azz = az*az*vth;
  const double axy = ax*ay*vth;
  const double ayz = ay*az*vth;
  const double azx = az*ax*vth;

  ax *= sth;
  ay *= sth;
  az *= sth;

  out_R << 1.0 - azz - ayy, -az + axy,       ay + azx,
    az + axy,        1.0 - azz - axx, -ax + ayz,
    -ay + azx,       ax + ayz,        1.0 - ayy - axx;
}
#endif
