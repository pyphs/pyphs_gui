#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:59:51 2017

@author: afalaize
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel)
from .fonts import boldFont


# --------------------------------------------------------------------------- #


class DescriptionWidget(QWidget):

    def __init__(self, label, desc, tooltip, parent=None):

        super(DescriptionWidget, self).__init__(parent)

        hbox = QHBoxLayout()

        self.label = QLabel(label[0].upper() + label[1:].lower() + ':')
        self.label.setFont(boldFont)
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
