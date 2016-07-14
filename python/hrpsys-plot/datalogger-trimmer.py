#!/usr/bin/env python

import argparse, os, glob, subprocess, linecache
import numpy as np

parser = argparse.ArgumentParser(description='trim log to reduce file size and load time')
parser.add_argument('-f', type=str, help='input file', metavar='file', required=True)
parser.add_argument('--min', type=float, help='minimum time', default=0.0)
parser.add_argument('--max', type=float, help='maximum time', default=None)
args = parser.parse_args()

t_data_orig=np.loadtxt(args.f)[:,0]
t_data=t_data_orig-t_data_orig[0]
trimmed_index=np.where((t_data >= args.min) * (t_data <= args.max))[0]
start_point = trimmed_index[0]
end_point = trimmed_index[-1]
root, ext = os.path.splitext(os.path.abspath(args.f))

print("trim from line {} to line {}".format(str(start_point), str(end_point)))

for log in glob.glob(os.path.splitext(os.path.abspath(args.f))[0]+'.*'):
    root, ext = os.path.splitext(log)
    new_log_name = root + "_new" + ext
    with open(new_log_name, 'w') as f:
        for i in range(start_point, end_point):
            f.write(linecache.getline(log, i))
