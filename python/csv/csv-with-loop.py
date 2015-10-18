#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt

input_data_list = [[], [], [], []]
with open('data.dat', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        for i, x in enumerate(row):
            input_data_list[i].append(float(x))

for i, d in enumerate(input_data_list):
    plt.plot(range(len(d)), d, label=str(i), linewidth=5-i)

plt.legend(loc=0)
plt.title('default-step-time 3.0, go-pos 0 0 0\nrtprint localhost:15005/abc.rtc:controlSwingSupportTime | cut -d"[" -f3 | cut -d"]" -f1 2>&1 | tee /tmp/data.dat')
plt.show()
