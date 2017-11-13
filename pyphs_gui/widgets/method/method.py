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
from PyQt5.QtGui import QFont, QIcon

from pyphs import Core, Graph, datum, Method

from pyphs.misc.latex.latexcore import LatexCore

from ..misc.tools import DescriptionWidget
from ..misc.latex import LatexLabel

from ..misc.tools import Element, NoneSig, BoolSig

from pyphs import netlist2tex, core2tex, graphplot2tex, texdocument
from pyphs import Core

from .. import iconspath


class MethodWidget(QWidget):

    _status = False
    _label = None

    config = {'grad': 'discret',  # In {‘discret’, ‘theta’, ‘trapez’}
              'theta': 0.,        # Theta-scheme for the structure
              'split': True,     # split implicit from explicit part
              }

    def get_core(self):
        return self.coreWidget.core
    core = property(get_core)

    def get_folder(self):
        return self.coreWidget.folder
    folder = property(get_folder)

    def __init__(self, coreWidget, parent=None):

        super(MethodWidget, self).__init__(parent)

        self.statusSig = BoolSig()
        self.modifSig = NoneSig()

        self.coreWidget = coreWidget

        self.method = self.core.to_method(self.config)

        self.modifSig.sig.emit()

        self._label = self.coreWidget.core.label

        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        self.status = QLabel()

        font = QFont()
        font.setBold(True)
        self.status.setFont(font)
        self.set_status(False)

        self.label = QLineEdit(self._label)
        self.label.textChanged[str].connect(self.update_label)

        title = QHBoxLayout()
        core_title = QLabel('Method')
        core_title.setFont(font)

        title.addWidget(core_title)
        title.addWidget(self.label)
        title.addStretch()
        title.addWidget(self.status)

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
        title.addWidget(buildbutton)

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
        title.addWidget(exportbutton)

        vbox.addLayout(title)
        self.positions = {'grad': (0, 0), 'theta': (0, 1),
                          'split': (0, 2)
                          }

        self.content = {'grad': {'desc': 'Discrete Evaluation of Hamiltonian gradient.',
                                 'label': 'Gradient',
                                 'value': self.config['grad'],
                                 'type': 'sel',
                                 'choices': ['discret', 'theta', 'trapez']
                                 },
                        'theta': {'desc': 'Theta scheme (0=explicit, 0.5=midpoint, 1=implicit).',
                                  'label': 'Theta',
                                  'value': self.config['theta'],
                                  'type': 'float',
                                  },
                        'split': {'desc': 'Pre-solve the affine part (matrix inversion).',
                                  'label': 'Pre-solve',
                                  'value': self.config['split'],
                                  'type': 'bool',
                                  },
                        }

        self.grid = QGridLayout()

        for k in self.content.keys():
            self.grid.addWidget(Element(**self.content[k]), *self.positions[k])
            item = self.grid.itemAtPosition(*self.positions[k])
            widget = item.widget()
            widget.modifSig.sig.connect(self.set_status)

        vbox.addLayout(self.grid)

        self.setLayout(vbox)
        self.resize(self.sizeHint())

        self.coreWidget.statusSig.sig.connect(self.coreStatusChanged)

    def coreStatusChanged(self, s):
        if not s:
            self.set_status()
        self.update_label(self.core.label)

    def update_config(self):
        for k in self.content.keys():
            item = self.grid.itemAtPosition(*self.positions[k])
            widget = item.widget()
            self.config[k] = widget.data['value']

    def _build(self):

        try:
            if not self.coreWidget.status.text() == 'Build OK':
                self.coreWidget._build()
            self.method = self.core.to_method(self.config)
            self.update_label(self._label)
            self.set_status(True)

        except:
            QMessageBox.question(self, 'Build issue',
                                 'Can not build method {}'.format(self._label),
                                 QMessageBox.Ok, QMessageBox.Ok)

        self.modifSig.sig.emit()

    def update_label(self, label):
        self._label = label
        self.label.setText(label)
        self.method.label = label

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

    def set_status(self, status=False):

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
