#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 11:54:56 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QHBoxLayout, QPushButton, QGridLayout)

from PyQt5.QtGui import QIcon

from .tools import perform_analysis
from ..misc.tools import DescriptionWidget
from ..misc.signals import NoneSig, BoolSig
from ..misc import TitleWidget
from .. import iconspath

from pyphs import Graph

class GraphWidget(QWidget):

    def get_status(self):
        return self.titleWidget.status
    status = property(get_status)

    def __init__(self, netlistWidget, parent=None):

        super(GraphWidget, self).__init__(parent)

        self.initSig = NoneSig()
        self.statusSig = BoolSig()

        self.netlistWidget = netlistWidget

        self.initUI()

    def initUI(self):

        self.graph = Graph(label=self.label)

        self.dimsLayout = QHBoxLayout()
        self.dimsLayout.setContentsMargins(0, 0, 0, 0)

        self.nodesWidget = DescriptionWidget('Nodes', '0', 'Number of nodes')
        self.edgesWidget = DescriptionWidget('Edges', '0', 'Number of edges')

        self.dimsLayout.addWidget(self.nodesWidget)
        self.dimsLayout.addWidget(self.edgesWidget)
        self.dimsLayout.addStretch()

        self.dimsWidget = QWidget(self)
        self.dimsWidget.setLayout(self.dimsLayout)

        # ---------------------------------------------------------------------
        # Define Graph Actions

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)

        build_icon = QIcon(os.path.join(iconspath, 'work.png'))
        self.buildAction = QAction(build_icon,
                                   "&Build the graph",
                                   self)
        self.buildAction.setShortcut('Ctrl+G')
        self.buildAction.setStatusTip("Build the graph from the netlist and perform realizability analysis")
        self.buildAction.triggered.connect(self._plot_graph)
        self.buildButton = QPushButton(build_icon, '')
        self.buildButton.setToolTip("Build the system's graph")
        self.buildButton.clicked.connect(self._build)
        self.buttonsLayout.addWidget(self.buildButton)

        # PlotGraph Action
        graph_icon = QIcon(os.path.join(iconspath, 'graph.png'))
        self.plotgraphAction = QAction(graph_icon,
                                       "&Plot system's graph", self)
        self.plotgraphAction.setShortcut('Ctrl+G')
        self.plotgraphAction.setStatusTip("Plot the system's graph")
        self.plotgraphAction.triggered.connect(self._plot_graph)
        self.plotgraphButton = QPushButton(graph_icon, '')
        self.plotgraphButton.setToolTip("Plot the system's graph")
        self.plotgraphButton.clicked.connect(self._plot_graph)
        self.buttonsLayout.addWidget(self.plotgraphButton)

        # PlotGraph MSA
        self.plotSTAction = QAction(graph_icon,
                                     '&Plot realizability spanning tree', self)
        self.plotSTAction.setShortcut('Ctrl+T')
        self.plotSTAction.setStatusTip('Plot the realizability spanning tree')
        self.plotSTAction.triggered.connect(self._plot_spantree)
        self.plotSTButton = QPushButton(graph_icon, '')
        self.plotSTButton.clicked.connect(self._plot_spantree)
        self.plotSTButton.setToolTip('Plot the realizability spanning tree')
        self.buttonsLayout.addWidget(self.plotSTButton)

        # ---------------------------------------------------------------------
        # title widget

        title = 'GRAPH'
        self.labelWidget = QLabel()
        status_labels = {True: 'OK',
                         False: 'Not OK'}
        self.titleWidget = TitleWidget(title=title,
                                       labelWidget=self.labelWidget,
                                       status_labels=status_labels,
                                       buttonsLayout=self.buttonsLayout)


        # ---------------------------------------------------------------------
        # signals
        self.netlistWidget.statusSig.sig.connect(self._status_changed)
        self.netlistWidget.initSig.sig.connect(self._netlist_init)

    def get_net(self):
        net = set(self.netlistWidget.netlist.netlist().splitlines())
        return net
    net = property(get_net)

    def get_folder(self):
        return self.netlistWidget.folder
    folder = property(get_folder)

    def get_label(self):
        return self.netlistWidget.label
    label = property(get_label)

    def _update(self):
        self.nodesWidget.desc.setText(str(self.graph.number_of_nodes()))
        self.edgesWidget.desc.setText(str(self.graph.number_of_edges()))

    def _netlist_init(self):
        self.graph.label = self.label
        self.initSig.sig.emit()

    def _status_changed(self, s=False):
        if not s:
            self._change_status(s)

    def _change_status(self, s=False):
            self.titleWidget._change_status(s)
            self.statusSig.sig.emit(s)

    def _build(self):
        if not self.netlistWidget.status:
            self.netlistWidget._save()
        self.graph = self.netlistWidget.netlist.to_graph()
        self.graph._build_analysis()
        res = perform_analysis(self.graph, self)
        self._change_status(res)
        if res:
            self._update()

    def _plot_graph(self):
        if not self.status:
            self._build()
        self.graph.plot()

    def _plot_spantree(self):
        if not self.status:
            self._build()
        self.graph.analysis.plot()

###############################################################################
