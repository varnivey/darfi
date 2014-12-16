from PyQt4 import QtGui, QtCore
import hsv_qslider, copy


class SettingsWindow(QtGui.QDialog):
      
    def __init__(self,settings):
        super(SettingsWindow, self).__init__()
        hbox = QtGui.QHBoxLayout(self)
        
        vbox1Area = QtGui.QWidget(self)
        vbox1 = QtGui.QVBoxLayout(vbox1Area)
        
        self.settings = settings

        
        sensitivityLabel = QtGui.QLabel(self)
        sensitivityLabel.setText("Sensitivity:")
        self.sensitivityField = QtGui.QDoubleSpinBox()
        self.sensitivityField.setRange(0,10)
        self.sensitivityField.setDecimals(0)
        self.sensitivityField.setValue(self.settings.sensitivity)
        vbox1.addWidget(sensitivityLabel)
        vbox1.addWidget(self.sensitivityField)
        

        min_cell_sizeLabel = QtGui.QLabel(self)
        min_cell_sizeLabel.setText("Minimal cell size:")
        self.min_cell_sizeField = QtGui.QDoubleSpinBox()
        self.min_cell_sizeField.setRange(0,4294967296)
        self.min_cell_sizeField.setDecimals(0)
        self.min_cell_sizeField.setValue(self.settings.min_cell_size)
        vbox1.addWidget(min_cell_sizeLabel)
        vbox1.addWidget(self.min_cell_sizeField)
        

        foci_lookup_sensivityLabel = QtGui.QLabel(self)
        foci_lookup_sensivityLabel.setText("Foci lookup sensitivity")
        self.foci_lookup_sensivityField = QtGui.QDoubleSpinBox()
        self.foci_lookup_sensivityField.setRange(0,100)
        self.foci_lookup_sensivityField.setDecimals(0)
        self.foci_lookup_sensivityField.setValue(self.settings.foci_lookup_sensivity)
        vbox1.addWidget(foci_lookup_sensivityLabel)
        vbox1.addWidget(self.foci_lookup_sensivityField)
        

        foci_min_val_percLabel = QtGui.QLabel(self)
        foci_min_val_percLabel.setText("Foci area fill percent")
        self.foci_area_fill_percentField = QtGui.QDoubleSpinBox()
        self.foci_area_fill_percentField.setRange(0,100)
        self.foci_area_fill_percentField.setDecimals(0)
        self.foci_area_fill_percentField.setValue(self.settings.foci_area_fill_percent)
        vbox1.addWidget(foci_min_val_percLabel)
        vbox1.addWidget(self.foci_area_fill_percentField)
        

        min_foci_radiusLabel = QtGui.QLabel(self)
        min_foci_radiusLabel.setText("Min foci radius")
        self.min_foci_radiusField = QtGui.QDoubleSpinBox()
        self.min_foci_radiusField.setRange(0,4294967296)
        self.min_foci_radiusField.setDecimals(0)
        self.min_foci_radiusField.setValue(self.settings.min_foci_radius)
        vbox1.addWidget(min_foci_radiusLabel)
        vbox1.addWidget(self.min_foci_radiusField)

        max_foci_radiusLabel = QtGui.QLabel(self)
        max_foci_radiusLabel.setText("Max foci radius")
        self.max_foci_radiusField = QtGui.QDoubleSpinBox()
        self.max_foci_radiusField.setRange(0,4294967296)
        self.max_foci_radiusField.setDecimals(0)
        self.max_foci_radiusField.setValue(self.settings.max_foci_radius)
        vbox1.addWidget(max_foci_radiusLabel)
        vbox1.addWidget(self.max_foci_radiusField)
        
        vbox2Area = QtGui.QWidget(self)
        vbox2 = QtGui.QVBoxLayout(vbox2Area)        
        
        allowed_foci_overlapLabel = QtGui.QLabel(self)
        allowed_foci_overlapLabel.setText("Allowed foci overlap")
        self.allowed_foci_overlapField = QtGui.QDoubleSpinBox()
        self.allowed_foci_overlapField.setRange(0,100)
        self.allowed_foci_overlapField.setDecimals(0)
        self.allowed_foci_overlapField.setValue(self.settings.allowed_foci_overlap)
        vbox1.addWidget(allowed_foci_overlapLabel)
        vbox1.addWidget(self.allowed_foci_overlapField)
        

        foci_rescale_minLabel = QtGui.QLabel(self)
        foci_rescale_minLabel.setText("Foci rescale min (-1 for autoscale):")
        self.foci_rescale_minField = QtGui.QDoubleSpinBox()
        self.foci_rescale_minField.setRange(-1,255)
        try:
            self.foci_rescale_minField.setValue(self.settings.foci_rescale_min)
        except TypeError:
            self.foci_rescale_minField.setValue(-1)
        vbox2.addWidget(foci_rescale_minLabel)
        vbox2.addWidget(self.foci_rescale_minField)
        

        foci_rescale_maxLabel = QtGui.QLabel(self)
        foci_rescale_maxLabel.setText("Foci rescale max (-1 for autoscale):")
        self.foci_rescale_maxField = QtGui.QDoubleSpinBox()
        self.foci_rescale_maxField.setRange(-1,255)
        try:
            self.foci_rescale_maxField.setValue(self.settings.foci_rescale_max)
        except TypeError:
            self.foci_rescale_maxField.setValue(-1)
        vbox2.addWidget(foci_rescale_maxLabel)
        vbox2.addWidget(self.foci_rescale_maxField)
        

        self.nucleiColorSlider = hsv_qslider.slider()
        self.nucleiColorSlider.setPos(self.settings.nuclei_color)
        nuclei_colorLabel = QtGui.QLabel(self)
        nuclei_colorLabel.setText("Nuclei color:")
        vbox2.addWidget(nuclei_colorLabel)
        vbox2.addWidget(self.nucleiColorSlider)
        

        self.fociColorSlider = hsv_qslider.slider()
        self.fociColorSlider.setPos(self.settings.foci_color)
        foci_colorLabel = QtGui.QLabel(self)
        foci_colorLabel.setText("Foci color:")
        vbox2.addWidget(foci_colorLabel)
        vbox2.addWidget(self.fociColorSlider)
        
        self.normalize_intensity_box = QtGui.QCheckBox('Normalize intensity', self)
        self.normalize_intensity_box.setChecked(self.settings.normalize_intensity)
        vbox2.addWidget(self.normalize_intensity_box)
        
        self.return_circles_box = QtGui.QCheckBox('Draw foci with circles', self)
        self.return_circles_box.setChecked(self.settings.return_circles)
        vbox2.addWidget(self.return_circles_box)
        
        hbox.addWidget(vbox1Area)
        hbox.addWidget(vbox2Area)

    

    def getSettings(self):
        settings=copy.deepcopy(self.settings)
        settings.sensitivity = self.sensitivityField.value()
        settings.min_cell_size = self.min_cell_sizeField.value()
        settings.foci_lookup_sensivity = self.foci_lookup_sensivityField.value()
        settings.foci_area_fill_percent = self.foci_area_fill_percentField.value()
        settings.min_foci_radius = self.min_foci_radiusField.value()
        settings.max_foci_radius = self.max_foci_radiusField.value()
        settings.allowed_foci_overlap = self.allowed_foci_overlapField.value()
        settings.foci_rescale_min = self.foci_rescale_minField.value()
        settings.foci_rescale_min = None if settings.foci_rescale_min == -1 else settings.foci_rescale_min
        settings.foci_rescale_max = self.foci_rescale_maxField.value()
        settings.foci_rescale_max = None if settings.foci_rescale_max == -1 else settings.foci_rescale_max
        settings.nuclei_color = self.nucleiColorSlider.getPos()
        settings.foci_color = self.fociColorSlider.getPos()
        settings.normalize_intensity = self.normalize_intensity_box.checkState() == QtCore.Qt.Checked
        settings.return_circles = self.return_circles_box.checkState() == QtCore.Qt.Checked
        
        if settings.__dict__ == self.settings.__dict__:
            print "Settings had not changed"
            return settings,False
            
        else:
            print "Settings changed"
            return settings,True
