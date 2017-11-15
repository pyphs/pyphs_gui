#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 13:53:56 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QLineEdit)


from .signals import StrSig, BoolSig
from .fonts import boldFont


class TitleWidget(QWidget):

    def __init__(self, title=None, labelWidget=None, status_labels=None,
                 buttonsLayout=None, parent=None):

        super(TitleWidget, self).__init__(parent)

        # Title
        if title is None:
            self.title = ''
        else:
            self.title = title

        # Label
        if labelWidget is None:
            self.labelWidget = None
        else:
            self.labelWidget = labelWidget

        # Status
        if status_labels is None:
            self.status_labels = None
        else:
            self.status_labels = status_labels

        # Buttons
        if buttonsLayout is None:
            self.buttonsLayout = None
        else:
            self.buttonsLayout = buttonsLayout

        self.initUI()

    def initUI(self):

        # define layout
        hbox = QHBoxLayout()
#        hbox.setContentsMargins(0, 0, 0, 0)

        # define signals
        self.statusSignal = BoolSig()
        self.labelSignal = StrSig()

        # title widget
        self.titleWidget = QLabel(self.title)
        self.titleWidget.setFont(boldFont)
        hbox.addWidget(self.titleWidget)

        if self.labelWidget is not None:
            # label widget
            self.label = self.labelWidget.text()
            if isinstance(self.labelWidget, QLineEdit):
                self.labelWidget.textChanged[str].connect(self._update_label)
            hbox.addWidget(self.labelWidget)

        if self.status_labels is not None:
            # status widget
            self.statusWidget = QLabel()
            self.statusWidget.setFont(boldFont)
            self._change_status(False)
            hbox.addWidget(self.statusWidget)

        if isinstance(self.labelWidget, QLineEdit):
            self.labelWidget.textChanged[str].connect(self._update_label)

        hbox.addStretch()
        hbox.addLayout(self.buttonsLayout)
        self.setLayout(hbox)
        self.setFixedWidth(500)

    def _change_title(self, title):
        self.titleWidget.setText(title)
        self.title = title

    def _change_label(self, label):
        self.labelWidget.setText(label)
        self.label = label
        self._update_label()

    def _update_label(self, label=None):
        if not label == self.label:
            if label is None:
                self.label = self.labelWidget.text()
            else:
                self.label = label
            self.labelSignal.sig.emit(self.label)

    def _change_status(self, status=False):

        text = self.status_labels[status]
        color = 'green' if status else 'red'

        self.statusWidget.setStyleSheet("QLabel { color: %s}" % color)
        self.statusWidget.setText(text)

        self.status = status
        self.statusSignal.sig.emit(status)
