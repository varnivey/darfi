# -*- coding: utf-8 -*-
import sys,os,functools
sys.path.append('../engine')
import pic_an
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
# FIXME DOES NOT WORK     
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



class SettingsWindow(QtGui.QDialog):
      
    def __init__(self,parent,sensitivity,min_cell_size,peak_min_val_perc,\
        foci_min_val_perc,foci_radius,foci_min_level_on_bg,foci_rescale_min,\
        foci_rescale_max,nuclei_color,foci_color):
        super(SettingsWindow, self).__init__(parent)
        #print DarfiUI.sensitivity
        hbox = QtGui.QHBoxLayout(self)
        
        vbox1Area = QtGui.QWidget(self)
        vbox1 = QtGui.QVBoxLayout(vbox1Area)
        
        self.sensitivity = sensitivity
        sensitivityLabel = QtGui.QLabel(self)
        sensitivityLabel.setText("Sensitivity:")
        self.sensitivityField = QtGui.QDoubleSpinBox()
        self.sensitivityField.setRange(0,10)
        self.sensitivityField.setDecimals(0)
        self.sensitivityField.setValue(self.sensitivity)
        vbox1.addWidget(sensitivityLabel)
        vbox1.addWidget(self.sensitivityField)
        
        self.min_cell_size = min_cell_size
        min_cell_sizeLabel = QtGui.QLabel(self)
        min_cell_sizeLabel.setText("Min cell size:")
        self.min_cell_sizeField = QtGui.QDoubleSpinBox()
        self.min_cell_sizeField.setRange(0,4294967296)
        self.min_cell_sizeField.setDecimals(0)
        self.min_cell_sizeField.setValue(self.min_cell_size)
        vbox1.addWidget(min_cell_sizeLabel)
        vbox1.addWidget(self.min_cell_sizeField)
        
        self.peak_min_val_perc = peak_min_val_perc
        peak_min_val_percLabel = QtGui.QLabel(self)
        peak_min_val_percLabel.setText("Peak min val perc:")
        self.peak_min_val_percField = QtGui.QDoubleSpinBox()
        self.peak_min_val_percField.setRange(0,100)
        self.peak_min_val_percField.setDecimals(2)
        self.peak_min_val_percField.setValue(self.peak_min_val_perc)
        vbox1.addWidget(peak_min_val_percLabel)
        vbox1.addWidget(self.peak_min_val_percField)
        
        self.foci_min_val_perc = foci_min_val_perc
        foci_min_val_percLabel = QtGui.QLabel(self)
        foci_min_val_percLabel.setText("Foci min val perc:")
        self.foci_min_val_percField = QtGui.QDoubleSpinBox()
        self.foci_min_val_percField.setRange(0,100)
        self.foci_min_val_percField.setDecimals(2)
        self.foci_min_val_percField.setValue(self.foci_min_val_perc)
        vbox1.addWidget(foci_min_val_percLabel)
        vbox1.addWidget(self.foci_min_val_percField)
        
        self.foci_radius = foci_radius
        foci_radiusLabel = QtGui.QLabel(self)
        foci_radiusLabel.setText("Foci radius:")
        self.foci_radiusField = QtGui.QDoubleSpinBox()
        self.foci_radiusField.setRange(0,4294967296)
        self.foci_radiusField.setDecimals(0)
        self.foci_radiusField.setValue(self.foci_radius)
        vbox1.addWidget(foci_radiusLabel)
        vbox1.addWidget(self.foci_radiusField)
        
        
        vbox2Area = QtGui.QWidget(self)
        vbox2 = QtGui.QVBoxLayout(vbox2Area)
        self.foci_min_level_on_bg = foci_min_level_on_bg
        foci_min_level_on_bgLabel = QtGui.QLabel(self)
        foci_min_level_on_bgLabel.setText("Foci min level on bg:")
        self.foci_min_level_on_bgField = QtGui.QDoubleSpinBox()
        self.foci_min_level_on_bgField.setRange(0,255)
        self.foci_min_level_on_bgField.setDecimals(0)
        self.foci_min_level_on_bgField.setValue(self.foci_min_level_on_bg)
        vbox2.addWidget(foci_min_level_on_bgLabel)
        vbox2.addWidget(self.foci_min_level_on_bgField)
        
        self.foci_rescale_min = foci_rescale_min
        foci_rescale_minLabel = QtGui.QLabel(self)
        foci_rescale_minLabel.setText("Foci rescale min (-1 for autoscale):")
        self.foci_rescale_minField = QtGui.QDoubleSpinBox()
        self.foci_rescale_minField.setRange(-1,255)
        try:
            self.foci_rescale_minField.setValue(self.foci_rescale_min)
        except TypeError:
            self.foci_rescale_minField.setValue(-1)
        vbox2.addWidget(foci_rescale_minLabel)
        vbox2.addWidget(self.foci_rescale_minField)
        
        self.foci_rescale_max = foci_rescale_max
        foci_rescale_maxLabel = QtGui.QLabel(self)
        foci_rescale_maxLabel.setText("Foci rescale max (-1 for autoscale):")
        self.foci_rescale_maxField = QtGui.QDoubleSpinBox()
        self.foci_rescale_maxField.setRange(-1,255)
        try:
            self.foci_rescale_maxField.setValue(self.foci_rescale_max)
        except TypeError:
            self.foci_rescale_maxField.setValue(-1)
        vbox2.addWidget(foci_rescale_maxLabel)
        vbox2.addWidget(self.foci_rescale_maxField)
        
        self.nuclei_color = nuclei_color
        nuclei_colorLabel = QtGui.QLabel(self)
        nuclei_colorLabel.setText("Nuclei color:")
        self.nuclei_colorField = QtGui.QDoubleSpinBox()
        self.nuclei_colorField.setRange(0,1)
        self.nuclei_colorField.setValue(self.nuclei_color)
        vbox2.addWidget(nuclei_colorLabel)
        vbox2.addWidget(self.nuclei_colorField)
        
        self.foci_color = foci_color
        foci_colorLabel = QtGui.QLabel(self)
        foci_colorLabel.setText("Foci color:")
        self.foci_colorField = QtGui.QDoubleSpinBox()
        self.foci_colorField.setRange(0,1)
        self.foci_colorField.setValue(self.foci_color)
        vbox2.addWidget(foci_colorLabel)
        vbox2.addWidget(self.foci_colorField)
        
        hbox.addWidget(vbox1Area)
        hbox.addWidget(vbox2Area)


    def getSettings(self):
        
        sensitivity = self.sensitivityField.value()
        min_cell_size = self.min_cell_sizeField.value()
        peak_min_val_perc = self.peak_min_val_percField.value()
        foci_min_val_perc = self.foci_min_val_percField.value()
        foci_radius = self.foci_radiusField.value()
        foci_min_level_on_bg = self.foci_min_level_on_bgField.value()
        foci_rescale_min = self.foci_rescale_minField.value()
        foci_rescale_min = None if foci_rescale_min == -1 else foci_rescale_min
        foci_rescale_max = self.foci_rescale_maxField.value()
        foci_rescale_max = None if foci_rescale_max == -1 else foci_rescale_max
        nuclei_color = self.nuclei_colorField.value()
        foci_color = self.foci_colorField.value()
        
        return sensitivity,min_cell_size,peak_min_val_perc,\
        foci_min_val_perc,foci_radius,foci_min_level_on_bg,foci_rescale_min,\
        foci_rescale_max,nuclei_color,foci_color
    
