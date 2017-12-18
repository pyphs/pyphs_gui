#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 21:45:59 2017

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QFileDialog,
                             QHBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QFont

from pyphs.misc.tools import geteval

from ..misc.signals import NoneSig, BoolSig

from .. import iconspath
from .ioeditdialog import IoDialog


class IoWidget(QWidget):

    _names = 'u', 'y'
    io = {}

    def get_method(self):
        return self.methodWidget.method
    method = property(get_method)

    def __init__(self, methodWidget, parent=None):

        super(IoWidget, self).__init__(parent)

        self.methodWidget = methodWidget

        self.initUI()

    def symb2ref(self, symb):
        symb = self.method.symbols(str(symb))
        for name in self._names:
            symbs = geteval(self.method, name)
            if symb in symbs:
                index = symbs.index(symb)
            return (name, index)

    def ref2symb(self, ref):
        symb = geteval(self.method, ref[0])[ref[1]]
        return symb

    def initUI(self):

        self.modifSig = NoneSig()

        self.methodWidget.statusSig.sig.connect(self._status_changed)
        self._status_changed(True)

        font = QFont()
        font.setBold(True)
        title = QHBoxLayout()

        core_title = QLabel('Inputs/ouputs')
        core_title.setFont(font)

        title.addWidget(core_title)
        title.addStretch()

        self.toolbar = QHBoxLayout()

        # Open Action
        load_icon = QIcon(os.path.join(iconspath, 'open.png'))
        self.loadAction = QAction(load_icon,
                                  '&Load initial values', self)
        self.loadAction.setShortcut('Ctrl+I')
        self.loadAction.setStatusTip('Load initial values')
        self.loadAction.triggered.connect(self._load)
        loadButton = QPushButton(load_icon, '')
        loadButton.setToolTip('Load initial values')
        loadButton.clicked.connect(self._load)
        self.toolbar.addWidget(loadButton)

        # Save Action
        save_icon = QIcon(os.path.join(iconspath, 'save.png'))
        self.saveAction = QAction(save_icon,
                                  '&Save initial values', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save initial values')
        self.saveAction.triggered.connect(self._save)
        saveButton = QPushButton(save_icon, '')
        saveButton.setToolTip('Save the netlist')
        saveButton.clicked.connect(self._save)
        self.toolbar.addWidget(saveButton)

        # Editline Action
        edit_icon = QIcon(os.path.join(iconspath, 'edit.png'))
        self.editAction = QAction(edit_icon,
                                  '&Edit initial values', self)
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit initial values')
        self.editAction.triggered.connect(self._edit)
        editButton = QPushButton(edit_icon, '')
        editButton.setToolTip('Edit initial values')
        editButton.clicked.connect(self._edit)
        self.toolbar.addWidget(editButton)

        title.addLayout(self.toolbar)
        self.setLayout(title)

    def _status_changed(self, s=False):
        if s:
            for name in self._names:
                self.io[name] = [True]*len(geteval(self.method, name))

    def _edit(self):
        if not self.methodWidget.status:
            self.methodWidget._build()
        dialog = IoDialog(self, self)
        res = dialog.getInits(self, self)
        if res[1]:
            self.io = res[0]
            self.modifSig.sig.emit()

    def _load(self):
        if not self.methodWidget.status:
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.methodWidget.folder,
                                self.methodWidget.label + '.io')
        dialog.selectFile(filename)
        fname, _ = dialog.getOpenFileName(self,
                                          'Load initial values',
                                          filename,
                                          "All Files (*);;PyPHS input/output selection (*.io)",
                                          "PyPHS input/output selection (*.io)",
                                          options=options)
        if not fname == '':
            with open(fname, 'r') as f:
                for name in self._names:
                    line = f.readline()
                    # if 1 value or more
                    if len(line) > 0:
                        values = list(map(lambda s: s == 'True', line.split(' ')))
                        if not len(values) == len(geteval(self.method, name)):
                            text = 'Initial values shape error: ' + name
                            raise ValueError(text)
                    else:
                        values = []
                    self.io[name] = values
            self.modifSig.sig.emit()

    def _save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.methodWidget.folder,
                                self.methodWidget.label + '.io')
        dialog.selectFile(filename)
        fname, _ = dialog.getSaveFileName(self,
                                          "Save initial values file as...",
                                          filename,
                                          "All Files (*);;PyPHS input/output selection (*.io)",
                                          "PyPHS input/output selection (*.io)",
                                          options=options)
        if not fname == '':
            if not fname[-3:] == '.io':
                fname += '.io'
            try:
                os.remove(fname)
            except:
                pass
            with open(fname, 'w') as f:
                for name in self._names:
                    line = ' '.join(list(map(str, self.io[name])))+'\n'
                    f.write(line)


###############################################################################
