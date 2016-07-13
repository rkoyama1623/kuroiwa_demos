#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import math
import os
import multiprocessing
import cPickle as pickle
import numpy as np
import skimage.io

def getClassIndex(model, fname):
    img = skimage.img_as_float(skimage.io.imread(fname, as_grey=False)).astype(np.float32)
    h, loss = model([img], np.array([0], dtype=np.int32))
    ans = h.data.flatten().tolist()
    return ans.index(max(ans))

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        fname = filenames[0]
        self.window.button_pic.img_path = fname
        self.window.button_pic.img = wx.Image(fname)
        self.window.button_pic.Refresh()
        self.window.text_expl.SetValue(fname)
        global my_model
        if my_model:
            cls = getClassIndex(my_model, fname)
            global dir_list
            self.window.text_expl.SetValue(dir_list[cls])


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target", size=(-1, -1))

        self.jobs = []
        self.queue = multiprocessing.Queue()

        # The aspect ratio of root panel shoud be the one of A4
        root_panel = wx.Panel(self, wx.ID_ANY, size=(1000*math.sqrt(2), 1000))
        root_panel.SetBackgroundColour('red')
        sz = wx.BoxSizer(wx.VERTICAL)
        sz.Add(root_panel, flag=wx.SHAPED | wx.ALIGN_CENTER, proportion=1)
        self.SetSizer(sz)

        self.panels = [ExplanationDrawingPanel(root_panel) for i in range(6)]
        root_layout = wx.GridSizer(2, 3)
        for p in self.panels:
            root_layout.Add(p, flag=wx.SHAPED | wx.ALL, border=10)
            dt = MyFileDropTarget(p)
            p.SetDropTarget(dt)
        root_panel.SetSizer(root_layout)

        # about MultiProcess
        self.Bind(wx.EVT_SHOW, self.onShow)
        self.Bind(wx.EVT_IDLE, self.onIdle)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        # about Menu
        menu_file = wx.Menu()
        menu_file.Append(1, "Print")
        menu_file.Append(2, "Save")
        menu_setting = wx.Menu()
        menu_setting.Append(3, "Reset")
        candidate = wx.Menu()
        candidate.Append(4, "2 x 3")
        candidate.Append(5, "3 x 3")
        menu_setting.AppendSubMenu(candidate, "Layout")
        menu_help = wx.Menu()
        menu_help.Append(6, "Usage")
        menu_help.Append(7, "About")
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_file, "File")
        menu_bar.Append(menu_setting, "Setting")
        menu_bar.Append(menu_help, "Help")
        self.Bind(wx.EVT_MENU, self.onMenu)
        self.SetMenuBar(menu_bar)

    def setCNNmodel(self, path):
        model = pickle.load(open(path, "rb"))
        self.queue.put(model)
        print "Complete model loading"

    def onShow(self, event):
        dir_name = os.path.abspath(os.path.dirname(__file__))
        NEW_MODEL_PATH = os.path.join(dir_name, 'config/new_model.pkl')
        print "Loading {}".format(NEW_MODEL_PATH.split("/")[-1])
        job = multiprocessing.Process(target=self.setCNNmodel, args=(NEW_MODEL_PATH, ))
        self.jobs.append(job)
        job.start()

    def onIdle(self, event):
        if not self.queue.empty():
            global my_model
            my_model = self.queue.get()
            for p in self.panels:
                path = p.text_expl.GetValue()
                if os.path.isfile(path):
                    cls = getClassIndex(my_model, path)
                    global dir_list
                    p.text_expl.SetValue(dir_list[cls])

    def onClose(self, event):
        [job.terminate() for job in self.jobs]
        self.Destroy()

    def onMenu(self, event):
        id = event.GetId()
        if id == 3:             # Reset
            for p in self.panels:
                cur_img = p.button_pic.img
                (w, h) = cur_img.GetSize().Get()
                new_img = wx.EmptyImage(w, h)
                new_img.Replace(0,0,0,255,255,255) # convert to white
                p.button_pic.img = new_img
                p.button_pic.Refresh()
                p.button_pic.img_path = None
                p.text_expl.SetValue("")
        elif id == 2:           # Save
            import matplotlib.pyplot
            import PIL.Image
            f, (axes) = matplotlib.pyplot.subplots(2, 3)
            f.set_size_inches(11.69, 8.27)
            ax_list = axes.flatten()
            for i, p in enumerate(self.panels):
                img_path = p.button_pic.img_path
                if img_path:
                    ax_list[i].imshow(PIL.Image.open(img_path))
                ax_list[i].set_title(p.text_expl.GetValue())
                ax_list[i].tick_params(labelbottom='off', labelleft='off')
                ax_list[i].get_xaxis().set_ticks_position('none')
                ax_list[i].get_yaxis().set_ticks_position('none')
            f.savefig("/tmp/aaaaa.pdf")
            import subprocess
            subprocess.Popen(["/tmp/aaaaa.pdf"], shell=True)

            # dlg = wx.FileDialog(self, "Save to file", "", "", ".jpg",
            #                     wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            # if dlg.ShowModal() == wx.ID_OK:
            #     print dlg.GetFilename()
            #     print dlg.GetDirectory()
            # dlg.Destroy()

            # context = wx.ClientDC(self)
            # memory = wx.MemoryDC()
            # x, y = self.ClientSize
            # bitmap = wx.EmptyBitmap( x, y, -1 )
            # memory.SelectObject(bitmap)
            # memory.Blit( 0, 0, x, y, context, 0, 0)
            # memory.SelectObject( wx.NullBitmap)
            # bitmap.SaveFile( '/tmp/test.jpg', wx.BITMAP_TYPE_JPEG )


    def createHtml(self):
        html = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
        <meta charset="UFT-8">
        </head>
        <body>
        <table width="50%" height="60%"><tbody>
        <tr>
        <td>
        <figure id="1">
        <img src="/home/eisoku/Desktop/b.jpg" width="300">
        <figcaption>test</figcaption>
        </figure>
        </td>
        <td>
        <figure id="1">
        <img src="/home/eisoku/Desktop/b.jpg" width="300">
        <figcaption>test</figcaption>
        </figure>
        </td>
        <td>
        <figure id="1">
        <img src="/home/eisoku/Desktop/b.jpg" width="300">
        <figcaption>test</figcaption>
        </figure>
        </td>
        </tr>
        <tr>
        <td>
        <figure id="1">
        <img src="/home/eisoku/Desktop/b.jpg" width="300">
        <figcaption>test</figcaption>
        </figure>
        </td>
          <td>
        <figure id="1">
        <img src="/home/eisoku/Desktop/b.jpg" width="300">
        <figcaption>test</figcaption>
        </figure>
        </td>
        <td>
        <figure id="1">
        <img src="/home/eisoku/Desktop/b.jpg" width="300">
              <figcaption>test</figcaption>
        </figure>
        </td>
        </tr>
        </tbody>
        </table>
        </body>
        </html>
        """
        f = file('screenshot.htm', 'w')
        f.write(html)
        f.close()

class ExplanationDrawingPanel(wx.Panel):
    """
    This class contains Image and Explanation
    """
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
        self.img_path = None
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

if __name__=="__main__":
    my_model = None
    dir_name = os.path.abspath(os.path.dirname(__file__))
    dir_list = os.listdir(os.path.join(dir_name, 'data'))
    dir_list = [os.path.join(dir_name, 'data/'+d) for d in dir_list]
    dir_list = filter(lambda d: os.path.isdir(d), dir_list)
    dir_list = [d.split('/')[-1] for d in dir_list]
    app = wx.App()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()
