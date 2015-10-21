### Tips

save the following commands as ~/.gnome2/nautilus-scripts/hrpsys-plot.sh and ``chmod +x ~/.gnome2/nautilus-scripts/hrpsys-plot.sh``

```bash
#!/bin/bash
gnome-terminal -t "aho" -x $SHELL -ic '$HOME/kuroiwa_demos/python/hrpsys-plot/datalogger-plotter-with-pyqtgraph.py -f ${NAUTILUS_SCRIPT_SELECTED_FILE_PATHS%.*} --conf $(zenity --file-selection --filename="$HOME/kuroiwa_demos/python/hrpsys-plot/default.yaml" --file-filter=*.yaml)'
exit
```
