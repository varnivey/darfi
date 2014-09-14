# -*- coding: utf-8 -*-
import sys,os,functools
sys.path.append('../engine')
import pic_an_dir as Engine
from PyQt4 import QtGui, QtCore

        
class CheckableDirModel(QtGui.QDirModel):
    def __init__(self, parent=None):
        QtGui.QDirModel.__init__(self, None)
        self.checks = {}

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.CheckStateRole:
            return QtGui.QDirModel.data(self, index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)

    def flags(self, index):
        return QtGui.QDirModel.flags(self, index) | QtCore.Qt.ItemIsUserCheckable

    def checkState(self, index):
        if index in self.checks:
            return self.checks[index]
        else:
            return QtCore.Qt.Unchecked
#TODO FIXME I'M STUPID =D            
    def checkAll(self):
        print self.rowCount()
        for index in self.checks:
            self.setData(index,QtCore.QVariant(2),QtCore.Qt.CheckStateRole)
            
            
    def unCheckAll(self):
        for index in self.checks:
            self.setData(index,QtCore.QVariant(0),QtCore.Qt.CheckStateRole)
            
    def setData(self, index, value, role):
        if (role == QtCore.Qt.CheckStateRole and index.column() == 0):
            self.layoutAboutToBeChanged.emit()
            self.checks[index] = value
            #self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            self.layoutChanged.emit()
            return True 

        return QtGui.QDirModel.setData(self, index, value, role)

class DarfiUI(QtGui.QWidget):

    
    def __init__(self):
        super(DarfiUI, self).__init__()
        self.workDir=QtCore.QDir.homePath()

        self.initUI()

    def selectWorkDir(self):
        self.model.unCheckAll()
        self.fileMenu.setRootIndex(self.model.index(QtGui.QFileDialog.getExistingDirectory()))
        #self.model.checkAll()

        
    def updateImages(self):
        index = self.fileMenu.selectedIndexes()[0]
        #print QtGui.QDirModel.rowCount(index)
        path =  self.model.filePath(index)
        #QtCore.QStringList(filters)
        filters = ["*.TIF", "*.tif"]
        imageDir = QtCore.QDir(path)
        imageDir.setNameFilters(filters)
        try:
            imageName1 = imageDir.entryList()[0]
            imageName2 = imageDir.entryList()[1]
            pix1 = QtGui.QPixmap(path + "/" + imageName1)
            self.lbl1.setPixmap(pix1.scaledToWidth(300))
            self.lbl1.update()
            pix2 = QtGui.QPixmap(path + "/" + imageName2)
            self.lbl2.setPixmap(pix2.scaledToWidth(300))
            self.lbl2.update()
        except IndexError:
            print "No data image"
        
        #print imageDir.entryList()[0]
        #print imageList[1].absolutePath()

        
    def initUI(self):      
        windowInitWidth = 1024
        windowInitHeight = 768
        hbox = QtGui.QHBoxLayout(self)
        
        
        fileMenuArea = QtGui.QWidget(self)
        self.model = CheckableDirModel()
        self.model.setFilter(QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot)
        self.fileMenu = QtGui.QListView(self)
        self.fileMenu.setModel(self.model)
        self.fileMenu.clicked.connect(lambda: self.updateImages())

        fileMenuLayout = QtGui.QVBoxLayout(fileMenuArea)
        selectFolderButton = QtGui.QPushButton("Select workdir")
        selectFolderButton.clicked.connect(lambda: self.selectWorkDir())
        self.checkAllBox = QtGui.QCheckBox('Check/Uncheck All', self)
        self.checkAllBox.stateChanged.connect(lambda: (self.model.checkAll() if self.checkAllBox.isChecked() else self.model.unCheckAll()))
        fileMenuLayout.addWidget(selectFolderButton)
        fileMenuLayout.addWidget(self.checkAllBox)
        fileMenuLayout.addWidget(self.fileMenu)
        

        imagePreviewArea = QtGui.QWidget(self)
        imagePreviewLayout = QtGui.QHBoxLayout(imagePreviewArea)
        imagePreviewLayout.setAlignment(QtCore.Qt.AlignTop)
        #imagePreviewArea.setFrameShape(QtGui.QFrame.StyledPanel)


        self.lbl1 = QtGui.QLabel(self)
        self.lbl2 = QtGui.QLabel(self)

        imagePreviewLayout.addWidget(self.lbl1)
        imagePreviewLayout.addWidget(self.lbl2)

        buttonArea = QtGui.QWidget(self)
        buttonLayout = QtGui.QVBoxLayout(buttonArea)
        loadButton = QtGui.QPushButton("Load images")

        
        
        runCalcButton = QtGui.QPushButton("Calculate")
        runCalcButton.clicked.connect(lambda: self.dummyFunction())
        
        openSettingsButton = QtGui.QPushButton("Open settings")
        buttonLayout.addWidget(loadButton)
        loadButton.clicked.connect(lambda: self.print_path())
        buttonLayout.addWidget(runCalcButton)
        #buttonLayout.addWidget(openSettingsButton)
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
        splitter3.addWidget(fileMenuArea)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([windowInitWidth/4,windowInitWidth*3/4])

        hbox.addWidget(splitter3)
        self.setLayout(hbox)
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(0, 0,windowInitWidth, windowInitHeight)
        self.setWindowTitle('DARFI')
        self.show()

    def print_path(self):
        print "hello"
        for index,value in self.model.checks.items():
            if value.toBool():
                print self.model.filePath(index)

    def dummyFunction(self):
        #fileInfo = self.model.fileInfo()
        try:
            indexItem = self.fileMenu.selectedIndexes()[0]
            fileName = self.model.fileName(indexItem)
            filePath = self.model.filePath(indexItem)
            Engine.calc_foci_in_dir(str(filePath))
        except IndexError:
            print "select correct folder"
            

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DarfiUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
