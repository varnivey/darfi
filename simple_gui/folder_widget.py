import sys
from PyQt4 import QtGui,QtCore
class LayoutTest(QtGui.QWidget):
    def __init__(self):
        super(LayoutTest, self).__init__()
        self.workDir=QtCore.QDir.currentPath()
        self.Layout = QtGui.QVBoxLayout(self)
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 280))
        self.Layout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)
        
        self.Layout_2.addLayout(self.gridLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.selectDirButton = QtGui.QPushButton("Select work dir")
        self.Layout.addWidget(self.selectDirButton)
        self.Layout.addWidget(self.scrollArea)
        self.connect(self.selectDirButton, QtCore.SIGNAL("clicked()"), self.openWorkDir)
        self.setGeometry(300, 200, 200, 400)

    def openWorkDir(self):
        tempDir=QtGui.QFileDialog.getExistingDirectory(directory=self.workDir)
        if tempDir != "":
            #clearing from previous file selection
            for i in reversed(range(self.gridLayout.count())): 
                self.gridLayout.itemAt(i).widget().setParent(None)
            self.workDir=unicode(tempDir)
            self.selectDirButton.setText(unicode(QtCore.QDir(self.workDir).dirName()))
            folderIterator=QtCore.QDirIterator(self.workDir,QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot)
            self.checkAllBox = QtGui.QCheckBox('Check/Uncheck All', self)
            self.checkAllBox.setChecked(True)
            self.checkAllBox.stateChanged.connect(lambda: (self.checkAll() if self.checkAllBox.isChecked() else self.unCheckAll()))
            self.gridLayout.addWidget(self.checkAllBox)
            self.folderWidgets=[]
            while folderIterator.hasNext():
                
                tempDir=QtCore.QDir(folderIterator.next())
                
                self.folderWidgets.append(imageFolderWidget(tempDir))
                self.gridLayout.addWidget(self.folderWidgets[-1])
                self.folderWidgets[-1].signal_hideall.connect(self.hideAllImageLabels)

    def hideAllImageLabels(self):   
            
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].hideAllImageLabels()
            
    def checkAll(self):
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].checked.setChecked(True)
        
    def unCheckAll(self):
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].checked.setChecked(False)
            
            
class imageFolderWidget(QtGui.QWidget):

    def __init__(self,inDir):
        super(imageFolderWidget, self).__init__()
        self.isSelected=QtCore.QVariant(2)
        self.isHidden=True
        self.dir=inDir
        self.Layout = QtGui.QGridLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setContentsMargins(0,0,0,0)
        self.Layout.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        #self.Layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.checked = QtGui.QCheckBox(self)
        self.checked.setTristate(False)
        self.checked.setChecked(True)
        self.r_button = QtGui.QPushButton(self.dir.dirName())
        self.r_button.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DirIcon))
        self.r_button.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Layout.addWidget(self.checked,0,0)
        self.Layout.addWidget(self.r_button,0,1)
    

        self.connect(self.r_button, QtCore.SIGNAL("clicked()"), self.showAllImageLabels)
        filters = ["*.TIF", "*.tif", "*.jpg", "*.JPG"]
        self.dir.setNameFilters(filters)
        pictureIterator=QtCore.QDirIterator(self.dir)
        i=1
        self.dirs=[]
        self.labels=[]
        while pictureIterator.hasNext():
            i+=1
            tempDir=QtCore.QDir(pictureIterator.next())
            
            self.dirs.append(tempDir)
            
            self.labels.append(ExtendedQLabel(unicode(self.dirs[-1].dirName())))
            self.connect(self.labels[-1], QtCore.SIGNAL("clicked()"), lambda key=i-2: self.updateImage(key))
            self.Layout.addWidget(self.labels[-1],i,1)
            #QtGui.QPalette.Highlight
            self.labels[-1].setAutoFillBackground(True)
            
            self.labels[-1].hide()
            print 
        
    signal_hideall = QtCore.pyqtSignal()        
    
    def hideAllImageLabels(self):

        self.isHidden=True
        for i in xrange(0,len(self.labels)):
            self.labels[i].hide()
    def showAllImageLabels(self):
        self.isHidden=False
        self.signal_hideall.emit()
        for i in xrange(0,len(self.labels)):
            self.labels[i].show()
            
    def updateImage(self,numer):
        print unicode(self.dirs[numer].absolutePath())
            
class ExtendedQLabel(QtGui.QLabel):
 
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))
 
    def wheelEvent(self, ev):
        self.emit(QtCore.SIGNAL('scroll(int)'), ev.delta())


def run():

    app = QtGui.QApplication(sys.argv)
    ex = LayoutTest()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
