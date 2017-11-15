#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 22:36:31 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

import sys

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QLabel, QGridLayout,
                             QDialogButtonBox, QLineEdit,
                             QPushButton, QCheckBox, QMessageBox)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ..misc.element import ElementWidget
from ..misc.signals import NoneSig
from .editsignal import SignalEdit

from pyphs.misc.tools import geteval
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


# --------------------------------------------------------------------------- #


class PlotEdit(QDialog):

    def __init__(self, simu, parent=None):

        super(PlotEdit, self).__init__(parent)

        self.simu = simu

        self.initUI()

    def initUI(self):

        # define vbox
        vbox = QVBoxLayout()

        self.checkboxes = {}
        self.hboxes = []
        self.labels = {}

        for name in ['x', 'dx', 'dxH', 'w', 'z', 'u', 'y', 'p', 'o']:
            if name == 'dxH':
                labels = tuple(map(lambda x: 'dHd' + str(x), self.simu.method.x))
            elif name == 'z':
                labels = tuple(map(lambda w: 'z' + str(w)[1:], self.simu.method.w))
            else:
                labels = tuple(map(str, geteval(self.simu.method, name)))
            self.labels[name] = labels
            self.checkboxes[name] = tuple(map(lambda l: QCheckBox(l, self), labels))
            hbox = QHBoxLayout()
            for qcb in self.checkboxes[name]:
                hbox.addWidget(qcb)
            hbox.addStretch()
            vbox.addLayout(hbox)


        # OK and Cancel buttons
        hbox_but = QHBoxLayout()
        hbox_but.addStretch()
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        hbox_but.addWidget(buttons)
        hbox_but.addStretch()
        vbox.addLayout(hbox_but)

        # set layout and show
        self.setLayout(vbox)
        self.setWindowTitle('Select Signals to Plot')

# --------------------------------------------------------------------------- #


