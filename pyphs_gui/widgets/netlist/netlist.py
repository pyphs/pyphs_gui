#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 11:54:56 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sys
import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QApplication, QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView)

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal, QObject

from pyphs import Netlist, Graph, datum
from .editdialog import EditDialog


from .tools import perform_analysis
from ..misc.tools import DescriptionWidget, NoneSig, BoolSig
from .. import iconspath


class NetlistWidget(QWidget):

    def __init__(self, filepath=None, parent=None):

        super(QWidget, self).__init__(parent)

        self.initSig = NoneSig()
        self.statusSig = BoolSig()

        self.initUI()

        if filepath is None:
            self.initMessage()
        else:
            self.path = filepath
            self._read()

    def initUI(self):

        # --------------------

        font = QFont()
        font.setBold(True)

        labelWidget = DescriptionWidget('Netlist',
                                        '',
                                        '')

        desc = 'Key for reference node (e.g. electrical grounds and mechanical \
reference points).'
        datumWidget = DescriptionWidget('datum',
                                        datum,
                                        desc)
        status = QLabel()
        status.setFont(font)

        self.title = QGridLayout()
        self.title.addWidget(labelWidget, 0, 0)
        self.title.addWidget(status, 0, 1)
        self.title.addWidget(datumWidget, 0, 3)

        self.set_status(False)

        # ---------------------------------------------------------------------
        # Create Empty (nlines)x5 Table
        self.table = QTableWidget(self)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnCount(5)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.labels = ('Dictionary', 'Component', 'Label',
                       'Nodes', 'Arguments')

        # Add Header
        horHeaders = []
        for n, key in enumerate(self.labels):
            horHeaders.append(key)
        self.table.setHorizontalHeaderLabels(horHeaders)

        # ---------------------------------------------------------------------
        # Define Netlist Actions

        self.toolbarIO = QHBoxLayout()

        self.toolbarIO.addStretch()

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
        self.toolbarIO.addWidget(newButton)

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
        self.toolbarIO.addWidget(openButton)

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
        self.toolbarIO.addWidget(saveButton)

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
        self.toolbarIO.addWidget(saveasButton)

        self.toolbarIO.addStretch()

        self.toolbarEdit = QHBoxLayout()

        self.toolbarEdit.addStretch()

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
        self.toolbarEdit.addWidget(editButton)

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
        self.toolbarEdit.addWidget(addlineButton)

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
        self.toolbarEdit.addWidget(dellineButton)

        self.toolbarEdit.addSpacing(1)

        # PlotGraph Action
        graph_icon = QIcon(os.path.join(iconspath, 'graph.png'))
        self.plotgraphAction = QAction(graph_icon,
                                       "&Plot system's graph", self)
        self.plotgraphAction.setShortcut('Ctrl+G')
        self.plotgraphAction.setStatusTip("Plot the system's graph")
        self.plotgraphAction.triggered.connect(self._plot_graph)
        plotgraphButton = QPushButton(graph_icon, '')
        plotgraphButton.setToolTip("Plot the system's graph")
        plotgraphButton.clicked.connect(self._plot_graph)
        self.toolbarEdit.addWidget(plotgraphButton)

        # PlotGraph MSA
        self.plotSTAction = QAction(graph_icon,
                                     '&Plot realizability spanning tree', self)
        self.plotSTAction.setShortcut('Ctrl+T')
        self.plotSTAction.setStatusTip('Plot the realizability spanning tree')
        self.plotSTAction.triggered.connect(self._plot_spantree)
        plotSTButton = QPushButton(graph_icon, '')
        plotSTButton.clicked.connect(self._plot_spantree)
        plotSTButton.setToolTip('Plot the realizability spanning tree')
        self.toolbarEdit.addWidget(plotSTButton)

        self.toolbarEdit.addStretch()

        # ---------------------------------------------------------------------
        # set Layout
        vbox = QVBoxLayout()

        tempWidget = QWidget()
        tempWidget.setLayout(self.toolbarIO)
        self.title.addWidget(tempWidget, 0, 2)
        vbox.addLayout(self.title)
        vbox.addLayout(self.toolbarEdit)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def initMessage(self):
        msgBox = QMessageBox()
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

        for label in self.labels:
            data.update({label: list()})

        for netline in self.Netlist:
            for label in self.labels:
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
        self.table.setRowCount(self.Netlist.nlines())
        for n, key in enumerate(self.labels):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.table.setItem(m, n, newitem)
        self.table.setMaximumWidth(500)
#        # Adjust size of Table
#        self.table.resizeColumnsToContents()
#        self.table.resizeRowsToContents()

        self.set_status(False)

        # update Graph
        self._update_graph()

    def set_status(self, s=False):

        if s:
            text = 'Saved'
            color = 'green'

        else:
            text = 'Not Saved'
            color = 'red'
        self.statusSig.sig.emit(s)

        item = self.title.itemAtPosition(0, 1)
        status = item.widget()
        status.setStyleSheet("QLabel { color: %s}" % color)
        status.setText(text)

    def _update_graph(self):
        self.Netlist.graph = self.Netlist.to_graph()

    def _read(self):

        if not os.path.exists(self.path):
            self.Netlist = Netlist(self.path)

        if not hasattr(self, 'Netlist'):
            self.Netlist = Netlist(self.path)

        else:
            self.Netlist.path = self.path
            for n in range(self.Netlist.nlines()):
                self.Netlist.delline(0)
            self.Netlist.read()

        item = self.title.itemAtPosition(0, 0)
        w = item.widget()
        w._update('Netlist',
                  self.Netlist.filename,
                  self.Netlist.path)

        self.update()

        self.set_status(True)

    def _new(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        try:
            filename = os.path.join(self.Netlist.path)
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
            filename = os.path.join(self.Netlist.path)
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
            filename = os.path.join(self.Netlist.path)
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
            self.Netlist.write(fname)
            self.path = fname
            self._read()

    def _save(self):
        self.Netlist.write()
        self.set_status(True)

    def _plot_graph(self):
        self.Netlist.graph.plot()

    def _plot_spantree(self):
        if not hasattr(self.Netlist.graph, 'analysis'):
            self.Netlist.graph._build_analysis()
        perform_analysis(self.Netlist, self)
        self.Netlist.graph.analysis.plot()

    def _new_line(self):
        netline, res = EditDialog.getNetline(self)
        if res:
            self.Netlist.add_line(netline)
            self.update()

    def _del_line(self):
        for i in range(self.table.rowCount()):
            r = range(self.table.columnCount())
            if any([self.table.item(i, j).isSelected() for j in r]):
                break
        self.Netlist.delline(i)
        self.update()

    def _edit_line(self):

        for i in range(self.table.rowCount()):
            r = range(self.table.columnCount())
            if any([self.table.item(i, j).isSelected() for j in r]):
                break
        line = self.Netlist[i]
        e = EditDialog
        netline, res = EditDialog.getNetline(self, line)
        if res:
            self.Netlist.setline(i, netline)
            self.update()

###############################################################################
