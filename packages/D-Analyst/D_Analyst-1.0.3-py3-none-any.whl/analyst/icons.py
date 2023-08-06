import os
from qtop.qtpy import QtCore
from qtop.qtpy import QtGui

__all__ = ['get_icon']

def get_icon(name):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "icons/%s.png" % name)
    icon = QtGui.QIcon(path)
    return icon