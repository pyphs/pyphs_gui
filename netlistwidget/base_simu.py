#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 14:40:59 2017

@author: Falaize
"""


from __future__ import absolute_import, division, print_function
#from builtins import *

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication, QLabel,
                             QMainWindow, qApp, QComboBox, QLineEdit,
                             QPushButton, QFileDialog, QHBoxLayout,
                             QProgressBar)
from PyQt5.QtCore import Qt
iconspath = '.' + os.sep + 'icons' + os.sep
from pyphs.misc.signals.synthesis import parameters, names, signalgenerator
from pyphs import netlist2core, Simulation
from pyphs.config import simulations as config


class GradientWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.QCombo = QComboBox(self)
        for par in ['discret', 'theta', 'trapez']:
            self.QCombo.addItem(par)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Gradient', self))
        self.hbox.addWidget(self.QCombo)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class LanguageWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.QCombo = QComboBox(self)
        for par in ['python', 'c++']:
            self.QCombo.addItem(par)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Language', self))
        self.hbox.addWidget(self.QCombo)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class SplitWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.QCombo = QComboBox(self)
        for par in ['True', 'False']:
            self.QCombo.addItem(par)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Split Explicit', self))
        self.hbox.addWidget(self.QCombo)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class FsWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Qpar = QLineEdit(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Sample Rate', self))
        self.hbox.addWidget(self.Qpar)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class ThetaWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Qpar = QLineEdit(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Theta', self))
        self.hbox.addWidget(self.Qpar)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class MaxitWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Qpar = QLineEdit(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Iteration max', self))
        self.hbox.addWidget(self.Qpar)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class X0Widget(QWidget):

    def __init__(self, core):
        QWidget.__init__(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('State init ' + str(tuple(core.x))[1:-1],
                                   self))
        self.hbox.addStretch(1)
        self.widgets = list()
        for i in range(len(core.x)):
            self.widgets.append(QLineEdit(self))
            self.hbox.addWidget(self.widgets[-1])
        self.setLayout(self.hbox)
        self.show()

    def update(self, x0):
        for i, val in enumerate(x0):
            self.widgets[i].setText(str(val))


class TWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Qpar = QLineEdit(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Duration', self))
        self.hbox.addWidget(self.Qpar)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class PathWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Qpar = QLineEdit(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Path', self))
        self.hbox.addWidget(self.Qpar)
        self.setLayout(self.hbox)
        self.show()


class SimuWidget(QWidget):

    def __init__(self, fname=None):
        QWidget.__init__(self)  # super().__init__()
        self._open(fname)
        self._T = 0.
        self.config = config.copy()
        self.config['progressbar'] = True
        self.initUI()
        self.update_T()

    def initUI(self):
        self.vbox = QVBoxLayout()
        path = self.filename[:self.filename.rfind(os.sep)] + os.sep + 'data'
        self.config['path'] = path
        self.path = PathWidget()
        self.path.Qpar.setText(self.config['path'])
        self.vbox.addWidget(self.path)
        self.path.Qpar.textChanged[str].connect(self.onActivated_path)

        self.language = LanguageWidget()
        self.vbox.addWidget(self.language)
        index = self.language.QCombo.findText(self.config['language'],
                                              Qt.MatchFixedString)
        self.language.QCombo.setCurrentIndex(index)
        self.language.QCombo.activated[str].connect(self.onActivated_language)

        self.fs = FsWidget()
        self.fs.Qpar.setText(str(self.config['fs']))
        self.vbox.addWidget(self.fs)
        self.fs.Qpar.textChanged[str].connect(self.onActivated_fs)

        self.twidget = TWidget()
        self.vbox.addWidget(self.twidget)
        self.twidget.Qpar.textChanged[str].connect(self.onActivated_twidget)

        self.gradient = GradientWidget()
        self.vbox.addWidget(self.gradient)
        index = self.gradient.QCombo.findText(self.config['gradient'],
                                              Qt.MatchFixedString)
        self.gradient.QCombo.setCurrentIndex(index)
        self.gradient.QCombo.activated[str].connect(self.onActivated_gradient)

        self.theta = ThetaWidget()
        self.theta.Qpar.setText(str(self.config['theta']))
        self.vbox.addWidget(self.theta)
        self.theta.Qpar.textChanged[str].connect(self.onActivated_theta)

        self.split = SplitWidget()
        self.vbox.addWidget(self.split)
        index = self.split.QCombo.findText(str(self.config['split']),
                                           Qt.MatchFixedString)
        self.split.QCombo.setCurrentIndex(index)
        self.split.QCombo.activated[str].connect(self.onActivated_split)

        self.maxit = MaxitWidget()
        self.maxit.Qpar.setText(str(self.config['maxit']))
        self.vbox.addWidget(self.maxit)
        self.maxit.Qpar.textChanged[str].connect(self.onActivated_maxit)

        self.x0 = [0., ]*len(self.core.x)
        self.x0widget = X0Widget(self.core)
        self.x0widget.update(self.x0)
        self.vbox.addWidget(self.x0widget)

        self.pbtn = QPushButton("Process")
        self.pbtn.clicked.connect(self.process)
        self.bbtn = QPushButton("Build")
        self.bbtn.clicked.connect(self.build_simulation)
        # self.pbar = QProgressBar(self)
        hbox = QHBoxLayout()
        # hbox.addWidget(self.pbar)
        hbox.addStretch(1)
        hbox.addWidget(self.bbtn)
        hbox.addWidget(self.pbtn)
        self.vbox.addLayout(hbox)

        def gen_onactivated_x0(i):
            def onactivated_x0(text):
                self.x0[i] = float(text)
            return onactivated_x0
        self.all_onactivated_x0 = list()
        for i in range(len(self.core.x)):
            self.all_onactivated_x0.append(gen_onactivated_x0(i))
            self.x0widget.widgets[i].textChanged[str].connect(self.all_onactivated_x0[i])

        self.signals = list()

        def gen_signalWidget(label):
            sw = SignalWidget(label, self.config['fs'])
            return sw
        for el in self.core.u + self.core.p:
            label = str(el)
            self.signals.append(gen_signalWidget(label))
            self.signals[-1].Qpar.textChanged[str].connect(self.onActivated_par)
            self.vbox.addWidget(self.signals[-1])

        self.vbox.addStretch(1)

        self.pparameters = {'type': 'power balance',
                            'custom': tuple()}
        self.ptw = PlotTypeWidget()
        self.pcw = PlotCustomWidget()
        self.ppbtn = QPushButton('Plot', self)
        self.vbox_plots = QVBoxLayout()
        self.vbox_plots.addWidget(self.ptw)
        self.vbox_plots.addWidget(self.pcw)
        hbox_plots = QHBoxLayout()
        hbox_plots.addStretch(1)
        hbox_plots.addWidget(self.pbtn)
        self.vbox_plots.addLayout(hbox_plots)
        self.vbox_plots.addStretch(1)
        self.ptw.QCombo.activated[str].connect(self.onActivated_ptype)
        self.pcw.line_edit.textChanged[str].connect(self.onActivated_pcustom)
        self.ppbtn.clicked.connect(self.onActivated_plotbtn)

        self.mainbox = QHBoxLayout()
        self.mainbox.addLayout(self.vbox)
        self.mainbox.addLayout(self.vbox_plots)
        self.setLayout(self.mainbox)
        #self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PHS Simulation')
        self.show()

    def onActivated_ptype(self, text):
        self.pparameters['type'] = text

    def onActivated_pcustom(self, text):
        self.pparameters['custom'] = text

    def onActivated_plotbtn(self):
        if self.pparameters['type'] == 'power balance':
            self.simulation.data.plot_powerbal(mode='single')
        elif self.pparameters['type'] == 'custom':
            def format_text(t):
                l = list()
                for tp in '{}'.format(t).split('), ('):
                    tp = str(tp).strip().replace('(', '').replace(')', '')
                    e1, e2 = map(str.strip, tp.split(','))
                    try:
                        l.append((str(e1), int(e2)))
                    except:
                        pass
                return tuple(l)
            print(format_text(self.pparameters['custom']))
            self.simulation.data.plot(format_text(self.pparameters['custom']))
        elif self.pparameters['type'] == 'inputs':
            temp = list()
            for i, u in enumerate(self.simulation.nums.method.core.u):
                temp.append(('u', i))
            self.simulation.data.plot(temp)
        elif self.pparameters['type'] == 'parameters':
            temp = list()
            for i, u in enumerate(self.simulation.nums.method.core.p):
                temp.append(('p', i))
            self.simulation.data.plot(temp)

    def _open(self, fname):
        if fname is None:
            fname = QFileDialog.getOpenFileName(self,
                                                'Open netlist file',
                                                os.getcwd())
        if not fname[0] == '':
            self.filename = '{}'.format(fname[0])
            self.core = netlist2core(self.filename)
            self._new = True
        else:
            self._new = False

    def onActivated_par(self, text):
        self.update_T()

    def onActivated_gradient(self, text):
        self.config['gradient'] = text

    def onActivated_twidget(self, text):
        self._T = float(text)
        self.twidget.Qpar.setText(str(self.T()))

    def onActivated_language(self, text):
        self.config['language'] = text

    def onActivated_fs(self, text):
        try:
            fs = max(0., float(text))
        except:
            fs = 0.

        self.config['fs'] = fs
        for s in self.signals:
            s.parameters['fs'] = self.config['fs']

    def onActivated_maxit(self, text):
        maxit = max(1., int(text))
        self.config['maxit'] = maxit
        self.maxit.setText[str(maxit)]

    def onActivated_theta(self, text):
        t = min(1., max(0., float(text)))
        self.config['theta'] = t
        self.theta.setText[str(t)]

    def onActivated_split(self, text):
        self.config['split'] = bool(text)

    def onActivated_path(self, text):
        self.config['path'] = r''.format(text)

    def signals_parameters(self, attr=None):
        if attr is None:
            return (el.parameters for el in self.signals)
        else:
            return (el.parameters[attr] for el in self.signals)

    def signals_T(self):
        return (el.T() for el in self.signals)

    def T(self):
        if len(self.signals) > 0:
            return max(list(self.signals_T()) + [self._T, ])
        else:
            return self._T

    def update_T(self):
        self.twidget.Qpar.setText(str(self.T()))

    def build_sequences(self):

        gens_u = list()
        gens_p = list()

        for i, (p, t) in enumerate(zip(self.signals_parameters(),
                                       self.signals_T())):

            p['tend'] = p['tend'] + self.T()-t
            pars = {}
            for k in p.keys():
                if not k == 'label':
                    pars[k] = p[k]
            gen = signalgenerator(**pars)
            if i < self.core.dims.y():
                gens_u.append(gen)
            else:
                gens_p.append(gen)

        def seq_u():
            if self.core.dims.y() > 0:
                for e in zip(*map(lambda el: el(), gens_u)):
                    yield e
            else:
                i = 0
                while i < self.T()*self.config['fs']:
                    yield tuple()
                    i += 1

        def seq_p():
            if self.core.dims.p() > 0:
                for e in zip(*map(lambda el: el(), gens_p)):
                    yield e
            else:
                i = 0
                while i < self.T()*self.config['fs']:
                    yield tuple()
                    i += 1

        self.seq_u = seq_u
        self.seq_p = seq_p

    def build_simulation(self):
        self.simulation = PHSSimulation(self.core, self.config)
        # self.set_pb_update()
        self.bbtn.setText('Re-Build')
        self.pbtn.setText('Process')

    def process(self):
        self.build_sequences()
        # self.simulation.init_pb()
        self.simulation.init(seqp=self.seq_p(), sequ=self.seq_u(),
                             x0=self.x0, nt=int(self.T()*self.config['fs']))
        self.simulation.process()
        self.pbtn.setText('Re-Process')

    def set_pb_update(self):

        def init_pb():
            self.pbar.setValue(0)

        def update_pb():
            self.pbar.setValue(int(100*(self.simulation.n+1) /
                               self.simulation.data.config['nt']))

        def close_pb():
            self.pbtn.setText('Finished')

        self.simulation.init_pb = init_pb
        self.simulation.update_pb = update_pb
        self.simulation.close_pb = close_pb

class SignalWidget(QWidget):

    def __init__(self, label, fs):
        QWidget.__init__(self)  # super().__init__()
        self._init = True

        self.parameters = parameters.copy()
        self.parameters['label'] = label
        self.parameters['fs'] = fs
        self.parameters['tsig'] = 0.

        self.initUI()

        init_par = 'tsig'
        index = self.Qparameter.findText(init_par, Qt.MatchFixedString)
        self.Qparameter.setCurrentIndex(index)
        self.onActivated_parameter(init_par)

    def T(self):
        ndeb = int(self.parameters['tdeb']*self.parameters['fs'])
        nend = int(self.parameters['tend']*self.parameters['fs'])
        nsig = int(self.parameters['tsig']*self.parameters['fs'])
        ncycles = int(self.parameters['ncycles'])
        return (ndeb + nend + ncycles*nsig) / self.parameters['fs']

    def initUI(self):

#        self.Tlbl = QLabel('{}'.format(self.T()), self)
        self.Qpar = QLineEdit(self)

        self.Qsignal = QComboBox(self)
        for sig in names:
            self.Qsignal.addItem(sig)

        self.Qparameter = QComboBox(self)
        for par in self.parameters.keys():
            if par not in ['label', 'fs', 'which']:
                self.Qparameter.addItem(par)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel(self.parameters['label'], self))
#        self.hbox.addWidget(self.Tlbl)
        self.hbox.addWidget(self.Qsignal)
        self.hbox.addWidget(self.Qparameter)
        self.hbox.addWidget(self.Qpar)
        self.hbox.addStretch(1)

        self.Qsignal.activated[str].connect(self.onActivated_signal)
        self.Qparameter.activated[str].connect(self.onActivated_parameter)
        self.Qpar.textChanged[str].connect(self.onActivated_par)

#        vbox = QVBoxLayout()
#        vbox.addWidget(self.lbl)
#        vbox.addLayout(self.hbox)
#
        self.setLayout(self.hbox)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def onActivated_signal(self, text):
        self.parameters['which'] = text
        self.update_Tlabel()

    def onActivated_parameter(self, text):
        self.par_text = text
        value = self.parameters[self.par_text]
        self.Qpar.setText('{}'.format(value))
        self.update_Tlabel()

    def onActivated_par(self, text):
        try:
            self.parameters[self.par_text] = float(text)
        except:
            self.parameters[self.par_text] = bool('{}'.format(text))
        self.update_Tlabel()

    def update_Tlabel(self):
        pass
#        self.Tlbl.setText('{}'.format(self.T()))
#        self.Tlbl.adjustSize()


class PlotTypeWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.QCombo = QComboBox(self)
        for par in ['inputs', 'parameters', 'power balance', 'custom']:
            self.QCombo.addItem(par)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Plot ', self))
        self.hbox.addWidget(self.QCombo)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


class PlotCustomWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('Selection', self))
        self.line_edit = QLineEdit('', self)
        self.hbox.addWidget(self.line_edit)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = 'test'
    fs = 120.
    e = SimuWidget()  # ShowWidget(SignalsWidget)
    sys.exit(app.exec_())
