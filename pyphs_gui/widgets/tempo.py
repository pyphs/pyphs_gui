#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:58:51 2017

@author: afalaize
"""
    def _plot_graph(self):
        self.Netlist.graph.plot()

    def _plot_spantree(self):
        if not hasattr(self.Netlist.graph, 'analysis'):
            self.Netlist.graph._build_analysis()
        perform_analysis(self.Netlist, self)
        self.Netlist.graph.analysis.plot()


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
