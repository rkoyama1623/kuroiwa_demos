#!/usr/bin/env python

import csv, argparse, numpy, math, time, struct, yaml, sys, functools

try:
    import pyqtgraph
except:
    print "please install pyqtgraph. see http://www.pyqtgraph.org/"
    sys.exit(1)

class MainWindow(pyqtgraph.QtGui.QWidget):
    def __init__(self, fname, yname, title, parent=None):
        self.app = pyqtgraph.Qt.QtGui.QApplication([])
        super(MainWindow, self).__init__(parent)

        self.log_parser = DataloggerLogParserController(fname, yname, title)
        parser = self.log_parser
        self.fname = fname
        with open(yname, "r") as f:
            self.plot_dic = yaml.load(f)
        self.main_layout = pyqtgraph.QtGui.QGridLayout()
        self.setLayout(self.main_layout)
        if title == '':
            self.setWindowTitle(fname.split('/')[-1])
        else:
            self.setWindowTitle(title)
        self.dummy_graph_widgets = []# for axis link

        for r in range(parser.row_num):
            self.dummy_graph_widgets.append(pyqtgraph.GraphicsLayoutWidget())
            self.dummy_graph_widgets[r].addPlot(name='r'+str(r))

            row_layout = pyqtgraph.QtGui.QGridLayout()
            self.main_layout.addLayout(row_layout,r,1)

            button = pyqtgraph.QtGui.QPushButton("+")
            button.setCheckable(True)
            button.setChecked(True)
            button.setMaximumHeight(25)
            button.setMaximumWidth(25)
            button.clicked.connect(functools.partial(self.switchRowDisplayCustomed,row=r))
            self.main_layout.addWidget(button,r,0)

            parser.items.append([])
            for c in range(parser.col_num):
                button = pyqtgraph.QtGui.QPushButton("+")
                button.setCheckable(True)
                button.setChecked(True)
                button.setMaximumHeight(15)
                button.setMaximumWidth(15)
                button.clicked.connect(functools.partial(self.switchGraphDisplay,row=r,col=c))
                row_layout.addWidget(button,0,c)

                graph_widget = pyqtgraph.GraphicsLayoutWidget()
                graph_widget.setBackground('w')
                row_layout.addWidget(graph_widget,1,c)
                plot_item = graph_widget.addPlot(row=None, col=None)
                customed_plot_item = CustomedPlotItem(plot_item)
                plot_item.setXLink('r0')
                parser.items[r].append(customed_plot_item)

    def switchRowDisplayCustomed(self, row):
        func = self.main_layout.itemAtPosition(row,0).widget().isChecked() and self.addGraph or self.removeGraph
        for col in range(0,self.main_layout.itemAtPosition(row,1).columnCount()):
            if self.main_layout.itemAtPosition(row,1).itemAtPosition(0,col).widget().isChecked():
                func(row, col)

    def switchRowDisplay(self, row):
        for col in range(0,self.main_layout.itemAtPosition(row,1).columnCount()):
            self.switchGraphDisplay(row,col)

    def switchGraphDisplay(self, row, col):
        if self.main_layout.itemAtPosition(row,1).itemAtPosition(0,col).widget().isChecked():
            self.addGraph(row, col)
        else:
            self.removeGraph(row, col)

    def removeGraph(self, row, col):
        self.main_layout.itemAtPosition(row,1).itemAtPosition(1,col).widget().deleteLater()

    def addGraph(self, row, col):
        gwidget = pyqtgraph.GraphicsLayoutWidget()
        gwidget.setBackground('w')
        self.log_parser.items[row][col].plot_item = gwidget.addPlot()
        self.log_parser.items[row][col].plot_item.setXLink('r0')
        self.main_layout.itemAtPosition(row,1).addWidget(gwidget,1,col)
        self.log_parser.items[row][col].plotAllData(1)

