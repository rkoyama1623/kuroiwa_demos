#!/bin/bash
script_dir=$(cd $(dirname $(readlink -f $0 || echo $0));pwd -P)
gnome-terminal -t "trim" -x $SHELL -ic $script_dir'/../datalogger-trimmer.py -f $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS --min $(zenity --entry --text="minimum time[s]") --max $(zenity --entry --text="maximum time[s]")'
