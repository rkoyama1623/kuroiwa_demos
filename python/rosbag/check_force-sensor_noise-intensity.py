#!/usr/bin/env python

import rosbag
import argparse, numpy, os
import matplotlib.pyplot
from matplotlib.backends.backend_pdf import PdfPages

parser = argparse.ArgumentParser(description='plot and analyze force sensor data')
parser.add_argument('-f', help='target rosbag file', type=str, required=True)
parser.add_argument('--no_display', help='do not display the graph', default=True, action='store_false')
args = parser.parse_args()

# get data from bag file
tm_list = []
force_6axis_list = []
for topic, msg, t in rosbag.Bag(args.f):
    if topic == "/lfsensor" or topic == "/rfsensor" or topic == "/lhsensor" or topic == "/rhsensor":
        tmp = msg.wrench
        force_6axis_list.append([tmp.force.x, tmp.force.y, tmp.force.z,
                                 tmp.torque.x, tmp.torque.y, tmp.torque.z])
        tm_list.append(t.to_time())

# set start time to 0.0
min_time = tm_list[0]
tm_list = [t - min_time for t in tm_list]

# fix average to 0
ave_list = [0, 0, 0, 0, 0, 0]
for f6 in force_6axis_list:
    ave_list = [x + y for (x, y) in zip(f6, ave_list)]
ave_list = [x / len(force_6axis_list) for x in ave_list]
force_6axis_list = [[x-y for (x, y) in zip(f6, ave_list)] for f6 in force_6axis_list]

# graph setting
row_title = ['Force', 'Moment']
unit_list = ['[N]', '[Nm]']
range_list = [4, 0.4]
col_title = ['x', 'y', 'z']
clr_list = ['r', 'g', 'b']
fig, (axes_array) = matplotlib.pyplot.subplots(len(col_title), len(row_title), sharex=True, sharey=False)
for i in range(len(col_title)):
    for j in range(len(row_title)):
        tmp_y_list = [f6[i + j * len(col_title)] for f6 in force_6axis_list]
        axes_array[i][j].plot(tm_list,
                              tmp_y_list,
                              color=clr_list[i])
        axes_array[i][j].set_title(row_title[j] + " " + col_title[i] + " " + unit_list[j])
        axes_array[i][j].text(0.95, 0.05, 'std : ' + "{0:.3f}".format(numpy.std(tmp_y_list)),
                              verticalalignment='bottom', horizontalalignment='right',
                              transform=axes_array[i][j].transAxes,
                              color='black', fontsize=15,
                              bbox={'facecolor':'yellow', 'alpha':0.8, 'pad':10})
        axes_array[i][j].set_ylim(ymin=-1*range_list[j], ymax=1*range_list[j])


# trivial setting
fig.suptitle(args.f, fontweight='bold')
for ax in fig.axes:
    ax.minorticks_on()
    ax.grid(True)

# save and show
fig.set_size_inches(10.0, 7.5)
path, ext = os.path.splitext(os.path.basename(args.f))
pp = PdfPages('/tmp/'+path+'.pdf')
pp.savefig(fig)
pp.close()
print 'saved to ' + '/tmp/'+path+'.pdf'
if args.no_display == True:
    matplotlib.pyplot.show()
