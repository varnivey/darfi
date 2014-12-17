import sys, os
sys.path.append(os.path.join('..','engine'))
import pic_an
from PyQt4 import QtGui,QtCore
'''
This widget implements folders and pictures
'''
class FolderWidget(QtGui.QWidget):
    def __init__(self,parent):
        super(FolderWidget, self).__init__(parent)
        self.parent=parent
        self.selectedImage=""
        self.selectedImageDir=""
        self.workDir=self.parent.workDir
        

       
        self.foldersScrollArea = QtGui.QScrollArea(self)
        self.foldersScrollArea.setWidgetResizable(True)
        
        self.foldersScrollAreaWidget = QtGui.QWidget()
        self.foldersScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 380, 280))
        self.folderLayout = QtGui.QGridLayout(self.foldersScrollAreaWidget)
        self.folderLayout.setAlignment(QtCore.Qt.AlignTop)
        self.foldersScrollArea.setWidget(self.foldersScrollAreaWidget)
        
        self.selectWorkDirButton = QtGui.QPushButton("Select work dir")
        self.connect(self.selectWorkDirButton, QtCore.SIGNAL("clicked()"), self.openWorkDir)

        self.mainLayout = QtGui.QVBoxLayout(self)
        self.mainLayout.addWidget(self.selectWorkDirButton)
        self.mainLayout.addWidget(self.foldersScrollArea)
        
        self.setGeometry(300, 200, 200, 400)

    signal_update_image = QtCore.pyqtSignal()
    signal_update_images = QtCore.pyqtSignal()

    def setWorkDir(self,workDir):
        self.workDir=workDir
    
    def openWorkDir(self,workdir=None):
        if not(workdir):
            workdir=QtGui.QFileDialog.getExistingDirectory(directory=self.workDir)
        if workdir != "":
            self.workDir=unicode(workdir)
            for i in reversed(range(self.folderLayout.count())): 
                self.folderLayout.itemAt(i).widget().setParent(None)
            self.selectedImage=""
            self.selectedImageDir=""
            self.checkedPaths=[]
            
            folderIterator=QtCore.QDirIterator(self.workDir,QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot)
            
            self.checkAllBox = QtGui.QCheckBox('Check/Uncheck All', self)
            self.checkAllBox.setChecked(True)
            self.checkAllBox.stateChanged.connect(lambda:
                (self.checkAll() if self.checkAllBox.isChecked()
                else self.unCheckAll()))
            self.folderLayout.addWidget(self.checkAllBox)
            
            self.folderWidgets=[]
            self.imageDirs=[]
            self.cell_set = pic_an.cell_set(name=self.workDir, cells=[])
            i=0
            while folderIterator.hasNext():
                
                imageQDir=QtCore.QDir(folderIterator.next())
                if not(self.parent.settings.foci_name):
                    self.imageDirs.append(pic_an.image_dir(unicode(imageQDir.absolutePath()),
                                         unicode(self.parent.settings.nuclei_name)))
                else:
                    
                    self.imageDirs.append(pic_an.image_dir(unicode(imageQDir.absolutePath()),
                                         unicode(self.parent.settings.nuclei_name),
                                         unicode(self.parent.settings.foci_name)))
                                         
                self.folderWidgets.append(imageFolderWidget(imageQDir))
                imageList= imageQDir.entryList(["*.TIF", "*.tif", "*.jpg", "*.JPG"])
                
                self.folderLayout.addWidget(self.folderWidgets[-1])
                self.folderWidgets[-1].signal_hideall.connect(self.hideAllImageLabels)
                ##########
                self.folderWidgets[-1].signal_show_image.connect(lambda key=i: self.updateImage(key))
                self.folderWidgets[-1].signal_show_all_images.connect(lambda key=i: self.updateImages(key))
                ############
                i+=1
            try:
                self.updateImages(0)
            except IndexError:
                self.signal_update_images.emit()
            print str(len(self.imageDirs)) + ' dirs found in working directory'
        
    
    def calculateSelected(self):
        self.cell_set = pic_an.cell_set(name=QtCore.QDir(self.workDir).dirName(), cells=[])
        tasksize=len(self.getCheckedPaths())
        self.parent.pbar.show()
        pbarvalue=0
        self.parent.pbar.setValue(pbarvalue)
        pbarstep = (100 - 10 )/ tasksize
