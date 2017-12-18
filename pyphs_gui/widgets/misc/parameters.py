#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 13:53:56 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QWidget, QHBoxLayout)

from .element import ElementWidget
from .lists import HListWidget
from .signals import NoneSig


class ParametersWidget(QWidget):

    def __init__(self, title=None, content=None, tooltip=None, parent=None):

        super(ParametersWidget, self).__init__(parent)

        # Title
        self.title = title

        # desc
        if tooltip is None:
            self.tooltip = ''
        else:
            self.tooltip = tooltip

        # data
        if content is None:
            self.content = {}
        else:
            self.content = content

        self.initUI()

    def initUI(self):

        # define signals
        self.modifiedSig = NoneSig()

        self.widgets = []

        self.parameters = {}

        for key in self.content.keys():
            self.parameters[key] = self.content[key]['value']
            d = self.content[key]
            w = ElementWidget(**d)
            onchange = self.build_onchange(key)
            w.modifiedSig.sig.connect(onchange)
            w.valueWidget.resize(w.valueWidget.minimumSizeHint())
            w.resize(w.minimumSizeHint())
            self.widgets.append(w)

        self.list = HListWidget(self.title, self.tooltip, self.widgets)
        self.list.setFixedHeight(70)

        # define layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.list)
        hbox.addStretch()
        self.setLayout(hbox)
        self.setContentsMargins(0, 0, 0, 0)

    def _modified(self, label):
        self.labelWidget.setText(label)
        self.label = label
        self._update_label()

    def build_onchange(self, key):

        def onchange(value):
            if not self.parameters[key] == value:
                self.parameters[key] = value
                self.modifiedSig.sig.emit()

        return onchange
