#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 12:03:33 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QLabel, QGridLayout,
                             QComboBox, QLineEdit, QDialogButtonBox,
                             QScrollArea)

from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

from pyphs.misc.tools import geteval

from ..misc import ElementWidget

###############################################################################


class LabelWidget(QLineEdit):
    """
    Widget that display a text line.
    """
    def __init__(self, label=None):
        QLineEdit.__init__(self)
        if label is None:
            label = ""
        self.setText(label)

###############################################################################


class InitDialog(QDialog):
    """
    Widget for netlist line creation and edition.
    """

    def __init__(self, initWidget, parent=None):
        """
        Widget for inits edition.
        """
        super(InitDialog, self).__init__(parent)

        self.initWidget = initWidget
        self.initUI()

    def initUI(self):

        font = QFont()
        font.setBold(True)

        vbox = QVBoxLayout()

        self.grids = []
        # -------------------------------
        for i, name in enumerate(self.initWidget._names):
            h = QHBoxLayout()
            l = QLabel(name)
            l.setFont(font)
            h.addWidget(l)

            self.grids.append(QGridLayout())

            for j, s in enumerate(geteval(self.initWidget.method, name)):
                pos = (0, j)
                content = {'desc': '',
                           'label': str(s),
                           'value': self.initWidget.inits[name][j],
                           'type': 'float'
                           }

                self.grids[i].addWidget(ElementWidget(**content), *pos)
                w = self.grids[i].itemAtPosition(*pos).widget()
                onchange = self.build_onchange(i, j)
                w.modifiedSig.sig.connect(onchange)

                h.addLayout(self.grids[i])

            h.addStretch()

            scroll = QScrollArea()
            widget = QWidget()
            widget.setLayout(h)
            scroll.setWidget(widget)
            scroll.setFixedHeight(80)
            scroll.setWidgetResizable(True)
            vbox.addWidget(scroll)

        # -------------------------------

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # -------------------------------

        vbox.addStretch(1)
        vbox.addWidget(buttons)
        self.setLayout(vbox)
        self.setWindowTitle('Edit component')

    def name2index(self, name):
        return self.initWidget._names.index(name)

    def build_onchange(self, i, j):

        name = self.initWidget._names[i]

        def onchange():
            item = self.grids[i].itemAtPosition(0, j)
            widget = item.widget()
            value = widget.data['value']
            self.initWidget.inits[name][j] = value
            print(name, j, value)
            print(self.initWidget.inits)
        return onchange

    @staticmethod
    def getInits(initWidget=None, parent=None):
        dialog = InitDialog(initWidget, parent=parent)
        result = dialog.exec_()
        dialog.close()
        dialog.destroy()
        return (dialog.initWidget.inits, result == QDialog.Accepted)
