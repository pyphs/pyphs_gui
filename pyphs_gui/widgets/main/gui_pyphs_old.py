#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows
how to use QSplitter widget.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QAction, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QWidget, QGridLayout,
                             QFormLayout)
from PyQt5.QtGui import QIcon

from ..netlist.netlist import NetlistWidget
from ..core.core import CoreWidget
from ..method.method import MethodWidget
from ..graph.graph import GraphWidget
from ..numerics.numerics import NumericWidget
from ..simulation.simulation import SimulationWidget

from .. import iconspath
import os


class MainWidget(QWidget):
    def __init__(self, netpath):
        QWidget.__init__(self)

        hbox = QHBoxLayout()

        vboxL = QGridLayout()
        vboxL.setContentsMargins(*[0]*4)

        # ---------------------------------------------------------------------
        # Netlist

        self.netlist = NetlistWidget(netpath, self)

        vboxL.addWidget(self.netlist.titleWidget.titleWidget,
                        0, 0,
                        1, 1)

        vboxL.addWidget(self.netlist.titleWidget.labelWidget,
                        0, 1,
                        1, 1)

        vboxL.addWidget(self.netlist.titleWidget.statusWidget,
                        0, 2,
                        1, 1)

        vboxL.addWidget(self.netlist.saveButton,
                        0, 3,
                        1, 1)

        vboxL.addWidget(self.netlist.saveasButton,
                        0, 4,
                        1, 1)

        vboxL.addWidget(self.netlist.newButton,
                        0, 5,
                        1, 1)

        vboxL.addWidget(self.netlist.openButton,
                        0, 6,
                        1, 1)

        vboxL.addWidget(self.netlist.datumWidget.label,
                        1, 0,
                        1, 1)

        vboxL.addWidget(self.netlist.datumWidget.desc,
                        1, 1,
                        1, 1)

        vboxL.addWidget(self.netlist.editButton,
                        1, 3,
                        1, 1)

        vboxL.addWidget(self.netlist.addlineButton,
                        1, 4,
                        1, 1)

        vboxL.addWidget(self.netlist.dellineButton,
                        1, 5,
                        1, 1)

        vboxL.addWidget(self.netlist.tableWidget,
                        2, 0,
                        1, 7)

        # ---------------------------------------------------------------------
        # Graph

        self.graph = GraphWidget(self.netlist, self)

        vboxL.addWidget(self.graph.titleWidget.titleWidget,
                        3, 0,
                        1, 1)

        vboxL.addWidget(self.graph.titleWidget.labelWidget,
                        3, 1,
                        1, 1)

        vboxL.addWidget(self.graph.titleWidget.statusWidget,
                        3, 2,
                        1, 1)

        vboxL.addWidget(self.graph.buildButton,
                        3, 3,
                        1, 1)

        vboxL.addWidget(self.graph.plotgraphButton,
                        3, 4,
                        1, 1)

        vboxL.addWidget(self.graph.plotSTButton,
                        3, 5,
                        1, 1)

        vboxL.addWidget(self.graph.nodesWidget.label,
                        4, 0,
                        1, 1)

        vboxL.addWidget(self.graph.nodesWidget.desc,
                        4, 1,
                        1, 1)

        vboxL.addWidget(self.graph.edgesWidget.label,
                        4, 2,
                        1, 1)

        vboxL.addWidget(self.graph.edgesWidget.desc,
                        4, 3,
                        1, 1)


        # ---------------------------------------------------------------------
        # Core

        self.core = CoreWidget(self.graph, self)

        vboxL.addWidget(self.core.titleWidget.titleWidget,
                        5, 0,
                        1, 1)

        vboxL.addWidget(self.core.titleWidget.labelWidget,
                        5, 1,
                        1, 1)

        vboxL.addWidget(self.core.titleWidget.statusWidget,
                        5, 2,
                        1, 1)

        vboxL.addWidget(self.core.buildButton,
                        5, 3,
                        1, 1)

        vboxL.addWidget(self.core.exportButton,
                        5, 4,
                        1, 1)

        vboxL.addWidget(self.core.storageWidget.label,
                        6, 0,
                        1, 1)

        vboxL.addWidget(self.core.storageWidget.desc,
                        6, 1,
                        1, 1)

        vboxL.addWidget(self.core.dissipationWidget.label,
                        6, 2,
                        1, 1)

        vboxL.addWidget(self.core.dissipationWidget.desc,
                        6, 3,
                        1, 1)

        vboxL.addWidget(self.core.sourceWidget.label,
                        6, 4,
                        1, 1)

        vboxL.addWidget(self.core.sourceWidget.desc,
                        6, 5,
                        1, 1)

        vboxL.addWidget(self.core.parametersWidget,
                        7, 0,
                        1, 7)



        vboxR = QFormLayout()
        vboxR.addRow(self.netlist)
