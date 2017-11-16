#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 22:36:31 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QDialog, QLabel, QPushButton)

from PyQt5.QtGui import QFont
from .editsignal import SignalEdit

from pyphs import signalgenerator
import numpy


# --------------------------------------------------------------------------- #

class Signal(QWidget):

    def __init__(self, label, parent=None, **data):

        self.data = dict()
        self.data['which'] = 'zero'
        self.data['tsig'] = 1.
        self.data['ncycles'] = 1
        self.data['tdeb'] = 0.
        self.data['tend'] = 0.
        self.data['fs'] = int(1e3)
        self.data['A'] = 1.
        self.data['A1'] = 0.
        self.data['f0'] = 100.
        self.data['f1'] = None
        self.data['cycle_ratio'] = 1.
        self.data['attack_ratio'] = 0.
        self.data['decay_ratio'] = 0.
        self.data['ramp_on'] = False
        self.data['bkgrd_noise'] = 0.
        self.data['time'] = 1.

        super(Signal, self).__init__(parent)

        self.label = label
        self.data.update(data)

        self.initUI()

    def initUI(self):

        # define hbox
        hbox = QHBoxLayout()

        # Edit Widget
        button = QPushButton('edit')
        button.clicked.connect(self.on_click)
        hbox.addWidget(button)

        # Label widget
        font = QFont()
        font.setBold(True)
        label = QLabel(str(self.label)+':')
        label.setFont(font)
        hbox.addWidget(label)

        # Value widget
        self.valueWidget = QLabel('')
        hbox.addWidget(self.valueWidget)

        hbox.addStretch()

        self.update_value()

        # set layout and show
        self.setLayout(hbox)

    def update_value(self):
        value = 'type: {0}, duration: {1}'.format(self.data['which'],
                                                  self.data['time'])
        self.valueWidget.setText(value)

    def on_click(self):
        data, res = Signal.edit(self.label, parent=self, **self.data)
        if res:
            self.data = data
            self.update_value()

    @staticmethod
    def edit(label, parent=None, **data):
        dialog = SignalEdit(label, parent, **data)
        result = dialog.exec_()
        dialog.update_data()
        data = dialog.data
        return (data, result == QDialog.Accepted)

# --------------------------------------------------------------------------- #


class Signals(QWidget):

    def __init__(self, method, fs, parent=None):

        super(Signals, self).__init__(parent)

        self.method = method

        self.fs = fs

        self.initUI()

    def initUI(self):

        # define hbox
        vbox = QVBoxLayout()

        self.signals = {}
        for u in self.method.u:
            self.signals.update({u: Signal(str(u), parent=self, fs=self.fs)})
            vbox.addWidget(self.signals[u])

        # set layout and show
        self.setLayout(vbox)

    def build_generator(self, symbs, fs, time):
        sigs = []
        for u in symbs:
            signal = self.signals[u]
            delta = time - signal.data['time']
            if delta > 0:
                signal.data['tend'] += delta
            signal.data['fs'] = fs
            sigs.append(signalgenerator(**signal.data)())
            import matplotlib.pyplot as plt
            plt.figure()
            plt.plot(list(signalgenerator(**signal.data)()))

        def u():
            i = 0
            while i < time*fs:
                si = [next(sig) for sig in sigs]
                i += 1
                yield numpy.array(si)

        return u
