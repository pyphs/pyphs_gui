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

from PyQt5.QtWidgets import (QAction, qApp, QMainWindow)
from PyQt5.QtGui import QIcon

from simulationwidget.base_new import iconspath, SimulationWidget


class Simulation(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.simulation = SimulationWidget()
        if self.simulation._new:
            self.initUI()
        else:
            qApp.quit()

    def initUI(self):

        self.setCentralWidget(self.simulation)

        #############################################################
        #############################################################
        #############################################################

        # Main Actions

        # Exit Action
        exitAction = QAction(QIcon(iconspath + 'exit.png'),
                             '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(qApp.quit)

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

        self.toolbarSimulation = self.addToolBar('Simulation')
        self.toolbarSimulation.addAction(self.simulation.newAction)
        self.toolbarSimulation.addAction(self.simulation.openAction)
        self.toolbarSimulation.addAction(self.simulation.saveAction)
        self.toolbarSimulation.addAction(self.simulation.saveasAction)
        self.toolbarSimulation.addAction(self.simulation.addlineAction)
        self.toolbarSimulation.addAction(self.simulation.editAction)
        self.toolbarSimulation.addAction(self.simulation.plotgraphAction)

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
        fileMenu.addAction(self.simulation.newAction)
        fileMenu.addAction(self.simulation.openAction)
        fileMenu.addAction(self.simulation.saveAction)
        fileMenu.addAction(self.simulation.saveasAction)
        fileMenu.addAction(exitAction)

        # Netlist menu
        netlistMenu = menubar.addMenu('&Line')
        netlistMenu.addAction(self.simulation.addlineAction)
        netlistMenu.addAction(self.simulation.editAction)

        # Plots menu
        plotsMenu = menubar.addMenu('&Plots')
        plotsMenu.addAction(self.simulation.plotgraphAction)

        #############################################################

        self.resize(640, 300)
        self.setWindowTitle('PyPHS Editor')
        self.show()
