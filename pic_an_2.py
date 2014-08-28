#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np

from scipy import misc

from skimage import exposure

import pic_an

class cell:
    '''Class representing cell variables and methods'''

    def __init__(self, nucleus, pic_nucleus, pic_foci):
        '''Construct cell from mask and channel pics'''

        self.nucleus = nucleus
        self.pic_nucleus = pic_nucleus
        self.pic_foci  = pic_foci
        self.area      = np.sum(nucleus)

    def calculate_foci(self):
        '''Finds foci and its parameters'''

        nucleus_new = (self.pic_foci != 0)

        results = pic_an.foci_plm(self.rescaled_foci_pic, nucleus_new)

        self.foci_number    = results[0]
        self.foci_soid      = results[1]
        self.foci_area      = results[2]
        self.foci_seeds     = results[3]
        self.foci_binary    = results[4]




class cell_set:
    '''Class representing set of cells'''

    def __init__(self, name = '', cells = []):
        '''Constract set from the list of cells given'''

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

            rescaled_norm_pic = exposure.rescale_intensity(cur_cell.rescaled_nucleus_pic, in_range=(p2, p98))

            cur_cell.rescaled_nucleus_pic = np.floor(rescaled_norm_pic*200).astype(int)


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

            rescaled_norm_pic = exposure.rescale_intensity(cur_cell.rescaled_foci_pic, in_range=(p2, p100))

            cur_cell.rescaled_foci_pic = np.floor(rescaled_norm_pic*255).astype(int)


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


    def append(self,cell):
        '''Add a new cell to the set'''

        self.cells.append(cell)

    def extend(self, other_cell_set):
        '''Add new cells from another cell set'''

        self.cells.extend(other_cell_set.cells)




class image_dir(cell_set):
    '''Class representing directory with images'''

    def __init__(self,dir_path):
        '''Constructor'''

        self.dir_path = dir_path
        self.cells = []

    def load_separate_images(self, nuclei_name, foci_name, min_cell_size = 1500):
        '''Load nuclei and foci from separate images'''

        nuclei_abspath = os.path.join(self.dir_path,nuclei_name)
        foci_abspath   = os.path.join(self.dir_path,  foci_name)

        pic_nuclei = pic_an.image_hsv_value(nuclei_abspath)
        pic_foci   = pic_an.image_hsv_value(  foci_abspath)

        nuclei = pic_an.find_nuclei(pic_nuclei, min_cell_size)

        for label_num in np.arange(np.max(nuclei)) + 1:

            nucleus = (nuclei == label_num)
            cell_pic_nucleus = nucleus*pic_nuclei
            cell_pic_foci    = nucleus*pic_foci

            self.append(cell(nucleus, cell_pic_nucleus, cell_pic_foci))

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

        rescaled_nuclei_pics = []
        rescaled_foci_pics   = []
        seed_pics            = []
        foci_bin_pics        = []

        for cur_cell in self.cells:

            rescaled_nuclei_pics.append(cur_cell.rescaled_nucleus_pic)
            rescaled_foci_pics.append(cur_cell.rescaled_foci_pic)
            seed_pics.append(cur_cell.foci_seeds)
            foci_bin_pics.append(cur_cell.foci_binary)


        rescaled_nuclei_pic = sum(rescaled_nuclei_pics)
        rescaled_foci_pic   = sum(rescaled_foci_pics)
        seeds               = sum(seed_pics)
        foci_binary         = sum(foci_bin_pics)

        print self.dir_path
        print np.max(self.nuclei)
        print rescaled_nuclei_pic.shape

        nuclei_colored = pic_an.color_objects(self.pic_nuclei, self.nuclei)
        merged = pic_an.nice_merged_pic(rescaled_nuclei_pic, rescaled_foci_pic, self.nuclei, foci_binary, 0.66, 0.33)


        misc.imsave(pic_colored_nuclei_path, nuclei_colored)
        misc.imsave(pic_merged_path, merged)
        misc.imsave(pic_seeds_path, seeds)
        misc.imsave(pic_rescaled_foci_path, rescaled_foci_pic)

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




