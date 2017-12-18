PyPHS_GUI
=========

|pypi version| |Licence badge| |python versions| |Website badge|

.. |pypi version| image:: https://badge.fury.io/py/pyphs.svg
    :target: https://badge.fury.io/py/pyphs
.. |Licence badge| image:: https://img.shields.io/badge/licence-CeCILL--B-blue.svg
    :target: http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
.. |python versions| image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6-blue.svg
    :target: https://www.travis-ci.org/pyphs/pyphs
.. |Website badge| image:: https://img.shields.io/badge/documentation-website-blue.svg
    :target: https://pyphs.github.io/pyphs/

A Graphical User Interface for the Python software PyPHS dedicated to the simulation of multi-physical Port-Hamiltonian Systems (PHS) described by graph structures.

Licence
=======
`PyPHS <https://github.com/pyphs/pyphs/>`_ and the present graphical user interface are distributed under the french `CeCILL-B <http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html>`_ licence.

Installation
==============

Python prerequisites
--------------------

The `PyPHS <https://github.com/pyphs/pyphs/>`_ package run on Python 2.7 and Python
3.5 or newer (3.4 is no longer tested), with the following packages installed:

- `pyphs <https://github.com/pyphs/pyphs/>`_
- `PyQt5 <https://riverbankcomputing.com/software/pyqt/intro>`_

Please refer to the `requirements.txt <requirements.txt>`_ file for the required
versions and make sure that these modules are up to date.

C++ prerequisites
------------------

The generated C++ sources build with `CMake <https://cmake.org/>`_ >= 3.1 (see **Configuration** below). The code relies on the `Eigen library <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ (not needed for pure Python usage).

LaTeX prerequisites
-------------------

The PyPHS package can automatically generate a LaTeX documentation file that compiles with the standard TeX distributions.

Install from package
--------------------

The easiest way to install the package is via `pip` from the `PyPI (Python
Package Index) <https://pypi.python.org/pypi>`_::

    pip install pyphs_gui

This includes the latest code and should install all dependencies automatically. If it complains about some missing dependencies, install them the same way with `pip` beforehand.

You might need higher privileges (use su or sudo) to install the package globally. Alternatively you can install the package locally
(i.e. only for you) by adding the `--user` argument::

    pip install --user pyphs

Configuration
--------------

After installation, it is recommended to configure the `config.py <https://github.com/pyphs/pyphs/tree/master/pyphs/config.py>`_ to your needs. Particularly, this is where the local path to the CMake binary.

Your local `config.py <https://github.com/pyphs/pyphs/tree/master/pyphs/config.py>`_ file is located at the root of the `PyPHS <https://github.com/pyphs/pyphs/>`_ package, which can be recovered in a Python interpreter with


.. code:: python

    from pyphs import path_to_configuration_file
    print(path_to_configuration_file)

Documentation
==============

Most of the documentation can be found in the `website <https://pyphs.github.io/pyphs/>`_.

Theoretical overview
--------------------

The development of `PyPHS <https://github.com/pyphs/pyphs/>`_ started as an implementation of the methods proposed in the reference [GraphAnalysis2016], in which the port-Hamiltonian formalism, the graph analysis and the structure preserving numerical method are exposed. This is worth to read before using the package.

Q&A Mailing list
-----------------

The package mailing list is at https://groups.google.com/forum/#!forum/pyphs.

Tutorials and examples
-----------------------

The package comes with a set of tutorials for the use of the main functionalities (`definition <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/core.py>`_, `evaluation <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/evaluation.py>`_, and `simulation <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/simulation.py>`_ of a core PHS structure). More tutorials are to come. Additionally, you can see the `examples <https://github.com/pyphs/pyphs/tree/master/pyphs/examples>`_ scripts. Both the *tutorials* and the *examples* folders are located at your package root, which can be recovered in Python interpreter with

.. code:: python

    from pyphs import path_to_examples, path_to_tutorials
    print(path_to_examples)
    print(path_to_tutorials)

Authors and Affiliations
========================

PyPHS is mainly developed by `Antoine Falaize <https://afalaize.github.io/>`_ and `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`_, respectively in

- the `Team M2N <http://lasie.univ-larochelle.fr/Axe-AB-17>`_ (Mathematical and Numerical Methods), `LaSIE Research Lab <http://lasie.univ-larochelle.fr>`_ (CNRS UMR 7356), hosted by the `University of La Rochelle <http://www.univ-larochelle.fr/>`_,
- the `Team S3AM <http://s3.ircam.fr/?lang=en>`_ (Sound Systems and Signals: Audio/Acoustics, InstruMents) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`_ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`_ in Paris.

See the `AUTHORS <https://github.com/pyphs/pyphs/blob/master/AUTHORS>`_ file for the complete list of authors.

References
==========

.. [NumericalMethod2015] Lopes, N., Hélie, T., & Falaize, A. (2015). Explicit second-order accurate method for the passive guaranteed simulation of port-Hamiltonian systems. IFAC-PapersOnLine, 48(13), 223-228.

.. [GraphAnalysis2016] Falaize, A., & Hélie, T. (2016). Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach. Applied Sciences, 6(10), 273.
