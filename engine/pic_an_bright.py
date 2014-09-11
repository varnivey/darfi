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
import pic_an

def calc_multiple_dirs(dir_path, nuclei_name='3DAPI.TIF', foci_name='3FITС.TIF'):
    '''Separately calculates foci for all subdirs'''

    subdirs = [os.path.join(dir_path, directory) for directory in os.listdir(dir_path) \
            if os.path.isdir(os.path.join(dir_path, directory))]

    for subdir in subdirs:

        print 'Calculation has STARTED in', os.path.split(subdir)[0]

        calc_foci_in_dir(subdir, nuclei_name, foci_name)

        print 'Calculation has FINISHED in', os.path.split(subdir)[0]


def calc_bright_cells_in_dir(dir_path, nuclei_name='3DAPI.TIF', foci_name='3FITС.TIF', outfile = 'result.txt'):
    '''Calculates foci from dir'''

    dirs_with_images = [os.path.join(dir_path, directory) for directory in os.listdir(dir_path)]

    pre_image_dirs = [image_dir for image_dir in dirs_with_images if \
            (os.path.isfile(os.path.join(image_dir,nuclei_name)) and os.path.isfile(os.path.join(image_dir, foci_name)))]

    image_dirs = [pic_an.image_dir(image_dir, nuclei_name, foci_name) for image_dir in pre_image_dirs]

    path1,name2 = os.path.split(dir_path)
    name1       = os.path.split(path1)[1]

    name = name1 + '_' + name2
    absoutfile = os.path.join(dir_path,outfile)

    remained = len(image_dirs)

    print "We have", remained, 'images to load for', name

    print "Image loading have started for", name

    cell_num          = 0
    bright_nuclei_num = 0
    bright_foci_num   = 0

    for image_dir in image_dirs:
        image_dir.load_separate_images(sensitivity = 7., min_cell_size = 200)

        image_dir.calc_nuclei_mean_value()
        image_dir.calc_foci_mean_value()

        bright_nuclei_num += image_dir.bright_nuclei_count()
        bright_foci_num   += image_dir.bright_foci_count()

        cell_num += image_dir.number_of_cells()

        image_dir.write_pic_with_bright_nuclei_colored(0.95)
        image_dir.write_pic_with_bright_foci_colored(0.45)
        image_dir.write_pic_with_nuclei_colored()


        remained -= 1

        if remained == 0:
            print "Сalculation have finished for", name
        elif remained == 1:
            print remained, 'image  remained to calculate for', name
        else:
            print remained, 'images remained to calculate for', name



    print 'Overall cell count for ' + name + ' : ', cell_num
    print 'Number of bright cells on the 1st image for ' + name + ' : ', bright_nuclei_num
    print 'Number of bright cells on the 2nd image for' + name + ' : ', bright_foci_num



