#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:59:51 2017

@author: afalaize
"""


from PyQt5.QtCore import QObject, pyqtSignal


class NoneSig(QObject):

    sig = pyqtSignal()


class BoolSig(QObject):

    sig = pyqtSignal(bool)


class IntSig(QObject):

    sig = pyqtSignal(int)


class FloatSig(QObject):

    sig = pyqtSignal(float)


class StrSig(QObject):

    sig = pyqtSignal(str)
