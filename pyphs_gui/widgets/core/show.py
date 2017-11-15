#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 21:22:42 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

import sys
import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QApplication, QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox, QLineEdit,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView, QFrame,
                             QSplitter, QGroupBox, QFormLayout,
                             QScrollArea)
from PyQt5.QtGui import QIcon, QFont

from PyQt5.QtCore import Qt

from pyphs import Core, Graph, datum

from ..misc.tools import DescriptionWidget
from ..misc.latex import LatexLabel, LatexWidget

from pyphs.misc.latex.tools import obj2tex, symbol_names
from pyphs.misc.latex.latexcore import LatexCore


FS = 6


class Element(QWidget):

    def __init__(self, name, desc, latexcode, parent=None):
        super().__init__(parent)

        self.name, self.desc, self.latexcode = name, desc, latexcode
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        title = DescriptionWidget(self.name, self.desc, self.desc)
        latex = LatexLabel(self.latexcode, FS, self)

        vbox.addWidget(title)
        vbox.addWidget(latex)

        self.setLayout(vbox)


class StorageWidget(QWidget):

    def __init__(self, latexcore, parent=None):
        super().__init__(parent)

        self.latexcore = latexcore

        self.initUI()


    def initUI(self):

        mygroupbox = QGroupBox()
        myform = QFormLayout()

        label = QLabel('STORAGE', self)
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(label)
        hbox.addStretch()
        myform.addRow(hbox)

        x = Element('State', 'State of the system', self.latexcore.x,
                    parent=self)
        myform.addRow(x)

        H = Element('Hamiltonian', 'Storage function',
                    self.latexcore.H,
                    parent=self)
        myform.addRow(H)

        dxH = Element("Hamiltonian's gradient",
                      'Gradient of the storage function',
                      self.latexcore.dxH,
                      parent=self)
        myform.addRow(dxH)

        for t in self.latexcore.dxH_elements:
            myform.addRow(LatexLabel(t, FS, self))

        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class DissipationWidget(QWidget):

    def __init__(self, latexcore, parent=None):
        super().__init__(parent)

        self.latexcore = latexcore

        self.initUI()

    def initUI(self):

        mygroupbox = QGroupBox()
        myform = QFormLayout()

        label = QLabel('DISSIPATION', self)
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(label)
        hbox.addStretch()
        myform.addRow(hbox)

        w = Element('Variable', 'Dissipation variable',
                    self.latexcore.w,
                    parent=self)
        myform.addRow(w)

        z = Element('Function', 'Dissipation function',
                    self.latexcore.z,
                    parent=self)
        myform.addRow(z)

        for t in self.latexcore.z_elements:
            myform.addRow(LatexLabel(t, FS, self))

        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class PortsWidget(QWidget):

    def __init__(self, latexcore, parent=None):
        super().__init__(parent)

        self.latexcore = latexcore

        self.initUI()

    def initUI(self):

        mygroupbox = QGroupBox()
        myform = QFormLayout()

        label = QLabel('PORTS', self)
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(label)
        hbox.addStretch()
        myform.addRow(hbox)

        u = Element('Inputs', 'Input variables',
                    self.latexcore.u,
                    parent=self)
        myform.addRow(u)

        y = Element('Outputs', 'Output variables',
                    self.latexcore.y,
                    parent=self)
        myform.addRow(y)

        for t in self.latexcore.y_elements:
            myform.addRow(LatexLabel(t, FS, self))

        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class ParametersWidget(QWidget):

    def __init__(self, latexcore, parent=None):
        super().__init__(parent)

        self.latexcore = latexcore

        self.initUI()

    def initUI(self):

        mygroupbox = QGroupBox()
        myform = QFormLayout()

        label = QLabel('PARAMETERS', self)
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(label)
        hbox.addStretch()
        myform.addRow(hbox)

        subs = Element('Substitutions', 'Constant parameters',
                       self.latexcore.subs,
                       parent=self)
        myform.addRow(subs)

        p = Element('Parameters', 'Controled parameters',
                    self.latexcore.p,
                    parent=self)
        myform.addRow(p)

        o = Element('Observers', 'Observed quantities',
                    self.latexcore.o,
                    parent=self)
        myform.addRow(o)

        for t in self.latexcore.o_elements:
            myform.addRow(LatexLabel(t, FS, self))

        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class StructureWidget(QWidget):

    def __init__(self, latexcore, parent=None):
        super().__init__(parent)

        self.latexcore = latexcore

        self.initUI()

    def initUI(self):

        mygroupbox = QGroupBox()
        myform = QFormLayout()

        label = QLabel('STRUCTURE', self)
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(label)
        hbox.addStretch()
        myform.addRow(hbox)
        tex = r'$\mathbf M = \mathbf J - \mathbf R$'
        myform.addRow(LatexLabel(tex, FS, self))

        for n in 'MJR':
            t = getattr(self.latexcore, n)
            myform.addRow(LatexLabel(t, FS, self))
            for i in 'xwy':
                for j in 'xwy':
                    t = getattr(self.latexcore, n + i + j)
                    myform.addRow(LatexLabel(t, FS, self))

        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class PHSWidget(QWidget):

    def __init__(self, core):
        super().__init__()

        self.latexcore = LatexCore(core)
        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout(self)

        topL = StorageWidget(self.latexcore)
        topR = DissipationWidget(self.latexcore)

        botL = PortsWidget(self.latexcore)
#        botR = StructureWidget(self.latexcore)

        splittertop = QSplitter(Qt.Horizontal)
        splittertop.addWidget(topL)
        splittertop.addWidget(topR)

        splitterbottom = QSplitter(Qt.Horizontal)
        splittertop.addWidget(botL)
#        splittertop.addWidget(botR)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(splittertop)
        splitter.addWidget(splitterbottom)

        hbox.addWidget(splitter)
        self.setLayout(hbox)
