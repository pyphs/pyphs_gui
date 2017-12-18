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

from ..misc.signals import NoneSig

from pyphs import signalgenerator
import numpy


# --------------------------------------------------------------------------- #

class Signal(QWidget):

    def __init__(self, label, parent=None, const=None, **data):

        self.data = dict()
        self.data['tsig'] = 1.
        self.data['ncycles'] = 1
        self.data['tdeb'] = 0.
        self.data['tend'] = 0.
        self.data['fs'] = int(1e3)
        self.data['A1'] = 0.
        self.data['f0'] = 100.
        self.data['f1'] = None
        self.data['cycle_ratio'] = 1.
        self.data['attack_ratio'] = 0.
        self.data['decay_ratio'] = 0.
        self.data['ramp_on'] = False
        self.data['bkgrd_noise'] = 0.
        self.data['time'] = 1.

        if const is None:
            self.data['which'] = 'sin'
            self.data['A'] = 1.
        else:
            self.data['which'] = 'const'
            self.data['A'] = const

        super(Signal, self).__init__(parent)

        self.label = label
        self.data.update(data)

        self.initUI()

    def initUI(self):

        self.changeSig = NoneSig()

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
        value = 'type: {0}, amplitude: {1}, duration: {2}'.format(self.data['which'],
                                                                  self.data['A'],
                                                                  self.data['time'])
        self.valueWidget.setText(value)

    def on_click(self):
        data, res = Signal.edit(self.label, parent=self, **self.data)
        if res:
            self.data = data
            self.update_value()
            self.changeSig.sig.emit()

    @staticmethod
    def edit(label, parent=None, **data):
        dialog = SignalEdit(label, parent, **data)
        result = dialog.exec_()
        dialog.update_data()
        data = dialog.data
        return (data, result == QDialog.Accepted)

# --------------------------------------------------------------------------- #


class Signals(QWidget):

    def __init__(self, method, fs, uconst, pconst, parent=None):

        super(Signals, self).__init__(parent)

        self.signals = {}

        self.initUI(method, fs, uconst, pconst)

    def initUI(self, method, fs, uconst, pconst):

        self.changeSig = NoneSig()

        self.method = method
        self.fs = fs

        # define hbox
        vbox = QVBoxLayout()

        for u, const in zip(method.u, uconst):
            self.signals[u] = Signal(str(u), const=const, fs=self.fs)
            vbox.addWidget(self.signals[u])
            self.signals[u].changeSig.sig.connect(self.changeSig.sig.emit)

        for p, const in zip(method.p, pconst):
            self.signals[p] = Signal(str(p), const=const, fs=self.fs)
            vbox.addWidget(self.signals[p])
            self.signals[p].changeSig.sig.connect(self.changeSig.sig.emit)

        # set layout and show
        self.setLayout(vbox)

    def build_generator(self, usymbs, psymbs, fs, time):
        usigs = []
        for u in usymbs:
            usignal = self.signals[u]
            delta = time - usignal.data['time']
            if delta > 0:
                usignal.data['tend'] += delta
            usignal.data['fs'] = fs
            usigs.append(signalgenerator(**usignal.data)())

        def u():
            i = 0
            while i < time*fs:
                si = [next(usig) for usig in usigs]
                i += 1
                yield numpy.array(si)

        psigs = []
        for p in psymbs:
            psignal = self.signals[p]
            delta = time - psignal.data['time']
            if delta > 0:
                psignal.data['tend'] += delta
            psignal.data['fs'] = fs
            psigs.append(signalgenerator(**psignal.data)())

        def p():
            i = 0
            while i < time*fs:
                si = [next(sig) for sig in psigs]
                i += 1
                yield numpy.array(si)

        return u, p
