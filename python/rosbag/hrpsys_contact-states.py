#!/usr/bin/env python
import matplotlib.pyplot
import sys
import rosbag
from hrpsys_ros_bridge.msg import ContactState, ContactStateStamped, ContactStatesStamped

legs_contact = [[], []]
legs_remaining = [[], []]
tm_list = []

# for topic, msg, t in rosbag.Bag("/home/eisoku/2015-11-01-14-54-03.bag"):
for topic, msg, t in rosbag.Bag(sys.argv[1]):
    if topic == "/ref_contact_states":
        tm_list.append(t.to_time())
        for i, css in enumerate(msg.states):
            if i == 0 or i == 1:
                legs_contact[i].append(css.state.state)
                legs_remaining[i].append(css.state.remaining_time)

tm_list = [t - tm_list[0] for t in tm_list]

matplotlib.pyplot.plot(tm_list, legs_contact[0], linewidth=8, color=[1,0,0], label="Rleg contact")
matplotlib.pyplot.plot(tm_list, legs_contact[1], linewidth=6, color=[0,1,0], label="Lleg contact")
matplotlib.pyplot.plot(tm_list, legs_remaining[0], linewidth=4, color=[1,0,0.8], label="Rleg time", linestyle="--")
matplotlib.pyplot.plot(tm_list, legs_remaining[1], linewidth=2, color=[0,1,0.8], label="Lleg time", linestyle="--")

matplotlib.pyplot.annotate(r'Lleg starts landing',
                           xy=(0.6, 1.0), xycoords='data',
                           xytext=(+30, +60), textcoords='offset points', fontsize=16,
                           arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
matplotlib.pyplot.annotate(r'Rleg starts lifting',
                           xy=(0.8, 1.0), xycoords='data',
                           xytext=(+10, +30), textcoords='offset points', fontsize=16,
                           arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.xlim(0.0, 6.0)
matplotlib.pyplot.minorticks_on()
matplotlib.pyplot.grid(True)

matplotlib.pyplot.show()
