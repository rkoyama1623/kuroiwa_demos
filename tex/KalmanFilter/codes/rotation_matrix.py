#!/usr/bin/env python
from sympy import *
interactive.printing.init_printing(use_latex=true)
var("a:z")
roll = Matrix([[1, 0, 0],
               [0, cos(a), -sin(a)],
               [0, sin(a), cos(a)]])
pitch = Matrix([[cos(b), 0, sin(b)],
                [0, 1, 0],
                [-sin(b), 0, cos(b)]])
yaw = Matrix([[cos(c), -sin(c), 0],
              [sin(c), cos(c), 0],
              [0, 0, 1]])
rot = yaw * pitch * roll
tar = Matrix([[cos(b)*cos(c), -sin(c), 0],
              [cos(b)*sin(c), cos(c), 0],
              [-sin(b), 0, 1]])
Q = rot.transpose() * tar
print expand(Q[1,0])
