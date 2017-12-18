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
                             QFormLayout, QMessageBox, QDialog,
                             QDialogButtonBox, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ..netlist.netlist import NetlistWidget
from ..core.core import CoreWidget
from ..method.method import MethodWidget
from ..graph.graph import GraphWidget
from ..numerics.numerics import NumericWidget
from ..simulation.simulation import SimulationWidget

from .. import iconspath
import os


class Graph(QWidget):
    """
    Widget for netlist edition and graph plot
    """

    def __init__(self, parent=None, netpath=None):
        """
        Widget for netlist line creation and edition.
        if 'netline' is None, a new line is created.
        """
        super(Graph, self).__init__(parent)

        vboxL = QGridLayout()
#        vboxL.setContentsMargins(*[0]*4)
        vboxL.setAlignment(Qt.AlignCenter)

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

        # OK and Cancel buttons
        self.coreButton = QPushButton('Build PHS Core')
        vboxL.addWidget(self.coreButton,
                        5, 0,
                        1, 7)

        self.setLayout(vboxL)
        self.setWindowTitle('PyPHS - Netlist and Graph')

        icon = QIcon(os.path.join(iconspath, 'pyphs.png'))
        self.setWindowIcon(icon)


class Core(QWidget):
    """
    Widget for core and method
    """

    def __init__(self, graph, parent=None):
        """
        Widget for core and method.
        """
        super(Core, self).__init__(parent)

        vboxL = QGridLayout()
#        vboxL.setContentsMargins(*[0]*4)
        vboxL.setAlignment(Qt.AlignCenter)

        # ---------------------------------------------------------------------
        # Core

        self.core = CoreWidget(graph, self)

        line = -1

        line += 1
        vboxL.addWidget(self.core.titleWidget.titleWidget,
                        line, 0,
                        1, 1)

        vboxL.addWidget(self.core.titleWidget.labelWidget,
                        line, 1,
                        1, 2)

        vboxL.addWidget(self.core.titleWidget.statusWidget,
                        line, 3,
                        1, 1)

        vboxL.addWidget(self.core.buildButton,
                        line, 4,
                        1, 1)

        vboxL.addWidget(self.core.exportButton,
                        line, 5,
                        1, 1)

        line += 1
        vboxL.addWidget(self.core.parametersWidget,
                        line, 0,
                        1, 7)

        line += 1
        vboxL.addWidget(self.core.storageWidget.label,
                        line, 0,
                        1, 1)

        vboxL.addWidget(self.core.storageWidget.desc,
                        line, 1,
                        1, 1)

        vboxL.addWidget(self.core.dissipationWidget.label,
                        line, 2,
                        1, 1)

        vboxL.addWidget(self.core.dissipationWidget.desc,
                        line, 3,
                        1, 1)

        vboxL.addWidget(self.core.sourceWidget.label,
                        line, 4,
                        1, 1)

        vboxL.addWidget(self.core.sourceWidget.desc,
                        line, 5,
                        1, 1)

        # ---------------------------------------------------------------------
        # Method

        line += 1
        self.method = MethodWidget(self.core, self)

        vboxL.addWidget(self.method.titleWidget.titleWidget,
                        line, 0,
                        1, 1)

        vboxL.addWidget(self.method.titleWidget.labelWidget,
                        line, 1,
                        1, 2)

        vboxL.addWidget(self.method.titleWidget.statusWidget,
                        line, 3,
                        1, 1)

        vboxL.addWidget(self.method.buildButton,
                        line, 4,
                        1, 1)

        vboxL.addWidget(self.method.exportButton,
                        line, 5,
                        1, 1)

        line += 1
        vboxL.addWidget(self.method.parametersWidget,
                        line, 0,
                        1, 7)

        line += 1
        vboxL.addWidget(self.method.expliciteWidget.label,
                        line, 0,
                        1, 1)

        vboxL.addWidget(self.method.expliciteWidget.desc,
                        line, 1,
                        1, 1)

        vboxL.addWidget(self.method.impliciteWidget.label,
                        line, 2,
                        1, 1)

        vboxL.addWidget(self.method.impliciteWidget.desc,
                        line, 3,
                        1, 1)

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # OK and Cancel buttons
        self.exportButton = QPushButton('Code generation')
        vboxL.addWidget(self.exportButton,
                        6, 0,
                        1, 3)

        self.simuButton = QPushButton('Simulation')
        vboxL.addWidget(self.simuButton,
                        6, 3,
                        1, 3)

        self.setLayout(vboxL)
        self.setWindowTitle('PyPHS - Core PHS and numerical Method')

        icon = QIcon(os.path.join(iconspath, 'pyphs.png'))
        self.setWindowIcon(icon)


