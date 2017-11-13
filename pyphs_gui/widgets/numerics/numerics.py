
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:05:03 2017

@author: afalaize
"""


from __future__ import absolute_import, division, print_function

import sys
import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QApplication, QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox, QLineEdit,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView)
from PyQt5.QtGui import QIcon, QFont
from pyphs import Core, Graph, datum, Method

from pyphs.misc.tools import geteval

from ..misc.tools import DescriptionWidget
from ..misc.latex import LatexLabel

from ..misc.tools import Element, NoneSig, BoolSig

from pyphs import netlist2tex, core2tex, graphplot2tex, texdocument
from pyphs import Core

from .. import iconspath
from .editdialog import InitDialog

from pyphs.misc.juce import fx
from pyphs.misc.faust import write_faust_fx, MethodInvMat

class InitWidget(QWidget):

    statusSig = BoolSig()
    modifSig = NoneSig()

    _status = False
    _label = None
    _names = 'x', 'dx', 'w', 'u', 'p', 'o'
    inits = {}

    def get_method(self):
        return self.methodWidget.method
    method = property(get_method)

    def __init__(self, methodWidget, parent=None):

        super(InitWidget, self).__init__(parent)

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

        self.methodWidget.modifSig.sig.connect(self.init)
        self.init()

        font = QFont()
        font.setBold(True)
        title = QHBoxLayout()

        core_title = QLabel('Initial values')
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

    def init(self):
        for name in self._names:
            self.inits[name] = [0.]*len(geteval(self.method, name))

    def _edit(self):
        if not self.methodWidget.status.text() == 'Build OK':
            self.methodWidget._build()
        dialog = InitDialog(self, self)
        res = dialog.getInits(self, self)
        if res[1]:
            self.inits = res[0]

    def _load(self):
        if not self.methodWidget.status.text() == 'Build OK':
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.methodWidget.folder,
                                self.method.label + '.init')
        dialog.selectFile(filename)
        fname, _ = dialog.getOpenFileName(self,
                                          'Load initial values',
                                          filename,
                                          "All Files (*);;PyPHS initial values (*.init)",
                                          "PyPHS initial values (*.init)",
                                          options=options)
        if not fname == '':
            with open(fname, 'r') as f:
                for name in self._names:
                    line = f.readline()
                    if len(line) > 0:
                        values = list(map(float, line.split(' ')))
                        if not len(values) == len(geteval(self.method, name)):
                            text = 'Initial values shape error: ' + name
                            raise ValueError(text)
                    else:
                        values = []
                    self.inits[name] = values

    def _save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.methodWidget.folder, self.method.label + '.init')
        dialog.selectFile(filename)
        fname, _ = dialog.getSaveFileName(self,
                                          "Save initial values file as...",
                                          filename,
                                          "All Files (*);;PyPHS initial values (*.init)",
                                          "PyPHS initial values (*.init)",
                                          options=options)
        if not fname == '':
            if not fname[-5:] == '.init':
                fname += '.init'
            try:
                os.remove(fname)
            except:
                pass
            with open(fname, 'w') as f:
                for name in self._names:
                    line = ' '.join(list(map(str, self.inits[name])))+'\n'
                    f.write(line)

###############################################################################

class NumericWidget(QWidget):

    _status = False
    _label = None

    config = {'eps': 1e-9,
              'epsdg': 1e-12,
              'fs': 48000.0,
              'maxit': 10}

    def get_method(self):
        return self.methodWidget.method
    method = property(get_method)

    def get_folder(self):
        return self.methodWidget.folder
    folder = property(get_folder)

    def __init__(self, methodWidget, parent=None):

        super(NumericWidget, self).__init__(parent)

        self.methodWidget = methodWidget

        self.initUI()

    def initUI(self):

        self.statusSig = BoolSig()
        self.modifSig = NoneSig()

        vbox = QVBoxLayout()
        font = QFont()
        font.setBold(True)
        title = QHBoxLayout()

        core_title = QLabel('Numeric')
        core_title.setFont(font)

        title.addWidget(core_title)
        title.addStretch()

        # cpp export Action
        cpp_icon = QIcon(os.path.join(iconspath, 'c++.png'))
        self.cppAction = QAction(cpp_icon,
                                    '&Export c++ code', self)
        self.cppAction.setShortcut('Ctrl+L')
        self.cppAction.setStatusTip('Export a bunch of c++ for numerical simulations')
        self.cppAction.triggered.connect(self._writecpp)
        cppbutton = QPushButton(cpp_icon, '')
        cppbutton.setToolTip('Export c++ code')
        cppbutton.clicked.connect(self._writecpp)
        title.addWidget(cppbutton)

        # faust export Action
        faust_icon = QIcon(os.path.join(iconspath, 'faust.png'))
        self.faustAction = QAction(faust_icon,
                                    '&Export FAUST code', self)
        self.faustAction.setShortcut('Ctrl+L')
        self.faustAction.setStatusTip('Export FAUST code')
        self.faustAction.triggered.connect(self._writefaust)
        faustbutton = QPushButton(faust_icon, '')
        faustbutton.setToolTip('Export FAUST code')
        faustbutton.clicked.connect(self._writefaust)
        title.addWidget(faustbutton)

        # juce export Action
        juce_icon = QIcon(os.path.join(iconspath, 'juce.png'))
        self.juceAction = QAction(juce_icon,
                                    '&Export JUCE code', self)
        self.juceAction.setShortcut('Ctrl+L')
        self.juceAction.setStatusTip('Export JUCE code')
        self.juceAction.triggered.connect(self._writejuce)
        jucebutton = QPushButton(juce_icon, '')
        jucebutton.setToolTip('Export JUCE code')
        jucebutton.clicked.connect(self._writejuce)
        title.addWidget(jucebutton)

        vbox.addLayout(title)

        self.inits = InitWidget(self.methodWidget, parent=self)
        vbox.addWidget(self.inits)
        # --------------------

        self.positions = {'fs': (0, 0),
                          'maxit': (0, 1), 'eps': (0, 2),
                          }

        self.content = {'fs': {'desc': 'Sample Rate (Hz)',
                               'label': 'Sample Rate',
                               'value': self.config['fs'],
                               'type': 'float',
                               },

                        'maxit': {'desc': 'Maximum number of implicit iterations.',
                                  'label': 'Iterations',
                                  'value': self.config['maxit'],
                                  'type': 'int',
                                  },
                        'eps': {'desc': 'Numerical tolerance on implicit iterations.',
                                  'label': 'Tolerance',
                                  'value': self.config['eps'],
                                  'type': 'float',
                                  },
                        }

        self.grid = QGridLayout()

        for k in self.content.keys():
            self.grid.addWidget(Element(**self.content[k]), *self.positions[k])

        vbox.addLayout(self.grid)

        self.setLayout(vbox)

    def update_config(self):
        for k in self.content.keys():
            item = self.grid.itemAtPosition(*self.positions[k])
            widget = item.widget()
            self.config[k] = widget.data['value']

    def _writecpp(self):
        if not self.methodWidget.status.text() == 'Build OK':
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.selectFile(self.folder)
        folder = dialog.getExistingDirectory(self,
                                             "Save c++ files in...",
                                             self.folder,
                                             options=options)
        if not folder == '':
            folder = os.path.join(folder, self.method.label + '_Sources')
            self.update_config()
            args = {'objlabel': self.method.label,
                    'path': folder,
                    'inits': self.inits.inits,
                    'config': self.config,
                    'subs': None
                    }
            self.method.to_cpp(**args)

    def _writejuce(self):
        if not self.methodWidget.status.text() == 'Build OK':
            self.methodWidget._build()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.selectFile(self.folder)
        folder = dialog.getExistingDirectory(self,
                                             "Save JUCE snippets files in...",
                                             self.folder,
                                             options=options)
        if not folder == '':
            self.update_config()
            fx.method2jucefx(self.method, path=folder,
                             io=None, inits=self.inits.inits,
                             config=self.config)

    def _writefaust(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        filename = os.path.join(self.folder, self.method.label + '.dsp')
        dialog.selectFile(filename)
        fname, _ = dialog.getSaveFileName(self,
                                          "Save FAUST code as...",
                                          filename,
                                          "All Files (*);;FAUST code (*.dsp)",
                                          "FAUST code (*.dsp)",
                                          options=options)
        if not fname == '':
            if not self.methodWidget.status.text() == 'Build OK':
                self.methodWidget._build()
            if not fname.endswith('.dsp'):
                fname += '.dsp'
            self.update_config()
            print('reduce Z')
            self.method._core.reduce_z()
            print('substitute')
            self.method._core.substitute(selfall=True)
            print('inverse')
            methodIMat = MethodInvMat(self.method._core,
                                      self.methodWidget.config,
                                      self.method.label)
            print('write')
            write_faust_fx(methodIMat, path=fname,
                           inputs=None, outputs=None,
                           inits=self.inits.inits, nIt=self.config['maxit'])

###############################################################################
