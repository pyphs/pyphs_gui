#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 13:19:18 2017

@author: afalaize
"""
from PyQt5.QtWidgets import (QWidget, QAction, QLabel, QVBoxLayout,
                             QApplication, QFileDialog, QHBoxLayout,
                             QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView)

from pyphs.graphs.exceptions import (CanNotUnlock, EffortCtrlIsFluxCtrl,
                                     FluxCtrlIsEffortCtrl, UndefinedPotential)


def perform_analysis(graph, parent):

    if not hasattr(graph, 'analysis'):
        graph._build_analysis()

    text = ''

    try:
        graph.analysis.perform()

    except UndefinedPotential as error:
        text += 'UndefinedPotential: ' + error.__str__()

    except CanNotUnlock as error:
        text += 'CanNotUnlock: ' + error.__str__()

    except EffortCtrlIsFluxCtrl as error:
        text += 'EffortCtrlIsFluxCtrl: ' + error.__str__()

    except FluxCtrlIsEffortCtrl as error:
        text += 'FluxCtrlIsEffortCtrl: ' + error.__str__()

    except UndefinedPotential as error:
        text += 'UndefinedPotential: ' + error.__str__()

    if len(text) > 0:
        temp = 'Can not complete the realizability analysis of\n'
        temp += 'netlist "{}"\n'.format(graph.label)
        text = temp + text
        QMessageBox.question(parent, 'Realizability issue', text,
                             QMessageBox.Ok, QMessageBox.Ok)
        return False
    else:
        return True
