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

#from scipy.ndimage import distance_transform_edt


from skimage import img_as_ubyte
from skimage.filter import gaussian_filter
from skimage.filter import canny as canny_filter
from skimage.filter.rank import median as median_filter
from skimage.feature import peak_local_max
from skimage.measure import label as measure_label
from skimage.morphology import binary_dilation, binary_erosion
from skimage.morphology import remove_small_objects, watershed
from skimage.morphology import medial_axis
from skimage.segmentation import relabel_sequential
from skimage.color import hsv2rgb



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




############################################################################

################    The functions below need revision    ###################

############################################################################


def find_nuclei(pic_with_nuclei, sensitivity = 5., min_cell_size = 1500, frame_size = 5, cutoff_shift = 0.):
    '''Returns pic with labeled nuclei'''

#    print sensitivity

#    binary = binarize_otsu(pic_with_nuclei, frame_size, cutoff_shift)
    binary = binarize_canny(pic_with_nuclei, sensitivity)
#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/binary_nuclei.jpg', binary)

    labels = label_nuclei(binary, min_cell_size)

    return labels

#    print np.max(labels)


def binarize_canny(pic_source, sensitivity = 5.):

    ht = 5. + ((10 - sensitivity)/5.)*20.

#    print ht

    edges = canny_filter(pic_source, sigma = 3, high_threshold = ht, low_threshold = 2.)

    selem_morph = np.array([0,1,0,1,1,1,0,1,0], dtype=bool).reshape((3,3))

    for i in (1,2):
        edges = binary_dilation(edges, selem_morph)

#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/edges.jpg', edges)

#    binary = ndimage.binary_fill_holes(edges)

    labels = measure_label(edges)

    labelcount = np.bincount(labels.ravel())

    bg = np.argmax(labelcount)

    edges[labels != bg] = 255

    selem_med = np.ones((3,3), dtype = bool)

    binary = median_filter(edges, selem_med)

    for i in (1,2,3):
        binary = binary_erosion(edges, selem_morph)

    return edges


def label_nuclei(binary, min_size):
    '''Label, watershed and remove small objects'''

    distance = medial_axis(binary, return_distance=True)[1]

    distance_blured = gaussian_filter(distance, 5)

    local_maxi = peak_local_max(distance_blured, indices=False, labels=binary, min_distance = 30)

    markers = measure_label(local_maxi)

#    markers[~binary] = -1

#    labels_rw = segmentation.random_walker(binary, markers)

#    labels_rw[labels_rw == -1] = 0

#    labels_rw = segmentation.relabel_sequential(labels_rw)

    labels_ws = watershed(-distance, markers, mask=binary)

    labels_large = remove_small_objects(labels_ws,min_size)

    labels_clean_border = clear_border(labels_large)

    labels_from_one = relabel_sequential(labels_clean_border)

#    plt.imshow(ndimage.morphology.binary_dilation(markers))
#    plt.show()

    return labels_from_one[0]


def clear_border(pic_labeled):
    '''Removes objects which touch the border'''

    borders = np.zeros(pic_labeled.shape, np.bool)

    borders[ 0,:] = 1
    borders[-1,:] = 1
    borders[:, 0] = 1
    borders[:,-1] = 1

    at_border = np.unique(pic_labeled[borders])

    for obj in at_border:
        pic_labeled[pic_labeled == obj] = 0

    return pic_labeled

def color_objects(pic_grey,labels):
    '''Return image with colored nuclei'''


#    hsv_source = color.rgb2hsv(pic_source)

    if np.max(labels) == 0:
        return pic_grey

    try:
        hue_step = 1./np.max(labels)
    except:
        return pic_grey
    hue = labels*hue_step

    val = pic_grey

    sat = (labels != 0)*0.5
#    sat = (labels != 0)

#    sat.resize(val.shape)

    pic_shape = list(val.shape)
    pic_shape.append(3)

    hsv_result = np.dstack((hue,sat,val))

    hsv_result.resize(pic_shape)

    rgb_result = hsv2rgb(hsv_result).astype(np.uint8)

    return rgb_result


def nice_merged_pic(source_nuclei, source_foci, nuclei, foci, color_nuclei=0., color_foci=0.33):
    '''Returns enchanced picture with black bg and merged channels inside the objects'''


    pic_shape = list(nuclei.shape)
    pic_shape.append(3)

    nuclei = (nuclei != 0)
    foci   = (foci   != 0)

    nuclei_only = nuclei - foci

    hue = color_nuclei*nuclei_only + foci*color_foci

    foci_enhanced = 255 - np.floor((255 - source_foci)*0.6)

    val = source_nuclei*nuclei_only + foci*foci_enhanced

#    val = nuclei*((source_nuclei > foci_enhanced)*source_nuclei + (source_nuclei < foci_enhanced)*foci_enhanced)

    sat = nuclei*1.

    hsv_result = np.dstack((hue,sat,val))

    hsv_result.resize(pic_shape)

    rgb_result = hsv2rgb(hsv_result).astype(np.uint8)

#    rgb_blured = ndimage.gaussian_filter(rgb_result, 3)

    return rgb_result


