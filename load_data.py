import os
import numpy as np
import cv2
import config

def read_img(filename):
    # It's grayscale already, just take the R channel.
    return cv2.imread(filename)[:,:,0, np.newaxis]

def format_images(directory_name, filenames):
    images = np.array([read_img(os.path.join(directory_name, filename)) for filename in filenames])
    return np.swapaxes(np.array(images), 3, 1)

def get_subimages():
    # load up all the subimages in the directory
    # the names match between lossy and clean, so take all the names from LOSSY_DIR (eg '4_2.png')
    subimage_filenames = [filename for filename in os.listdir(config.LOSSY_DIR)]

    subimages_lossy = format_images(config.LOSSY_DIR, subimage_filenames)
    subimages_clean = format_images(config.CLEAN_DIR, subimage_filenames)
    # subimages_clean = [read_img(os.path.join(config.CLEAN_DIR, filename)) for filename in subimage_filenames]

    print 'got %i subimages' % len(subimage_filenames)
    print 'debug: subimages_lossy.shape is', subimages_lossy.shape

    return subimages_lossy, subimages_clean
