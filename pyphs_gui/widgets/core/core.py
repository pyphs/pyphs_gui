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
from ..misc.signals import BoolSig

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
        return self.graphWidget.folder
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

        dimsLayout = QHBoxLayout()
        dimsLayout.setContentsMargins(0, 0, 0, 0)

        self.storageWidget = DescriptionWidget('Storages', '0', 'Dimension of the state vector')
        self.dissipationWidget = DescriptionWidget('Dissipations', '0', 'Dimension of the dissipation vector')
        self.sourceWidget = DescriptionWidget('Ports', '0', 'Dimension of the inpuut/output vectors')

        dimsLayout.addWidget(self.storageWidget)
        dimsLayout.addWidget(self.dissipationWidget)
        dimsLayout.addWidget(self.sourceWidget)
        dimsLayout.addStretch()
        dimsLayout.setContentsMargins(0, 0, 0, 0)

        # ---------------------------------------------------------------------
        # Define Core Actions

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 0)

        # Build Action
        build_icon = QIcon(os.path.join(iconspath, 'work.png'))
        self.buildAction = QAction(build_icon,
                                 '&Build PHS Core', self)
        self.buildAction.setShortcut('Ctrl+B')
        self.buildAction.setStatusTip('Build Port-Hamiltonian System equations')
        self.buildAction.triggered.connect(self._build)
        buildbutton = QPushButton(build_icon, '')
        buildbutton.setToolTip('Build Port-Hamiltonian System equations')
        buildbutton.clicked.connect(self._build)
        buttonsLayout.addWidget(buildbutton)

        # Latex export Action
        export_icon = QIcon(os.path.join(iconspath, 'latex.png'))
        self.exportAction = QAction(export_icon,
                                    '&Export LaTeX document', self)
        self.exportAction.setShortcut('Ctrl+L')
        self.exportAction.setStatusTip('Export a LaTeX document that describes the Port-Hamiltonian System')
        self.exportAction.triggered.connect(self._writelatex)
        exportbutton = QPushButton(export_icon, '')
        exportbutton.setToolTip('Export a LaTeX document')
        exportbutton.clicked.connect(self._writelatex)
        buttonsLayout.addWidget(exportbutton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'CORE'

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
            content = netlist2tex(self.graphWidget.netlistWidget.netlist)
            content += graphplot2tex(self.graphWidget.graph)
            content += core2tex(self.core)
            title = self.core.label
            texdocument(content, fileName, title)