# Calculation
        if len(self.folderWidgets) != 0:
            for i in xrange(0,len(self.folderWidgets)):
                if self.folderWidgets[i].checked.checkState() == QtCore.Qt.Checked :
                    #if not(self.parent.settings.foci_name):
                    #    self.imageDirs[i].detect_cells(self.parent.settings.sensitivity, 
                    #                    self.parent.settings.min_cell_size, load_foci=False)
                    #else:
                    self.imageDirs[i].detect_cells(self.parent.settings.sensitivity, 
                                        self.parent.settings.min_cell_size, load_foci=True)
                    self.cell_set.extend(self.imageDirs[i])
                    pbarvalue+=pbarstep
                    self.parent.pbar.setValue(pbarvalue)
            self.cell_set.calculate_foci(self.parent.settings.foci_lookup_sensivity,
                                         self.parent.settings.foci_area_fill_percent,
                                         self.parent.settings.min_foci_radius,
                                         self.parent.settings.max_foci_radius,
                                         self.parent.settings.allowed_foci_overlap,
                                         self.parent.settings.return_circles,
                                         self.parent.settings.normalize_intensity,
                                         (self.parent.settings.foci_rescale_min,
                                          self.parent.settings.foci_rescale_max))
# Retrieving results
            self.cell_set.calculate_foci_parameters()
            try:
                self.params = self.cell_set.get_parameters()
                abspath=os.path.join(self.workDir,unicode(self.parent.outfile))
                self.cell_set.write_parameters(abspath)
            except:
                pass
            
            for i in xrange(0,len(self.folderWidgets)):
                if self.folderWidgets[i].checked.checkState() == QtCore.Qt.Checked :
                    self.imageDirs[i].write_all_pic_files(self.parent.settings.nuclei_color,
                                                          self.parent.settings.foci_color)
                #self.folderWidgets[i]=imageFolderWidget(imageDirPath)
# Table update          
            self.parent.statusArea.hide()
            self.parent.statusArea.setItem(0,0,QtGui.QTableWidgetItem(str(self.params[0])))
            for i in xrange(1,15):
                self.parent.statusArea.setItem((i+1)%2,(i+1)//2,QtGui.QTableWidgetItem(str(self.params[i])))
            self.parent.statusArea.show()            
            self.refreshImages()
            self.updateAllImageLabels()
            self.parent.pbar.setValue(100)

    def getScaleFromSelected(self):
        self.cell_set = pic_an.cell_set(name=self.workDir, cells=[])
        tasksize=len(self.getCheckedPaths())
        self.parent.pbar.show()
        pbarvalue=0
        self.parent.pbar.setValue(pbarvalue)
        pbarstep = (100 - 10 )/ tasksize
        if len(self.folderWidgets) != 0:
            for i in xrange(0,len(self.folderWidgets)):
                if self.folderWidgets[i].checked.checkState() == QtCore.Qt.Checked :
                    #if not(self.parent.settings.foci_name):
                    #    self.imageDirs[i].detect_cells(self.parent.settings.sensitivity, 
                    #                    self.parent.settings.min_cell_size, load_foci=False)
                    #else:
                    self.imageDirs[i].detect_cells(self.parent.settings.sensitivity, 
                                        self.parent.settings.min_cell_size, load_foci=True)
                    self.cell_set.extend(self.imageDirs[i])
                    pbarvalue+=pbarstep
                    self.parent.pbar.setValue(pbarvalue)
            (self.parent.settings.foci_rescale_min,
             self.parent.settings.foci_rescale_max) = self.cell_set.get_foci_rescale_values()
            print 'Foci rescale values changed to:\nmin: ' + str(self.parent.settings.foci_rescale_min) \
                                                + '\nmax: '+ str(self.parent.settings.foci_rescale_max)
            self.parent.pbar.setValue(100)
             
             
    def hideAllImageLabels(self):   
            
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].hideAllImageLabels()
            
    def updateAllImageLabels(self):   
            
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].updateImageLabels()
            
    def checkAll(self):
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].checked.setChecked(True)
        
    def unCheckAll(self):
        for i in xrange(0,len(self.folderWidgets)):
            self.folderWidgets[i].checked.setChecked(False)

    def getCheckedPaths(self):
        paths=[]
        try:
            for i in xrange(0,len(self.folderWidgets)):
                if self.folderWidgets[i].checked.checkState() == QtCore.Qt.Checked :
                    paths.append(unicode(self.folderWidgets[i].dir.absolutePath()))
        except AttributeError:
            ()
        #####
        print "No selected folders" if len(paths) == 0 else str(len(paths))+" folders selected"
        #####
        return paths
    
##################  i think thats OBSOLEETE
    def updateImage(self,key):
        self.selectedImage = self.folderWidgets[key].selectedPic
        self.signal_update_image.emit()
        
    def updateImages(self,key):
        if not(self.folderWidgets[key].selectedPic):
            self.selectedImageDir = self.folderWidgets[key].dir
            self.signal_update_images.emit()
            self.selectedImage =None
        else:
            self.selectedImage = self.folderWidgets[key].selectedPic
            self.signal_update_image.emit()

    def refreshImages(self):
        if not(self.selectedImage):
            self.signal_update_images.emit()
        else:
            
            self.signal_update_image.emit()
    
    def setCheckedFromPaths(self,paths):
        try:
            for i in xrange(0,len(self.folderWidgets)):
                if unicode(self.folderWidgets[i].dir.absolutePath()) in paths:
                    self.folderWidgets[i].checked.setChecked(True)
                else:
                    self.folderWidgets[i].checked.setChecked(False)
        except AttributeError:
            ()