class DarfiUI(QtGui.QWidget):
    
    def __init__(self):
        super(DarfiUI, self).__init__()
        self.workDir=QtCore.QDir.homePath()
        self.nuclei_name = u'3DAPI.TIF'
        self.foci_name = u'3FITС.TIF'
        self.outfile = u'result.txt'
        self.sensitivity = 8.0
        self.min_cell_size = 1500
        self.peak_min_val_perc = 60.
        self.foci_min_val_perc = 90.
        self.foci_radius = 10
        self.foci_min_level_on_bg = 40
        self.foci_rescale_min = None
        self.foci_rescale_max = None
        self.nuclei_color = 0.66
        self.foci_color = 0.33

        self.initUI()
        
    def resizeEvent( self, oldsize):
        ''' override resize event to redraw pictures'''
        self.updateImages()
    
    def openSettings(self):
        self.settings = SettingsWindow(self,self.sensitivity,self.min_cell_size,self.peak_min_val_perc,\
        self.foci_min_val_perc,self.foci_radius,self.foci_min_level_on_bg,self.foci_rescale_min,\
        self.foci_rescale_max,self.nuclei_color,self.foci_color)
        self.settings.exec_()
        self.sensitivity,self.min_cell_size,self.peak_min_val_perc,\
        self.foci_min_val_perc,self.foci_radius,self.foci_min_level_on_bg,self.foci_rescale_min,\
        self.foci_rescale_max,self.nuclei_color,self.foci_color = self.settings.getSettings()
        
    def setNuclei_name(self,text):
        self.nuclei_name = text
        
    def setFoci_name(self,text):
        self.foci_name = text
        
    def setOutfile(self,text):
        self.outfile = text
        

    def selectWorkDir(self):
        self.model.unCheckAll()
        self.workDir=QtGui.QFileDialog.getExistingDirectory()
        self.fileMenu.setRootIndex(self.model.index(self.workDir))
    
    def selectFileName(self):
        self.outfile=QtGui.QFileDialog.getSaveFileName()
        print self.outfile
        
    def updateImages(self):
        try:
            index = self.fileMenu.selectedIndexes()[0]
            path =  self.model.filePath(index)
        #TODO may be we shold avoid using path
            imageDir = QtCore.QDir(path)
            filters = ["*.TIF", "*.tif"]

            imageDir.setNameFilters(filters)
            try:
                imageName1 = imageDir.entryList()[0]

                pix1 = QtGui.QPixmap(path + QtCore.QDir.separator() + imageName1)
                self.lbl1.setPixmap(pix1.scaled(self.lbl1.size(), QtCore.Qt.KeepAspectRatio))
                self.lbl1.update()
            except IndexError:
                self.lbl1.clear()
 
            try:
                imageName2 = imageDir.entryList()[1]
                pix2 = QtGui.QPixmap(path + QtCore.QDir.separator() + imageName2)
                self.lbl2.setPixmap(pix2.scaled(self.lbl2.size(), QtCore.Qt.KeepAspectRatio))
                self.lbl2.update()
            except IndexError:
                self.lbl2.clear()
                
            filters = ["*.jpg", "*.JPG"]
            imageDir.setNameFilters(filters)
            try:
                pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[0])
                self.lbl3.setPixmap(pix.scaled(self.lbl3.size(), QtCore.Qt.KeepAspectRatio))
                self.lbl3.update()
            except IndexError:
                self.lbl3.clear()
            
            try:    
                pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[1])
                self.lbl4.setPixmap(pix.scaled(self.lbl4.size(), QtCore.Qt.KeepAspectRatio))
                self.lbl4.update()
            except IndexError:
                self.lbl4.clear()
            
            try:    
                pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[2])
                self.lbl5.setPixmap(pix.scaled(self.lbl5.size(), QtCore.Qt.KeepAspectRatio))
                self.lbl5.update()
            except IndexError:
                self.lbl5.clear()
            
            try:    
                pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[3])
                self.lbl6.setPixmap(pix.scaled(self.lbl6.size(), QtCore.Qt.KeepAspectRatio))
                self.lbl6.update()
            except IndexError:
                self.lbl6.clear()
        except IndexError:
            ()
        
    def initUI(self):      

