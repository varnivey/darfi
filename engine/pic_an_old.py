#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is a part of DARFI project (dna Damage And Repair Foci Imager)
#    Copyright (C) 2014  Ivan V. Ozerov
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as 
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

import matplotlib
matplotlib.use('QT4Agg')

import matplotlib.pyplot as plt
from scipy import misc
from scipy import ndimage
import numpy as np

from skimage import filter as filt
from skimage import morphology
from skimage import feature
from skimage import segmentation
from skimage import color
#This module does not exist in python-skimage package from ubuntu repo. Use pip or easy_install instead
from skimage import restoration
#
from skimage import exposure
from skimage import measure
from skimage import draw


def calc_temp(image_with_nuclei, image_with_foci, frame_size = 3, cutoff_shift = 0.5):
    '''Temporary function for testing'''
    
    pic_nuclei = image_hsv_value(image_with_nuclei)
    pic_foci   = image_hsv_value(image_with_foci  )

#    foci_deconvolved = deconvolved_image(pic_foci)
#    nuclei_deconvolved = deconvolved_image(pic_nuclei)

    nuclei = find_nuclei(pic_nuclei)
#    foci   = find_foci(nuclei, pic_foci, frame_size, cutoff_shift)

#    rescaled_nuclei, rescaled_foci_list = normalized_pics(nuclei, pic_nuclei, [pic_foci])
#    rescaled_foci = rescaled_foci_list[0]

    rescaled_nuclei = normalized_pic(nuclei, pic_nuclei)
    rescaled_foci  = normalized_foci(nuclei, pic_foci)

#    foci   = find_foci(nuclei, rescaled_foci, frame_size, cutoff_shift)
    foci   = find_foci(rescaled_foci, nuclei)


    nuclei_colored = color_objects(pic_nuclei, nuclei)
#    foci_colored   = color_objects(pic_foci,   foci  )

    merged = nice_merged_pic(rescaled_nuclei, rescaled_foci, nuclei, foci, 0.66, 0.33)

    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/source_nuclei.jpg', pic_nuclei)
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/source_fitc.jpg', pic_foci)
#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/deconv_nuclei.jpg', nuclei_deconvolved)
#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/deconv_foci.jpg'  ,   foci_deconvolved)
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/rescaled_nuclei.jpg', rescaled_nuclei)
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/rescaled_foci.jpg',   rescaled_foci)
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/colored_nuclei.jpg', nuclei_colored)
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/binary_foci.jpg', foci)
#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/colored_foci.jpg', foci_colored)
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/merged.jpg', merged)

#    plt.imshow(binary)
#    plt.show()

def image_hsv_value(image_file):
    '''Returns HSV value as numpy array for image file given'''

    pic_source = misc.imread(image_file)

    pic_grey = np.max(pic_source,2)

    return pic_grey

def deconvolved_image(source_pic):
    '''Returns deconvolved image'''

    denoised = restoration.denoise_bilateral(source_pic)
    return denoised

def find_nuclei(pic_with_nuclei, sensitivity = 5., min_cell_size = 1500, frame_size = 5, cutoff_shift = 0.):
    '''Returns pic with labeled nuclei'''

#    print sensitivity

#    binary = binarize_otsu(pic_with_nuclei, frame_size, cutoff_shift)
    binary = binarize_canny(pic_with_nuclei, sensitivity)
#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/binary_nuclei.jpg', binary)

    labels = label_nuclei(binary, min_cell_size)

    return labels

#    print np.max(labels)


#def find_foci(nuclei, pic_with_foci, frame_size = 3, cutoff_shift = 0.5):
#    '''Returns pic with labeled foci'''

#    binary = binarize_otsu(pic_with_foci, frame_size, cutoff_shift)
#    binary = binarize_otsu_foci(pic_with_foci, nuclei, cutoff_shift)

#    labeled_foci = nuclei*binary

#    return labeled_foci


def foci_log(foci_pic):
    '''Find foci using LoG algorithm'''

    blobs_log = blob_log(foci_pic, max_sigma=30, num_sigma=10, threshold=.1)

#    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

def find_foci(foci_pic, nuclei):
    '''Returns pic with labeled foci'''

    nuclei_bin_new = (foci_pic != 0)
    nuclei = nuclei*nuclei_bin_new

    nuclei_num = np.max(nuclei)

    foci_nums = []
    foci_area = []
    foci_soid = []
    foci_bins = []
    foci_seeds = []

