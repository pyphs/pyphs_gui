#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 17:39:31 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QApplication, QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox, QLineEdit,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView, QScrollArea)

from .tools import DescriptionWidget

HEIGHT = 85
WIDTH = 2*HEIGHT


class HListWidget(QWidget):
    def __init__(self, label, tooltip, widgets, parent=None):
        super(HListWidget, self).__init__(parent)

        h = QHBoxLayout()
        for w in widgets:
            h.addWidget(w)

        widget = QWidget()
        widget.setLayout(h)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setFixedHeight(HEIGHT)
        scroll.setWidgetResizable(True)

        hbox = QHBoxLayout()
        hbox.addWidget(DescriptionWidget(label, '', tooltip))
        hbox.addWidget(scroll)

        self.setLayout(hbox)


class VListWidget(QWidget):
    def __init__(self, label, tooltip, widgets, parent=None):
        super(HListWidget, self).__init__(parent)

        title = QHBoxLayout()
        title.addStretch()
        title.addWidget(DescriptionWidget(label, '', tooltip))
        title.addStretch()

        v = QVBoxLayout()
        for w in widgets:
            v.addWidget(w)

        widget = QWidget()
        widget.setLayout(v)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setFixedWidth(WIDTH)
        scroll.setWidgetResizable(True)

        vbox = QVBoxLayout()
        vbox.addLayout(title)
        vbox.addWidget(scroll)

        self.setLayout(vbox)
