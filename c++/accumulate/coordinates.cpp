#include "coordinates.h"

Eigen::Vector3d matrix_log(const Eigen::Matrix3d& m) {
  Eigen::Vector3d mlog;
  double q0, th;
  Eigen::Vector3d q;
  double norm;

  Eigen::Quaternion<double> eiq(m);
  q0 = eiq.w();
  q = eiq.vec();
  norm = q.norm();
  if (norm > 0) {
    if ((q0 > 1.0e-10) || (q0 < -1.0e-10)) {
      th = 2 * std::atan(norm / q0);
    } else if (q0 > 0) {
      th = M_PI / 2;
    } else {
      th = -M_PI / 2;
    }
    mlog = (th / norm) * q ;
  } else {
    mlog = Eigen::Vector3d::Zero();
  }
  return mlog;
}

void rotm3times (Eigen::Matrix3d& m12, const Eigen::Matrix3d& m1, const Eigen::Matrix3d& m2) {
  Eigen::Quaternion<double> eiq1(m1);
  Eigen::Quaternion<double> eiq2(m2);
  Eigen::Quaternion<double> eiq3;
  eiq3 = eiq1 * eiq2;
  eiq3.normalize();
  m12 = eiq3.toRotationMatrix();
}

void mid_rot(Eigen::Matrix3d& mid_rot, const double p, const Eigen::Matrix3d& rot1, const Eigen::Matrix3d& rot2) {
  Eigen::Matrix3d r(rot1.transpose() * rot2);
  Eigen::Vector3d omega(matrix_log(r));
  if (eps_eq(omega.norm(),0.0)) { // c1.rot and c2.rot are same
    mid_rot = rot1;
  } else {
    calcRodrigues(r, omega.normalized(), omega.norm()*p);
    //mid_rot = c1.rot * r;
    rotm3times(mid_rot, rot1, r);
  }
};

void mid_coords(coordinates& mid_coords, const double p, const coordinates& c1, const coordinates& c2) {
  mid_coords.pos = (1 - p) * c1.pos + p * c2.pos;
  mid_rot(mid_coords.rot, p, c1.rot, c2.rot);
};