#    print nuclei_num

    for label in range(nuclei_num):

        nucleus = (nuclei == label + 1)
        cur_foci_pic = foci_pic*nucleus

        num, soid, area, seeds, binary = foci_plm(cur_foci_pic, nucleus)

        foci_nums.append(num)
        foci_area.append(area)
        foci_soid.append(soid)
        foci_seeds.append(seeds)
        foci_bins.append(binary)

    binary = sum(foci_bins)
    markers = sum(foci_seeds)

    labeled_foci = nuclei*binary
    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/seeds_foci.jpg', markers)

    return labeled_foci


def foci_plm(foci_pic, nucleus, peak_min_val_perc = 60, foci_min_val_perc = 80, foci_radius = 10, foci_min_level_on_bg = 40):
    '''Find foci using peak_local_max seed search followed by watershed'''

#    print np.max(foci_pic)

    foci_pic_blured = ndimage.gaussian_filter(foci_pic, 1)

    foci_values = np.extract(nucleus, foci_pic)

    min_peak_val = np.percentile(foci_values, (peak_min_val_perc))

#    min_peak_val_2 = bg_val*peak_on_bg_min_val_koef

#    min_peak_val = max(min_peak_val_1, min_peak_val_2)

#    print 'New cell'

    local_maxi = feature.peak_local_max(foci_pic_blured, min_distance=5, threshold_abs=min_peak_val, indices=False, labels=nucleus)

    markers = measure.label(local_maxi)

#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/maxi.jpg', markers_fin)

    labels_ws = morphology.watershed(-foci_pic_blured, markers, mask=nucleus)

#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/watershed_foci.jpg', labels_ws)

    labels_num = np.max(labels_ws)

    foci_list = []

    npsum         = np.sum
    npfloor       = np.floor
    nppercentile  = np.percentile
    npnonzero     = np.nonzero
    nptranspose   = np.transpose
    nppower       = np.power
    npindices     = np.indices
    nplogical_and = np.logical_and
    npextract     = np.extract

    pic_shape = labels_ws.shape

    markers_fin = np.zeros(pic_shape, dtype = bool)
    markers_num = 0

    foci_radius_2 = nppower(foci_radius,2)

    for label_num in range(labels_num):

        label_ws = (labels_ws == label_num + 1)

        marker = (markers == label_num + 1)
        marker_size = npsum(marker)

        x_m,y_m = nptranspose(npnonzero(marker))[0]
        x,y = npindices(pic_shape)

        label_circle = nppower(x - x_m,2) + nppower(y - y_m,2) < foci_radius_2

        label = nplogical_and(label_ws,label_circle)
        pic_label = label*foci_pic

        label_values = npextract(label, pic_label)

        bg_val,peak_val = nppercentile(label_values, (20,95))

#        peak_val = npsum(marker*foci_pic)/marker_size

#        print peak_val

#        local_cutoff = npfloor(bg_val + (peak_val - bg_val)*foci_min_val_koef).astype(int)

        discount_focus = (peak_val - bg_val) < foci_min_level_on_bg

#        print bg_val, peak_val, peak_val - bg_val, not discount_focus

        if discount_focus:
            continue

        markers_fin[x_m,y_m] = True

        markers_num += 1

        local_cutoff = nppercentile(label_values, (foci_min_val_perc)).astype(int)

        foci_list.append(pic_label > local_cutoff)

#        print local_cutoff, npsum(pic_label >= local_cutoff)

    markers_fin = ndimage.binary_dilation(markers_fin, iterations = 2)

#    print markers_num

    foci_bin = sum(foci_list)

    foci_area = np.sum(foci_bin)

    if foci_area != 0:
        foci_soid = np.sum(foci_bin*foci_pic)/(1.*foci_area)
    else:
        foci_soid = 0.

    return [markers_num,foci_area,foci_soid,markers_fin, foci_bin]



def binarize_otsu(pic_source, frame_size = 3, cutoff_shift = 0):
    '''Binarize image using Otsu threshold'''

    pic_smooth = ndimage.gaussian_filter(pic_source, frame_size)

    cutoff_otsu = filt.threshold_otsu(pic_source)

    cutoff = np.floor(cutoff_otsu*(cutoff_shift + 1.)).astype(int)

    binary = pic_smooth > cutoff

    return binary


