import sys,os,functools
sys.path.append('../engine')
import pic_an_dir as Engine
from PyQt4 import QtGui, QtCore



class DarfiUI(QtGui.QWidget):

    
    def __init__(self):
        super(DarfiUI, self).__init__()

        self.initUI()

        
        
    def initUI(self):      
        windowInitWidth = 1024
        windowInitHeight = 768
        hbox = QtGui.QHBoxLayout(self)
        
        self.model = QtGui.QFileSystemModel()
        self.model.removeColumn(0)
        self.model.setRootPath(QtCore.QDir.homePath())
        self.fileMenu = QtGui.QTreeView(self)
        self.fileMenu.setHeaderHidden(1)
        self.fileMenu.setModel(self.model)
        self.fileMenu.hideColumn(1)
        self.fileMenu.hideColumn(2)
        self.fileMenu.hideColumn(3)
        self.fileMenu.setRootIndex(self.model.index(QtCore.QDir.homePath()))
        
 
        imagePreviewArea = QtGui.QFrame(self)
        imagePreviewArea.setFrameShape(QtGui.QFrame.StyledPanel)

        buttonArea = QtGui.QWidget(self)
        buttonLayout = QtGui.QVBoxLayout(buttonArea)
        loadButton = QtGui.QPushButton("Load images")

        
        
        runCalcButton = QtGui.QPushButton("Calculate")
        runCalcButton.clicked.connect(lambda: self.dummyFunction())
        openSettingsButton = QtGui.QPushButton("Open settings")
        buttonLayout.addWidget(loadButton)
        buttonLayout.addWidget(runCalcButton)
        buttonLayout.addWidget(openSettingsButton)
        buttonLayout.setAlignment(QtCore.Qt.AlignTop)
        
        statusArea = QtGui.QFrame(self)
        statusArea.setFrameShape(QtGui.QFrame.StyledPanel)
        

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(imagePreviewArea)
        splitter1.addWidget(buttonArea)
        splitter1.setSizes([windowInitWidth*12/20,windowInitWidth*3/20])

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(statusArea)
        splitter2.setSizes([windowInitHeight*3/4,windowInitHeight/4])
        
        splitter3 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter3.addWidget(self.fileMenu)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([windowInitWidth/4,windowInitWidth*3/4])

        hbox.addWidget(splitter3)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(0, 0,windowInitWidth, windowInitHeight)
        self.setWindowTitle('DARFI')
        self.show()

    def dummyFunction(self):
        #fileInfo = self.model.fileInfo()
        indexItem = self.fileMenu.selectedIndexes()
        fileName = self.model.fileName(indexItem[0])
        filePath = self.model.filePath(indexItem[0])
        Engine.calc_foci_in_dir(str(filePath))
        print filePath
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DarfiUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
