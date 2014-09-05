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


import numpy as np


from skimage import img_as_ubyte
from skimage.filter import gaussian_filter
from skimage.feature import peak_local_max
from skimage.measure import label as measure_label
from skimage.morphology import binary_dilation


def foci_plm(foci_pic, nucleus, peak_min_val_perc = 60, foci_min_val_perc = 90, foci_radius = 10, foci_min_level_on_bg = 40):
    '''Find foci using peak_local_max seed search followed by watershed'''

    label_circle = circle_mask(foci_radius)

    markers = get_markers(foci_pic, nucleus, peak_min_val_perc)

    x_max, y_max = markers.shape

    labels_num = np.max(markers)

    markers_fin = np.zeros((x_max, y_max), dtype = bool)
    markers_num = 0

    peace_list = []

    for label_num in range(labels_num):

        x_m,y_m = np.transpose(np.nonzero(markers == label_num + 1))[0]

        up, down       = y_m + foci_radius, y_m - foci_radius + 1
        right, left    = x_m + foci_radius, x_m - foci_radius + 1

        if  down < 0    : down  = 0
        if    up > y_max: up    = y_max
        if  left < 0    : left  = 0
        if right > x_max: right = x_max


        up_c, down_c    = up - y_m + foci_radius - 1, foci_radius - 1 - (y_m - down)
        right_c, left_c = right - x_m + foci_radius - 1, foci_radius - 1 - (x_m - left)

        label      = label_circle[left_c:right_c, down_c:up_c]
        new_pic    = foci_pic[left:right, down:up]

        pic_label = label*new_pic

        label_values = np.extract(label, pic_label)

        bg_val,peak_val = np.percentile(label_values, (20,95))

        discount_focus = (peak_val - bg_val) < foci_min_level_on_bg

        if discount_focus:
            continue

        markers_fin[x_m,y_m] = True

        markers_num += 1

        local_cutoff = np.floor(np.percentile(label_values, (foci_min_val_perc))).astype(np.uint8)

        peace_list.append(peace(pic_label > local_cutoff, (up,down,right,left)))

    selem = np.array([0,1,0,1,1,1,0,1,0], dtype=bool).reshape((3,3))

    markers_fin = binary_dilation(binary_dilation(markers_fin, selem), selem)

    foci_bin = join_peaces(peace_list, x_max, y_max)

    foci_area = np.sum(foci_bin)

    if foci_area != 0:
        foci_soid = np.sum(foci_bin*foci_pic)/(1.*foci_area)
    else:
        foci_soid = 0.

    return [markers_num,foci_area,foci_soid,markers_fin, foci_bin]


def get_markers(foci_pic, nucleus, peak_min_val_perc = 60):
    '''Return foci markers'''

    foci_pic_blured = img_as_ubyte(gaussian_filter(foci_pic, 1))

    foci_values = np.extract(nucleus, foci_pic)

    min_peak_val = np.percentile(foci_values, (peak_min_val_perc))

    local_maxi = peak_local_max(foci_pic_blured, min_distance=5, threshold_abs=min_peak_val, indices=False, labels=nucleus)

    return measure_label(local_maxi)


def circle_mask(radius = 10):
    '''Returns circle with given radius'''

    pic_size = radius*2 - 1

    x,y = np.indices((pic_size,pic_size))

    center = radius - 1

    radius_2 = np.power(radius, 2)

    circle = np.power(x - center,2) + np.power(y - center,2) < radius_2

    return circle



class peace:
    '''Class representing peace of the larger image'''

    def __init__(self, image, coords):
        '''Create peace form image and coords = (up,down,right,left) '''

        self.image = image
        self.coords = coords


def join_peaces(peace_list, x_max, y_max, dtype = bool):
    '''Join peaces into single image with (x_max, y_max) size'''

    result = np.zeros((x_max, y_max),dtype = dtype)

    for peace_item in peace_list:

        up,down,right,left = peace_item.coords

        result[left:right, down:up] += peace_item.image

    return result



