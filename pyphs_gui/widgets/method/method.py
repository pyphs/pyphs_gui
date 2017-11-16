#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""


from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QVBoxLayout, QFileDialog,
                             QHBoxLayout, QPushButton, QLineEdit, QMessageBox)

from ..misc.tools import DescriptionWidget
from ..misc.signals import BoolSig, NoneSig

from pyphs import netlist2tex, core2tex, graphplot2tex, texdocument
from ..misc import TitleWidget, ParametersWidget

from PyQt5.QtGui import QIcon
from .. import iconspath


class MethodWidget(QWidget):

    def get_net(self):
        return self.coreWidget.net
    net = property(get_net)

    def get_folder(self):
        return self.coreWidget.folder
    folder = property(get_folder)

    def get_label(self):
        return self.titleWidget.label
    label = property(get_label)

    def get_core(self):
        return self.coreWidget.core
    core = property(get_core)

    def get_status(self):
        return self.titleWidget.status
    status = property(get_status)

    def __init__(self, coreWidget, parent=None):

        super(MethodWidget, self).__init__(parent)

        self.parameters = {'grad': 'discret',  # In {‘discret’, ‘theta’, ‘trapez’}
                           'theta': 0.,        # Theta-scheme for the structure
                           'split': True,     # split implicit from explicit part
                           }

        self.coreWidget = coreWidget

        self.initUI()

    def initUI(self):

        self.method = self.coreWidget.core.to_method()

        self.statusSig = BoolSig()
        self.initSig= NoneSig()

        dimsLayout = QHBoxLayout()
        dimsLayout.setContentsMargins(0, 0, 0, 0)

        self.expliciteWidget = DescriptionWidget('Explicit', '0', 'Dimension of the explict update')
        self.impliciteWidget = DescriptionWidget('Implicit', '0', 'Dimension of the implict update')

        dimsLayout.addWidget(self.expliciteWidget)
        dimsLayout.addWidget(self.impliciteWidget)
        dimsLayout.addStretch()

        # ---------------------------------------------------------------------
        # Define Method Actions

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 0)

        # Build Action
        build_icon = QIcon(os.path.join(iconspath, 'work.png'))
        self.buildAction = QAction(build_icon,
                                 '&Build numerical Method', self)
        self.buildAction.setShortcut('Ctrl+B')
        self.buildAction.setStatusTip('Build numerical method equations')
        self.buildAction.triggered.connect(self._build)
        buildbutton = QPushButton(build_icon, '')
        buildbutton.setToolTip('Build numerical method equations')
        buildbutton.clicked.connect(self._build)
        buttonsLayout.addWidget(buildbutton)

        # Latex export Action
        export_icon = QIcon(os.path.join(iconspath, 'latex.png'))
        self.exportAction = QAction(export_icon,
                                    '&Export LaTeX document', self)
        self.exportAction.setShortcut('Ctrl+L')
        self.exportAction.setStatusTip('Export a LaTeX document that describes the Port-Hamiltonian System')
        self.exportAction.triggered.connect(self._build)
        exportbutton = QPushButton(export_icon, '')
        exportbutton.setToolTip('Export a LaTeX document')
        exportbutton.clicked.connect(self._writelatex)
        buttonsLayout.addWidget(exportbutton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'METHOD'

        self.labelWidget = QLineEdit(self.core.label)

        status_labels = {True: 'OK',
                         False: 'Not OK'}

        self.titleWidget = TitleWidget(title=title,
                                       labelWidget=self.labelWidget,
                                       status_labels=status_labels,
                                       buttonsLayout=buttonsLayout)

        # ---------------------------------------------------------------------
        # set parameters

        content = {}

        content['grad'] = {'desc': 'Discrete Evaluation of Hamiltonian gradient.',
                           'label': 'Gradient',
                           'value': self.parameters['grad'],
                           'type': 'sel',
                           'choices': ['discret', 'theta', 'trapez']
                           }
        content['theta'] = {'desc': 'Theta scheme (0=explicit, 0.5=midpoint, 1=implicit).',
                            'label': 'Theta',
                            'value': self.parameters['theta'],
                            'type': 'float',
                            }
        content['split'] = {'desc': 'Pre-solve the affine part (matrix inversion).',
                            'label': 'Pre-solve',
                            'value': self.parameters['split'],
                            'type': 'bool',
                            }

        tooltip = 'Method parameters'

        self.parametersWidget = ParametersWidget('', content, tooltip)

        # ---------------------------------------------------------------------
        # set Layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.titleWidget)
        vbox.addLayout(dimsLayout)
        vbox.addWidget(self.parametersWidget)
        self.setLayout(vbox)
        self.setContentsMargins(0, 0, 0, 0)

        # ---------------------------------------------------------------------
        # signals
        self.coreWidget.statusSig.sig.connect(self._status_changed)
        self.parametersWidget.modifiedSig.sig.connect(self._update_parameters)
        self.titleWidget.labelSignal.sig.connect(self._update_label)
        self.coreWidget.initSig.sig.connect(self._netlist_init)

    def _netlist_init(self):
        label = self.coreWidget.label
        self._update_label(label)
        self.initSig.sig.emit()

    def _update_parameters(self):
        if not self.parameters == self.parametersWidget.parameters:
            self.parameters.update(self.parametersWidget.parameters)
            self._change_status(False)

    def _update(self):
        self.expliciteWidget.desc.setText(str(self.method.dims.l()))
        self.impliciteWidget.desc.setText(str(self.method.dims.nl()))

    def _status_changed(self, s=False):
        if not s:
            self._change_status(s)

    def _change_status(self, s=False):
            self.titleWidget._change_status(s)
            self.statusSig.sig.emit(s)

    def _update_label(self, label):
        if not self.label == label:
            self.titleWidget._change_label(label)

    def _change_label(self, label):
        self.titleWidget._change_label(label)
        self._update_label(label)

    def _writelatex(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.folder, self.label + '.tex')
        dialog.selectFile(filename)
        fileName, _ = dialog.getSaveFileName(self,
                                             "Save LaTeX file as...",
                                             filename,
                                             "All Files (*);;Latex Files (*.tex)",
                                             "Latex Files (*.tex)",
                                             options=options)
        if not fileName == '':
            content = netlist2tex(self.coreWidget.graphWidget.netlistWidget.netlist)
            content += graphplot2tex(self.coreWidget.graphWidget.graph)
            content += core2tex(self.core)
            title = self.core.label
            texdocument(content, fileName, title)

    def _build(self):
        if not self.coreWidget.status:
            self.coreWidget._build()

        if self.coreWidget.status:
#            try:
                self.method = self.core.to_method(self.parameters)

                self.method.label = self.label

                self._update()

                self._change_status(True)
#            except:
#                QMessageBox.question(self, 'Build issue',
#                                     'Can not build method {}'.format(self.label),
#                                     QMessageBox.Ok, QMessageBox.Ok)

###############################################################################
