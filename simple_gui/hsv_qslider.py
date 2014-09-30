#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Grigoriy A. Armeev, 2014
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as·
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License v2 for more details.

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        style = """QSlider::groove:horizontal {
border: 1px solid #bbb;
background: qlineargradient(x1: 0, x2: 1,
    stop: 0 red, stop: 0.166666667 #ff0, stop: 0.333333333 #0f0, stop: 0.5 #0ff, stop: 0.666666667 #00f, stop: 0.833333333 #f0f, stop: 1.0 #f00);
height: 15px;

}

QSlider::sub-page:horizontal {
border: 1px solid #777;
height: 10px;
border-radius: 4px;
}

QSlider::add-page:horizontal {
border: 1px solid #777;
height: 10px;
border-radius: 4px;
}

QSlider::handle:horizontal {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #eee, stop:1 #ccc);
border: 1px solid #777;
width: 10px;
margin-left: -5px;
margin-right: -5px;
margin-top: 5px;
margin-bottom: -5px;
border-radius: 2px;
}

QSlider::handle:horizontal:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
border: 1px solid #444;
border-radius: 2px;
}

QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}

QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}

QSlider::handle:horizontal:disabled {
background: #eee;
border: 1px solid #aaa;
border-radius: 4px;
}

"""
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        #sld.setFocusPolicy(QtCore.Qt.NoFocus)
        sld.setGeometry(30, 40, 200, 30)
        sld.setStyleSheet(style)
       

        self.setWindowTitle('QtGui.QSlider')
        self.show()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

