#!/usr/bin/env python
import matplotlib.pyplot
import argparse, rosbag, tf, math

parser = argparse.ArgumentParser(description='check transformation between odom and base_footprint')
parser.add_argument('-f', help='target rosbag file', type=str, required=True)
args = parser.parse_args()

x_list = []
y_list = []
yaw_list = []
tm_list = []

for topic, msg, t in rosbag.Bag(args.f):
    if topic == "/tf":
        for trans in msg.transforms:
            if trans.child_frame_id == "base_footprint" and trans.header.frame_id == "odom":
                rot = trans.transform.rotation
                rpy = tf.transformations.euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])
                x_list.append(trans.transform.translation.x)
                y_list.append(trans.transform.translation.y)
                yaw_list.append(rpy[2])
                tm_list.append(t.to_time())

# plot yaw direction once every 30 times
for x, y, yaw, t in zip(x_list, y_list, yaw_list, tm_list)[::30]:
    matplotlib.pyplot.quiver(x, y, 0.05 * math.cos(yaw), 0.05 * math.sin(yaw), angles='xy', scale=2, headwidth=1)
# plot the start and end point
start = [x_list[0], y_list[0]]
end = [x_list[-1], y_list[-1]]
distance = math.sqrt(math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2))
matplotlib.pyplot.plot(start[0], start[1], 'ro')
matplotlib.pyplot.plot(end[0], end[1], 'go')
title = "start : [" + ("%.3f" % start[0]) + ", " + ("%.3f" % start[1]) + "], end : [" + ("%.3f" % end[0]) + ", " + ("%.3f" % end[1]) + "], distance : " + ("%.3f" % distance)
matplotlib.pyplot.title(title)
# plot all the points
matplotlib.pyplot.plot(x_list, y_list)
matplotlib.pyplot.minorticks_on()
matplotlib.pyplot.grid(True)
matplotlib.pyplot.axes().set_aspect('equal')
matplotlib.pyplot.show()
