conda_deps='pip libgfortran cython numpy scipy networkx matplotlib nose sympy theano'
conda install $conda_deps
pip_deps='stopit progressbar2 nose nose-exclude codecov coveralls progressbar2 stopit pyphs PyQt5'
pip install $pip_deps
# pip install -e .