class SimulationWidget(QWidget):

    _status = False
    _label = None

    config = {'eps': 1e-9,
              'epsdg': 1e-12,
              'fs': 48000.0,
              'maxit': 10}

    def get_method(self):
        return self.methodWidget.method
    method = property(get_method)

    def get_folder(self):
        return self.methodWidget.folder
    folder = property(get_folder)

    def __init__(self, numericWidget, parent=None):

        super(SimulationWidget, self).__init__(parent)

        self.numericWidget = numericWidget

        self.initUI()


    def __init__(self, method, path, parent=None):

        self.modifSig = Communicate()
        self.buildSig = Communicate()

        super(SimulationWidget, self).__init__(parent)

        self.method = None

        self._label = None

        self.config = {'lang': 'python',
                       'load': {'decim': 1, 'imax': None, 'imin': 0},
                       'path': path,
                       'pbar': True,
                       'T': 0.1}

        self.initUI()

    def initUI(self):

        # --------------------

        font = QFont()
        font.setBold(True)

        core_title = QLabel('Simulation')
        core_title.setFont(font)

        self.label = QLineEdit(self._label)
        self.label.textChanged[str].connect(self.update_label)

        self.status = QLabel()
        self.status.setFont(font)
        self.done = QLabel()
        self.done.setFont(font)

        self.set_status(False)

        title = QHBoxLayout()

        title.addWidget(core_title)
        title.addWidget(self.label)
        title.addStretch()
        title.addWidget(self.status)
        title.addWidget(self.done)

        # --------------------

        self.positions = {'fs': (0, 0), 'T': (0, 1),
                          'maxit': (1, 0), 'eps': (1, 1),
                          'lang': (2, 0),
                          }

        self.content = {'lang': {'desc': 'Computing Language',
                                 'label': 'Language',
                                 'value': self.config['lang'],
                                 'type': 'sel',
                                 'choices': ['python', 'c++']
                                 },
                        'fs': {'desc': 'Sample Rate (Hz)',
                               'label': 'Sample Rate',
                               'value': self.config['fs'],
                               'type': 'float',
                               },

                        'T': {'desc': 'Simulation duration (in seconds)',
                              'label': 'Duration',
                              'value': self.config['T'],
                              'type': 'float',
                              },
                        'maxit': {'desc': 'Maximum number of implicit iterations.',
                                  'label': 'Iterations',
                                  'value': self.config['maxit'],
                                  'type': 'int',
                                  },
                        'eps': {'desc': 'Numerical tolerance on implicit iterations.',
                                  'label': 'Tolerance',
                                  'value': self.config['eps'],
                                  'type': 'float',
                                  },
                        }

        self.grid = QGridLayout()

        for k in self.content.keys():
            self.grid.addWidget(Element(**self.content[k]), *self.positions[k])
            item = self.grid.itemAtPosition(*self.positions[k])
            widget = item.widget()
            widget.modifSig.signal.connect(self.set_status)


        # --------------------

        hbox1 = QHBoxLayout()
        buildbutton = QPushButton('Build SIMULATION')
        buildbutton.clicked.connect(self._build)
        hbox1.addWidget(buildbutton)

        buttonprocess = QPushButton('Process')
        buttonprocess.clicked.connect(self.process)
        hbox1.addWidget(buttonprocess)

        self.grid.addLayout(hbox1, 2, 1)

        # --------------------
        hbox2 = QHBoxLayout()
        buttonplot = QPushButton('Plot')
        buttonplot.clicked.connect(self.plot)
        hbox2.addWidget(buttonplot)

        # --------------------

        self.signalgrid = QGridLayout()

        # --------------------

        vbox = QVBoxLayout()
        vbox.addLayout(title)
        vbox.addLayout(self.grid)
        vbox.addLayout(hbox2)
        vbox.addLayout(self.signalgrid)
        vbox.addStretch()

        self.setLayout(vbox)

        # --------------------
        self.setWindowTitle('Simulation')

    def init_signals(self):

        self.signals = Signals(self.method, self.config['fs'], parent=self)

        item = self.signalgrid.itemAtPosition(0, 0)
        if item is not None:
            widget = item.widget()
            self.signalgrid.removeWidget(widget)
            widget.destroy()
        self.signalgrid.addWidget(self.signals, 0, 0)

    def update_config(self):
        for k in self.content.keys():
            item = self.grid.itemAtPosition(*self.positions[k])
            widget = item.widget()
            self.config[k] = widget.data['value']

    def update_label(self, label):
        self._label = label

    def process(self):
        if not self.status.text() == 'Build OK':
            self._build()
        self.simu.process()
        self.set_done(True)

    def plot(self):
        attrs, res = SimulationWidget.plotEdit(self.simu, self)
        if res:
            self.simu.data.plot(attrs)

    def set_status(self, status=False):

        if status:
            text = 'Build OK'
            color = 'green'

        else:
            text = 'Build Needed'
            color = 'red'
            self.set_done()

        self.status.setStyleSheet("QLabel { color: %s}" % color)
        self.status.setText(text)

    def set_done(self, status=False):

        if status:
            text = 'Process OK'
            color = 'green'
        else:
            text = 'Process Needed'
            color = 'red'

        self.done.setStyleSheet("QLabel { color: %s}" % color)
        self.done.setText(text)

    def update_method(self, method):
        self.method = method
        self.update_label(self.method.label)
        self.set_status(False)
        self.set_done(False)

    def _build(self):
        self.buildSig.signal.emit()

#        try:
#            self.update_config()
#            fs = self.config['fs']
#            T = self.config.pop('T')
#            nt = int(T*fs)
#            self.simu = self.method.to_simulation(config=self.config)
#            u = self.signals.build_generator(self.simu.method.u, fs, T)
#            self.simu.init(u=u(), nt=nt)
#            self.set_status(True)
#        except:
#
#            QMessageBox.question(self, 'Build issue',
#                                 'Can not build simulation of {}'.format(self._label),
#                                 QMessageBox.Ok, QMessageBox.Ok)
#
        self.update_config()
        fs = self.config['fs']
        T = self.config.pop('T')
        nt = int(T*fs)
        self.simu = self.method.to_simulation(config=self.config)
        u = self.signals.build_generator(self.simu.method.u, fs, T)
        self.simu.init(u=u(), nt=nt)
        self.set_status(True)

    @staticmethod
    def plotEdit(simu, parent=None):
        dialog = PlotEdit(simu, parent)
        result = dialog.exec_()
        data = []
        for k in dialog.labels.keys():
            for i, cb in enumerate(dialog.checkboxes[k]):
                if bool(cb.checkState()):
                    data.append((k, i))
        return (data, result == QDialog.Accepted)

# --------------------------------------------------------------------------- #
