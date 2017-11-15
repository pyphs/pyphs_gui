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

from PyQt5.QtWidgets import (QAction, qApp, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QWidget)
from PyQt5.QtGui import QIcon

from ..netlist.netlist import NetlistWidget
from ..core.core import CoreWidget
from ..method.method import MethodWidget
from ..simulation.simulation import SimulationWidget
import os

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


class MainWidget(QWidget):

    def __init__(self, netpath=None, parent=None):

        super(MainWidget, self).__init__(parent)

        self.netlist = NetlistWidget(netpath, parent=self)

        self.initUI()

    def initUI(self):
        try:
            self.core.destroy()
        except AttributeError:
            pass
        try:
            self.method.destroy()
        except AttributeError:
            pass
        try:
            self.simu.destroy()
        except AttributeError:
            pass

        self.core = CoreWidget(self.netlist)

        self.method = MethodWidget(self.core, self.iconspath)

        self.simu = SimulationWidget(self.method,
                                     self.netlist.Netlist.folder)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.netlist)
        hbox1.addWidget(self.core)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.method)
        hbox2.addWidget(self.simu)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)


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
        exitAction = QAction(QIcon(os.path.join(self.iconspath, 'exit.png')),
                             '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(self.destroy)

        # Simulation Action
        simuAction = QAction(QIcon(os.path.join(self.iconspath,
                                                'simulation.png')),
                             '&Simulation tool', self)
        simuAction.setShortcut('Ctrl+Shift+S')
        simuAction.setStatusTip('Show simulation tool')
        simuAction.triggered.connect(self.mainWidget.simu._build)

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

        self.toolbar = self.addToolBar('Netlist')
        self.toolbar.addAction(self.mainWidget.netlist.newAction)
        self.toolbar.addAction(self.mainWidget.netlist.openAction)
        self.toolbar.addAction(self.mainWidget.netlist.saveAction)
        self.toolbar.addAction(self.mainWidget.netlist.saveasAction)
        self.toolbar.addAction(self.mainWidget.netlist.addlineAction)
        self.toolbar.addAction(self.mainWidget.netlist.dellineAction)
        self.toolbar.addAction(self.mainWidget.netlist.editAction)
        self.toolbar.addAction(self.mainWidget.netlist.plotgraphAction)
        self.toolbar.addAction(self.mainWidget.netlist.plotMSAAction)
        self.toolbar.addAction(simuAction)

        #############################################################
        #############################################################
        #############################################################

        # Status Bar

        self.statusBar()

        #############################################################
        #############################################################
        #############################################################

        # MENU BAR

        menubar = self.menuBar()

        #############################################################
        # Needed on MacOSX only.                                    #
        # This forces in-window menu instead of standard OSX menu   #
        menubar.setNativeMenuBar(False)                             #
        #############################################################

        # PyPHS menu
        fileMenu = menubar.addMenu('&Netlist')
        fileMenu.addAction(self.mainWidget.netlist.newAction)
        fileMenu.addAction(self.mainWidget.netlist.openAction)
        fileMenu.addAction(self.mainWidget.netlist.saveAction)
        fileMenu.addAction(self.mainWidget.netlist.saveasAction)
        fileMenu.addAction(exitAction)

        # Netlist menu
        netlistMenu = menubar.addMenu('&Line')
        netlistMenu.addAction(self.mainWidget.netlist.addlineAction)
        netlistMenu.addAction(self.mainWidget.netlist.dellineAction)
        netlistMenu.addAction(self.mainWidget.netlist.editAction)

        # Plots menu
        plotsMenu = menubar.addMenu('&Plots')
        plotsMenu.addAction(self.mainWidget.netlist.plotgraphAction)
        plotsMenu.addAction(self.mainWidget.netlist.plotMSAAction)

        simuMenu = menubar.addMenu('&Simulation')
        simuMenu.addAction(simuAction)

        #############################################################

        self.setWindowTitle('PyPHS GUI')
        self.setWindowIcon(QIcon(os.path.join(self.iconspath,
                                              'pyphs.png')))
        self.show()

        #############################################################

        self.mainWidget.netlist.modifSig.signal.connect(self.modified_netlist)
        self.mainWidget.netlist.initSig.signal.connect(self.modified_netlist)
        self.mainWidget.method.buildSig.signal.connect(self.update_core)
        self.mainWidget.method.simuSig.signal.connect(self.update_signals)
        self.mainWidget.simu.buildSig.signal.connect(self.update_method)

    def update_core(self):
        if not self.mainWidget.core.status.text() == 'Build OK':
            self.mainWidget.core._build()
        self.mainWidget.method.update_core(self.mainWidget.core._core)

    def update_method(self):
        if ((not self.mainWidget.method.status.text() == 'Build OK') or
            self.mainWidget.simu.method is None):
            self.mainWidget.method._build()

    def update_signals(self):
        if not hasattr(self.mainWidget.simu, 'signals'):
            self.mainWidget.simu.update_method(self.mainWidget.method._method)
            self.mainWidget.simu.init_signals()

    def modified_netlist(self):
        self.mainWidget.core.set_net()
        self.mainWidget.method.set_status(False)