################## FILEMENU AREA  ########################################

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
        
################## IMAGE AREA  ########################################

        self.imagePreviewArea = QtGui.QScrollArea(self)
        imagePreviewLayout = QtGui.QGridLayout(self.imagePreviewArea)
            
        self.lbl1 = QtGui.QLabel(self)
        imagePreviewLayout.addWidget(self.lbl1, 0,0)
        self.lbl2 = QtGui.QLabel(self)
        imagePreviewLayout.addWidget(self.lbl2, 0,1)
        self.lbl3 = QtGui.QLabel(self)
        imagePreviewLayout.addWidget(self.lbl3, 1,0)
        self.lbl4 = QtGui.QLabel(self)
        imagePreviewLayout.addWidget(self.lbl4, 1,1)
        self.lbl5 = QtGui.QLabel(self)
        imagePreviewLayout.addWidget(self.lbl5, 2,0)
        self.lbl6 = QtGui.QLabel(self)
        imagePreviewLayout.addWidget(self.lbl6, 2,1)
       
################## SETTINGS AREA  ########################################

        buttonArea = QtGui.QWidget(self)
        buttonLayout = QtGui.QVBoxLayout(buttonArea)
        rescaleButton = QtGui.QPushButton("Get scale from selection")
        
        runCalcButton = QtGui.QPushButton("Calculate")
        runCalcButton.clicked.connect(lambda: self.runCalc())
         
        buttonLayout.addWidget(rescaleButton)
        rescaleButton.clicked.connect(lambda: self.getScale())
        buttonLayout.addWidget(runCalcButton)

        nuclNameFieldLabel = QtGui.QLabel(self)
        nuclNameFieldLabel.setText("Files with nuclei:")
        nuclNameField = QtGui.QLineEdit()
        nuclNameField.setText(self.nuclei_name)
        nuclNameField.textChanged[str].connect(lambda: self.setNuclei_name(nuclNameField.displayText()))
        buttonLayout.addWidget(nuclNameFieldLabel)
        buttonLayout.addWidget(nuclNameField)
        
        fociNameFieldLabel = QtGui.QLabel(self)
        fociNameFieldLabel.setText("Files with foci:")
        fociNameField = QtGui.QLineEdit()
        fociNameField.setText(self.foci_name)
        fociNameField.textChanged[str].connect(lambda: self.setFoci_name(fociNameField.displayText()))
        buttonLayout.addWidget(fociNameFieldLabel)
        buttonLayout.addWidget(fociNameField)
        
        outfileFieldLabel = QtGui.QLabel(self)
        outfileFieldLabel.setText("Outfile name:")
        outfileField = QtGui.QLineEdit()
        outfileField.setText(self.outfile)
        outfileField.textChanged[str].connect(lambda: self.setOutfile(outfileField.displayText()))
        buttonLayout.addWidget(outfileFieldLabel)
        buttonLayout.addWidget(outfileField)
        
        self.saveFile = QtGui.QPushButton("Choose save file")
        self.saveFile.clicked.connect(self.selectFileName)