def binarize_otsu_foci(foci_pic, nuclei, cutoff_shift = 0):
    '''Binarize image using Otsu threshold on nuclei only'''

    binary_nuclei = (nuclei != 0)

    foci_values = np.extract(binary_nuclei, foci_pic)

    cutoff_otsu = filt.threshold_otsu(foci_values)

    print max(foci_values)

    print cutoff_otsu

    cutoff = cutoff_otsu*(cutoff_shift + 1.)

    binary = foci_pic > cutoff

    return binary

def binarize_canny(pic_source, sensitivity = 5.):

    ht = 5. + ((10 - sensitivity)/5.)*20.

#    print ht

    edges = filt.canny(pic_source, sigma = 3, high_threshold = ht, low_threshold = 2.)

    selem_morph = np.array([0,1,0,1,1,1,0,1,0], dtype=bool).reshape((3,3))

    for i in (1,2):
        edges = morphology.binary_dilation(edges, selem_morph)

#    misc.imsave('/home/varnivey/Data/Biophys/Burnazyan/Experiments/fluor_calc/test/edges.jpg', edges)

#    binary = ndimage.binary_fill_holes(edges)

    labels = measure.label(edges)

    labelcount = np.bincount(labels.ravel())

    bg = np.argmax(labelcount)

    edges[labels != bg] = 255

    selem_med = np.ones((3,3), dtype = bool)

    binary = filt.rank.median(edges, selem_med)

    for i in (1,2,3):
        binary = morphology.binary_erosion(edges, selem_morph)

    return edges


def label_nuclei(binary, min_size):
    '''Label, watershed and remove small objects'''

    distance = ndimage.distance_transform_edt(binary)

    distance_blured = ndimage.gaussian_filter(distance, 5)

    local_maxi = feature.peak_local_max(distance_blured, indices=False, labels=binary, min_distance = 30)

    markers = measure.label(local_maxi)

#    markers[~binary] = -1

#    labels_rw = segmentation.random_walker(binary, markers)

#    labels_rw[labels_rw == -1] = 0

#    labels_rw = segmentation.relabel_sequential(labels_rw)

    labels_ws = morphology.watershed(-distance, markers, mask=binary)

    labels_large = morphology.remove_small_objects(labels_ws,min_size)

    labels_clean_border = clear_border(labels_large)

    labels_from_one = segmentation.relabel_sequential(labels_clean_border)

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

    hsv_result = np.hstack((hue,sat,val))

    hsv_result.resize(pic_shape)

    rgb_result = color.hsv2rgb(hsv_result).astype(np.uint8)

    return rgb_result


def nice_merged_pic(source_nuclei, source_foci, nuclei, foci, color_nuclei=0., color_foci=0.33):
    '''Returns enchanced picture with black bg and merged channels inside the objects'''


    pic_shape = list(nuclei.shape)
    pic_shape.append(3)

    nuclei = (nuclei != 0)
    foci   = (foci   != 0)

    nuclei_only = nuclei - foci

    hue = color_nuclei*nuclei_only + foci*color_foci

    foci_enhanced = 255 - np.floor((255 - source_foci)*0.8)

    val = source_nuclei*nuclei_only + foci*foci_enhanced

#    val = nuclei*((source_nuclei > foci_enhanced)*source_nuclei + (source_nuclei < foci_enhanced)*foci_enhanced)

    sat = nuclei*1.

    hsv_result = np.hstack((hue,sat,val))

    hsv_result.resize(pic_shape)

    rgb_result = color.hsv2rgb(hsv_result).astype(np.uint8)

#    rgb_blured = ndimage.gaussian_filter(rgb_result, 3)

    return rgb_result

def rescaled_pic(labels, source_pic):
    '''Returns pic with rescaled contrast for all oblects'''

    labels_num = np.max(labels)

    rescaled_pics = []

    for label_num in np.arange(labels_num) + 1:

        label = (labels == label_num)
        label_pic = label*source_pic

        label_values = np.extract(label, label_pic)
        p2, p100 = np.percentile(label_values, (2, 100))

        rescaled_pics.append(exposure.rescale_intensity(label_pic, in_range=(p2, p100)))

        rescaled_label_values = np.extract(label, rescaled_pics[-1])

        print str(label_num).rjust(4), str(round(np.mean(label_values),3)).rjust(10), str(round(np.mean(rescaled_label_values),3)).rjust(10)

    return sum(rescaled_pics)


