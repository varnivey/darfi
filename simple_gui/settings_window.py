from PyQt4 import QtGui, QtCore
import hsv_qslider

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
        
        self.nuclei_color=nuclei_color
        self.nucleiColorSlider = hsv_qslider.slider()
        self.nucleiColorSlider.setPos(self.nuclei_color)
        nuclei_colorLabel = QtGui.QLabel(self)
        nuclei_colorLabel.setText("Nuclei color:")
        vbox2.addWidget(nuclei_colorLabel)
        vbox2.addWidget(self.nucleiColorSlider)
        
        self.foci_color=foci_color        
        self.fociColorSlider = hsv_qslider.slider()
        self.fociColorSlider.setPos(self.foci_color)
        
        foci_colorLabel = QtGui.QLabel(self)
        foci_colorLabel.setText("Foci color:")
        vbox2.addWidget(foci_colorLabel)
        vbox2.addWidget(self.fociColorSlider)
        
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
        nuclei_color = self.nucleiColorSlider.getPos()
        foci_color = self.fociColorSlider.getPos()
        
        if (sensitivity == self.sensitivity) &\
        (min_cell_size == self.min_cell_size)&\
        (peak_min_val_perc == self.peak_min_val_perc)&\
        (foci_min_val_perc == self.foci_min_val_perc)&\
        (foci_radius == self.foci_radius)&\
        (foci_min_level_on_bg == self.foci_min_level_on_bg)&\
        (foci_rescale_min == self.foci_rescale_min)&\
        (foci_rescale_max == self.foci_rescale_max)&\
        (nuclei_color == self.nuclei_color)&\
        (foci_color == self.foci_color):
            print "Settings had not changed"
            return sensitivity,min_cell_size,peak_min_val_perc,\
            foci_min_val_perc,foci_radius,foci_min_level_on_bg,foci_rescale_min,\
            foci_rescale_max,nuclei_color,foci_color,False
            
        else:
            print "Settings changed"
            return sensitivity,min_cell_size,peak_min_val_perc,\
            foci_min_val_perc,foci_radius,foci_min_level_on_bg,foci_rescale_min,\
            foci_rescale_max,nuclei_color,foci_color,True
