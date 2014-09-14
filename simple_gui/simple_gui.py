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
        sensitivityField = QtGui.QDoubleSpinBox()
        sensitivityField.setRange(0,10)
        sensitivityField.setDecimals(0)
        sensitivityField.setValue(self.sensitivity)
        vbox1.addWidget(sensitivityLabel)
        vbox1.addWidget(sensitivityField)
        
        self.min_cell_size = min_cell_size
        min_cell_sizeLabel = QtGui.QLabel(self)
        min_cell_sizeLabel.setText("Min cell size:")
        min_cell_sizeField = QtGui.QDoubleSpinBox()
        min_cell_sizeField.setRange(0,4294967296)
        min_cell_sizeField.setDecimals(0)
        min_cell_sizeField.setValue(self.min_cell_size)
        vbox1.addWidget(min_cell_sizeLabel)
        vbox1.addWidget(min_cell_sizeField)
        
        self.peak_min_val_perc = peak_min_val_perc
        peak_min_val_percLabel = QtGui.QLabel(self)
        peak_min_val_percLabel.setText("Peak min val perc:")
        peak_min_val_percField = QtGui.QDoubleSpinBox()
        peak_min_val_percField.setRange(0,100)
        peak_min_val_percField.setDecimals(2)
        peak_min_val_percField.setValue(self.peak_min_val_perc)
        vbox1.addWidget(peak_min_val_percLabel)
        vbox1.addWidget(peak_min_val_percField)
        
        self.foci_min_val_perc = foci_min_val_perc
        foci_min_val_percLabel = QtGui.QLabel(self)
        foci_min_val_percLabel.setText("Foci min val perc:")
        foci_min_val_percField = QtGui.QDoubleSpinBox()
        foci_min_val_percField.setRange(0,100)
        foci_min_val_percField.setDecimals(2)
        foci_min_val_percField.setValue(self.foci_min_val_perc)
        vbox1.addWidget(foci_min_val_percLabel)
        vbox1.addWidget(foci_min_val_percField)
        
        self.foci_radius = foci_radius
        foci_radiusLabel = QtGui.QLabel(self)
        foci_radiusLabel.setText("Foci radius:")
        foci_radiusField = QtGui.QDoubleSpinBox()
        foci_radiusField.setRange(0,4294967296)
        foci_radiusField.setDecimals(0)
        foci_radiusField.setValue(self.foci_radius)
        vbox1.addWidget(foci_radiusLabel)
        vbox1.addWidget(foci_radiusField)
        
        
        vbox2Area = QtGui.QWidget(self)
        vbox2 = QtGui.QVBoxLayout(vbox2Area)
        #foci_min_level_on_bg,foci_rescale_min,foci_rescale_max,nuclei_color,foci_color
        self.foci_min_level_on_bg = foci_min_level_on_bg
        foci_min_level_on_bgLabel = QtGui.QLabel(self)
        foci_min_level_on_bgLabel.setText("Foci min level on bg:")
        foci_min_level_on_bgField = QtGui.QDoubleSpinBox()
        foci_min_level_on_bgField.setRange(0,255)
        foci_min_level_on_bgField.setDecimals(0)
        foci_min_level_on_bgField.setValue(self.foci_min_level_on_bg)
        vbox2.addWidget(foci_min_level_on_bgLabel)
        vbox2.addWidget(foci_min_level_on_bgField)
        
        self.foci_rescale_min = foci_rescale_min
        foci_rescale_minLabel = QtGui.QLabel(self)
        foci_rescale_minLabel.setText("Foci rescale min (-1 for autoscale):")
        foci_rescale_minField = QtGui.QDoubleSpinBox()
        foci_rescale_minField.setRange(-1,255)
        try:
            foci_rescale_minField.setValue(self.foci_rescale_min)
        except TypeError:
            foci_rescale_minField.setValue(-1)
        vbox2.addWidget(foci_rescale_minLabel)
        vbox2.addWidget(foci_rescale_minField)
        
        self.foci_rescale_max = foci_rescale_max
        foci_rescale_maxLabel = QtGui.QLabel(self)
        foci_rescale_maxLabel.setText("Foci rescale max (-1 for autoscale):")
        foci_rescale_maxField = QtGui.QDoubleSpinBox()
        foci_rescale_maxField.setRange(-1,255)
        try:
            foci_rescale_maxField.setValue(self.foci_rescale_max)
        except TypeError:
            foci_rescale_maxField.setValue(-1)
        vbox2.addWidget(foci_rescale_maxLabel)
        vbox2.addWidget(foci_rescale_maxField)
        
        self.nuclei_color = nuclei_color
        nuclei_colorLabel = QtGui.QLabel(self)
        nuclei_colorLabel.setText("Nuclei color:")
        nuclei_colorField = QtGui.QDoubleSpinBox()
        nuclei_colorField.setRange(0,1)
        nuclei_colorField.setValue(self.nuclei_color)
        vbox2.addWidget(nuclei_colorLabel)
        vbox2.addWidget(nuclei_colorField)
        
        self.foci_color = foci_color
        foci_colorLabel = QtGui.QLabel(self)
        foci_colorLabel.setText("Foci color:")
        foci_colorField = QtGui.QDoubleSpinBox()
        foci_colorField.setRange(0,1)
        foci_colorField.setValue(self.foci_color)
        vbox2.addWidget(foci_colorLabel)
        vbox2.addWidget(foci_colorField)
        
        hbox.addWidget(vbox1Area)
        hbox.addWidget(vbox2Area)
    
    