def normalized_pic(labels, source_pic):
    '''Returns pic with equal mean intensity for all objects'''

    labels_num = np.max(labels)

    new_values = []
    label_pics = []

    for label_num in np.arange(labels_num) + 1:

        label = (labels == label_num)
        label_pic = label*source_pic

        label_values = np.extract(label, label_pic)

        mean_value = np.mean(label_values, dtype = float)

        new_values.append(label_values/mean_value)
        label_pics.append(label_pic/mean_value)

    p2,p100 = np.percentile(np.concatenate(new_values),(2,100))

    norm_pic = sum(label_pics)

    rescaled_norm_pic = exposure.rescale_intensity(norm_pic, in_range=(p2, p100))

#    return rescaled_norm_pic
    return np.floor(rescaled_norm_pic*255).astype(int)


def normalized_pics(nuclei, source_nuclei, source_foci_pic_list):
    '''Returns pic with equal mean intensity of nuclei and \
            pics with foci intensity normalized on nuclei'''

    labels_num = np.max(nuclei)

    new_nucleus_values = []
    nucleus_pics = []
    mean_values = []

#    foci_pics_list = []


    for label_num in np.arange(labels_num) + 1:

        label = (nuclei == label_num)
        nucleus_pic = label*source_nuclei

        nucleus_values = np.extract(label, nucleus_pic)

        mean_value = np.mean(nucleus_values, dtype = float)

        mean_values.append(mean_value)
        new_nucleus_values.append(nucleus_values/mean_value)
        nucleus_pics.append(nucleus_pic/mean_value)


    p2,p100 = np.percentile(np.concatenate(new_nucleus_values),(2,100))

    norm_nucleus_pic = sum(nucleus_pics)

    rescaled_norm_nucleus_pic = exposure.rescale_intensity(norm_nucleus_pic, in_range=(p2, p100))

    print len(source_foci_pic_list)

    rescaled_norm_foci_pic_list = [normalized_foci(nuclei, source_foci, mean_values) for source_foci in source_foci_pic_list]

    return (rescaled_norm_nucleus_pic, rescaled_norm_foci_pic_list)



def normalized_foci(nuclei, source_foci):
    '''Normalize foci pics using nuclei mean values'''

    labels_num = np.max(nuclei)

    new_foci_values = []
    foci_pics = []

    for label_num in np.arange(labels_num) + 1:

        label = (nuclei == label_num)
        foci_pic = label*source_foci

        foci_values = np.extract(label, foci_pic)

        mean_value = np.percentile(foci_values, (20))

        new_foci_values.append(foci_values/mean_value)
        foci_pics.append(foci_pic/mean_value)

    p2,p100 = np.percentile(np.concatenate(new_foci_values),(2,100))

    norm_foci_pic = sum(foci_pics)

    rescaled_norm_foci_pic = exposure.rescale_intensity(norm_foci_pic, in_range=(p2, p100))

#    return rescaled_norm_foci_pic
    return np.floor(rescaled_norm_foci_pic*255).astype(int)


def normalized_foci_on_bg(nuclei, source_foci):
    '''Returns foci intensity normalized on foci bg'''

    labels_num = np.max(nuclei)

    new_foci_values = []
    foci_pics = []

    for label_num in np.arange(labels_num) + 1:

        label = (nuclei == label_num)
        foci_pic = label*source_foci

        foci_values = np.extract(label, foci_pic)

        p10,p15,p20 = np.percentile(foci_values, (10,15,20))

        mean_value = (p10+p15+p20)/3

        new_foci_values.append(foci_values/mean_value)
        foci_pics.append(foci_pic/mean_value)

    p2,p100 = np.percentile(np.concatenate(new_foci_values),(2,100))

    norm_foci_pic = sum(foci_pics)

    rescaled_norm_foci_pic = exposure.rescale_intensity(norm_foci_pic, in_range=(p2, p100))

#    return rescaled_norm_foci_pic
    return np.floor(rescaled_norm_foci_pic*255).astype(int)