class Generation(QWidget):
    """
    Widget for code generation
    """

    def __init__(self, method, parent=None):
        """
        Widget for code generation
        """
        super(Generation, self).__init__(parent)

        vboxL = QGridLayout()
#        vboxL.setContentsMargins(*[0]*4)
        vboxL.setAlignment(Qt.AlignCenter)

        # ---------------------------------------------------------------------
        # Numeric

        self.numeric = NumericWidget(method, self)
        self.numeric.titleWidget.deleteLater()
        self.numeric.titleWidget = None

        line = -1
        line += 1
        vboxL.addWidget(self.numeric.inits,
                        line, 0,
                        1, 6)

        line += 1
        vboxL.addWidget(self.numeric.io,
                        line, 0,
                        1, 6)

        line += 1
        vboxL.addWidget(self.numeric.parametersWidget,
                        line, 0,
                        1, 6)

        line += 1
        self.numeric.cppButton.setText('C++ object')
        vboxL.addWidget(self.numeric.cppButton,
                        line, 0,
                        1, 6)

        line += 1
        self.numeric.juceButton.setText('JUCE FX snippets')
        vboxL.addWidget(self.numeric.juceButton,
                        line, 0,
                        1, 6)

        line += 1
        self.numeric.faustButton.setText('FAUST FX dsp')
        vboxL.addWidget(self.numeric.faustButton,
                        line, 0,
                        1, 6)

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------

        self.setLayout(vboxL)
        self.setWindowTitle('PyPHS - Code Generation')

        icon = QIcon(os.path.join(iconspath, 'pyphs.png'))
        self.setWindowIcon(icon)


class Simulation(QWidget):
    """
    Widget for Simulation
    """

    def __init__(self, method, parent=None):
        """
        Widget for Simulation
        """
        super(Simulation, self).__init__(parent)

        vboxL = QGridLayout()
#        vboxL.setContentsMargins(*[0]*4)
        vboxL.setAlignment(Qt.AlignCenter)

        # ---------------------------------------------------------------------
        # Numeric

        self.numeric = NumericWidget(method, self)

        self.numeric.titleWidget.deleteLater()
        self.numeric.titleWidget = None

        line = -1

        self.simulation = SimulationWidget(self.numeric, self)

        line += 1
        vboxL.addWidget(self.simulation.titleWidget.titleWidget,
                        line, 0,
                        1, 1)

        line += 1
        vboxL.addWidget(self.simulation.statusWidget.titleWidget,
                        line, 0,
                        1, 1)

        vboxL.addWidget(self.simulation.statusWidget.statusWidget,
                        line, 1,
                        1, 1)

        vboxL.addWidget(self.simulation.doneWidget.titleWidget,
                        line, 2,
                        1, 1)

        vboxL.addWidget(self.simulation.doneWidget.statusWidget,
                        line, 3,
                        1, 1)

        line += 1
        vboxL.addWidget(self.simulation.parametersWidget,
                        line, 0,
                        1, 6)

        line += 1
        vboxL.addWidget(self.numeric.parametersWidget,
                        line, 0,
                        1, 6)

        line += 1
        vboxL.addWidget(self.numeric.inits,
                        line, 0,
                        1, 6)

        self.numeric.io.deleteLater()
        self.numeric.io = None

        line += 1
        vboxL.addWidget(self.simulation.signalsWidget,
                        line, 0,
                        1, 6)

        line += 1
        self.simulation.buildButton.setText('Build')
        vboxL.addWidget(self.simulation.buildButton,
                        line, 0,
                        1, 6)

        line += 1
        self.simulation.processButton.setText('Process')
        vboxL.addWidget(self.simulation.processButton,
                        line, 0,
                        1, 6)

        line += 1
        self.simulation.plotButton.setText('Plots')
        vboxL.addWidget(self.simulation.plotButton,
                        line, 0,
                        1, 6)

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------

        self.setLayout(vboxL)
        self.setWindowTitle('PyPHS - Code Generation')

        icon = QIcon(os.path.join(iconspath, 'pyphs.png'))
        self.setWindowIcon(icon)


