#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:32:42 2017

@author: afalaize

Code taken from:
https://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget
"""

import os
import sys

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QLabel, QGridLayout,
                             QComboBox, QLineEdit, QDialogButtonBox,
                             QPushButton, QSpinBox)

from PyQt5 import QtWidgets, QtGui
from pyphs.config import latex_compiler_path
from pyphs.numerics.simulations.simulation import system_call

FSINIT = QtGui.QFont().pointSize()


class LatexWidget(QWidget):

    def __init__(self, latexcode, fs=6):

        QWidget.__init__(self)

        # Fontsize widget
        fontsize = QHBoxLayout()
        fontsize.addWidget(QLabel('Font Size'))

        # Latex widget
        self.latex = LatexLabel(latexcode, FSINIT)

        self.qcb = QComboBox(self)
        self.qcb.addItems(list(map(str, range(1, 11))))
        self.qcb.activated[str].connect(self.onchange_fontsize)
        self.qcb.setCurrentIndex(fs)
        self.onchange_fontsize(self.qcb.itemText(fs))
        fontsize.addWidget(self.qcb)
        fontsize.addStretch()

        # define vbox
        vbox = QVBoxLayout()
        vbox.addLayout(fontsize)
        vbox.addWidget(self.latex)

        # set layout and show
        self.setLayout(vbox)

    def onchange_fontsize(self, fs):
        self.latex.fs = int(fs)
        self.latex.update()

    def update_code(self, latexcode):
        self.latex.code = latexcode
        self.latex.update()


class LatexLabel(QtWidgets.QLabel):
    def __init__(self, latexcode, fontsize, parent=None):
        super(LatexLabel, self).__init__(parent=parent)
        self.code = latexcode
        self.fs = fontsize
        self.update()

    def update(self):
        qpm = laTex_to_QPixmap(self.code, self.fs)
        self.setPixmap(qpm)
        self.resize(qpm.size())


def laTex_to_QPixmap(laTex, fs=5):

    folder = os.getcwd()

    texpath = os.path.join(folder, 'pyphsguitemp.tex')
    dvipath = os.path.join(folder, 'pyphsguitemp.dvi')
    pngpath = os.path.join(folder, 'pyphsguitemp1.png')
    auxpath = os.path.join(folder, 'pyphsguitemp.aux')
    logpath = os.path.join(folder, 'pyphsguitemp.log')

    compilerpath = os.path.join(latex_compiler_path, 'latex')
    dvi2pngpath = os.path.join(latex_compiler_path, 'dvipng')

    if fs >= 10:
        size = r'\Huge'
    elif fs == 9:
        size = r'\huge'
    elif fs == 8:
        size = r'\LARGE'
    elif fs == 7:
        size = r'\Large'
    elif fs == 6:
        size = r'\large'
    elif fs == 5:
        size = r'\normalsize'
    elif fs == 4:
        size = r'\small'
    elif fs == 3:
        size = r'\footnotesize'
    elif fs == 2:
        size = r'\scriptsize'
    else:
        size = r'\tiny'

    content = r"""
\documentclass{standalone}
\begin{document}
""" + size + r"""
""" + laTex + r"""
\end{document}
"""
    with open(texpath, 'w') as f:
        f.write(content)

    exe = ' '.join([compilerpath, texpath])
    system_call(exe)

    exe = ' '.join([dvi2pngpath, '-z 1 -bg Transparent', dvipath])
    system_call(exe)

    qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(pngpath))

    qpixmap = QtGui.QPixmap(qimage)

    for file in [texpath, dvipath, pngpath, auxpath, logpath]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    return qpixmap
