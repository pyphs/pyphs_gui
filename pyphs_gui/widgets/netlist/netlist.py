#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 11:54:56 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem,
                             QAbstractItemView)

from PyQt5.QtGui import QIcon


from pyphs import Netlist, datum
from .editdialog import EditDialog

from ..misc.tools import DescriptionWidget
from ..misc.signals import NoneSig, BoolSig
from ..misc import TitleWidget
from .. import iconspath


class NetlistWidget(QWidget):

    def get_status(self):
        return self.titleWidget.status
    status = property(get_status)

    def get_label(self):
        fn = self.netlist.filename
        label = fn[:fn.rfind('.')]
        return label
    label = property(get_label)

    def __init__(self, filepath=None, parent=None):

        super(NetlistWidget, self).__init__(parent)

        self.initSig = NoneSig()
        self.statusSig = BoolSig()

        self.initUI()

        if filepath is None:
            self.initMessage()
        else:
            self.path = filepath
            self._read()

    def initUI(self):

        # ---------------------------------------------------------------------
        # Create Empty (nlines)x5 Table
        self.tableWidget = QTableWidget()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableLabels = ('Dictionary', 'Component', 'Label',
                            'Nodes', 'Arguments')

        # Add Header
        horHeaders = []
        for n, key in enumerate(self.tableLabels):
            horHeaders.append(key)
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)

        self.tableWidget.setFixedWidth(520)
        # ---------------------------------------------------------------------
        # Define Netlist File Actions

        buttonsLayout = QHBoxLayout()

        # New Action
        new_icon = QIcon(os.path.join(iconspath, 'new.png'))
        self.newAction = QAction(new_icon,
                                 '&New Netlist', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Create a new netlist')
        self.newAction.triggered.connect(self._new)
        newButton = QPushButton(new_icon, '')
        newButton.setToolTip('Create a new netlist')
        newButton.clicked.connect(self._new)
        buttonsLayout.addWidget(newButton)

        # Open Action
        open_icon = QIcon(os.path.join(iconspath, 'open.png'))
        self.openAction = QAction(open_icon,
                                  '&Open Netlist', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open an existing netlist')
        self.openAction.triggered.connect(self._open)
        openButton = QPushButton(open_icon, '')
        openButton.setToolTip('Open an existing netlist')
        openButton.clicked.connect(self._open)
        buttonsLayout.addWidget(openButton)

        # Save Action
        save_icon = QIcon(os.path.join(iconspath, 'save.png'))
        self.saveAction = QAction(save_icon,
                                  '&Save Netlist', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save the netlist')
        self.saveAction.triggered.connect(self._save)
        saveButton = QPushButton(save_icon, '')
        saveButton.setToolTip('Save the netlist')
        saveButton.clicked.connect(self._save)
        buttonsLayout.addWidget(saveButton)

        # Saveas Action
        saveas_icon = QIcon(os.path.join(iconspath, 'saveas.png'))
        self.saveasAction = QAction(saveas_icon,
                                    '&Save Netlist as', self)
        self.saveasAction.setShortcut('Ctrl+Shift+S')
        self.saveasAction.setStatusTip('Save as a new netlist')
        self.saveasAction.triggered.connect(self._saveas)
        saveasButton = QPushButton(saveas_icon, '')
        saveasButton.setToolTip('Save the netlist as a new netlist')
        saveasButton.clicked.connect(self._saveas)
        buttonsLayout.addWidget(saveasButton)

        # ---------------------------------------------------------------------
        # Define Netlist Line Actions

        actionsLayout = QHBoxLayout()

        # Editline Action
        edit_icon = QIcon(os.path.join(iconspath, 'edit.png'))
        self.editAction = QAction(edit_icon,
                                  '&Edit line', self)
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit an existing line of the netlist')
        self.editAction.triggered.connect(self._edit_line)
        editButton = QPushButton(edit_icon, '')
        editButton.setToolTip('Edit an existing line of the netlist')
        editButton.clicked.connect(self._edit_line)
        actionsLayout.addWidget(editButton)

        # addline Action
        add_icon = QIcon(os.path.join(iconspath, 'add.png'))
        self.addlineAction = QAction(add_icon,
                                     '&New line', self)
        self.addlineAction.setShortcut('Ctrl+L')
        self.addlineAction.setStatusTip('Add a new line to the netlist')
        self.addlineAction.triggered.connect(self._new_line)
        addlineButton = QPushButton(add_icon, '')
        addlineButton.setToolTip('Add a new line to the netlist')
        addlineButton.clicked.connect(self._new_line)
        actionsLayout.addWidget(addlineButton)

        # delline Action
        del_icon = QIcon(os.path.join(iconspath, 'del.png'))
        self.dellineAction = QAction(del_icon,
                                     '&Delete line', self)
        self.dellineAction.setShortcut('Ctrl+L')
        self.dellineAction.setStatusTip('Delete a line from the netlist')
        self.dellineAction.triggered.connect(self._del_line)
        dellineButton = QPushButton(del_icon, '')
        dellineButton.setToolTip('Delete a line from the netlist')
        dellineButton.clicked.connect(self._del_line)
        actionsLayout.addWidget(dellineButton)

        actionsLayout.addStretch()

        # ---------------------------------------------------------------------
        # Datum widget
        desc = 'Key for reference node (e.g. electrical grounds and mechanical reference points).'
        datumWidget = DescriptionWidget('datum',
                                        datum,
                                        desc)
        actionsLayout.addWidget(datumWidget)

        # ---------------------------------------------------------------------
        # title widget

        title = 'NETLIST'
        self.labelWidget = QLabel()
        status_labels = {True: 'Saved',
                         False: 'Not Saved'}
        self.titleWidget = TitleWidget(title=title,
                                       labelWidget=self.labelWidget,
                                       status_labels=status_labels,
                                       buttonsLayout=buttonsLayout)

        self.tableWidget.setMaximumWidth(self.titleWidget.width())

        # ---------------------------------------------------------------------
        # set Layout
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.titleWidget)
        vbox.addLayout(actionsLayout)
        vbox.addWidget(self.tableWidget)
        self.setLayout(vbox)
        self.setFixedWidth(544)

    def initMessage(self):
        msgBox = QMessageBox(self)
        msgBox.setText('Netlist file selection')
        msgBox.addButton(QPushButton('New'), QMessageBox.YesRole)
        msgBox.addButton(QPushButton('Open'), QMessageBox.NoRole)
        init = msgBox.exec_()
        if init == 0:
            self._new()
        else:
            assert init == 1
            self._open()

    def update(self):

        # read data
        data = dict()

        for label in self.tableLabels:
            data.update({label: list()})

        for netline in self.netlist:
            for label in self.tableLabels:
                el = netline[label.lower()]
                if isinstance(el, dict):
                    string = ''
                    for k in el.keys():
                        string += "{0!s}: {1!s}; ".format(k, el[k])
                    string = string[:-1]
                elif isinstance(el, tuple):
                    string = ''
                    for obj in el:
                        string += "{0!s}, ".format(obj)
                    string = string[:-1]
                else:
                    string = str(el)

                data[label].append(string)

        # Enter data onto Table
        self.tableWidget.setRowCount(self.netlist.nlines())
        for n, key in enumerate(self.tableLabels):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.tableWidget.setItem(m, n, newitem)

        self._update_path()
        self._change_status(False)

    def _change_status(self, s=False):
        if not self.status == s:
            self.titleWidget._change_status(s)
            self.statusSig.sig.emit(s)

    def _update_path(self):
        label = self.netlist.filename
        self.titleWidget.labelWidget.setToolTip(self.netlist.path)
        self.titleWidget._change_label(label)

    def _read(self):

        if not os.path.exists(self.path):
            self.netlist = Netlist(self.path)

        if not hasattr(self, 'Netlist'):
            self.netlist = Netlist(self.path)

        else:
            self.netlist.path = self.path
            for n in range(self.netlist.nlines()):
                self.netlist.delline(0)
            self.netlist.read()

        self.update()

        self._change_status(True)
        self.initSig.sig.emit()

    def _new(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        try:
            filename = os.path.join(self.netlist.path)
        except AttributeError:
            filename = os.path.join(os.getcwd(), 'netlist.net')
        dialog.selectFile(filename)
        fname, _ = dialog.getSaveFileName(self,
                                          "Save new netlist file as...",
                                          filename,
                                          "All Files (*);;PyPHS netlist files (*.net)",
                                          "PyPHS netlist files (*.net)",
                                          options=options)
        if not fname == '':
            if not fname[-4:] == '.net':
                fname += '.net'
            self.path = fname
            self._read()

    def _open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        try:
            filename = os.path.join(self.netlist.path)
        except AttributeError:
            filename = os.path.join(os.getcwd(), 'netlist.net')
        dialog.selectFile(filename)
        fname, _ = dialog.getOpenFileName(self,
                                          'Open netlist file',
                                          filename,
                                          "All Files (*);;PyPHS netlist files (*.net)",
                                          "PyPHS netlist files (*.net)",
                                          options=options)
        if not fname == '':
            self.path = fname
            self._read()

    def _saveas(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        try:
            filename = os.path.join(self.netlist.path)
        except AttributeError:
            filename = os.path.join(os.getcwd(), 'netlist.net')
        dialog.selectFile(filename)
        fname, _ = dialog.getSaveFileName(self,
                                          "Save netlist file as...",
                                          filename,
                                          "All Files (*);;PyPHS netlist files (*.net)",
                                          "PyPHS netlist files (*.net)",
                                          options=options)
        if not fname == '':
            if not fname[-4:] == '.net':
                fname += '.net'
            self.netlist.write(fname)
            self.path = fname
            self._read()

    def _save(self):
        self.netlist.write()
        self._change_status(True)

    def _new_line(self):
        netline, res = EditDialog.getNetline(self)
        if res:
            self.netlist.add_line(netline)
            self.update()

    def _del_line(self):
        for i in range(self.tableWidget.rowCount()):
            r = range(self.tableWidget.columnCount())
            if any([self.tableWidget.item(i, j).isSelected() for j in r]):
                break
        self.netlist.delline(i)
        self.update()

    def _edit_line(self):

        for i in range(self.tableWidget.rowCount()):
            r = range(self.tableWidget.columnCount())
            if any([self.tableWidget.item(i, j).isSelected() for j in r]):
                break
        line = self.netlist[i]
        netline, res = EditDialog.getNetline(self, line)
        if res:
            self.netlist.setline(i, netline)
            self.update()

###############################################################################
