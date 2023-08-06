# coding:utf-8

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-03-22 22:55:38"

"""

"""

import os
import sys

repo = (lambda f: lambda p=__file__: f(f, p))(
    lambda f, p: p
    if [
        d
        for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p))
        if d == ".github"
    ]
    else None
    if os.path.dirname(p) == p
    else f(f, os.path.dirname(p))
)()
sys.path.insert(0, repo) if repo not in sys.path else None

from QBinder import Binder
from QBinder import constant
from Qt import QtGui, QtWidgets, QtCore

from functools import partial


class LineEditWidget(QtWidgets.QWidget):

    state = Binder()
    with state("dumper"):
        state.message = "asd"

    def __init__(self):
        super(LineEditWidget, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.edit = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.edit)
        layout.addWidget(self.label)

        self.edit.setText(lambda: self.state.message)
        self.label.setText(lambda: "message is %s" % self.state.message)


def main():
    app = QtWidgets.QApplication([])

    widget = LineEditWidget()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()

# import sys
# MODULE = r"G:\repo\QBinder\example\form"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import lineEditTest
# reload(lineEditTest)
# widget = lineEditTest.WidgetTest()
# widget.show()
