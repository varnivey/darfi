#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is a part of DARFI project (dna Damage And Repair Foci Imager)
#    Copyright (C) 2014  Ivan V. Ozerov
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as·
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License v2 for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import os
import numpy as np

from skimage.exposure import rescale_intensity
from skimage import img_as_ubyte

from skimage.io import imsave
from skimage.io import imread

#from scipy.misc import imsave
#from scipy.misc import imread

import pic_an_old

#from pic_an_old import foci_plm
from pic_an_calc import foci_plm
from pic_an_calc import join_peaces
from pic_an_calc import peace

class cell:
    '''Class representing cell variables and methods'''

    def __init__(self, nucleus, pic_nucleus, pic_foci, coords = (0,0,0,0)):
        '''Construct cell from mask and channel pics'''

        self.nucleus      = nucleus
        self.pic_nucleus  = pic_nucleus
        self.pic_foci     = pic_foci
        self.coords       = coords
        self.area         = np.sum(nucleus)

    def calculate_foci(self):
        '''Finds foci and its parameters'''

        nucleus_new = (self.pic_foci != 0)

        results = foci_plm(self.rescaled_foci_pic, nucleus_new)

        self.foci_number    = results[0]
        self.foci_soid      = results[1]
        self.foci_area      = results[2]
        self.foci_seeds     = results[3]
        self.foci_binary    = results[4]




class cell_set:
    '''Class representing set of cells'''

    def __init__(self, name = '', cells = []):
        '''Construct set from the list of cells given'''

        self.cells = cells
        self.name  = name


    def rescale_nuclei(self):
        '''Rescale nuclei in the set'''

        new_values = []

        for cur_cell in self.cells:

            nucleus_values = np.extract(cur_cell.nucleus, cur_cell.pic_nucleus)

            mean_value = np.mean(nucleus_values, dtype = float)

            new_values.append(nucleus_values/mean_value)

            cur_cell.rescaled_nucleus_pic = cur_cell.pic_nucleus/mean_value

        p2,p98 = np.percentile(np.concatenate(new_values),(2,98))

        for cur_cell in self.cells:

            rescaled_norm_pic = rescale_intensity(cur_cell.rescaled_nucleus_pic, in_range=(p2, p98))

            cur_cell.rescaled_nucleus_pic = np.floor(rescaled_norm_pic*200).astype(np.uint8)


    def rescale_foci(self):
        '''Rescale foci in the set'''

        new_foci_values = []

        for cur_cell in self.cells:

            foci_values = np.extract(cur_cell.nucleus, cur_cell.pic_foci)

            mean_value = np.percentile(foci_values, (20))

            new_foci_values.append(foci_values/mean_value)

            cur_cell.rescaled_foci_pic = cur_cell.pic_foci/mean_value

        p2,p100 = np.percentile(np.concatenate(new_foci_values),(2,100))

        for cur_cell in self.cells:

            rescaled_norm_pic = rescale_intensity(cur_cell.rescaled_foci_pic, in_range=(p2, p100))

            cur_cell.rescaled_foci_pic = np.floor(rescaled_norm_pic*255).astype(np.uint8)


    def calculate_foci(self):
        '''Calculate foci_plm for all cells'''

        remained = len(self.cells)

        name = self.name

        print 'Foci calculation have started for', name

        for cur_cell in self.cells:
            cur_cell.calculate_foci()

            remained -= 1

            if remained == 0:
                print 'Foci calculation have finished for', name

            else:
                print remained, 'nuclei remained for', name


    def calculate_foci_parameters(self):
        '''Calculate absolute and relative foci number, area and soid in 10-90 percent interval'''

        abs_foci_nums  = []
        abs_foci_areas = []
        abs_foci_soids = []

        rel_foci_nums  = []
        rel_foci_areas = []
        rel_foci_soids = []

        for cur_cell in self.cells:

            abs_foci_nums.append(  cur_cell.foci_number)
            abs_foci_areas.append( cur_cell.foci_area  )
            abs_foci_soids.append( cur_cell.foci_soid  )

            try:
                rel_foci_nums.append(  cur_cell.foci_number*2000/np.float(cur_cell.area))
                rel_foci_areas.append( cur_cell.foci_area*2000/  np.float(cur_cell.area))
                rel_foci_soids.append( cur_cell.foci_soid*2000/  np.float(cur_cell.area))
            except:
                pass


        self.abs_foci_num_param   = mean_and_MSE(abs_foci_nums)
        self.abs_foci_area_param  = mean_and_MSE(abs_foci_areas)
        self.abs_foci_soid_param  = mean_and_MSE(abs_foci_soids)

        self.rel_foci_num_param   = mean_and_MSE(rel_foci_nums)
        self.rel_foci_area_param  = mean_and_MSE(rel_foci_areas)
        self.rel_foci_soid_param  = mean_and_MSE(rel_foci_soids)



    def write_parameters(self, outfilename):
        '''Write file with set parameters'''

        params = [len(self.cells)]
        params.extend(self.abs_foci_num_param)
        params.extend(self.abs_foci_area_param)
        params.extend(self.abs_foci_soid_param)
        params.extend(self.rel_foci_num_param)
        params.extend(self.rel_foci_area_param)
        params.extend(self.rel_foci_soid_param)

        str_params = [str(round(item, 4)).rjust(12) for item in params]
        str_params.insert(0,self.name.rjust(20))

        with open(outfilename, 'w') as outfile:
            outfile.write(' '.join(str_params))


    def append(self,new_cell):
        '''Add a new cell to the set'''

        self.cells.append(new_cell)

    def extend(self, other_cell_set):
        '''Add new cells from another cell set'''

        self.cells.extend(other_cell_set.cells)




