#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""


from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QVBoxLayout, QDialog,
                             QHBoxLayout, QPushButton, QLineEdit,
                             QGridLayout)

from ..misc.signals import BoolSig, NoneSig

from ..misc import TitleWidget, ParametersWidget

from .signals import Signals
from .plots import PlotEdit

from PyQt5.QtGui import QIcon
from .. import iconspath


class SimulationWidget(QWidget):

    def get_net(self):
        return self.numericWidget.net
    net = property(get_net)

    def get_inits(self):
        return self.numericWidget.inits.inits
    inits = property(get_inits)

    def get_io(self):
        return self.numericWidget.io.io
    io = property(get_io)

    def get_gains(self):
        return self.numericWidget.gains.gains
    gains = property(get_gains)

    def get_folder(self):
        return self.numericWidget.folder
    folder = property(get_folder)

    def get_label(self):
        return self.titleWidget.label
    label = property(get_label)

    def get_core(self):
        return self.numericWidget.core
    core = property(get_core)

    def get_method(self):
        return self.numericWidget.method
    method = property(get_method)

    def get_status(self):
        return self.statusWidget.status
    status = property(get_status)

    def get_done(self):
        return self.doneWidget.status
    done = property(get_done)

    def get_fs(self):
        return self.numericWidget.parameters['fs']
    fs = property(get_fs)

    def get_config(self):
        config = {}
        config['path'] = self.folder
        config.update(self.parameters)
        config.update(self.numericWidget.parameters)
        return config
    config = property(get_config)

    def __init__(self, numericWidget, parent=None):

        super(SimulationWidget, self).__init__(parent)

        self.parameters = {'lang': 'python',
                           'T': 1.,
                           }

        self.numericWidget = numericWidget

        self.initUI()

    def initUI(self):

        self.statusSig = BoolSig()
        self.initSig = NoneSig()

        # ---------------------------------------------------------------------
        # Define simulation Actions

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 0)

        # Build Action
        build_icon = QIcon(os.path.join(iconspath, 'work.png'))
        self.buildAction = QAction(build_icon,
                                   '&Build numerical evaluation', self)
        self.buildAction.setShortcut('Ctrl+B')
        self.buildAction.setStatusTip('Build numerical evaluation')
        self.buildAction.triggered.connect(self._build)
        self.buildButton = QPushButton(build_icon, '')
        self.buildButton.setToolTip('Build numerical evaluation')
        self.buildButton.clicked.connect(self._build)
        buttonsLayout.addWidget(self.buildButton)

        # process Action
        process_icon = QIcon(os.path.join(iconspath, 'process.png'))
        self.processAction = QAction(process_icon,
                                     '&Run the simulation', self)
        self.processAction.setShortcut('Ctrl+L')
        self.processAction.setStatusTip('Run the simulation')
        self.processAction.triggered.connect(self._build)
        self.processButton = QPushButton(process_icon, '')
        self.processButton.setToolTip('Run the simulation')
        self.processButton.clicked.connect(self._process)
        buttonsLayout.addWidget(self.processButton)

        # plot Action
        plot_icon = QIcon(os.path.join(iconspath, 'plot.png'))
        self.plotAction = QAction(plot_icon,
                                  '&Plot simulation results', self)
        self.plotAction.setShortcut('Ctrl+L')
        self.plotAction.setStatusTip('Plot simulation results')
        self.plotAction.triggered.connect(self._build)
        self.plotButton = QPushButton(plot_icon, '')
        self.plotButton.setToolTip('Plot simulation results')
        self.plotButton.clicked.connect(self._plot)
        buttonsLayout.addWidget(self.plotButton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'SIMULATION'

        self.labelWidget = QLineEdit(self.method.label)

        self.titleWidget = TitleWidget(title=title,
                                       labelWidget=self.labelWidget,
                                       status_labels=None,
                                       buttonsLayout=buttonsLayout)

        # ---------------------------------------------------------------------
        # status widget

        statusLayout = QHBoxLayout()
        statusLayout.setContentsMargins(0, 0, 0, 0)

        status_labels = {True: 'OK',
                         False: 'Not OK'}
        self.statusWidget = TitleWidget(title='Status',
                                        labelWidget=None,
                                        status_labels=status_labels,
                                        buttonsLayout=None)

        status_labels = {True: 'Done',
                         False: 'Not run'}
        self.doneWidget = TitleWidget(title='Process',
                                      labelWidget=None,
                                      status_labels=status_labels,
                                      buttonsLayout=None)

        statusLayout.addWidget(self.statusWidget)
        statusLayout.addWidget(self.doneWidget)
        statusLayout.addStretch()

        self.signalsWidget = QWidget()
        setattr(self.signalsWidget, 'gridLayout', QGridLayout())
        self.signalsWidget.setLayout(self.signalsWidget.gridLayout)
        self._init_signals()

        # ---------------------------------------------------------------------
        # set parameters
        content = {}

        content['lang'] = {'desc': 'Computing Language',
                           'label': 'Language',
                           'value': self.parameters['lang'],
                           'type': 'sel',
                           'choices': ['python', 'c++']
                           }
        content['T'] = {'desc': 'Simulation duration (in seconds)',
                        'label': 'Duration',
                        'value': self.parameters['T'],
                        'type': 'float',
                        }

        tooltip = 'Simulation parameters'

        self.parametersWidget = ParametersWidget('', content, tooltip)

        # ---------------------------------------------------------------------
        # set Layout
#        self.grid = QGridLayout(self)
#        self.grid.setContentsMargins(0, 0, 0, 0)
#        self.grid.addWidget(self.titleWidget, 0, 0)
#        self.grid.addLayout(statusLayout, 1, 0)
#        self.grid.addWidget(self.parametersWidget, 2, 0)
#        self.setLayout(self.grid)
#        self.setContentsMargins(0, 0, 0, 0)
#
        # ---------------------------------------------------------------------
        # signals
        self.numericWidget.statusSig.sig.connect(self._status_changed)
        self.parametersWidget.modifiedSig.sig.connect(self._update_parameters)
        self.titleWidget.labelSignal.sig.connect(self._update_label)
        self.numericWidget.initSig.sig.connect(self._netlist_init)
        self.numericWidget.methodWidget.statusSig.sig.connect(self._status_changed)
        self.numericWidget.methodWidget.statusSig.sig.connect(self._init_signals)
        self.numericWidget.inits.modifSig.sig.connect(self._init_signals)
        self.numericWidget.io.modifSig.sig.connect(self._init_signals)

    def _init_signals(self, a=None):

        item = self.signalsWidget.gridLayout.itemAtPosition(0, 0)
        if item is not None:
            w = item.widget()
            self.signalsWidget.gridLayout.removeWidget(w)
            w.deleteLater()
            w = None

        uconst = list()
        for c, b in zip(self.inits['u'], self.io['u']):
            if b:
                uconst.append(c)
            else:
                uconst.append(None)

        pconst = list()
        for c in self.inits['p']:
            pconst.append(c)

        w = Signals(self.method, self.fs, uconst, pconst)
        w.changeSig.sig.connect(self._status_changed)
        self.signalsWidget.gridLayout.addWidget(w, 0, 0)

    def _netlist_init(self):
        label = self.numericWidget.label
        self._update_label(label)
        self.initSig.sig.emit()
        self._status_changed(False)

    def _update_parameters(self):
        if not self.parameters == self.parametersWidget.parameters:
            self.parameters.update(self.parametersWidget.parameters)
            self._status_changed(False)

    def _status_changed(self, s=False):
        if not s:
            self._change_status(s)
            self._change_done(s)

    def _change_status(self, s=False):
            self.statusWidget._change_status(s)

    def _change_done(self, s=False):
            self.doneWidget._change_status(s)

    def _update_label(self, label):
        if not self.label == label:
            self.titleWidget._change_label(label)

    def _change_label(self, label):
        self.titleWidget._change_label(label)
        self._update_label(label)

    def _build(self):

        if not self.numericWidget.status:
            self.numericWidget.methodWidget._build()

        config = self.config
        print(config)
        T = config.pop('T')
        self.simu = self.method.to_simulation(config=config,
                                              inits=self.inits)
        item = self.signalsWidget.gridLayout.itemAtPosition(0, 0)

        w = item.widget()
        u, p = w.build_generator(self.method.u, self.method.p,
                                 config['fs'], T)
        self.simu.init(u=u(), p=p(), nt=int(config['fs']*T))
        self.simu.label = self.label
        self._change_status(True)

    def _process(self):
        if not self.status:
            self._build()
        self.simu.process()
        self._change_done(True)

    def _plot(self):
        if self.done:
            attrs, res = self.plotEdit(self.simu, self)
            if res:
                self.simu.data.plot(attrs)

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

###############################################################################
