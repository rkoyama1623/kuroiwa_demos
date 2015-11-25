### Tips

##### Left Click

save the following commands as ~/.gnome2/nautilus-scripts/hrpsys-plot.sh and ``chmod +x ~/.gnome2/nautilus-scripts/hrpsys-plot.sh`` and then ``nautilus -q``

```bash
#!/bin/bash
gnome-terminal -t "aho" -x $SHELL -ic '$HOME/kuroiwa_demos/python/hrpsys-plot/datalogger-plotter-with-pyqtgraph.py -f ${NAUTILUS_SCRIPT_SELECTED_FILE_PATHS%.*} --conf $(zenity --file-selection --filename="$HOME/kuroiwa_demos/python/hrpsys-plot/config/default.yaml" --file-filter=*.yaml)'
exit
```

##### Trim

After you plot all the data, you can see the plot during 0 ~ T[s].
So, if you want to trim a[s] ~ b[s],

```bash
a=5 \
b=10 \
T=1000 \
num=`wc -l \`ls | grep st_originRefCogVel\` | cut -d" " -f1` \
start=`expr $num / $T * \( $T - a \)` \
len=`expr $num / $T * \( $b - $a \)` \
mkdir /tmp/ahoaho/ \
for i in *; do tail $i -n $start | head -n $len > /tmp/ahoaho/$i; done
```
