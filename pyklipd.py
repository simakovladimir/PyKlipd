#! /usr/bin/env python

# PyQt-based Clipboard Mananger
# Hooks all global Clipboard/Selection changes
#   taking ownership of current Clipboard/Selection contents
# This allows actual Clipboard/Selection stuff to be available
#   persistently in time (even if source application has been closed)
# Designed to be run as a daemon/service
# License: MIT
# Dedicated to Nothing

# Copyright 2017 Vladimir Simakov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

cbd_data = list()
cbd_formats = list()
cbd = QMimeData()
sel_data = list()
sel_formats = list()
sel = QMimeData()

@pyqtSlot()
def dataChanged():
  if not QApplication.clipboard().ownsClipboard():
    del cbd_data[:]
    del cbd_formats[:]
    cbd = QMimeData()
    for x in QApplication.clipboard().mimeData(QClipboard.Clipboard).formats():
      cbd_data.append(
        QByteArray(QApplication.clipboard().mimeData(QClipboard.Clipboard).data(x)))
      cbd_formats.append(x)
      cbd.setData(cbd_formats[-1], cbd_data[-1])
    QApplication.clipboard().setMimeData(cbd, QClipboard.Clipboard)

@pyqtSlot()
def selectionChanged():
  if not QApplication.clipboard().ownsSelection():
    del sel_data[:]
    del sel_formats[:]
    sel = QMimeData()
    for x in QApplication.clipboard().mimeData(QClipboard.Selection).formats():
      sel_data.append(
        QByteArray(QApplication.clipboard().mimeData(QClipboard.Selection).data(x)))
      sel_formats.append(x)
      sel.setData(sel_formats[-1], sel_data[-1])
    QApplication.clipboard().setMimeData(sel, QClipboard.Selection)

if __name__ == "__main__":
  pid = os.fork()
  if pid == 0:
    while True:
      try:
        app = QApplication(sys.argv)
        QApplication.clipboard().dataChanged.connect(dataChanged)
        QApplication.clipboard().selectionChanged.connect(selectionChanged)
        os._exit(app.exec_())
      except:
        pass
      else:
        break
  else:
    sys.exit(0)