#        buttonLayout.addWidget(self.saveFile)
        
        self.openSettingsButton = QtGui.QPushButton("Open settings")
        self.openSettingsButton.clicked.connect(self.openSettings)
        buttonLayout.addWidget(self.openSettingsButton)
        self.pbar = QtGui.QProgressBar(self)
        
        self.pbar.hide()
        buttonLayout.addWidget(self.pbar)
        buttonLayout.setAlignment(QtCore.Qt.AlignTop)
        
################## STATUS AREA  ########################################

        self.statusArea = QtGui.QTableWidget(self)
        self.statusArea.setRowCount(2)
        self.statusArea.setColumnCount(7)
        self.statusArea.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Cell number"))
        self.statusArea.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Abs foci number"))
        self.statusArea.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Abs foci area"))
        self.statusArea.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("Abs foci soid"))
        self.statusArea.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("Rel foci number"))
        self.statusArea.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("Rel foci area"))
        self.statusArea.setHorizontalHeaderItem(6, QtGui.QTableWidgetItem("Rel foci soid"))
        self.statusArea.setVerticalHeaderItem(0, QtGui.QTableWidgetItem("Mean"))
        self.statusArea.setVerticalHeaderItem(1, QtGui.QTableWidgetItem("MSE"))
        

################## COMPOSITING  ########################################

        windowInitWidth = 1024
        windowInitHeight = 768
        hbox = QtGui.QHBoxLayout(self)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.imagePreviewArea)
        splitter1.addWidget(buttonArea)
        splitter1.setSizes([windowInitWidth*12/20,windowInitWidth*3/20])

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.statusArea)
        splitter2.setSizes([windowInitHeight*7/8,windowInitHeight/8])
        
        splitter3 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter3.addWidget(fileMenuArea)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([windowInitWidth/4,windowInitWidth*3/4])

        hbox.addWidget(splitter3)
        self.setLayout(hbox)
       
        self.setGeometry(0, 0,windowInitWidth, windowInitHeight)
        self.setWindowTitle('DARFI')
        self.show()



