#!/usr/bin/env python
import matplotlib.pyplot
import sys
import rosbag
from hrpsys_ros_bridge.msg import ContactState, ContactStateStamped, ContactStatesStamped

legs_contact_ref = [[], []]
legs_contact_act = [[], []]
legs_remaining = [[], []]
tm_list = [[], []]

for topic, msg, t in rosbag.Bag(sys.argv[1]):
    if topic == "/ref_contact_states":
        tm_list[0].append(t.to_time())
        for i, css in enumerate(msg.states):
            if i == 0 or i == 1:
                legs_contact_ref[i].append(css.state.state)
                legs_remaining[i].append(css.state.remaining_time)
    elif topic == "/act_contact_states":
        tm_list[1].append(t.to_time())
        for i, css in enumerate(msg.states):
            if i == 0 or i == 1:
                legs_contact_act[i].append(css.state.state)

tm_list = [[t - min([tm_list[0][0], tm_list[0][0]]) for t in ts] for ts in tm_list]

matplotlib.pyplot.plot(tm_list[0], legs_contact_ref[0], linewidth=8, color=[1,0,0], label="REF contact")
matplotlib.pyplot.plot(tm_list[1], legs_contact_act[0], linewidth=4, color=[0,1,0], label="ACT contact", linestyle="-")
matplotlib.pyplot.plot(tm_list[0], legs_remaining[0], linewidth=2, color=[1,0,0.8], label="remaining time", linestyle="--")

matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.xlim(4.8, 6.0)
matplotlib.pyplot.minorticks_on()
matplotlib.pyplot.grid(True)

matplotlib.pyplot.show()
