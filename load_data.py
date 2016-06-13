import os
import numpy as np
import cv2
import config

def read_img(filename):
    # It's grayscale already, just take the R channel.
    return cv2.imread(filename)[:,:,0, np.newaxis]

def load_images(directory_name, filenames=None):
    """
    Reads all the images in a directory and places them into a numpy array
    with dimensions that the CNN in Keras expects as an input.
    """
    if filenames is None:
        filenames = os.listdir(directory_name)

    images = np.array([read_img(os.path.join(directory_name, filename)) for filename in filenames])
    return np.swapaxes(np.array(images), 3, 1)

def write_images(directory_name, filenames, image_array):
    # print image_array.shape # (65, 1, 33, 33)
    for img, filename in zip(image_array, filenames):
        img = np.swapaxes(img, 0, 2)
        cv2.imwrite(os.path.join(directory_name, filename), img)

def get_subimages():
    # load up all the subimages in the directory
    # the names match between lossy and clean, so take all the names from LOSSY_DIR (eg '4_2.png')
    subimage_filenames = os.listdir(config.LOSSY_DIR)

    subimages_lossy = load_images(config.LOSSY_DIR, subimage_filenames)
    subimages_clean = load_images(config.CLEAN_DIR, subimage_filenames)
    # subimages_clean = [read_img(os.path.join(config.CLEAN_DIR, filename)) for filename in subimage_filenames]

    print 'got %i subimages' % len(subimage_filenames)
    print 'debug: subimages_lossy.shape is', subimages_lossy.shape

    return subimages_lossy, subimages_clean
