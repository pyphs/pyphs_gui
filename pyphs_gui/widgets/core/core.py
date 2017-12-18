#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""


from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QVBoxLayout, QFileDialog,
                             QHBoxLayout, QPushButton, QLineEdit)

from pyphs import Core

from ..misc.tools import DescriptionWidget
from ..misc.signals import BoolSig, NoneSig

from pyphs import netlist2tex, core2tex, graphplot2tex, texdocument
from ..misc import TitleWidget, ParametersWidget

from PyQt5.QtGui import QIcon
from .. import iconspath


coretex = r"""
$
\left(
\begin{array}{c}
\dot{\mathbf x} \\
\mathbf w \\
\mathbf y \\
\end{array}
\right)
=
\left(
\begin{array}{lll}
\mathbf{M_{xx}} & \mathbf{M_{xw}} & \mathbf{M_{xy}} \\
\mathbf{M_{wx}} & \mathbf{M_{ww}} & \mathbf{M_{wy}} \\
\mathbf{M_{yx}} & \mathbf{M_{yw}} &  \mathbf{M_{yy}} \\
\end{array}
\right)
\cdot
\left(
\begin{array}{c}
\\nnabla \mathrm H\\
\mathbf z \\
\mathbf u \\
\end{array}
\right)
$
""".replace(r'\n', '')


class CoreWidget(QWidget):

    def get_net(self):
        net = set(self.graphWidget.netlistWidget.netlist.netlist().splitlines())
        return net
    net = property(get_net)

    def get_folder(self):
        return self.graphWidget.netlistWidget.netlist.folder
    folder = property(get_folder)

    def get_label(self):
        return self.titleWidget.label
    label = property(get_label)

    def get_status(self):
        return self.titleWidget.status
    status = property(get_status)

    def __init__(self, graphWidget, parent=None):

        super(CoreWidget, self).__init__(parent)

        self.parameters = {'reduce z': False,
                           'substitute': False}

        self.graphWidget = graphWidget

        self.initUI()

    def initUI(self):

        self.core = Core(self.graphWidget.label)

        self.statusSig = BoolSig()
        self.initSig= NoneSig()

        self.dimsLayout = QHBoxLayout()
        self.dimsLayout.setContentsMargins(0, 0, 0, 0)

        self.storageWidget = DescriptionWidget('Storages', '0', 'Dimension of the state vector')
        self.dissipationWidget = DescriptionWidget('Dissipations', '0', 'Dimension of the dissipation vector')
        self.sourceWidget = DescriptionWidget('Ports', '0', 'Dimension of the inpuut/output vectors')

        self.dimsLayout.addWidget(self.storageWidget)
        self.dimsLayout.addWidget(self.dissipationWidget)
        self.dimsLayout.addWidget(self.sourceWidget)
        self.dimsLayout.addStretch()
        self.dimsLayout.setContentsMargins(0, 0, 0, 0)

        self.dimsWidget = QWidget(self)
        self.dimsWidget.setLayout(self.dimsLayout)

        # ---------------------------------------------------------------------
        # Define Core Actions

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)

        # Build Action
        build_icon = QIcon(os.path.join(iconspath, 'work.png'))
        self.buildAction = QAction(build_icon,
                                 '&Build PHS Core', self)
        self.buildAction.setShortcut('Ctrl+B')
        self.buildAction.setStatusTip('Build Port-Hamiltonian System equations')
        self.buildAction.triggered.connect(self._build)
        self.buildButton = QPushButton(build_icon, '')
        self.buildButton.setToolTip('Build Port-Hamiltonian System equations')
        self.buildButton.clicked.connect(self._build)
        self.buttonsLayout.addWidget(self.buildButton)

        # Latex export Action
        export_icon = QIcon(os.path.join(iconspath, 'latex.png'))
        self.exportAction = QAction(export_icon,
                                    '&Export LaTeX document', self)
        self.exportAction.setShortcut('Ctrl+L')
        self.exportAction.setStatusTip('Export a LaTeX document that describes the Port-Hamiltonian System')
        self.exportAction.triggered.connect(self._writelatex)
        self.exportButton = QPushButton(export_icon, '')
        self.exportButton.setToolTip('Export a LaTeX document')
        self.exportButton.clicked.connect(self._writelatex)
        self.buttonsLayout.addWidget(self.exportButton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'CORE'

        self.labelWidget = QLineEdit(self.core.label)
        self.labelWidget.adjustSize()
        status_labels = {True: 'OK',
                         False: 'Not OK'}

        self.titleWidget = TitleWidget(title=title,
                                       labelWidget=self.labelWidget,
                                       status_labels=status_labels,
                                       buttonsLayout=self.buttonsLayout)

        # ---------------------------------------------------------------------
        # set parameters

        content = {}

        content['reduce z'] = {'desc': 'Reduce linear dissipations into the R-matrix.',
                               'label': 'Reduce z',
                               'value': self.parameters['reduce z'],
                               'type': 'bool'
                               }

        content['substitute'] = {'desc': 'Substitute all symbols by their numerical value.',
                                 'label': 'Substitute',
                                 'value': self.parameters['substitute'],
                                 'type': 'bool'
                                 }
        tooltip = 'Core parameters'

        self.parametersWidget = ParametersWidget('', content, tooltip)

        # ---------------------------------------------------------------------
        # signals
        self.graphWidget.initSig.sig.connect(self._netlist_init)
        self.graphWidget.statusSig.sig.connect(self._status_changed)
        self.parametersWidget.modifiedSig.sig.connect(self._update_parameters)
        self.titleWidget.labelSignal.sig.connect(self._update_label)

    def _update_parameters(self):
        if not self.parameters == self.parametersWidget.parameters:
            self.parameters.update(self.parametersWidget.parameters)
            self._change_status(False)

    def _update(self):
        self.storageWidget.desc.setText(str(self.core.dims.x()))
        self.dissipationWidget.desc.setText(str(self.core.dims.w()))
        self.sourceWidget.desc.setText(str(self.core.dims.y()))

    def _status_changed(self, s=False):
        if not s:
            self._change_status(s)

    def _change_status(self, s=False):
            self.titleWidget._change_status(s)
            self.statusSig.sig.emit(s)

    def _netlist_init(self):
        label = self.graphWidget.label
        self._update_label(label)
        self.initSig.sig.emit()

    def _update_label(self, label):
        if not self.core.label == label:
            self.graphWidget.graph.label = label
            self.core.label = label
            self.titleWidget._change_label(label)

    def _change_label(self, label):
        self.titleWidget._change_label(label)
        self._update_label(label)

    def _build(self):
        if not self.graphWidget.status:
            self.graphWidget._build()

        if self.graphWidget.status:
            self.core = self.graphWidget.graph.to_core(self.core.label)

            if self.parameters['reduce z']:
                self.core.reduce_z()

            if self.parameters['substitute']:
                self.core.substitute(selfall=True)

            self._update()
            self._change_status(True)

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
            folder = filename[:filename.rfind(os.sep)]
            content = netlist2tex(self.graphWidget.netlistWidget.netlist)
            content += graphplot2tex(self.graphWidget.graph,
                                     folder=folder)
            content += core2tex(self.core)
            title = self.core.label
            texdocument(content, fileName, title)