class DataloggerLogParserController:
    def __init__(self, fname, yname, title):
        self.fname = fname
        with open(yname, "r") as f:
            self.plot_dic = yaml.load(f)
        # self.dataListDict = {'time':[]}
        self.dataListDict = {}
        self.app = pyqtgraph.Qt.QtGui.QApplication([])
        self.items = []
        self.row_num = sum([len(x[1]["field"]) for x in self.plot_dic.items()])
        self.col_num = max([max([len(fld) for fld in x[1]["field"]]) for x in self.plot_dic.items()])

    def readData(self, xmin, xmax):
        print '[%f] : start readData' % (time.time() - start_time)
        # store data
        topic_list = list(set(reduce(lambda x, y : x + y, [sum(x["arg"],[]) for x in self.plot_dic.values()])))
        tmpDataListDict = {}
        for topic in topic_list:
            self.dataListDict[topic] = [[]] # first list is for time
            tmpDataListDict[topic] = []
            with open(self.fname + '.' + topic, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    self.dataListDict[topic][0].append(float(row[0]))
                    dl = row[1:]
                    dl = filter(lambda x: x != '', dl)
                    tmpDataListDict[topic].append([float(x) for x in dl])
        # fix servoState
        if 'RobotHardware0_servoState' in topic_list:
            ss_tmp = tmpDataListDict['RobotHardware0_servoState']
            for i, ssl in enumerate(ss_tmp):
                ss_tmp[i] = [struct.unpack('f', struct.pack('i', int(ss)))[0] for ss in ssl]
            tmpDataListDict['RobotHardware0_servoState'] = ss_tmp
        min_time = min([self.dataListDict[topic][0][0] for topic in topic_list])
        for topic in topic_list:
            self.dataListDict[topic][0] = numpy.array([x - min_time for x in self.dataListDict[topic][0]])
            self.dataListDict[topic].append(numpy.array(tmpDataListDict[topic]))
        print '[%f] : finish readData' % (time.time() - start_time)

    def plotData(self, mabiki):
        print '[%f] : start plotData' % (time.time() - start_time)
        # tm = self.dataListDict['time'][::mabiki]
        self.color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        cur_row = 0
        for plot in self.plot_dic.items(): # plot : ('joint_velocity', {'field':[[0,1],[2,3]], 'log':['rh_q', 'st_q']})
            cur_fields = plot[1]['field']
            cur_args = plot[1]['arg']
            cur_logs = list(set(sum(cur_args,[])))
            cur_funcs = 'func' in plot[1].keys() and plot[1]['func'] or None
            cur_names = 'name' in plot[1].keys() and plot[1]['name'] or []
            post_processes = 'post-process' in plot[1].keys() and plot[1]['post-process'] or None
            for cf in cur_fields: # cf : [0,1] -> [2,3]
                for cur_col in cf:
                    self.items[cur_row][cur_col-cf[0]].setPlotData(cur_field_offset=cf[0], row_num=self.row_num, group=plot[0], col_idx=cur_col, row_idx=cur_row, args_list=cur_args, funcs=cur_funcs, names=cur_names, post_processes=post_processes)
                    for cur_log in cur_logs:
                         self.items[cur_row][cur_col-cf[0]].plot_data_dict[cur_log] ={"data":self.dataListDict[cur_log][1], "tm":self.dataListDict[cur_log][0]}
                    self.items[cur_row][cur_col-cf[0]].plotAllData(mabiki)
                y_min = min([val.plot_item.viewRange()[1][0] for val in self.items[cur_row]])
                y_max = max([val.plot_item.viewRange()[1][1] for val in self.items[cur_row]])
                if plot[0] != "joint_angle" and plot[0].find("_force") == -1 and plot[0] != "imu" and plot[0] != "comp":
                    self.items[cur_row][0].plot_item.setYRange(y_min, y_max)
                    for p in self.items[cur_row]:
                        p.plot_item.setYLink('r'+str(cur_row))
                # increase current row
                cur_row = cur_row + 1
        print '[%f] : finish plotData' % (time.time() - start_time)

class CustomedPlotItem():
    def __init__(self, plot_item, parent=None):
        self.plot_item = plot_item
        self.color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        self.plot_data_dict = {}
        self.args_list = None
        self.funcs = None

    def setPlotData(self, cur_field_offset, row_num, group, col_idx, row_idx, args_list, funcs, names, post_processes):
        if self.args_list == None:
            self.cur_field_offset = cur_field_offset
            self.row_num = row_num
            self.group = group
            self.col_idx = col_idx
            self.row_idx = row_idx
            self.args_list = args_list
            self.funcs = funcs
            self.func_codes = []
            self.names = names
            self.post_processes = post_processes

            assert self.funcs == None or len(self.funcs) == len(self.args_list)
            assert self.post_processes == None or len(self.post_processes) == len(self.args_list)

            if self.funcs != None:
                for func_src in self.funcs:
                    self.func_codes.append(eval(func_src))

    def plotAllData(self, mabiki):
        if self.args_list != None:
            for i in range(len(self.args_list)):
                self.plotData(i, mabiki)

    def plotData(self, i, mabiki):
        args = self.args_list[i]
        name = len(self.names) == len(self.args_list) and self.names[i] or args[0]
        plot_data = self.plot_data_dict[args[0]]
        cl = args[0]
        cur_data = plot_data["data"]
        cur_tm = plot_data["tm"]
        cur_plot_item = self.plot_item
        cur_plot_item.setTitle(self.group+" "+str(self.col_idx))
        cur_plot_item.showGrid(x=True, y=True)
        cur_plot_item.addLegend(offset=(0, 0))
        if self.row_idx == self.row_num -1:
            cur_plot_item.setLabel("bottom", text="time", units="s")
        if self.col_idx-self.cur_field_offset == 0:
            tmp_units = None
            if self.group == "12V" or self.group == "80V":
                tmp_units = "V"
            elif self.group == "current":
                tmp_units = "A"
            elif self.group == "temperature" or self.group == "joint_angle" or self.group == "attitude" or self.group == "tracking":
                tmp_units = "deg"
            elif self.group == "joint_velocity":
                tmp_units = "deg/s"
            elif self.group == "watt":
                tmp_units = "W"
            cur_plot_item.setLabel("left", text="", units=tmp_units)
        if self.funcs == None or self.funcs[i] == '':
            assert len(args) == 1
            plot_data = self.plot_data_dict[args[0]]
            cur_plot_item.plot(plot_data["tm"], plot_data["data"][:, self.col_idx][::mabiki], pen=pyqtgraph.mkPen(self.color_list[i], width=len(self.args_list)-i), name=name)
        else:
            data_list = [self.plot_data_dict[arg]["data"] for arg in args]
            func_src = self.funcs[i]
            self.plot_item.plot(self.plot_data_dict[args[0]]["tm"], self.func_codes[i](data_list, self.col_idx, mabiki),  pen=pyqtgraph.mkPen(self.color_list[i], width=len(self.args_list)-i), name=name)
        if self.post_processes != None:
            exec(self.post_processes[i])

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
    main_window = MainWindow(args.f, args.conf, args.t)
    main_window.log_parser.readData(args.min_time, args.max_time)
    main_window.log_parser.plotData(args.mabiki)
    main_window.showMaximized()
    pyqtgraph.Qt.QtGui.QApplication.instance().exec_()
