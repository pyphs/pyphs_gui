#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 12:03:33 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sys

from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QGridLayout,
                             QDialogButtonBox,
                             QPushButton)
from PyQt5.QtCore import Qt

from pyphs import signalgenerator
from ..misc.element import ElementWidget

# --------------------------------------------------------------------------- #


class SignalEdit(QDialog):

    def __init__(self, label, parent=None, **data):

        super(SignalEdit, self).__init__(parent)

        self.label = label
        self.data = data.copy()

        if (self.data.keys().isdisjoint({'which'}) or
            self.data['which'] is None):
            self.data['which'] = 'zero'

        if (self.data.keys().isdisjoint({'tsig'}) or
            self.data['tsig'] is None):
            self.data['tsig'] = 1.

        if (self.data.keys().isdisjoint({'ncycles'}) or
            self.data['ncycles'] is None):
            self.data['ncycles'] = 1

        if (self.data.keys().isdisjoint({'tdeb'}) or
            self.data['tdeb'] is None):
            self.data['tdeb'] = 0.

        if (self.data.keys().isdisjoint({'tend'}) or
            self.data['tend'] is None):
            self.data['tend'] = 0.

        if (self.data.keys().isdisjoint({'fs'}) or
            self.data['fs'] is None):
            self.data['fs'] = int(1e3)

        if (self.data.keys().isdisjoint({'A'}) or
            self.data['A'] is None):
            self.data['A'] = 1.

        if (self.data.keys().isdisjoint({'A1'}) or
            self.data['A1'] is None):
            self.data['A1'] = 0.

        if (self.data.keys().isdisjoint({'f0'}) or
            self.data['f0'] is None):
            self.data['f0'] = 100.

        if (self.data.keys().isdisjoint({'f1'}) or
            self.data['f1'] is None):
            self.data['f1'] = None

        if (self.data.keys().isdisjoint({'cycle_ratio'}) or
            self.data['cycle_ratio'] is None):
            self.data['cycle_ratio'] = 1.

        if (self.data.keys().isdisjoint({'attack_ratio'}) or
            self.data['attack_ratio'] is None):
            self.data['attack_ratio'] = 0.

        if (self.data.keys().isdisjoint({'decay_ratio'}) or
            self.data['decay_ratio'] is None):
            self.data['decay_ratio'] = 0.

        if (self.data.keys().isdisjoint({'ramp_on'}) or
            self.data['ramp_on'] is None):
            self.data['ramp_on'] = False

        if (self.data.keys().isdisjoint({'bkgrd_noise'}) or
            self.data['bkgrd_noise'] is None):
            self.data['bkgrd_noise'] = 0.

        self.initUI()

    def initUI(self):

        self.positions = {'which': (0, 0),
                          'tsig': (1, 0), 'ncycles': (1, 1),
                          'tdeb': (2, 0), 'tend': (2, 1),
                          'A': (3, 0), 'A1': (3, 1),
                          'f0': (4, 0), 'f1': (4, 1),
                          'cycle_ratio': (5, 0), 'ramp_on': (5, 1),
                          'attack_ratio': (6, 0), 'decay_ratio': (6, 1),
                          'bkgrd_noise': (7, 0),
                          }

        self.content = {'which': {'desc': 'Signal type',
                                  'label': 'Signal type',
                                  'value': self.data['which'],
                                  'type': 'sel',
                                  'choices': ['zero', 'const', 'sin', 'cos',
                                              'noise', 'sweep', 'step']
                                  },
                        'tsig': {'desc': 'Single cycle duration (in seconds)',
                                 'label': 'Cycle duration',
                                 'value': self.data['tsig'],
                                 'type': 'float',
                                 },
                        'ncycles': {'desc': 'Number of cycles',
                                    'label': 'Nb cycles',
                                    'value': self.data['ncycles'],
                                    'type': 'int',
                                    },
                        'tdeb': {'desc': 'Duration of the sequence of 0 generated before the cycles (in seconds).',
                                 'label': 'Zeros start',
                                 'value': self.data['tdeb'],
                                       'type': 'float',
                                        },
                              'tend': {'desc': 'Duration of the sequence of 0 generated after the cycles (in seconds).',
                                       'label': 'Zeros end',
                                       'value': self.data['tend'],
                                       'type': 'float',
                                        },
                              'A': {'desc': 'Amplitude of the principal component.',
                                    'label': 'Amplitude 1',
                                    'value': self.data['A'],
                                    'type': 'float',
                                    },
                              'A1': {'desc': 'Amplitude of a second sin wave (‘sin’ mode only).',
                                     'label': 'Amplitude 2',
                                     'value': self.data['A1'],
                                     'type': 'float',
                                     },
                              'f0': {'desc': 'Frequency of the principal component (Hz).',
                                     'label': 'Frequency 1',
                                     'value': self.data['f0'],
                                     'type': 'float',
                                     },
                              'f1': {'desc': 'Final frequency (‘sweep’ mode) or add a second sin wave (‘sin’ mode).',
                                     'label': 'Frequency 2',
                                     'value': self.data['f1'],
                                     'type': 'float',
                                     },
                              'cycle_ratio': {'desc': 'Final frequency (‘sweep’ mode) or add a second sin wave (‘sin’ mode).',
                                     'label': 'Cycle Ratio',
                                     'value': self.data['cycle_ratio'],
                                     'type': 'float',
                                     },
                              'ramp_on': {'desc': 'Linear increasing of output during all cycles.',
                                     'label': 'Increase',
                                     'value': self.data['ramp_on'],
                                     'type': 'bool',
                                     },
                              'attack_ratio': {'desc': 'Attack envelope ratio w.r.t. Cycle Ratio.',
                                     'label': 'Attack Ratio',
                                     'value': self.data['attack_ratio'],
                                     'type': 'float',
                                     },
                              'decay_ratio': {'desc': 'Decay envelope ratio w.r.t. Cycle Ratio.',
                                     'label': 'Decay Ratio',
                                     'value': self.data['decay_ratio'],
                                     'type': 'float',
                                     },
                              'bkgrd_noise': {'desc': 'Amplitude of an overall background noise from uniform p.d.f.',
                                     'label': 'Noise',
                                     'value': self.data['bkgrd_noise'],
                                     'type': 'float',
                                     },
                          }

        self.grid = QGridLayout()

        for k in self.content.keys():
            self.grid.addWidget(Element(**self.content[k]), *self.positions[k])

        # Edit Widget
        button = QPushButton('plot')
        button.clicked.connect(self.plot)
        self.grid.addWidget(button, 0, 1)

        # OK and Cancel buttons
        hbox_but = QHBoxLayout()
        hbox_but.addStretch()
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        hbox_but.addWidget(buttons)

        # set layout and show
        vbox = QVBoxLayout()
        vbox.addLayout(self.grid)
        vbox.addStretch()
        vbox.addLayout(hbox_but)

        self.setLayout(vbox)
        self.setWindowTitle('Edit Signal {}'.format(self.label))
        self.show()

    def update_data(self):
        for k in self.content.keys():
            item = self.grid.itemAtPosition(*self.positions[k])
            widget = item.widget()
            self.data[k] = widget.data['value']

        time = (self.data['tdeb'] +
                self.data['tsig']*self.data['ncycles'] +
                self.data['tend'])
        self.data['time'] = time

    def plot(self):
        import matplotlib.pyplot as plt
        self.update_data()
        data = self.data.copy()
        data.pop('time')
        sig = list(signalgenerator(**data)())
        nt = len(sig)
        t = [n*self.data['fs']**-1 for n in range(nt)]
        plt.plot(t, sig)
        plt.title(self.label)
        plt.show()

# --------------------------------------------------------------------------- #
