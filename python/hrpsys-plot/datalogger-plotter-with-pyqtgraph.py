#!/usr/bin/env python

import csv, argparse, numpy, math, time, struct, yaml, sys

try:
    import pyqtgraph
except:
    print "please install pyqtgraph. see http://www.pyqtgraph.org/"
    sys.exit(1)

class DataloggerLogParserController:
    def __init__(self, fname, yname, title):
        self.fname = fname
        with open(yname, "r") as f:
            self.plot_dic = yaml.load(f)
        # self.dataListDict = {'time':[]}
        self.dataListDict = {}
        self.app = pyqtgraph.Qt.QtGui.QApplication([])
        self.view = pyqtgraph.GraphicsLayoutWidget()
        self.view.setBackground('w')
        if title == '':
            self.view.setWindowTitle(fname.split('/')[-1])
        else:
            self.view.setWindowTitle(title)
        self.items = []
        self.row_num = sum([len(x[1]["field"]) for x in self.plot_dic.items()])
        self.col_num = max([max([len(fld) for fld in x[1]["field"]]) for x in self.plot_dic.items()])
        for r in range(self.row_num):
            self.items.append([])
            for c in range(self.col_num):
                if c == 0:
                    p = self.view.addPlot(row=r, col=c, name='r'+str(r)+'c'+str(c))
                else:
                    p = self.view.addPlot(row=r, col=c)
                p.setXLink('r0c0')
                self.items[r].append(p)

    def readData(self, xmin, xmax):
        print '[%f] : start readData' % (time.time() - start_time)
        # store data
        topic_list = list(set(reduce(lambda x, y : x + y, [x[1]["log"] for x in self.plot_dic.items()])))
        for topic in topic_list:
            self.dataListDict[topic] = [[]] # first list is for time
            with open(self.fname + '.' + topic, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    self.dataListDict[topic][0].append(float(row[0]))
                    dl = row[1:]
                    dl = filter(lambda x: x != '', dl)
                    self.dataListDict[topic].append([float(x) for x in dl])
        # set the fastest time as 0
        min_time = min([self.dataListDict[topic][0][0] for topic in topic_list])
        for topic in topic_list:
            self.dataListDict[topic][0] = [x - min_time for x in self.dataListDict[topic][0]]
        # fix servoState
        if 'RobotHardware0_servoState' in topic_list:
            ss_tmp = self.dataListDict['RobotHardware0_servoState'][1:]
            for i, ssl in enumerate(ss_tmp):
                ss_tmp[i] = [struct.unpack('f', struct.pack('i', int(ss)))[0] for ss in ssl]
            self.dataListDict['RobotHardware0_servoState'][1:] = ss_tmp
        print '[%f] : finish readData' % (time.time() - start_time)

    def plotData(self, mabiki):
        print '[%f] : start plotData' % (time.time() - start_time)
        # tm = self.dataListDict['time'][::mabiki]
        color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        cur_row = 0
        for plot in self.plot_dic.items(): # plot : ('joint_velocity', {'field':[[0,1],[2,3]], 'log':['rh_q', 'st_q']})
            cur_fields = plot[1]['field']
            cur_logs = plot[1]['log']
            for cf in cur_fields: # cf : [0,1] -> [2,3]
                for i, cl in enumerate(cur_logs): # cl : 'rh_q' -> 'st_q'
                    cur_data = numpy.array(self.dataListDict[cl][1:])
                    cur_tm = numpy.array(self.dataListDict[cl][0])
                    for cur_col in cf:
                        cur_plot_item = self.items[cur_row][cur_col-cf[0]]
                        cur_plot_item.setTitle(plot[0]+" "+str(cur_col))
                        cur_plot_item.showGrid(x=True, y=True)
                        cur_plot_item.addLegend(offset=(0, 0))
                        if cur_row == self.row_num -1:
                            cur_plot_item.setLabel("bottom", text="time", units="s")
                        if cl == 'RobotHardware0_servoState':
                            if plot[0] == "12V":
                                cur_plot_item.plot(cur_tm, cur_data[:, (12+1) * cur_col + (9+1)][::mabiki], pen=pyqtgraph.mkPen('r', width=2), name='12V')
                            elif plot[0] == "80V":
                                cur_plot_item.plot(cur_tm, cur_data[:, (12+1) * cur_col + (2+1)][::mabiki], pen=pyqtgraph.mkPen('g', width=2), name='80V')
                            elif plot[0] == "current":
                                cur_plot_item.plot(cur_tm, cur_data[:, (12+1) * cur_col + (1+1)][::mabiki], pen=pyqtgraph.mkPen('b', width=2), name='current')
                            elif plot[0] == "temperature":
                                cur_plot_item.plot(cur_tm, cur_data[:, (12+1) * cur_col + (0+1)][::mabiki], pen=pyqtgraph.mkPen('r', width=2), name='motor_temp')
                                cur_plot_item.plot(cur_tm, cur_data[:, (12+1) * cur_col + (7+1)][::mabiki], pen=pyqtgraph.mkPen('g', width=1), name='motor_outer_temp')
                            elif plot[0] == "tracking":
                                cur_plot_item.plot(cur_tm, [math.degrees(x) for x in cur_data[:, (12+1) * cur_col + (6+1)][::mabiki]], pen=pyqtgraph.mkPen('g', width=2), name='abs - enc')
                        elif plot[0] == "tracking":
                            if cl == "RobotHardware0_q":
                                cur_plot_item.plot(cur_tm, [math.degrees(x) for x in numpy.array(self.dataListDict['st_q'][1:])[:, cur_col][::mabiki] - cur_data[:, cur_col][::mabiki]], pen=pyqtgraph.mkPen('r', width=2), name="st_q - rh_q")
                            else:
                                pass
                        elif plot[0] == "joint_angle" or plot[0] == "joint_velocity" or plot[0] == "attitude":
                            cur_plot_item.plot(cur_tm, [math.degrees(x) for x in cur_data[:, cur_col][::mabiki]], pen=pyqtgraph.mkPen(color_list[i], width=len(cur_logs)-i), name=cl)
                        elif plot[0] == "watt":
                            if cl == "RobotHardware0_dq":
                                cur_plot_item.plot(cur_tm, [math.degrees(x) for x in numpy.array(self.dataListDict['RobotHardware0_tau'][1:])[:, cur_col][::mabiki] * cur_data[:, cur_col][::mabiki]], pen=pyqtgraph.mkPen(color_list[i], width=len(cur_logs)-i), name=cl, fillLevel=0, fillBrush=color_list[i])
                            else:
                                pass
                        elif plot[0] == "imu":
                            if cl == 'RobotHardware0_gsensor':
                                self.items[cur_row][0].plot(cur_tm, cur_data[:, cur_col][::mabiki], pen=pyqtgraph.mkPen(color_list[cur_col%3], width=3-cur_col%3), name=['x', 'y', 'z'][cur_col%3])
                            elif cl == 'RobotHardware0_gyrometer':
                                self.items[cur_row][1].plot(cur_tm, cur_data[:, cur_col][::mabiki], pen=pyqtgraph.mkPen(color_list[cur_col%3], width=3-cur_col%3), name=['x', 'y', 'z'][cur_col%3])
                        else:
                            cur_plot_item.plot(cur_tm, cur_data[:, cur_col][::mabiki], pen=pyqtgraph.mkPen(color_list[i], width=len(cur_logs)-i), name=cl)
                # calculate y range of each rows using autofit function and then link y range each row
                y_min = min([p.viewRange()[1][0] for p in self.items[cur_row]])
                y_max = max([p.viewRange()[1][1] for p in self.items[cur_row]])
                if plot[0] != "joint_angle" and plot[0].find("_force") == -1 and plot[0] != "imu":
                    self.items[cur_row][0].setYRange(y_min, y_max)
                    for p in self.items[cur_row]:
                        p.setYLink('r'+str(cur_row)+'c0')
                # increase current row
                cur_row = cur_row + 1
        self.view.showMaximized()
        print '[%f] : finish plotData' % (time.time() - start_time)

if __name__  == '__main__':
    # time
    start_time = time.time()
    print '[%f] : start !!!' % (time.time() - start_time)
    # args
    parser = argparse.ArgumentParser(description='plot data from hrpsys log')
    parser.add_argument('-f', type=str, help='input file', metavar='file', required=True)
    parser.add_argument('--conf', type=str, help='configure file', metavar='file', required=True)
    parser.add_argument('--min_time', type=float, help='xmin for graph : not implemented yet', default=0.0)
    parser.add_argument('--max_time', type=float, help='xmax for graph : not implemented yet', default=0.0)
    parser.add_argument('-t', type=str, help='title', default="")
    parser.add_argument('--mabiki', type=int, help='mabiki step', default=1)
    parser.set_defaults(feature=False)
    args = parser.parse_args()
    # main
    a = DataloggerLogParserController(args.f, args.conf, args.t)
    a.readData(args.min_time, args.max_time)
    a.plotData(args.mabiki)
    pyqtgraph.Qt.QtGui.QApplication.instance().exec_()