class image_dir(cell_set):
    '''Class representing directory with images'''

    def __init__(self,dir_path):
        '''Constructor'''

        self.dir_path = dir_path
        self.cells = []

    def load_separate_images(self, nuclei_name, foci_name, sensitivity = 5., min_cell_size = 1500):
        '''Load nuclei and foci from separate images'''

        nuclei_abspath = os.path.join(self.dir_path,nuclei_name)
        foci_abspath   = os.path.join(self.dir_path,  foci_name)

        pic_nuclei = image_hsv_value(nuclei_abspath)
        pic_foci   = image_hsv_value(  foci_abspath)

        nuclei = pic_an_old.find_nuclei(pic_nuclei, sensitivity, min_cell_size)

        for label_num in np.arange(np.max(nuclei)) + 1:

            nucleus = (nuclei == label_num)
            cell_pic_nucleus = nucleus*pic_nuclei
            cell_pic_foci    = nucleus*pic_foci

            coords = find_cell_coords(nucleus)
            up,down,right,left = coords

            nucleus          =          nucleus[left:right,down:up]
            cell_pic_nucleus = cell_pic_nucleus[left:right,down:up]
            cell_pic_foci    =    cell_pic_foci[left:right,down:up]

            self.append(cell(nucleus, cell_pic_nucleus, cell_pic_foci, coords))

        self.nuclei = nuclei

        self.pic_nuclei = pic_nuclei


    def write_all_pic_files(self):
        '''Write file with colored nuclei'''


        if self.number_of_cells() == 0:
            print "No cells found in" + self.dir_path

            return

        pic_colored_nuclei_path = os.path.join(self.dir_path,'colored_nuclei.jpg')
        pic_merged_path         = os.path.join(self.dir_path,'merged.jpg')
        pic_seeds_path          = os.path.join(self.dir_path,'seeds_foci.jpg')
        pic_rescaled_foci_path  = os.path.join(self.dir_path,'rescaled_foci.jpg')

        rescaled_nuclei_peaces = []
        rescaled_foci_peaces   = []
        seed_peaces            = []
        foci_bin_peaces        = []

        x_max, y_max = self.nuclei.shape

        for cur_cell in self.cells:

            coords = cur_cell.coords

            rescaled_nuclei_peaces.append(peace(cur_cell.rescaled_nucleus_pic, coords))
            rescaled_foci_peaces.append(peace(cur_cell.rescaled_foci_pic, coords))
            seed_peaces.append(peace(cur_cell.foci_seeds, coords))
            foci_bin_peaces.append(peace(cur_cell.foci_binary, coords))


        rescaled_nuclei_pic = join_peaces(rescaled_nuclei_peaces, x_max, y_max, dtype = np.uint8)
        rescaled_foci_pic   = join_peaces(rescaled_foci_peaces, x_max, y_max, dtype = np.uint8)
        seeds               = (255*join_peaces(seed_peaces, x_max, y_max)).astype(np.uint8)
        foci_binary         = join_peaces(foci_bin_peaces, x_max, y_max)

        nuclei_colored = pic_an_old.color_objects(self.pic_nuclei, self.nuclei)
        merged = pic_an_old.nice_merged_pic(rescaled_nuclei_pic, rescaled_foci_pic, self.nuclei, foci_binary, 0.66, 0.33)


        imsave(pic_colored_nuclei_path, nuclei_colored)
        imsave(pic_merged_path, merged)
        imsave(pic_seeds_path, seeds)
        imsave(pic_rescaled_foci_path, rescaled_foci_pic)

    def number_of_cells(self):
        '''Return number of cells from this image_dir'''

        return len(self.cells)




def mean_and_MSE(value_list):
    '''Returns list with the mean value and MSE for value_list in 10-90 percentile'''

    if(len(value_list) == 0):
        return [0.,0.]

    np_value_list = np.array(value_list)

    p10,p90 = np.percentile(np_value_list, (10,90))

    match_10_90 = np.logical_and(np_value_list >= p10, np_value_list <= p90)

    new_values = np.extract(match_10_90, np_value_list)

    mean = np.mean(new_values)

    MSE = np.power(np.sum(np.power(new_values - mean, 2)/len(new_values)), 0.5)

    return [mean, MSE]


def image_hsv_value(image_file):
    '''Returns HSV value as numpy array for image file given'''


    pic_source = img_as_ubyte(imread(image_file))

    pic_grey = np.max(pic_source,2)

    return pic_grey


def find_cell_coords(nucleus):
    '''Find min and max coords = (up,down,right,left) of the cell area in the image'''

    x_sum = np.sum(nucleus,1).astype(bool)
    y_sum = np.sum(nucleus,0).astype(bool)

    x_ind = np.transpose(x_sum.nonzero())
    y_ind = np.transpose(y_sum.nonzero())

    left  = x_ind[0]
    right = x_ind[-1] + 1

    down  = y_ind[0]
    up    = y_ind[-1] + 1

    return (up, down, right, left)


