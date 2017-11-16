#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""


from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QVBoxLayout, QDialog,
                             QHBoxLayout, QPushButton, QLineEdit)

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

    def __init__(self, numericWidget, parent=None):

        super(SimulationWidget, self).__init__(parent)

        self.parameters = {'lang': 'c++',
                           'T': 0.1
                           }

        self.numericWidget = numericWidget

        self.initUI()

    def initUI(self):

        self.simulation = self.method.to_simulation()

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
        buildbutton = QPushButton(build_icon, '')
        buildbutton.setToolTip('Build numerical evaluation')
        buildbutton.clicked.connect(self._build)
        buttonsLayout.addWidget(buildbutton)

        # process Action
        process_icon = QIcon(os.path.join(iconspath, 'latex.png'))
        self.processAction = QAction(process_icon,
                                     '&Run the simulation', self)
        self.processAction.setShortcut('Ctrl+L')
        self.processAction.setStatusTip('Run the simulation')
        self.processAction.triggered.connect(self._build)
        processbutton = QPushButton(process_icon, '')
        processbutton.setToolTip('Run the simulation')
        processbutton.clicked.connect(self._process)
        buttonsLayout.addWidget(processbutton)

        # plot Action
        plot_icon = QIcon(os.path.join(iconspath, 'plot.png'))
        self.plotAction = QAction(plot_icon,
                                  '&Plot simulation results', self)
        self.plotAction.setShortcut('Ctrl+L')
        self.plotAction.setStatusTip('Plot simulation results')
        self.plotAction.triggered.connect(self._build)
        plotbutton = QPushButton(plot_icon, '')
        plotbutton.setToolTip('Plot simulation results')
        plotbutton.clicked.connect(self._plot)
        buttonsLayout.addWidget(plotbutton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'SIMULATION'

        self.labelWidget = QLineEdit(self.core.label)

        self.titleWidget = TitleWidget(title=title,
                                       labelWidget=self.labelWidget,
                                       status_labels=None,
                                       buttonsLayout=buttonsLayout)
        self.statusWidget = self.titleWidget.statusWidget
        self.titlWidget.removeWidget(self.titleWidget.statusWidget)

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
                        },

        tooltip = 'Simulation parameters'

        self.parametersWidget = ParametersWidget('', content, tooltip)

        # ---------------------------------------------------------------------
        # set Layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.titleWidget)
        vbox.addLayout(statusLayout)
        vbox.addWidget(self.parametersWidget)
        self.setLayout(vbox)
        self.setContentsMargins(0, 0, 0, 0)

        # ---------------------------------------------------------------------
        # signals
        self.coreWidget.statusSig.sig.connect(self._status_changed)
        self.parametersWidget.modifiedSig.sig.connect(self._update_parameters)
        self.titleWidget.labelSignal.sig.connect(self._update_label)
        self.numericWidget.initSig.sig.connect(self._netlist_init)

    def _netlist_init(self):
        label = self.numericWidget.label
        self._update_label(label)
        self.initSig.sig.emit()

    def _update_parameters(self):
        if not self.parameters == self.parametersWidget.parameters:
            self.parameters.update(self.parametersWidget.parameters)
            self._change_status(False)

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

        if self.numericWidget.status:

            config = {}
            config.update(self.parameters)
            config.update(self.numericWidget.parameters)
            self.simu = self.method.to_simulation(config=config,
                                                  inits=self.inits)
            u = self.signals.build_generator(self.simu.method.u,
                                             config['fs'], config['T'])
            self.simu.init(u=u(), nt=int(config['fs']*config['T']))
            self.set_status(True)

            self.method = self.core.to_method(self.parameters)
            self.simulation.label = self.label
            self._update()
            self._change_status(True)

    def init_signals(self):

        self.signals = Signals(self.method, self.config['fs'], parent=self)

        item = self.signalgrid.itemAtPosition(0, 0)
        if item is not None:
            widget = item.widget()
            self.signalgrid.removeWidget(widget)
            widget.destroy()
        self.signalgrid.addWidget(self.signals, 0, 0)

    def _process(self):
        if not self.status:
            self._build()
        self.simulation.process()
        self._change_done(True)

    def plot(self):
        if self.done:
            attrs, res = SimulationWidget.plotEdit(self.simu, self)
            if res:
                self.simulation.data.plot(attrs)

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
