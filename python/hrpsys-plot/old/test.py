#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyqtgraph

app = pyqtgraph.Qt.QtGui.QApplication([])

view = pyqtgraph.GraphicsLayoutWidget()

items = []
for r in range(4):
    items.append([])
    for c in range(6):
        items[r].append(view.addPlot(row=r, col=c))

view.show()
