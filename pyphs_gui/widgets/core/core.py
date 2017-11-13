#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""


from __future__ import absolute_import, division, print_function

import sys
import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QApplication, QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox, QLineEdit,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView)
from PyQt5.QtGui import QIcon, QFont
from pyphs import Core, Graph, datum

from pyphs.misc.latex.latexcore import LatexCore

from ..netlist.tools import perform_analysis
from ..misc.tools import DescriptionWidget, NoneSig, BoolSig
from ..misc.latex import LatexLabel

from .show import (StorageWidget, StructureWidget, DissipationWidget,
                   PortsWidget, ParametersWidget)

from pyphs import netlist2tex, core2tex, graphplot2tex, texdocument

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

    built_net = None

    def get_net(self):
        net = set(self.netlistWidget.Netlist.netlist().splitlines())
        return net
    net = property(get_net)

    def get_folder(self):
        return self.netlistWidget.Netlist.folder
    folder = property(get_folder)

    def __init__(self, netlistWidget, parent=None):

        super(CoreWidget, self).__init__(parent)

        self.statusSig = BoolSig()

        self.netlistWidget = netlistWidget
        fn = self.netlistWidget.Netlist.filename
        label = fn[:fn.rfind('.')]
        self.core = Core(label)

        self.initUI()


    def initUI(self):

        vbox = QVBoxLayout()

        self.status = QLabel()

        font = QFont()
        font.setBold(True)
        self.status.setFont(font)
        self.set_status(False)

        self.label = QLineEdit(self.core.label)
        self.label.textChanged[str].connect(self.update_label)

        title = QHBoxLayout()
        core_title = QLabel('Core')
        core_title.setFont(font)

        title.addWidget(core_title)
        title.addWidget(self.label)
        title.addStretch()
        title.addWidget(self.status)

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
        title.addWidget(buildbutton)

        storagebutton = QPushButton('Storage')
        storagebutton.clicked.connect(self._storage)

        dissbutton = QPushButton('Dissipation')
        dissbutton.clicked.connect(self._diss)

        portsbutton = QPushButton('Ports')
        portsbutton.clicked.connect(self._ports)

        parsbutton = QPushButton('Parameters')
        parsbutton.clicked.connect(self._pars)

        strucbutton = QPushButton('Structure')
        strucbutton.clicked.connect(self._stru)

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
        title.addWidget(exportbutton)

        buttons1 = QHBoxLayout()
        buttons1.addWidget(storagebutton)
        buttons1.addWidget(dissbutton)
        buttons1.addWidget(portsbutton)
        buttons1.addWidget(strucbutton)
        buttons1.addWidget(parsbutton)

        vbox.addLayout(title)

        temp = QHBoxLayout()
        temp.addStretch()
        temp.addWidget(LatexLabel(coretex, 6, self))
        temp.addStretch()
        vbox.addLayout(temp)
        vbox.addLayout(buttons1)
        vbox.addStretch()

        self.setLayout(vbox)
        self.resize(self.sizeHint())

        self.netlistWidget.statusSig.sig.connect(self.netlistStatusChanged)

    def netlistStatusChanged(self, s):
        self.check_net()
        fn = self.netlistWidget.Netlist.filename
        label = fn[:fn.rfind('.')]
        self.label.setText(label)
        self.update_label(label)

    def _build(self):

        item = self.netlistWidget.title.itemAtPosition(0, 1)
        status = item.widget()

        if not status.text() == 'Saved':
            self.netlistWidget._save()

        res = perform_analysis(self.netlistWidget.Netlist, self)

        if res:
            self.core = self.netlistWidget.Netlist.graph.to_core(self.core.label,
                                                                 force=False)
            self.built_net = self.net
            self.set_status(True)
            self.latexcore = LatexCore(self.core)
        else:
            self.core = Core(label=self.core.label)

    def _storage(self):
        self._w = StorageWidget(self.latexcore)
        self._w.show()

    def _diss(self):
        self._w = DissipationWidget(self.latexcore)
        self._w.show()

    def _ports(self):
        self._w = PortsWidget(self.latexcore)
        self._w.show()

    def _pars(self):
        self._w = ParametersWidget(self.latexcore)
        self._w.show()

    def _stru(self):
        self._w = StructureWidget(self.latexcore)
        self._w.show()

    def update_label(self, label):
        self.netlistWidget.Netlist.graph.label = label
        self.core.label = label

    def _writelatex(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.folder, self.core.label + '.tex')
        dialog.selectFile(filename)
        fileName, _ = dialog.getSaveFileName(self,
                                             "Save LaTeX file as...",
                                             filename,
                                             "All Files (*);;Latex Files (*.tex)",
                                             "Latex Files (*.tex)",
                                             options=options)
        if not fileName == '':
            content = netlist2tex(self.netlistWidget.Netlist)
            content += graphplot2tex(self.netlistWidget.Netlist.graph)
            content += core2tex(self.core)
            title = self.core.label
            texdocument(content, fileName, title)

    def check_net(self):
        self.set_status(self.net == self.built_net)

    def set_status(self, status):

        if status:
            text = 'Build OK'
            color = 'green'
        else:
            text = 'Build Needed'
            color = 'red'

        self.statusSig.sig.emit(status)

        self.status.setStyleSheet("QLabel { color: %s}" % color)
        self.status.setText(text)


###############################################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = CoreWidget()
    sys.exit(app.exec_())
