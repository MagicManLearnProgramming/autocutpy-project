#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/4 14:45
# @Author  : Magicman
# @Site    : 
# @File    : gui.py
# @Software: PyCharm Community Edition

import Tkinter
import Tkconstants
import tkFileDialog
import ttk
import os
from threading import Thread
import time
from autocutpy import multiple_trim


class CutFrame(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        # define options for opening
        self.file_name = []
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.jpg')]
        options['initialfile'] = 'myimage.jpg'
        options['parent'] = root
        options['title'] = 'Select file(s) to cut and trim'
        options['multiple'] = 1

        # defining options for saving a directory
        self.dir = ''
        self.dir_opt = options = {}
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Select a folder to save the results'

        # options for labels & buttons
        label_opt = {'fill': Tkconstants.BOTH, 'padx': 1, 'pady': 1}
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        radio_opt = {"side": "left", 'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # define labels & buttons
        Tkinter.Button(self, text='Select your file(s)', command=self.askfile).pack(**button_opt)
        Tkinter.Button(self, text='Select a folder to save the results', command=self.askdirectory).pack(**button_opt)
        Tkinter.Label(self,
                      text="Choose the graininess. The bigger graininess,\n"
                           " the larger size and the less number of photos.") \
            .pack(**label_opt)

        # defining grn for autocutpy
        self.grn = Tkinter.IntVar()
        self.grn.set(5)
        self.bfm = Tkinter.Frame(self)
        for i in xrange(6):
            Tkinter.Radiobutton(self.bfm, variable=self.grn, text=str(i), value=i).pack(**radio_opt)
            # rd.grid(column=i, row=5, sticky=Tkinter.W)
            # rd.pack(side="left")
        self.bfm.pack()
        Tkinter.Button(self, text='Submit', command=self.submit).pack(side="bottom", **button_opt)

        # define a progress bar
        self.progress_var = Tkinter.DoubleVar()
        progressbar = ttk.Progressbar(root, variable=self.progress_var)
        progressbar.pack(side="bottom", fill='x', expand=1)
        self.progress_var.set(0)
        self.pro_v = 0

        # Tkinter.Button(self, text='test', command=self.test).pack(side="bottom", **button_opt)

    def test(self):
        pass

    def askopenfile(self):
        """Returns an opened file in read mode."""

        return tkFileDialog.askopenfile(mode='r', **self.file_opt)

    def askfile(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        self.file_name = tkFileDialog.askopenfilename(**self.file_opt)
        if self.file_name:
            cur_dir = os.path.split(self.file_name[0])[0]
            self.file_opt['initialdir'] = self.dir_opt['initialdir'] = cur_dir

    def askdirectory(self):
        """Returns a selected directoryname."""
        self.dir = self.dir_opt['initialdir'] = tkFileDialog.askdirectory(**self.dir_opt)
        return self.dir

    def submit(self):
        """
        :return: Cut and trim the photos
        """
        if self.file_name:
            trimer = Thread(target=multiple_trim, args=(self.file_name, self.grn.get(), self.dir))
            # multiple_trim(self.file_name, self.grn.get(), self.dir)
            self.progress_var.set(0)
            pger = Thread(target=self.progress_update)
            trimer.start()
            pger.start()

    def progress_update(self):
        present = 0
        total = len(self.file_name)

        while present < 100:
            finished = ''.join(os.listdir(self.dir))
            i = 0
            for fn in self.file_name:
                if os.path.basename(fn)[: -4] in finished:
                    i += 1
            present = 100.0 * i / total
            self.progress_var.set(present)
            time.sleep(0.1)


def main():
    root = Tkinter.Tk()
    CutFrame(root).pack()
    root.mainloop()


if __name__ == "__main__":
    main()
