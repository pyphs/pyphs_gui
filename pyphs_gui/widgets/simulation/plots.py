#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 00:04:31 2017

@author: afalaize
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QCheckBox, QDialogButtonBox)
from PyQt5.QtCore import Qt

from pyphs.misc.tools import geteval

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
                labels = tuple(map(lambda x: 'dHd' + str(x),
                                   self.simu.method.x))
            elif name == 'z':
                labels = tuple(map(lambda w: 'z' + str(w)[1:],
                                   self.simu.method.w))
            else:
                labels = tuple(map(str, geteval(self.simu.method, name)))
            self.labels[name] = labels
            self.checkboxes[name] = tuple(map(lambda l: QCheckBox(l, self),
                                              labels))
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
