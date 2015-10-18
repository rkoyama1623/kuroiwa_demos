#!/usr/bin/env python


import yaml
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv, argparse, numpy, math, time, struct

try:
    import progressbar
except:
    print "Please install progressbar by sudo aptitude install python-progressbar"
    sys.exit(1)

class DataloggerLogParser:
    def __init__(self, log_name, yaml_name):
        self.col_num = None
        self.row_num = None
        self.log_name = log_name
        self.yaml_name = yaml_name
        self.title = log_name.split('/')[-1]
        with open(self.yaml_name, 'r') as f:
            data = yaml.load(f)
        self.set_layout(data)
        self.limbs = data["limbs"]
        self.target_limbs = data["target_limbs"]
        self.plots = data["plots"]
        self.fig, (self.axes_array) = plt.subplots(self.row_num, self.col_num, sharex=True, sharey=False)
        for ax in self.fig.axes:
            ax.minorticks_on()
            ax.grid(True)
        self.fig.suptitle(self.title)

    def set_layout(self, data):
        self.col_num = max([x.values()[0] for x in data["limbs"] if x.keys()[0] in [y.keys()[0] for y in data["target_limbs"]]])
        self.row_num = len(data["plots"]) * len(data["target_limbs"])

    def parse(self):
        for k_i, k in enumerate(self.plots.keys()): # k : joint_angle / joint_velocity / ...
            for plt_i, plt in enumerate(self.plots[k]): # plt : sh_qOut / ic_q / ...
                y_vals = []
                t_vals = []
                with open(self.log_name + '.' + plt, 'r') as f:
                    reader = csv.reader(f, delimiter=' ')
                    for row in reader:
                        dl = row[1:]
                        dl = filter(lambda x: x != '', dl)
                        y_vals.append([float(x) for x in dl])
                        t_vals.append(float(row[0]))
                y_vals = numpy.array(y_vals)
                for l_i, l in enumerate(self.target_limbs): # l : {"rleg" : [0, 5]} / {"lleg" : [6, 11]} / ...
                    for c_i in range(l.values()[0][0], l.values()[0][1]+1, 1): # c_i : 6 / 7 / 8 / ...
                        # print "k", k
                        # print "plt", plt
                        # print "l", l
                        # print "c_i", c_i
                        # print "k_i", k_i
                        # print "l_i", l_i
                        # print k_i * len(self.limbs) + l_i
                        # print c_i - l.values()[0][0]
                        ax = self.axes_array[k_i * len(self.target_limbs) + l_i][c_i - l.values()[0][0]]
                        ax.plot(t_vals,
                                [x for x in y_vals[:, c_i]],
                                linewidth=len(self.plots[k])-plt_i,
                                label=plt)
                        ax.set_title(k + ' ' + l.keys()[0] + ' joint ' + str(c_i - l.values()[0][0]) + ' [unit]')
                        # if c_i == l.values()[0][0]: # first column
                        #     ax.legend(loc=0)
                self.fig.show()
