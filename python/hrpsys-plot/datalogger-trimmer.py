#!/usr/bin/env python

import argparse, os, glob, subprocess, linecache

parser = argparse.ArgumentParser(description='trim log to reduce file size and load time')
parser.add_argument('-f', type=str, help='input file', metavar='file', required=True)
parser.add_argument('--min', type=float, help='minimum time', default=0.0)
parser.add_argument('--max', type=float, help='maximum time', default=None)
parser.add_argument('--dt', type=float, help='one step time of log', default=0.002)
args = parser.parse_args()

dt = args.dt
fl = sum(1 for line in open(os.path.abspath(args.f)))
duration = fl * dt
start_point = int(args.min / duration * fl)
end_point = int(args.max / duration * fl) if args.max else fl
root, ext = os.path.splitext(os.path.abspath(args.f))

print duration, start_point, end_point, fl

for log in glob.glob(os.path.splitext(os.path.abspath(args.f))[0]+'.*'):
    root, ext = os.path.splitext(log)
    new_log_name = root + "_new" + ext
    with open(new_log_name, 'w') as f:
        for i in range(start_point, end_point):
            f.write(linecache.getline(log, i))