class MainWidget(QWidget):
    def __init__(self, netpath):

        QWidget.__init__(self)

        self.graphWidget = Graph(netpath=netpath)

        self.graphWidget.coreButton.clicked.connect(self._showCore)

        self.graphWidget.adjustSize()
        self.graphWidget.show()

    def _showCore(self):

        if hasattr(self, 'coreWidget'):
            self.coreWidget.deleteLater()
            self.coreWidget = None
            delattr(self, 'coreWidget')

        self.graphWidget.graph._build()
        self.coreWidget = Core(self.graphWidget.graph)
        self.coreWidget.exportButton.clicked.connect(self._showGeneration)
        self.coreWidget.simuButton.clicked.connect(self._showSimulation)
        self.coreWidget.adjustSize()
        self.coreWidget.show()

    def _showGeneration(self):

        if hasattr(self, 'generationWidget'):
            self.generationWidget.deleteLater()
            self.generationWidget = None
            delattr(self, 'generationWidget')

        if hasattr(self, 'simulationWidget'):
            self.simulationWidget.deleteLater()
            self.simulationWidget = None
            delattr(self, 'simulationWidget')

        self.coreWidget.method._build()
        self.generationWidget = Generation(self.coreWidget.method)
        self.generationWidget.adjustSize()
        self.generationWidget.show()

    def _showSimulation(self):

        if hasattr(self, 'generationWidget'):
            self.generationWidget.deleteLater()
            self.generationWidget = None
            delattr(self, 'generationWidget')

        if hasattr(self, 'simulationWidget'):
            self.simulationWidget.deleteLater()
            self.simulationWidget = None
            delattr(self, 'simulationWidget')

        self.coreWidget.method._build()
        self.simulationWidget = Simulation(self.coreWidget.method)
        self.simulationWidget.adjustSize()
        self.simulationWidget.show()

#        # ---------------------------------------------------------------------
#        # ---------------------------------------------------------------------
#
#        vboxR = QGridLayout()
#        vboxR.setContentsMargins(*[0]*4)
#        vboxR.setAlignment(Qt.AlignCenter)
#
#        # ---------------------------------------------------------------------
#        # Numeric
#
#        self.numeric = NumericWidget(self.method, self)
#
#        vboxR.addWidget(self.numeric.labelWidget,
#                        0, 0,
#                        1, 1)
#
#        vboxR.addWidget(self.numeric.cppButton,
#                        0, 3,
#                        1, 1)
#
#        vboxR.addWidget(self.numeric.juceButton,
#                        0, 4,
#                        1, 1)
#
#        vboxR.addWidget(self.numeric.faustButton,
#                        0, 5,
#                        1, 6)
#
#        vboxR.addWidget(self.numeric.inits,
#                        1, 0,
#                        1, 6)
#
#        vboxR.addWidget(self.numeric.io,
#                        2, 0,
#                        1, 6)
#
#        vboxR.addWidget(self.numeric.parametersWidget,
#                        3, 0,
#                        1, 6)
#
#        # ---------------------------------------------------------------------
#        # Simulation
#
#        self.simulation = SimulationWidget(self.numeric, self)
#
#        vboxR.addWidget(self.simulation.titleWidget.titleWidget,
#                        4, 0,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.buildButton,
#                        4, 3,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.processButton,
#                        4, 4,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.plotButton,
#                        4, 5,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.statusWidget.titleWidget,
#                        5, 0,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.statusWidget.statusWidget,
#                        5, 1,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.doneWidget.titleWidget,
#                        5, 2,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.doneWidget.statusWidget,
#                        5, 3,
#                        1, 1)
#
#        vboxR.addWidget(self.simulation.parametersWidget,
#                        6, 0,
#                        1, 6)
#
#        vboxR.addWidget(self.simulation.signalsWidget,
#                        7, 0,
#                        1, 6)

#        vboxR.addWidget(self.simulation)

#        spliter = QSplitter()
#        wL = QWidget()
#        wL.setLayout(vboxL)
#        wR = QWidget()
#        wR.setLayout(vboxL)
#        spliter.addWidget(wL)
#        spliter.addWidget(wR)

#        hbox.addLayout(vboxL)
#        hbox.addLayout(vboxR)
#        vbox.addWidget(self.core)
#
#        self.method = MethodWidget(self.core, self)
#        vbox.addWidget(self.method)
#
#        self.numeric = NumericWidget(self.method, self)
#        vbox.addWidget(self.numeric)

#        self.setLayout(hbox)


class PyphsGui(QMainWindow):

    def __init__(self, netpath=None):

        QMainWindow.__init__(self)

        self.initUI(netpath)

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
        icon = QIcon(os.path.join(iconspath, 'pyphs.png'))

        self.setWindowIcon(icon)
        self.setContentsMargins(0, 0, 0, 0)
        self.show()