#
#        self.method = MethodWidget(self.core, self)
#        vboxR.addWidget(self.method)
#
#        self.numeric = NumericWidget(self.method, self)
#        vboxR.addWidget(self.numeric)
#
#        self.simulation = SimulationWidget(self.numeric, self)
#        vboxR.addWidget(self.simulation)

#        spliter = QSplitter()
#        wL = QWidget()
#        wL.setLayout(vboxL)
#        wR = QWidget()
#        wR.setLayout(vboxL)
#        spliter.addWidget(wL)
#        spliter.addWidget(wR)

        hbox.addLayout(vboxL)
        hbox.addLayout(vboxR)
#        vbox.addWidget(self.core)
#
#        self.method = MethodWidget(self.core, self)
#        vbox.addWidget(self.method)
#
#        self.numeric = NumericWidget(self.method, self)
#        vbox.addWidget(self.numeric)

        self.setLayout(hbox)
        self.resize(self.minimumSizeHint())


class PyphsGui(QMainWindow):

    def __init__(self, netpath=None):

        QMainWindow.__init__(self)

        self.initUI(netpath)

#        if self.netlist._new:
#            self.initUI()
#        else:
#            qApp.quit()
#
    def initUI(self, netpath):

        self.mainWidget = MainWidget(netpath=netpath)

        self.setCentralWidget(self.mainWidget)

        #############################################################
        #############################################################
        #############################################################

        # Define Main Actions

        # Exit Action
        exitAction = QAction(QIcon(os.path.join(iconspath, 'exit.png')),
                             '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(self.destroy)

        # Simulation Action
        simuAction = QAction(QIcon(os.path.join(iconspath,
                                                'simulation.png')),
                             '&Simulation tool', self)
        simuAction.setShortcut('Ctrl+Shift+S')
        simuAction.setStatusTip('Show simulation tool')

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

#        self.toolbar = self.addToolBar('PyPHS GUI')
#        self.toolbar.addAction(self.mainWidget.netlist.newAction)
#        self.toolbar.addAction(self.mainWidget.netlist.openAction)
#        self.toolbar.addAction(self.mainWidget.netlist.saveAction)
#        self.toolbar.addAction(self.mainWidget.netlist.saveasAction)
#        self.toolbar.addAction(self.mainWidget.netlist.addlineAction)
#        self.toolbar.addAction(self.mainWidget.netlist.dellineAction)
#        self.toolbar.addAction(self.mainWidget.netlist.editAction)
#        self.toolbar.addAction(self.mainWidget.graph.plotgraphAction)
#        self.toolbar.addAction(self.mainWidget.graph.plotSTAction)
#        self.toolbar.addAction(simuAction)
#
        #############################################################
        #############################################################
        #############################################################

        # Status Bar

#        self.statusBar()
#
#        #############################################################
#        #############################################################
#        #############################################################
#
#        # MENU BAR
#
#        menubar = self.menuBar()
#
#        #############################################################
#        # Needed on MacOSX only.                                    #
#        # This forces in-window menu instead of standard OSX menu   #
#        menubar.setNativeMenuBar(False)                             #
#        #############################################################
#
#        # PyPHS menu
#        fileMenu = menubar.addMenu('&Netlist')
#        fileMenu.addAction(self.mainWidget.netlist.newAction)
#        fileMenu.addAction(self.mainWidget.netlist.openAction)
#        fileMenu.addAction(self.mainWidget.netlist.saveAction)
#        fileMenu.addAction(self.mainWidget.netlist.saveasAction)
#        fileMenu.addAction(exitAction)
#
#        # Netlist menu
#        netlistMenu = menubar.addMenu('&Line')
#        netlistMenu.addAction(self.mainWidget.netlist.addlineAction)
#        netlistMenu.addAction(self.mainWidget.netlist.dellineAction)
#        netlistMenu.addAction(self.mainWidget.netlist.editAction)
#
#        # Plots menu
#        plotsMenu = menubar.addMenu('&Plots')
#        plotsMenu.addAction(self.mainWidget.graph.plotgraphAction)
#        plotsMenu.addAction(self.mainWidget.graph.plotSTAction)
#
#        simuMenu = menubar.addMenu('&Simulation')
#        simuMenu.addAction(simuAction)

        #############################################################

        self.setWindowTitle('PyPHS')
        self.setWindowIcon(QIcon(os.path.join(iconspath,
                                              'pyphs.png')))
        self.setContentsMargins(0, 0, 0, 0)
        self.show()
