#!/usr/bin/env python

import csv, argparse, numpy, math, time, struct, yaml, sys, functools, itertools

try:
    import pyqtgraph
except:
    print "please install pyqtgraph. see http://www.pyqtgraph.org/"
    sys.exit(1)

def makeProxy(max_height=15, max_width=15, isChecked=True):
    prox = pyqtgraph.Qt.QtGui.QGraphicsProxyWidget()
    btn = pyqtgraph.Qt.QtGui.QPushButton("+")
    btn.setCheckable(True)
    btn.setChecked(isChecked)
    btn.setMaximumHeight(max_height)
    btn.setMaximumWidth(max_width)
    prox.setWidget(btn)
    return prox

class MainWindow(pyqtgraph.QtGui.QWidget):
    def __init__(self, fname, yname, title, display_button, parent=None):
        self.app = pyqtgraph.Qt.QtGui.QApplication([])
        super(MainWindow, self).__init__(parent)

        self.log_parser = DataloggerLogParserController(fname, yname, title)
        parser = self.log_parser
        self.fname = fname
        with open(yname, "r") as f:
            self.plot_dic = yaml.load(f)

        self.main_layout = pyqtgraph.QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

        self.menu_dict = {}
        self.menubar = pyqtgraph.QtGui.QMenuBar(self)
        self.menu_dict["file"] = self.menubar.addMenu('File')
        self.menu_dict["view"] = self.menubar.addMenu('View')
        self.menu_dict["setting"] = self.menubar.addMenu('Setting')
        action = self.menu_dict["view"].addAction('hide button',self.switchProxyDisplay)
        action.setCheckable(True)
        if not display_button: action.setChecked(True)

        self.graph_widget = pyqtgraph.GraphicsLayoutWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.ci.setSpacing(0)
        self.graph_widget.ci.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.graph_widget)

        self.graph_button_max_width = 15
        self.graph_button_max_height = 15
        self.row_button_max_width = 25
        self.row_button_max_height = 25

        if title == '':
            self.setWindowTitle(fname.split('/')[-1])
        else:
            self.setWindowTitle(title)

        # for xlink sync
        self.dummy_widget = pyqtgraph.GraphicsLayoutWidget()
        self.dummy_plot = self.dummy_widget.addPlot()
        self.dummy_plot.plot(numpy.random.normal(size=1000),numpy.random.normal(size=1000))
        self.dummy_widget.showMinimized()
        # self.closeEvent = self.dummy_widget.destroy

        for r in range(parser.row_num):
            row_layout = self.graph_widget.addLayout(r,0)
            row_layout.setSpacing(0)
            row_layout.setContentsMargins(0,0,0,0)

            if display_button:
                proxy = makeProxy(max_height=self.row_button_max_height, max_width=self.row_button_max_width)
                proxy.widget().clicked.connect(functools.partial(self.switchRowDisplayCustomed, row=r))
                row_layout.addItem(proxy,row=0,col=0)

            parser.items.append([])
            for c in range(parser.col_num):
                cell_layout = row_layout.addLayout(row=0, col=c+1)
                cell_layout.setSpacing(0)
                cell_layout.setContentsMargins(0,0,0,0)

                if display_button:
                    proxy = makeProxy()
                    proxy.widget().clicked.connect(functools.partial(self.switchGraphDisplay, row=r, col=c))
                    cell_layout.addItem(proxy, row=0, col=0)

                plot_item = cell_layout.addPlot(row=1,col=0)
                customed_plot_item = CustomedPlotItem(plot_item)
                parser.items[r].append(customed_plot_item)
                plot_item.setXLink(self.dummy_plot)

    def closeEvent(self, event):
        self.dummy_widget.destroy()
        self.destroy()

    def switchProxyDisplay(self):
        # func = self.menu_dict["view"].actionAt(pyqtgraph.QtCore.QPoint(0,1)).isChecked() and self.removeRowProxy or self.addRowProxy
        func = self.menu_dict["view"].actions()[0].isChecked() and self.removeRowProxy or self.addRowProxy
        for row in range(self.log_parser.row_num):
            func(row)

    def removeRowProxy(self, row):
        self.graph_widget.getItem(row,0).getItem(0,0).widget().setMaximumWidth(0)
        self.graph_widget.getItem(row,0).getItem(0,0).widget().setMaximumHeight(0)
        for col in range(self.graph_widget.getItem(row,0).currentCol-1):
            self.removeProxy(row, col)

    def addRowProxy(self, row):
        self.graph_widget.getItem(row,0).getItem(0,0).widget().setMaximumWidth(self.row_button_max_width)
        self.graph_widget.getItem(row,0).getItem(0,0).widget().setMaximumHeight(self.row_button_max_height)
        for col in range(self.graph_widget.getItem(row,0).currentCol-1):
            self.addProxy(row, col)

    def removeProxy(self, row, col):
        self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(0,0).widget().setMaximumWidth(0)
        self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(0,0).widget().setMaximumHeight(0)

    def addProxy(self, row, col):
        self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(0,0).widget().setMaximumWidth(self.graph_button_max_width)
        self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(0,0).widget().setMaximumHeight(self.graph_button_max_height)

    def switchRowDisplayCustomed(self, row):
        func = self.graph_widget.getItem(row,0).getItem(0,0).widget().isChecked() and self.addGraph or self.removeGraph
        for col in range(self.graph_widget.getItem(row,0).currentCol-1):
            if self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(0,0).widget().isChecked():
                func(row, col)

    def switchRowDisplay(self, row):
        for col in range(0,self.view.ci.getItem(row,0).columnCount()):
            self.switchGraphDisplay(row,col)

    def switchGraphDisplay(self, row, col):
        if self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(0,0).widget().isChecked():
            self.addGraph(row, col)
        else:
            self.removeGraph(row, col)

    def removeGraph(self, row, col):
        self.graph_widget.getItem(row,0).getItem(0,col+1).getItem(1,0).deleteLater()

    def addGraph(self, row, col):
        self.log_parser.items[row][col].plot_item = self.graph_widget.getItem(row,0).getItem(0,col+1).addPlot(row=1,col=0)
        self.log_parser.items[row][col].plot_item.setXLink(self.dummy_plot)
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
        topic_list = list(set(reduce(lambda x, y : x + y, [list(itertools.chain.from_iterable(x["arg"])) for x in self.plot_dic.values()])))
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
            cur_args_list = plot[1]['arg']
            cur_logs = list(set(sum(cur_args_list,[])))
            cur_funcs = 'func' in plot[1].keys() and plot[1]['func'] or None
            cur_names_lists = 'name' in plot[1].keys() and plot[1]['name'] or [[[] for cur_field in cur_fields] for args in cur_args_list]
            cur_indices_lists = 'index' in plot[1].keys() and plot[1]['index'] or [[cur_fields for arg in args] for args in cur_args_list]
            post_processes = 'post-process' in plot[1].keys() and plot[1]['post-process'] or None

            assert len(cur_args_list) == len(cur_indices_lists)
            for args, indices_list in zip(cur_args_list, cur_indices_lists): assert len(args) == len(indices_list)

            for field_idx, cf in enumerate(cur_fields): # cf : [0,1] -> [2,3]
                for col_idx, cur_col in enumerate(cf):
                    # procedure for parsing indices_list and names_list
                    indices_list = []
                    names = []
                    for args, idxs_list, nms_list in zip(cur_args_list, cur_indices_lists, cur_names_lists):
                        tmp = []
                        for arg, idxs in zip(args, idxs_list):
                            if idxs[field_idx] == []:
                                idxs[field_idx] = cf
                            else: assert len(idxs[field_idx]) == len(cf)
                            tmp.append(idxs[field_idx][col_idx])
                        indices_list.append(tmp)
                        if nms_list[field_idx] == []:
                            nms_list[field_idx] = [args[0] for val in cf]
                        else: assert len(nms_list[field_idx]) == len(cf)
                        names.append(nms_list[field_idx][col_idx])

                    self.items[cur_row][cur_col-cf[0]].pushPlotData(cur_field_offset=cf[0], row_num=self.row_num, group=plot[0], col_idx=cur_col, row_idx=cur_row, args_list=cur_args_list, funcs=cur_funcs, names=names, post_processes=post_processes, indices_list=indices_list)
                    for cur_log in cur_logs:
                         self.items[cur_row][cur_col-cf[0]].plot_data_dict[cur_log] ={"data":self.dataListDict[cur_log][1], "tm":self.dataListDict[cur_log][0]}

                for col_idx, cur_col in enumerate(cf):
                    # procedure for parsing indices_list
                    self.items[cur_row][col_idx].plotAllData(mabiki)

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
        self.args_list = []
        self.funcs = []
        self.func_codes = []
        self.post_processes = []
        self.indices_list = []
        self.names = []

    def pushPlotData(self, cur_field_offset, row_num, group, col_idx, row_idx, args_list, funcs, names, post_processes, indices_list):
        self.cur_field_offset = cur_field_offset
        self.row_num = row_num
        self.group = group
        self.col_idx = col_idx
        self.row_idx = row_idx
        self.args_list += args_list
        if funcs != None: self.funcs += funcs
        if post_processes != None: self.post_processes += post_processes
        self.names += names
        self.indices_list += indices_list

        assert funcs == None or len(funcs) == len(args_list)
        assert post_processes == None or len(post_processes) == len(args_list)

        if funcs != None:
            for func_src in funcs:
                self.func_codes.append(eval(func_src))

    def plotAllData(self, mabiki):
        if self.args_list != []:
            for i in range(len(self.args_list)):
                self.plotData(i, mabiki)

    def plotData(self, i, mabiki):
        args = self.args_list[i]
        indices = self.indices_list[i]
        name = self.names[i]
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
        if self.funcs == [] or self.funcs[i] == '':
            assert len(args) == 1
            plot_data = self.plot_data_dict[args[0]]
            cur_plot_item.plot(plot_data["tm"][::mabiki], plot_data["data"][:, indices[0]][::mabiki], pen=pyqtgraph.mkPen(self.color_list[i], width=2), name=name)
        else:
            data_list = [self.plot_data_dict[arg]["data"] for arg in args]
            func_src = self.funcs[i]
            self.plot_item.plot(self.plot_data_dict[args[0]]["tm"][::mabiki], self.func_codes[i](data_list, indices, mabiki), pen=pyqtgraph.mkPen(self.color_list[i], width=2), name=name)
        if self.post_processes != []:
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
    parser.add_argument('-b', type=bool, help='show button', default=False)
    parser.set_defaults(feature=False)
    args = parser.parse_args()
    # main
    main_window = MainWindow(args.f, args.conf, args.t, args.b)
    main_window.log_parser.readData(args.min_time, args.max_time)
    main_window.log_parser.plotData(args.mabiki)
    main_window.showMaximized()
    pyqtgraph.Qt.QtGui.QApplication.instance().exec_()
