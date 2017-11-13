#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 12:03:33 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sys

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QLabel, QGridLayout,
                             QComboBox, QLineEdit, QDialogButtonBox,
                             QScrollArea)

from PyQt5.QtCore import Qt

from pyphs.graphs.netlists import print_netlist_line
import pyphs.dictionary as PHSdictionary
import ast

###############################################################################


class LabelWidget(QLineEdit):
    """
    Widget that display a text line.
    """
    def __init__(self, label=None):
        QLineEdit.__init__(self)
        if label is None:
            label = ""
        self.setText(label)

###############################################################################


class EditDialog(QDialog):
    """
    Widget for netlist line creation and edition.
    """

    def __init__(self, parent=None, netline=None):
        """
        Widget for netlist line creation and edition.
        if 'netline' is None, a new line is created.
        """
        super(EditDialog, self).__init__(parent)

        self.initUI(netline)

    def initUI(self, netline):

        # -------------------------------

        if netline is None:
            netline = {'arguments': None,
                       'component': None,
                       'dictionary': None,
                       'label': None,
                       'nodes': None}
        self.netline = netline

        # -------------------------------

        self.netlistQlabel = QLabel('', self)

        # -------------------------------

        self.titlegrid = QGridLayout()
        self.titlegrid.addWidget(QLabel('Label'), 0, 0)
        self.titlegrid.addWidget(QLabel('Dictionary'), 0, 2)
        self.titlegrid.addWidget(QLabel('Component'), 0, 4)

        # -------------------------------

        self.label = LabelWidget(self.netline['label'])
        self.label.textChanged[str].connect(self.onChanged_label)
        self.titlegrid.addWidget(self.label, 0, 1)

        # -------------------------------

        self.Qdico = QComboBox(self.parent())
        self.Qdico.activated[str].connect(self.onActivated_Qdico)
        self.titlegrid.addWidget(self.Qdico, 0, 3)
        self.Qdico.addItem('Select below...')
        for dico in PHSdictionary.__all__:
            self.Qdico.addItem(dico)

        # -------------------------------

        self.Qcomp = QComboBox(self.parent())
        self.Qcomp.activated[str].connect(self.onActivated_Qcomp)
        self.titlegrid.addWidget(self.Qcomp, 0, 5)
        self.Qcomp.addItem('Select dictionary...')

        # -------------------------------

        self.hnodes = QHBoxLayout()
        self.hnodes.addWidget(QLabel('Nodes'))

        self.nodesgrid = QGridLayout()
        self.nodesgrid.addWidget(QLineEdit(), 0, 0)

        self.hnodes.addLayout(self.nodesgrid)

        self.hnodes.addStretch()


        # -------------------------------

        self.hargs = QHBoxLayout()
        self.hargs.addWidget(QLabel('Parameters'))

        self.argsgrid = QGridLayout()
        self.argsgrid.addWidget(QLineEdit(), 0, 0)

        self.hargs.addLayout(self.argsgrid)

        self.hargs.addStretch()

        # -------------------------------

        index = self.Qdico.findText(self.netline['dictionary'],
                                    Qt.MatchFixedString)
        if index >= 0:
            self.Qdico.setCurrentIndex(index)

        self.init_comp()

        # -------------------------------

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # -------------------------------

        vbox = QVBoxLayout()

        scrollnetlistQlabel = QScrollArea()
        scrollnetlistQlabel.setWidget(self.netlistQlabel)
        scrollnetlistQlabel.setFixedHeight(100)
        scrollnetlistQlabel.setWidgetResizable(True)

        vbox.addWidget(scrollnetlistQlabel)

        vbox.addLayout(self.titlegrid)

        scrollnodes = QScrollArea()
        widgetnodes = QWidget()
        widgetnodes.setLayout(self.hnodes)
        scrollnodes.setWidget(widgetnodes)
        scrollnodes.setFixedHeight(100)
        scrollnodes.setWidgetResizable(True)

        scrollargs = QScrollArea()
        widgetargs = QWidget()
        widgetargs.setLayout(self.hargs)
        scrollargs.setWidget(widgetargs)
        scrollargs.setFixedHeight(100)
        scrollargs.setWidgetResizable(True)

        vbox.addWidget(scrollnodes)
        vbox.addWidget(scrollargs)
        vbox.addStretch(1)
        vbox.addWidget(buttons)
        self.setLayout(vbox)
        self.setWindowTitle('Edit component')

    def onChanged_label(self, text):
        self.netline['label'] = str(text)
        self.update_Qlabel()

    def update_Qlabel(self):
        text = print_netlist_line(self.netline)
        self.netlistQlabel.setText(text)
        self.netlistQlabel.adjustSize()

    ###########################################################################
    def onActivated_Qdico(self, text):
        if str(text) == 'Select below...':

            self.netline.update({'dictionary': None,
                                 'arguments': None,
                                 'component': None,
                                 'nodes': None})
        else:
            self.netline.update({'dictionary': str(text),
                                 'arguments': None,
                                 'component': None,
                                 'nodes': None})
        self.update_Qlabel()
        self.init_comp()

    ###########################################################################

    def get_dico(self):
        if self.netline['dictionary'] is None:
            return None
        else:
            return getattr(PHSdictionary, self.netline['dictionary'])

    def get_comp(self):
        if (self.netline['dictionary'] is None or
                self.netline['component'] is None):
            return None
        else:
            compname = (self.netline['component'][0].upper() +
                        self.netline['component'][1:].lower())
            return getattr(self.get_dico(), compname)

    def init_comp(self):

        while self.Qcomp.itemText(0) != '':
            self.Qcomp.removeItem(0)

        if self.netline['dictionary'] is None:
            self.Qcomp.addItem('Select dictionary...')
            self.netline['component'] = None

        else:
            self.Qcomp.addItem('Select below...')

            dico = self.get_dico()
            for component in dico.__all__:
                self.Qcomp.addItem(component)
            index = self.Qcomp.findText(self.netline['component'],
                                        Qt.MatchFixedString)
            if index >= 0:
                self.Qcomp.setCurrentIndex(index)

        self.init_parameters()

    def onActivated_Qcomp(self, text):
        if str(text) in ['Select dictionary...', 'Select below...']:
            self.netline.update({'component': None,
                                 'arguments': None,
                                 'nodes': None})
        else:
            self.netline.update({'component': str(text).lower(),
                                 'arguments': None,
                                 'nodes': None})
        self.init_parameters()

    ###########################################################################

    def init_parameters(self):

        i = 0
        item = self.nodesgrid.itemAtPosition(0, 0)
        while item is not None:
            w = item.widget()
            self.nodesgrid.removeWidget(w)
            w.deleteLater()
            w = None
            i += 1
            item = self.nodesgrid.itemAtPosition(0, i)

        i = 0
        item = self.argsgrid.itemAtPosition(0, 0)
        while item is not None:
            w = item.widget()
            self.argsgrid.removeWidget(w)
            w.deleteLater()
            w = None
            i += 1
            item = self.argsgrid.itemAtPosition(0, i)

        if (self.netline['dictionary'] is None or
                self.netline['component'] is None):
            self.nodesgrid.addWidget(QLineEdit(), 0, 0)
            self.argsgrid.addWidget(QLineEdit(), 0, 0)
        else:

            comp = self.get_comp()

            if self.netline['nodes'] is None:
                nodes = comp.metadata()['nodes']
                self.netline['nodes'] = nodes
            else:
                nodes = self.netline['nodes']

            for i, node in enumerate(nodes):
                w = self.widget_generator(comp.metadata()['nodes'][i])(self)
                onchange = self.onchange_generator('nodes', i)
                w.qle.textChanged[str].connect(onchange)
                w.qle.setText(node)
                self.nodesgrid.addWidget(w, 0, i)

            if self.netline['arguments'] is None:
                arguments = comp.metadata()['arguments']
                self.netline['arguments'] = arguments
            else:
                arguments = self.netline['arguments']

            for i, arg in enumerate(arguments.keys()):
                label = list(comp.metadata()['arguments'].keys())[i]
                w = self.widget_generator(label)(self)
                onchange = self.onchange_generator('arguments', arg)
                w.qle.textChanged[str].connect(onchange)
                obj = arguments[arg]
                if isinstance(obj, str):
                    w.qle.setText("'%s'" % obj)
                else:
                    w.qle.setText(str(obj))
                self.argsgrid.addWidget(w, 0, i)

        self.update_Qlabel()

    def widget_generator(self, label):
        class MyWidget(QWidget):
            def __init__(self, parent=None):
                super(MyWidget, self).__init__(parent)
                QWidget.__init__(self)
                hbox = QHBoxLayout()
                hbox.addWidget(QLabel(str(label) + ':'))
                self.qle = QLineEdit(self)
                self.qle.setMinimumWidth(100)
                hbox.addWidget(self.qle)
                self.setLayout(hbox)
        return MyWidget

    def onchange_generator(self, target, index):

        def onchange_node(text):
            tup = self.netline['nodes']
            lis = list(tup)
            lis[index] = str(text)
            self.netline['nodes'] = tuple(lis)
            self.update_Qlabel()

        def onchange_arg(text):
            try:
                value = ast.literal_eval(text)
            except (ValueError, SyntaxError):
                value = str(text)
            self.netline['arguments'][index] = value
            self.update_Qlabel()

        if target == 'nodes':
            return onchange_node
        elif target == 'arguments':
            return onchange_arg

    # static method to create the dialog and return (netline, accepted)
    @staticmethod
    def getNetline(parent=None, netline=None):
        dialog = EditDialog(parent, netline)
        result = dialog.exec_()
        netline = dialog.netline
        dialog.deleteLater()
        return (netline, result == QDialog.Accepted)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = EditDialog()
    sys.exit(app.exec_())