class DarfiUI(QtGui.QWidget):
    
    def __init__(self):
        super(DarfiUI, self).__init__()
        self.workDir=QtCore.QDir.homePath()
        self.nuclei_name = '3DAPI.TIF'
        self.foci_name = '3FITC.TIF'
        self.outfile = 'result.txt'
        self.sensitivity = 8.0
        self.min_cell_size = 1500
        self.peak_min_val_perc = 60
        self.foci_min_val_perc = 90
        self.foci_radius = 10
        self.foci_min_level_on_bg = 40
        self.foci_rescale_min = None
        self.foci_rescale_max = None
        self.nuclei_color = 0.66
        self.foci_color = 0.33
        
        

        self.initUI()
        
    
    def openSettings(self):
        self.settings = SettingsWindow(self,self.sensitivity,self.min_cell_size,self.peak_min_val_perc,\
        self.foci_min_val_perc,self.foci_radius,self.foci_min_level_on_bg,self.foci_rescale_min,\
        self.foci_rescale_max,self.nuclei_color,self.foci_color)
        self.settings.exec_()
        
    def setVar(self,var,text):
        var = text
        print var

    def selectWorkDir(self):
        self.model.unCheckAll()
        self.workDir=QtGui.QFileDialog.getExistingDirectory()
        #print self.workDir
        self.fileMenu.setRootIndex(self.model.index(self.workDir))
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
        nuclNameField.textChanged[str].connect(lambda: self.setVar(self.nuclei_name,nuclNameField.displayText()))
        buttonLayout.addWidget(nuclNameFieldLabel)
        buttonLayout.addWidget(nuclNameField)
        
        
        fociNameFieldLabel = QtGui.QLabel(self)
        fociNameFieldLabel.setText("Files with foci:")
        fociNameField = QtGui.QLineEdit()
        fociNameField.setText(self.foci_name)
        fociNameField.textChanged[str].connect(lambda: self.setVar(self.foci_name,fociNameField.displayText()))

        
        buttonLayout.addWidget(fociNameFieldLabel)
        buttonLayout.addWidget(fociNameField)
        
        self.openSettingsButton = QtGui.QPushButton("Open settings")
        self.openSettingsButton.clicked.connect(self.openSettings)
        buttonLayout.addWidget(self.openSettingsButton)
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

    def getScale(self):
        print 'lol'

    def runCalc(self):
        print "hello"
        dirsWithImages = []
        for index,value in self.model.checks.items():
            if value.toBool():
                dirsWithImages.append(str(self.model.filePath(index)))

        Engine.calc_foci_in_dirlist(str(self.workDir),dirsWithImages)

               
          

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DarfiUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
