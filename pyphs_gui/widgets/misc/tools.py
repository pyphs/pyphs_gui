#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:59:51 2017

@author: afalaize
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QLabel, QGridLayout,
                             QComboBox, QLineEdit, QDialogButtonBox,
                             QPushButton, QSpinBox)


from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QObject, pyqtSignal

import ast


class NoneSig(QObject):

    sig = pyqtSignal()


class BoolSig(QObject):

    sig = pyqtSignal(bool)


class IntSig(QObject):

    sig = pyqtSignal(int)


class FloatSig(QObject):

    sig = pyqtSignal(float)


class StrSig(QObject):

    sig = pyqtSignal(str)


# --------------------------------------------------------------------------- #


class DescriptionWidget(QWidget):

    def __init__(self, label, desc, tooltip, parent=None):

        super(DescriptionWidget, self).__init__(parent)

        hbox = QHBoxLayout()

        font = QFont()
        font.setBold(True)

        self.label = QLabel(label[0].upper() + label[1:].lower() + ':')
        self.label.setFont(font)
        hbox.addWidget(self.label)
        self.desc = QLabel('{}'.format(desc))
        hbox.addWidget(self.desc)

        self.setLayout(hbox)
        self.setToolTip(tooltip)

    def _update(self, label, desc, tooltip):
        self.label.setText(label[0].upper() + label[1:].lower() + ':')
        self.desc.setText('{}'.format(desc))
        self.setToolTip(tooltip)


# --------------------------------------------------------------------------- #

class FloatArgEdit(QDialog):

    def __init__(self, parent=None, **data):

        super(FloatArgEdit, self).__init__(parent)

        self.data = data.copy()

        self.initUI()

    def initUI(self):

        # define hbox
        hbox = QHBoxLayout()

        # Label widget
        hbox.addWidget(QLabel(str(self.data['label'])))

        # Value widget
        self.qle = QLineEdit(self)
        self.qle.textChanged[str].connect(self.onchange)
        self.qle.setText(str(self.data['value']))
        hbox.addWidget(self.qle)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # define vbox
        vbox = QVBoxLayout()

        # Description widget
        vbox.addWidget(QLabel(self.data['desc']))
        vbox.addLayout(hbox)
        vbox.addWidget(buttons)

        # set layout and show
        self.setLayout(vbox)

    def onchange(self, text):
        self.data['value'] = float(ast.literal_eval(text))


# --------------------------------------------------------------------------- #

class IntArgEdit(QDialog):

    def __init__(self, parent=None, **data):

        super(IntArgEdit, self).__init__(parent)

        self.data = data.copy()

        self.initUI()

    def initUI(self):

        # define hbox
        hbox = QHBoxLayout()

        # Label widget
        hbox.addWidget(QLabel(str(self.data['label'])))

        # Value widget
        self.qsb = QSpinBox(self)
        self.qsb.valueChanged[int].connect(self.onchange)
        self.qsb.setValue(self.data['value'])
        hbox.addWidget(self.qsb)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # define vbox
        vbox = QVBoxLayout()

        # Description widget
        vbox.addWidget(QLabel(self.data['desc']))
        vbox.addLayout(hbox)
        vbox.addWidget(buttons)

        # set layout and show
        self.setLayout(vbox)

    def onchange(self, value):
        self.data['value'] = value


# --------------------------------------------------------------------------- #


class SelectArgEdit(QDialog):

    def __init__(self, parent=None, **data):

        super(SelectArgEdit, self).__init__(parent)

        self.data = data.copy()

        self.initUI()

    def initUI(self):

        # define vbox
        vbox = QVBoxLayout()

        # Description Layout
        hbox_desc = QHBoxLayout()
        hbox_desc.addStretch()
        hbox_desc.addWidget(QLabel(self.data['desc']))
        hbox_desc.addStretch()
        vbox.addLayout(hbox_desc)

        # Label and value
        hbox_val = QHBoxLayout()
        hbox_val.addStretch()
        hbox_val.addWidget(QLabel(str(self.data['label'])))

        self.qcb = QComboBox(self)
        for i, par in enumerate(self.data['choices']):
            self.qcb.addItem(par)
            if par == self.data['value']:
                self.qcb.setCurrentIndex(i)
        self.qcb.activated[str].connect(self.onchange)
        hbox_val.addWidget(self.qcb)
        hbox_val.addStretch()
        vbox.addLayout(hbox_val)

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

    def onchange(self, text):
        self.data['value'] = text

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #


class BoolArgEdit(QDialog):

    def __init__(self, parent=None, **data):

        super(BoolArgEdit, self).__init__(parent)

        self.data = data.copy()

        self.initUI()

    def initUI(self):

        # define vbox
        vbox = QVBoxLayout()

        # Description Layout
        hbox_desc = QHBoxLayout()
        hbox_desc.addStretch()
        hbox_desc.addWidget(QLabel(self.data['desc']))
        hbox_desc.addStretch()
        vbox.addLayout(hbox_desc)

        # Label and value
        hbox_val = QHBoxLayout()
        hbox_val.addStretch()
        hbox_val.addWidget(QLabel(str(self.data['label'])))
        self.qcb = QComboBox(self)
        for i, par in enumerate([str(False), str(True)]):
            self.qcb.addItem(par)
            if par == str(self.data['value']):
                self.qcb.setCurrentIndex(i)
        self.qcb.activated[str].connect(self.onchange)
        hbox_val.addWidget(self.qcb)
        hbox_val.addStretch()
        vbox.addLayout(hbox_val)

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

    def onchange(self, text):
        self.data['value'] = text == 'True'

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #


class Element(QWidget):


    def __init__(self, **data):

        QWidget.__init__(self)

        self.data = data.copy()

        self.initUI()

    def initUI(self):

        self.modifSig = NoneSig()
        # define hbox
        hbox = QHBoxLayout()

        # Label widget
        font = QFont()
        font.setBold(True)
        label = QLabel(str(self.data['label'])+':')
        label.setFont(font)
        label.setToolTip(self.data['desc'])
        hbox.addWidget(label)

        # Value widget
        if self.data['type'] == 'float':
            widget = QLineEdit(self)
            widget.textChanged[str].connect(self.onchange)
            widget.setText(str(self.data['value']))

        elif self.data['type'] == 'int':
            widget = QSpinBox(self)
            widget.valueChanged[int].connect(self.onchange)
            widget.setValue(self.data['value'])

        elif self.data['type'] == 'sel':
            widget = QComboBox(self)
            for i, par in enumerate(self.data['choices']):
                widget.addItem(par)
                if par == self.data['value']:
                    widget.setCurrentIndex(i)
            widget.activated[str].connect(self.onchange)

        elif self.data['type'] == 'bool':
            widget = QComboBox(self)
            for i, par in enumerate([str(False), str(True)]):
                widget.addItem(par)
                if par == str(self.data['value']):
                    widget.setCurrentIndex(i)
            widget.activated[str].connect(self.onchange)

        self.valueWidget = widget

        hbox.addWidget(self.valueWidget)

        # set layout and show
        self.setLayout(hbox)

    def onchange(self, text):
        if self.data['type'] == 'float':
            self.data['value'] = (None if text == 'None' else
                                  float(ast.literal_eval(text)))
        elif self.data['type'] == 'int':
            self.data['value'] = text
        elif self.data['type'] == 'sel':
            self.data['value'] = text
        elif self.data['type'] == 'bool':
            self.data['value'] = text == 'True'

        # Emit signal
        self.modifSig.sig.emit()


# --------------------------------------------------------------------------- #
