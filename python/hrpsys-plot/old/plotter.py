#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv, argparse, numpy, math, time, struct

class DataloggerLogParserController:
    def __init__(self, fname, title, hand_name, ljn):
        self.fname = fname
        self.portList = ['RobotHardware0_q', 'sh_qOut', 'abc_q', 'st_q',
                         'RobotHardware0_dq',
                         'RobotHardware0_tau',
                         'RobotHardware0_rfsensor', 'rmfo_off_rfsensor', 'st_refWrenchR', 'sh_rfsensorOut',
                         'RobotHardware0_lfsensor', 'rmfo_off_lfsensor', 'st_refWrenchL', 'sh_lfsensorOut',
                         'RobotHardware0_r'+hand_name, 'rmfo_off_r'+hand_name, 'sh_r'+hand_name+'Out',
                         'RobotHardware0_l'+hand_name, 'rmfo_off_l'+hand_name, 'sh_l'+hand_name+'Out',
                         'kf_rpy', 'sh_baseRpyOut', 'st_actBaseRpy', 'st_currentBaseRpy',
                         'RobotHardware0_gsensor', 'RobotHardware0_gyrometer',
                         'RobotHardware0_servoState']
        self.dataListDict = {'time':[]}
        self.limb_joint_num = ljn
        self.pp = PdfPages('/tmp/foo.pdf')
        self.fig = None
        self.axes_array = None
        if title == '':
            self.setLayout(fname.split('/')[-1])
        else:
            self.setLayout(title)

    def setLayout(self, title):
        self.fig, (self.axes_array) = plt.subplots(23, self.limb_joint_num, sharex=True, sharey=False)
        self.fig.set_size_inches(40.0, 60.0)
        # visual
        for ax in self.fig.axes:
            ax.minorticks_on()
            ax.grid(True)
        self.fig.suptitle(title)

    def readData(self, xmin, xmax):
        print '[%f] : start readData' % (time.time() - start_time)
        # store data
        for port in self.portList:
            self.dataListDict[port] = []
            with open(self.fname + '.' + port, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    dl = row[1:]
                    dl = filter(lambda x: x != '', dl)
                    self.dataListDict[port].append([float(x) for x in dl])
                    if port == 'sh_qOut':
                        self.dataListDict['time'].append(float(row[0]))
        self.dataListDict['time'] = [x - self.dataListDict['time'][0] for x in self.dataListDict['time']]
        # trim data
        min_index = -1
        max_index = -2
        tm_list_tmp = self.dataListDict['time']
        for i, tm in enumerate(tm_list_tmp):
            if min_index < 0:
                if tm > xmin:
                    min_index = i - 1
            if max_index < 0 and xmax > 0:
                if tm > xmax:
                    max_index = i - 1
        if max_index < 0:
            if min_index > 0:
                for k, v in self.dataListDict.iteritems():
                    self.dataListDict[k] = v[min_index:]
            else:
                pass
        else:
            if min_index > 0:
                for k, v in self.dataListDict.iteritems():
                    self.dataListDict[k] = v[min_index:max_index+1]
            else:
                exit()
        if xmin >0 and xmax > xmin:
            self.axes_array[0][0].set_xlim(xmin=xmin, xmax=xmax)
        elif xmin > 0:
            self.axes_array[0][0].set_xlim(xmin=xmin)
        else:
            pass
        # fix servoState
        ss_tmp = self.dataListDict['RobotHardware0_servoState']
        for i, ssl in enumerate(ss_tmp):
            ss_tmp[i] = [struct.unpack('f', struct.pack('i', int(ss))) for ss in ssl]
        self.dataListDict['RobotHardware0_servoState'] = ss_tmp
        print '[%f] : finish readData' % (time.time() - start_time)

    def plotData(self, mabiki, top_id, hand_name):
        print '[%f] : start plotData' % (time.time() - start_time)
        offset = 0
        plt.sca(self.axes_array[0][0])
        col_num = len(self.axes_array[0])
        tm = self.dataListDict['time'][::mabiki]
        # joint angle
        rh_q = numpy.array(self.dataListDict['RobotHardware0_q'])
        sh_qOut = numpy.array(self.dataListDict['sh_qOut'])
        abc_q = numpy.array(self.dataListDict['abc_q'])
        st_q = numpy.array(self.dataListDict['st_q'])
        for i in range(self.limb_joint_num*2):
            for j, ql in enumerate([rh_q, sh_qOut, abc_q, st_q]):
                self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, [math.degrees(x) for x in ql[:, (i+top_id)]][::mabiki], linewidth=5-j, label=['RobotHardware0_q', 'sh_qOut', 'abc_q', 'st_q'][j%4])
                self.axes_array[(i+offset)/col_num][i%col_num].set_title('position [deg] / ' + str(i+top_id))
        offset = offset + self.limb_joint_num*2
        # diff
        rh_ss = numpy.array(self.dataListDict['RobotHardware0_servoState'])
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, [math.degrees(x) for x in (st_q - rh_q)[:, (i+top_id)]][::mabiki], linewidth=1, label='st_q - rh_q', color='b')
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, [math.degrees(x) for x in rh_ss[:, (10+1)*(i+top_id)+(6+1)]][::mabiki], linewidth=2, label='abs - enc', color='y')
            self.axes_array[(i+offset)/col_num][i%col_num].axhline(y=4.5, linewidth=2, color='r')
            self.axes_array[(i+offset)/col_num][i%col_num].axhline(y=-4.5, linewidth=2, color='r')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('diff [deg] / ' + str(i+top_id))
            self.axes_array[(i+offset)/col_num][i%col_num].set_ylim([-4.5, 4.5])
        offset = offset + self.limb_joint_num*2
        # velocity
        rh_dq = numpy.array(self.dataListDict['RobotHardware0_dq'])
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, [math.degrees(x) for x in rh_dq[:, (i+top_id)]][::mabiki], color='b')
            self.axes_array[(i+offset)/col_num][i%col_num].axhline(y=250.0, linewidth=2, color='r')
            self.axes_array[(i+offset)/col_num][i%col_num].axhline(y=-250.0, linewidth=2, color='r')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('velocity : [deg/s] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # torque
        rh_tau = numpy.array(self.dataListDict['RobotHardware0_tau'])
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_tau[:, (i+top_id)][::mabiki], color='r')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('torque : [Nm] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # watt
        watt = rh_dq * rh_tau
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].fill_between(tm, [0]*len(watt[:, (i+top_id)][::mabiki]), watt[:, (i+top_id)][::mabiki], color='g')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('power : [W] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # force / moment
        for j, rl in enumerate(['r', 'l']):
            rh_f = numpy.array(self.dataListDict['RobotHardware0_' + rl + 'fsensor'])
            rmfo_f = numpy.array(self.dataListDict['rmfo_off_' + rl + 'fsensor'])
            st_f = numpy.array(self.dataListDict['st_refWrench' + rl.upper()])
            sh_f = numpy.array(self.dataListDict['sh_' + rl + 'fsensorOut'])
            for i in range(6):
                for k, fl in enumerate([rh_f, rmfo_f, st_f, sh_f]):
                    self.axes_array[(i+offset)/col_num+j][i%col_num].plot(tm, fl[:, i][::mabiki], linewidth=4-k, label=['RobotHardware0', 'rmfo_off', 'st_refWrench', 'sh'][k%4])
                if i < 3:
                    self.axes_array[(i+offset)/col_num+j][i%col_num].set_title('Force ' + ['x', 'y', 'z'][i] + ' [N] : ' + rl.upper() + 'leg')
                else:
                    self.axes_array[(i+offset)/col_num+j][i%col_num].set_title('Moment ' + ['x', 'y', 'z'][i-3] + ' [Nm] : ' + rl.upper() + 'leg')
        self.axes_array[10][2].set_ylim(ymin=-2000, ymax=2000)
        self.axes_array[11][2].set_ylim(ymin=-2000, ymax=2000)
        self.axes_array[10][3].set_ylim(ymin=-80, ymax=80)
        self.axes_array[11][3].set_ylim(ymin=-80, ymax=80)
        self.axes_array[10][4].set_ylim(ymin=-80, ymax=80)
        self.axes_array[11][4].set_ylim(ymin=-80, ymax=80)
        offset = offset + self.limb_joint_num*2
        # force / moment hand
        for j, rl in enumerate(['r', 'l']):
            rh_f = numpy.array(self.dataListDict['RobotHardware0_' + rl + hand_name])
            rmfo_f = numpy.array(self.dataListDict['rmfo_off_' + rl + hand_name])
            sh_f = numpy.array(self.dataListDict['sh_' + rl + hand_name + 'Out'])
            for i in range(6):
                for k, fl in enumerate([rh_f, rmfo_f, sh_f]):
                    self.axes_array[(i+offset)/col_num+j][i%col_num].plot(tm, fl[:, i][::mabiki], linewidth=4-k, label=['RobotHardware0', 'rmfo_off', 'sh'][k%3])
                if i < 3:
                    self.axes_array[(i+offset)/col_num+j][i%col_num].set_title('Force ' + ['x', 'y', 'z'][i] + ' [N] : ' + rl.upper() + 'hand')
                else:
                    self.axes_array[(i+offset)/col_num+j][i%col_num].set_title('Moment ' + ['x', 'y', 'z'][i-3] + ' [Nm] : ' + rl.upper() + 'hand')
        offset = offset + self.limb_joint_num*2
        # RPY / IMU
        kf = numpy.array(self.dataListDict['kf_rpy'])
        sh_rpy = numpy.array(self.dataListDict['sh_baseRpyOut'])
        st_act = numpy.array(self.dataListDict['st_actBaseRpy'])
        st_cur = numpy.array(self.dataListDict['st_currentBaseRpy'])
        rh_acc = numpy.array(self.dataListDict['RobotHardware0_gsensor'])
        rh_gyro = numpy.array(self.dataListDict['RobotHardware0_gyrometer'])
        for i in range(6):
            if i < 3:
                for j, rpyl in enumerate([kf, sh_rpy, st_act, st_cur]):
                    self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, [math.degrees(x) for x in rpyl[:, i]][::mabiki], linewidth=5-j, label=['kf', 'sh_baseRpyOut', 'st_actBaseRpy', 'st_currentBaseRpy'][j%4])
                    self.axes_array[(i+offset)/col_num][i%col_num].set_title(['Roll', 'Pitch', 'Yaw'][i] + ' [deg]')
            elif i == 3:
                for j in range(3):
                    self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_acc[:, j][::mabiki], label=['x','y','z'][j])
                    self.axes_array[(i+offset)/col_num][i%col_num].set_title('Acceleration [m/s^2]')
            elif i == 4:
                for j in range(3):
                    self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_gyro[:, j][::mabiki], label=['x','y','z'][j])
                    self.axes_array[(i+offset)/col_num][i%col_num].set_title('Gyro [rad/s]')
        offset = offset + self.limb_joint_num
        # 12V
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_ss[:, (10+1)*(i+top_id)+(9+1)][::mabiki], color='y')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('12V Line : [V] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # 80V
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_ss[:, (10+1)*(i+top_id)+(2+1)][::mabiki], color='m')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('80V Line : [V] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # temperature
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_ss[:, (10+1)*(i+top_id)+(0+1)][::mabiki], linewidth=1, label='inner', color='g')
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_ss[:, (10+1)*(i+top_id)+(7+1)][::mabiki], linewidth=2, label='outer', color='r')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('temperature : [deg] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # current
        for i in range(self.limb_joint_num*2):
            self.axes_array[(i+offset)/col_num][i%col_num].plot(tm, rh_ss[:, (10+1)*(i+top_id)+(1+1)][::mabiki], color='y')
            self.axes_array[(i+offset)/col_num][i%col_num].set_title('output current : [A] / ' + str(i+top_id))
        min_tmp = min([ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[0] for ax in self.axes_array[(i+offset)/col_num]])
        max_tmp = max([ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num-1]] + [ax.get_ylim()[1] for ax in self.axes_array[(i+offset)/col_num]])
        for ax in self.axes_array[(i+offset)/col_num-1]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        for ax in self.axes_array[(i+offset)/col_num]:
            ax.set_ylim(ymin=min_tmp, ymax=max_tmp)
        offset = offset + self.limb_joint_num*2
        # set legend
        self.axes_array[0][0].legend(loc=0)
        self.axes_array[2][0].legend(loc=0)
        self.axes_array[10][5].legend(loc=0)
        self.axes_array[12][5].legend(loc=0)
        self.axes_array[14][2].legend(loc=0)
        self.axes_array[14][3].legend(loc=0)
        self.axes_array[14][4].legend(loc=0)
        self.axes_array[20][0].legend(loc=0)
        print 'saving ...'
        self.pp.savefig(self.fig)
        self.pp.close()
        print '[%f] : finish plotData' % (time.time() - start_time)

if __name__  == '__main__':
    # time
    start_time = time.time()
    print '[%f] : start !!!' % (time.time() - start_time)
    # args
    parser = argparse.ArgumentParser(description='plot data from hrpsys log')
    parser.add_argument('-f', type=str, help='input file', metavar='file', default='/tmp/log/naname-block_JAXON_20150422')
    parser.add_argument('--xmin', type=float, help='xmin for graph', default=0.0)
    parser.add_argument('--xmax', type=float, help='xmax for graph', default=0.0)
    parser.add_argument('-t', type=str, help='title', default="")
    parser.add_argument('--mabiki', type=int, help='mabiki step', default=1)
    parser.add_argument('--hand_sensor_name', type=str, help='for staro : asensor', default='hsensor')
    parser.add_argument('--leg_top_id', type=int, help='for staro : 16', default=0)
    parser.add_argument('--limb_joint_num', type=int, help='for arm : 8', default=6)
    parser.set_defaults(feature=False)
    args = parser.parse_args()
    # main
    a = DataloggerLogParserController(args.f, args.t, args.hand_sensor_name, args.limb_joint_num)
    a.readData(args.xmin, args.xmax)
    a.plotData(args.mabiki, args.leg_top_id, args.hand_sensor_name)