#######################                

            
            
class imageFolderWidget(QtGui.QWidget):

    def __init__(self,inDir):
        super(imageFolderWidget, self).__init__()
        self.isHidden=True
        
        self.dir=inDir
        self.selectedPic=""
        
        self.Layout = QtGui.QGridLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setContentsMargins(0,0,0,0)
        self.Layout.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        self.checked = QtGui.QCheckBox(self)
        self.checked.setTristate(False)
        self.checked.setChecked(True)
        
        self.r_button = QtGui.QPushButton(self.dir.dirName())
        self.r_button.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DirIcon))
        self.r_button.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.r_button.setStyleSheet("text-align: left;padding: 3px")
        self.connect(self.r_button, QtCore.SIGNAL("clicked()"), self.showAllImageLabels)
        
        self.Layout.addWidget(self.checked,0,0)
        self.Layout.addWidget(self.r_button,0,1)

        
        filters = ["*.TIF", "*.tif", "*.jpg", "*.JPG"]
        self.dir.setNameFilters(filters)
        picQFileinfoList= self.dir.entryInfoList(filters,sort= QtCore.QDir.Name|QtCore.QDir.Type)
        self.i=1
        self.dirs=[]
        self.labels=[]
        for picQFileinfo in picQFileinfoList:
            self.i+=1
            tempDir=QtCore.QDir(picQFileinfo.absoluteFilePath())
            self.dirs.append(tempDir)
            
            self.labels.append(ExtendedQLabel(unicode(self.dirs[-1].dirName())))
            self.connect(self.labels[-1], QtCore.SIGNAL("clicked()"),
                         lambda key=self.i-2: self.selectPicture(key))
            self.Layout.addWidget(self.labels[-1],self.i,1)
            self.labels[-1].setAutoFillBackground(True)
            self.labels[-1].setStyleSheet( "background-color: none; qproperty-alignment: AlignCenter;")
            self.labels[-1].setFixedHeight(20)
            self.labels[-1].hide()
    
    def updateImageLabels(self):
        filters = ["*.TIF", "*.tif", "*.jpg", "*.JPG"]
        picQFileinfoList= self.dir.entryInfoList(filters,sort= QtCore.QDir.Name|QtCore.QDir.Type)
        for picQFileinfo in picQFileinfoList:
            
            tempDir=QtCore.QDir(picQFileinfo.absoluteFilePath())
            if not(tempDir in self.dirs):           
                self.i+=1
                self.dirs.append(tempDir)
                
                self.labels.append(ExtendedQLabel(unicode(self.dirs[-1].dirName())))
                self.connect(self.labels[-1], QtCore.SIGNAL("clicked()"),
                             lambda key=self.i-2: self.selectPicture(key))
                self.Layout.addWidget(self.labels[-1],self.i,1)
                self.labels[-1].setAutoFillBackground(True)
                self.labels[-1].setStyleSheet( "background-color: none; qproperty-alignment: AlignCenter;")
                self.labels[-1].setFixedHeight(20)
                self.labels[-1].hide()
        
    signal_hideall = QtCore.pyqtSignal()
    signal_show_image = QtCore.pyqtSignal()
    signal_show_all_images = QtCore.pyqtSignal()        
    
    def hideAllImageLabels(self):
        for i in xrange(0,len(self.labels)):
            self.labels[i].hide()
            self.labels[i].setStyleSheet( "background-color: none; qproperty-alignment: AlignCenter;");
            self.isHidden=True

    def showAllImageLabels(self):
        oldhide=self.isHidden
        self.signal_hideall.emit()
        self.selectedPic=None
        self.signal_show_all_images.emit()
        if oldhide:
            for i in xrange(0,len(self.labels)):
                self.labels[i].show()
            self.isHidden=False
        else:
            self.isHidden=True
    
    def selectPicture(self,item):
        for i in xrange(0,len(self.labels)):
            self.labels[i].setStyleSheet( "background-color: none; qproperty-alignment: AlignCenter;");
        self.labels[item].setStyleSheet( "background-color: palette(highlight); qproperty-alignment: AlignCenter;");
        self.selectedPic=unicode(self.dirs[item].absolutePath())
        self.signal_show_all_images.emit()
        

        
                
            
class ExtendedQLabel(QtGui.QLabel):
 
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))
 
    def wheelEvent(self, ev):
        self.emit(QtCore.SIGNAL('scroll(int)'), ev.delta())

def main():
    
    app = QtGui.QApplication(sys.argv)
    workDir=unicode(QtCore.QDir.currentPath())
    ex = FolderWidget(workDir)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

