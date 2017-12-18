#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 17:39:31 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QScrollArea, QGridLayout)

from .fonts import boldFont

HEIGHT = 85
WIDTH = 2*HEIGHT


class HListWidget(QWidget):
    def __init__(self, label=None, tooltip=None, widgets=None, parent=None):
        super(HListWidget, self).__init__(parent)

        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 0)
        for w in widgets:
            w.setContentsMargins(0, 0, 0, 0)
            h.addWidget(w)

        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(h)

        scroll = QScrollArea()
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(widget)
#        scroll.setFixedHeight(HEIGHT)
        scroll.setWidgetResizable(True)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(scroll)
        self.setToolTip(tooltip)
        self.setLayout(hbox)
        self.setContentsMargins(0, 0, 0, 0)


class VListWidget(QWidget):
    def __init__(self, label=None, tooltip=None, widgets=None,
                 parent=None):
        super(VListWidget, self).__init__(parent)

        v = QVBoxLayout()
        v.setContentsMargins(0, 0, 0, 0)
        for w in widgets:
            v.addWidget(w)

        widget = QWidget()
        widget.setLayout(v)
        widget.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        vbox = QVBoxLayout()

        if label is not None:
            labelWidget = QLabel(label)
            labelWidget.setFont(boldFont)
            title = QHBoxLayout()
            title.addStretch()
            title.addWidget(labelWidget)
            title.addStretch()
            vbox.addLayout(title)

        vbox.addWidget(scroll)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)
        self.setToolTip(tooltip)
        self.setContentsMargins(0, 0, 0, 0)
