#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QVBoxLayout, QFileDialog,
                             QHBoxLayout, QPushButton, QLineEdit, QLabel)

from ..misc.signals import BoolSig, NoneSig

from pyphs import netlist2tex, core2tex, graphplot2tex, texdocument
from pyphs.misc import juce, faust

from ..misc import TitleWidget, ParametersWidget, DescriptionWidget
from ..misc.fonts import boldFont
from PyQt5.QtGui import QIcon
from .. import iconspath
from .inits import InitWidget
from .io import IoWidget


class NumericWidget(QWidget):

    def get_net(self):
        return self.methodWidget.net
    net = property(get_net)

    def get_folder(self):
        return self.methodWidget.folder
    folder = property(get_folder)

    def get_label(self):
        return self.methodWidget.label
    label = property(get_label)

    def get_core(self):
        return self.methodWidget.method.core
    core = property(get_core)

    def get_method(self):
        return self.methodWidget.method
    method = property(get_method)

    def get_status(self):
        return self.methodWidget.status
    status = property(get_status)

    def get_inout(self):
        inputs = []
        outputs = []
        for i in range(self.method.dims.y()):
            if self.io.io['u'][i]:
                inputs.append(self.method.u[i])
            else:
                inputs.append(self.inits.inits['u'][i])
            if self.io.io['y'][i]:
                outputs.append(self.method.y[i])
            else:
                pass
        return inputs, outputs

    inout = property(get_inout)

    def __init__(self, methodWidget, parent=None):

        super(NumericWidget, self).__init__(parent)

        self.parameters = {'eps': 1e-9,
                           'epsdg': 1e-12,
                           'fs': 48000.0,
                           'maxit': 10}

        self.methodWidget = methodWidget

        self.initUI()

    def initUI(self):

        self.numeric = self.method.to_numeric()

        self.statusSig = BoolSig()
        self.initSig = NoneSig()

        # ---------------------------------------------------------------------
        # Define Method Actions

        buttonsLayout = QHBoxLayout()

        # cpp export Action
        cpp_icon = QIcon(os.path.join(iconspath, 'c++.png'))
        self.cppAction = QAction(cpp_icon,
                                    '&Export c++ code', self)
        self.cppAction.setShortcut('Ctrl+L')
        self.cppAction.setStatusTip('Export a bunch of c++ for numerical simulations')
        self.cppAction.triggered.connect(self._writecpp)
        self.cppButton = QPushButton(cpp_icon, '')
        self.cppButton.setToolTip('Export c++ code')
        self.cppButton.clicked.connect(self._writecpp)
        buttonsLayout.addWidget(self.cppButton)

        # faust export Action
        faust_icon = QIcon(os.path.join(iconspath, 'faust.png'))
        self.faustAction = QAction(faust_icon,
                                    '&Export FAUST code', self)
        self.faustAction.setShortcut('Ctrl+L')
        self.faustAction.setStatusTip('Export FAUST code')
        self.faustAction.triggered.connect(self._writefaust)
        self.faustButton = QPushButton(faust_icon, '')
        self.faustButton.setToolTip('Export FAUST code')
        self.faustButton.clicked.connect(self._writefaust)
        buttonsLayout.addWidget(self.faustButton)

        # juce export Action
        juce_icon = QIcon(os.path.join(iconspath, 'juce.png'))
        self.juceAction = QAction(juce_icon,
                                    '&Export JUCE code', self)
        self.juceAction.setShortcut('Ctrl+L')
        self.juceAction.setStatusTip('Export JUCE code')
        self.juceAction.triggered.connect(self._writejuce)
        self.juceButton = QPushButton(juce_icon, '')
        self.juceButton.setToolTip('Export JUCE code')
        self.juceButton.clicked.connect(self._writejuce)
        buttonsLayout.addWidget(self.juceButton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'NUMERIC'

        self.labelWidget = QLabel(title)
        self.labelWidget.setFont(boldFont)

        titleLayout = QHBoxLayout()

        titleLayout.addWidget(self.labelWidget)
        titleLayout.addStretch()
        titleLayout.addLayout(buttonsLayout)

        self.titleWidget = QWidget()
        self.titleWidget.setLayout(titleLayout)

        # ---------------------------------------------------------------------
        # set parameters

        content = {'fs': {'desc': 'Sample Rate (Hz)',
                          'label': 'Sample Rate',
                          'value': self.parameters['fs'],
                          'type': 'float',
                          },

                   'maxit': {'desc': 'Maximum number of implicit iterations.',
                             'label': 'Iterations',
                             'value': self.parameters['maxit'],
                             'type': 'int',
                             },

                   'eps': {'desc': 'Numerical tolerance on implicit iterations.',
                           'label': 'Tolerance',
                           'value': self.parameters['eps'],
                           'type': 'float',
                           },
                   }

        tooltip = 'Numerical parameters'

        self.parametersWidget = ParametersWidget('', content, tooltip)

        # ---------------------------------------------------------------------
        # inits

        self.inits = InitWidget(self.methodWidget)

        # ---------------------------------------------------------------------
        # io

        self.io = IoWidget(self.methodWidget)

        # ---------------------------------------------------------------------
        # set Layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.titleWidget)
        vbox.addWidget(self.inits)
        vbox.addWidget(self.io)
        vbox.addWidget(self.parametersWidget)
        self.setLayout(vbox)
        self.setContentsMargins(0, 0, 0, 0)

        self.methodWidget.initSig.sig.connect(self._netlist_init)
        self.parametersWidget.modifiedSig.sig.connect(self._modified)

    def _netlist_init(self):
        self.initSig.sig.emit()

    def _modified(self):
        self._update_parameters()
        self.statusSig.sig.emit(False)

    def _update_parameters(self):
        if not self.parameters == self.parametersWidget.parameters:
            self.parameters.update(self.parametersWidget.parameters)

    def _writecpp(self):
        if not self.status:
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.selectFile(self.folder)
        folder = dialog.getExistingDirectory(self,
                                             "Save c++ files in...",
                                             self.folder,
                                             options=options)
        if not folder == '':
            folder = os.path.join(folder, self.method.label + '_Sources')
            args = {'objlabel': self.method.label,
                    'path': folder,
                    'inits': self.inits.inits,
                    'config': self.parameters,
                    'subs': None
                    }
            self.method.to_cpp(**args)

    def _writejuce(self):
        if not self.status:
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.selectFile(self.folder)
        folder = dialog.getExistingDirectory(self,
                                             "Save JUCE snippets files in...",
                                             self.folder,
                                             options=options)
        if not folder == '':
            inputs = []
            for i, u in enumerate(self.method.u):
                if self.io.io['u'][i]:
                    inputs.append(u)
            outputs = []
            for i, y in enumerate(self.method.y):
                if self.io.io['y'][i]:
                    outputs.append(y)
            juce.fx.method2jucefx(self.method, path=folder,
                                  io=(inputs, outputs), inits=self.inits.inits,
                                  config=self.parameters)

    def _writefaust(self):
        if not self.status:
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.folder, self.method.label + '.dsp')
        dialog.selectFile(filename)
        fname, _ = dialog.getSaveFileName(self,
                                          "Save FAUST code as...",
                                          filename,
                                          "All Files (*);;FAUST code (*.dsp)",
                                          "FAUST code (*.dsp)",
                                          options=options)
        if not fname == '':
            if not fname.endswith('.dsp'):
                fname += '.dsp'
            print('FAUST: write '+fname)
            methodIMat = faust.MethodInvMat(self.method._core,
                                            self.methodWidget.parameters,
                                            self.method.label)

            faust.write_faust_fx(methodIMat, path=fname,
                                 inputs=self.inout[0], outputs=self.inout[1],
                                 inits=self.inits.inits,
                                 nIt=self.parameters['maxit'])
