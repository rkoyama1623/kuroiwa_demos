#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt

input_data_list = [[], [], [], [], []]
name_list = ["gyro", "observed", "x+", "x-", "y"]
with open('/tmp/gyro.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        for i, x in enumerate(row):
            input_data_list[i].append(float(x))

fig, ax1 = plt.subplots()
ax2=ax1.twinx()
for i, d in enumerate(input_data_list):
    if i == 1 or i == 2 or i == 3:
        ax1.plot([x * 0.002 for x in range(len(d))], d, label=name_list[i], linewidth=6-i)
    if i == 0:
        ax2.plot([x * 0.002 for x in range(len(d))], d, label=name_list[i], linewidth=6-i, color="y")

ax1.legend(loc=0)
ax2.legend(loc=0)
# plt.ylim(ymin=-0.0015,ymax=0.0015)
ax1.set_ylim(ymin=-0.0015,ymax=0.2)
plt.show()
