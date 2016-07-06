#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import math
import os, commands

def my_test(fname):
    os.system('rm /tmp/a.txt /tmp/a_scaled.txt /tmp/res.txt')
    os.system('./CNN/feature.py '+fname+' -c 1 --output /tmp/a.txt 2> /dev/null')
    os.system('svm-scale -r ./CNN/scale.txt /tmp/a.txt > /tmp/a_scaled.txt')
    os.system('svm-predict /tmp/a_scaled.txt ./CNN/my.model /tmp/res.txt')
    return commands.getoutput('cat /tmp/res.txt')

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        fname = filenames[0]
        self.window.button_pic.img = wx.Image(fname)
        self.window.button_pic.Refresh()
        self.window.text_expl.SetValue(fname)
        ret = my_test(fname)
        print ret
        if ret == '0':
            self.window.text_expl.SetValue('アコーディオン')
        elif ret == '1':
            self.window.text_expl.SetValue('カニ')
        elif ret == '2':
            self.window.text_expl.SetValue('ピザ')
        elif ret == '3':
            self.window.text_expl.SetValue('ヒトデ')
        elif ret == '4':
            self.window.text_expl.SetValue('陰陽')
        # for file in filenames:
        #     # print file
        #     self.window.button_pic.img = wx.Image(file)
        #     self.window.button_pic.Refresh()
        #     self.window.text_expl.SetValue(file)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target", size=(-1, -1))

        # The aspect ratio of root panel shoud be the one of A4
        root_panel = wx.Panel(self, wx.ID_ANY, size=(1000*math.sqrt(2), 1000))
        root_panel.SetBackgroundColour('red')
        sz = wx.BoxSizer(wx.VERTICAL)
        sz.Add(root_panel, flag=wx.SHAPED | wx.ALIGN_CENTER, proportion=1)
        self.SetSizer(sz)

        panels = [ExplanationDrawingPanel(root_panel) for i in range(6)]
        root_layout = wx.GridSizer(2, 3)
        for p in panels:
            root_layout.Add(p, flag=wx.SHAPED | wx.ALL, border=10)
            dt = MyFileDropTarget(p)
            p.SetDropTarget(dt)
        root_panel.SetSizer(root_layout)

class ExplanationDrawingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1, -1))
        layout = wx.BoxSizer(wx.VERTICAL)
        self.button_pic = MyImage(self)
        self.text_expl = wx.TextCtrl(self, wx.ID_ANY)
        layout.Add(self.button_pic, flag=wx.SHAPED | wx.ALIGN_CENTER, proportion=1)
        layout.Add(self.text_expl, flag=wx.GROW, proportion=0)
        self.SetSizer(layout)


class MyImage(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        default_img = wx.EmptyImage(400, 300) # black
        default_img.Replace(0,0,0,255,255,255) # convert to white
        self.img = default_img
        self.best_scale = default_img.GetSize().Get()
        self.Bind(wx.EVT_SIZE, self.onResize)
        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onResize(self, event):
        (W_MAX, H_MAX) = self.GetSizeTuple()
        (W, H) = self.img.GetSize().Get()
        if W > H:
            NewW = W_MAX
            NewH = H_MAX * H / W
        else:
            NewW = W_MAX * W / H
            NewH = H_MAX
        self.best_scale = (NewW, NewH)

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        bitmap = wx.BitmapFromImage(self.img.Scale(self.best_scale[0], self.best_scale[1]))
        dc.DrawBitmap(bitmap, 0, 0, useMask=False)

app = wx.App()
frm = MyFrame()
frm.Show()
app.MainLoop()