#BRUTEFORCE CODING ^___^ FIXME PLEASE

    def getScale(self):
        dirsWithImages = []
        for index,value in self.model.checks.items():
            if value.toBool():
                dirsWithImages.append(str(self.model.filePath(index)))
        
        dir_path = str(self.workDir)
        dirs_with_images = dirsWithImages
    
        pre_image_dirs = [image_dir for image_dir in dirs_with_images if \
                (os.path.isfile(os.path.join(image_dir,self.nuclei_name)) and os.path.isfile(os.path.join(image_dir, self.foci_name)))]

        image_dirs = [pic_an.image_dir(image_dir, self.nuclei_name, self.foci_name) for image_dir in pre_image_dirs]

        path1,name2 = os.path.split(dir_path)
        name1       = os.path.split(path1)[1]
        #print name1, name2, path1
        name = name1 + '_' + name2
        absoutfile = os.path.join(dir_path,str(self.outfile))
        print absoutfile
        cell_set = pic_an.cell_set(name=name, cells=[])

        remained = len(image_dirs)
        pbarval = 0
        self.pbar.show()
        self.pbar.setValue(pbarval)
        pbarstep = 100 / remained

        print "We have", remained, 'images to load for', name

        print "Image loading have started for", name

        for image_dir in image_dirs:
            image_dir.load_separate_images(self.sensitivity, self.min_cell_size)
            pbarval +=pbarstep
            self.pbar.setValue(pbarval)
            remained -= 1

            if remained == 0:
                print "Image loading have finished for", name
            else:
                print remained, 'images remained to load for', name

            cell_set.extend(image_dir)

        if len(cell_set.cells) == 0:
            print "There are no cells in the images from ", dir_path
            return

        print "We have", len(cell_set.cells), "cells to analyze for", name

        cell_set.rescale_nuclei()
        cell_set.rescale_foci((None, None))
        self.foci_rescale_min, self.foci_rescale_max = cell_set.get_foci_rescale_values()
        print "Foci rescale min max", self.foci_rescale_min, self.foci_rescale_max
        self.pbar.setValue(100)


    def runCalc(self):
        dirsWithImages = []
        for index,value in self.model.checks.items():
            if value.toBool():
                dirsWithImages.append(str(self.model.filePath(index)))
        
        dir_path = str(self.workDir)
        dirs_with_images = dirsWithImages
    
        pre_image_dirs = [image_dir for image_dir in dirs_with_images if \
                (os.path.isfile(os.path.join(image_dir,self.nuclei_name)) and os.path.isfile(os.path.join(image_dir, self.foci_name)))]

        image_dirs = [pic_an.image_dir(image_dir, self.nuclei_name, self.foci_name) for image_dir in pre_image_dirs]

        path1,name2 = os.path.split(dir_path)
        name1       = os.path.split(path1)[1]
        #print name1, name2, path1
        name = name1 + '_' + name2
        absoutfile = os.path.join(dir_path,str(self.outfile))
        print absoutfile
        cell_set = pic_an.cell_set(name=name, cells=[])

        remained = len(image_dirs)
        pbarval = 0
        self.pbar.show()
        self.pbar.setValue(pbarval)
        pbarstep = 100 / remained
        print "We have", remained, 'images to load for', name

        print "Image loading have started for", name

        for image_dir in image_dirs:
            image_dir.load_separate_images(self.sensitivity, self.min_cell_size)
            pbarval +=pbarstep
            self.pbar.setValue(pbarval)
            remained -= 1

            if remained == 0:
                print "Image loading have finished for", name
            else:
                print remained, 'images remained to load for', name

            cell_set.extend(image_dir)

        if len(cell_set.cells) == 0:
            print "There are no cells in the images from ", dir_path
            return

        print "We have", len(cell_set.cells), "cells to analyze for", name

        cell_set.rescale_nuclei()
        cell_set.rescale_foci((self.foci_rescale_min, self.foci_rescale_max))

        cell_set.calculate_foci(self.peak_min_val_perc, self.foci_min_val_perc, self.foci_radius, self.foci_min_level_on_bg)
        cell_set.calculate_foci_parameters()
        cell_set.write_parameters(absoutfile)
        params = cell_set.get_parameters()
        self.statusArea.hide()
        self.statusArea.setItem(0,0,QtGui.QTableWidgetItem(str(params[0])))
        for i in xrange(1,13):
            self.statusArea.setItem((i+1)%2,(i+1)//2,QtGui.QTableWidgetItem(str(params[i])))
        #self.update()
        for image_dir in image_dirs:
            image_dir.write_all_pic_files(self.nuclei_color, self.foci_color)
        self.statusArea.show()
        self.pbar.setValue(100)

        #Engine.calc_foci_in_dirlist(str(self.workDir),dirsWithImages)

               
          

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DarfiUI()
    ex.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
