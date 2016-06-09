import os
import numpy as np

# TODO: don't have 2 diff version of urllib
import urllib
from urllib2 import urlopen
import flickrapi

import config
import secrets

import cv2
print 'OpenCV Version (made to work with 3.1.0):'
print cv2.__version__

def crop_img(img, x, y, window_size):
    x2, y2 = x + window_size, y + window_size
    return img[y:y2,x:x2]

def random_crop(img, window_size):
    img_height, img_width = img.shape[:2]

    if (window_size > img_height) or (window_size > img_width):
        raise ValueError('img has resolution %i x %i, too small for %i px window' % (img_height, img_width, window_size))

    x = np.random.randint(0, img_width - window_size + 1)
    y = np.random.randint(0, img_height - window_size + 1)

    return crop_img(img, x, y, window_size)

def make_patches(img, n_patches, window_size, downsize_size):
    """
    Make n_patches random patches from a greyscale-converted image,
    which are squares of window_size pixels wide and tall.

    A lossy version is created by scaling the image down to a
    downsize_size pixel square then interpolate it back up to the
    original window size.

    Yields two patches: clean_crop, lossy_crop
    """
    downsize_tuple = (downsize_size,)*2
    windowsize_tuple = (window_size,)*2

    # convert to greyscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for _ in range(n_patches):
        clean_crop = random_crop(img, window_size)
        lossy_crop = cv2.resize(clean_crop, downsize_tuple, interpolation=cv2.INTER_AREA)
        lossy_crop = cv2.resize(lossy_crop, windowsize_tuple, interpolation=cv2.INTER_LINEAR)
        yield clean_crop, lossy_crop

def prev_filenumber(directory_names=[config.CLEAN_DIR, config.LOSSY_DIR]):
    """
    Get the highest filenumber in either folder
    or return False if no files are found
    """
    all_filenumbers = [int(filename.split('.')[0])
         for directory_name in directory_names
         for filename in os.listdir(directory_name)
        ]
    if all_filenumbers:
        return max(all_filenumbers)
    else:
        return False

def save_patches(*args, **kwargs):
    """Generate patches from a single image and save to disk"""
    prev_no = prev_filenumber()
    initial_no = prev_no or -1
    for idx, (clean, lossy) in enumerate(make_patches(*args, **kwargs)):
        fileno = idx + initial_no + 1
        cv2.imwrite(os.path.join(config.CLEAN_DIR, str(fileno) + config.FILE_EXT), clean)
        cv2.imwrite(os.path.join(config.LOSSY_DIR, str(fileno) + config.FILE_EXT), lossy)

def get_photo_url(photo_json):
    # https://www.flickr.com/services/api/misc.urls.html
    template = "http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_b.jpg"
    url = template.format(**photo_json)

    return url

def create_opencv_image_from_url(url, cv2_img_flag=0):
    #From http://stackoverflow.com/questions/13329445/how-to-read-image-from-in-memory-buffer-stringio-or-from-url-with-opencv-pytho
    request = urlopen(url)
    img_array = np.asarray(bytearray(request.read()), dtype=np.uint8)
    # Throws TypeError if image is invalid or does not exist
    return cv2.imdecode(img_array, cv2_img_flag)

def all_img_urls(flickr_api, tags):
    """
    Gets urls for all photos available from the flickr API that
    have the given tags.

    flickr_api : an instance of flickrapi.FlickrAPI
    tags : a list of strings
    """
    first_page = flickr_api.photos.search(tags=tags, per_page='500', page=1)
    no_pages = first_page['photos']['pages']
    for page_no in range(1,no_pages+1):
        photos = flickr_api.photos.search(tags=tags, per_page='500', page=page_no)
        for photo in photos['photos']['photo']:
            yield get_photo_url(photo)

def save_imgs_from_urls(urls, dest_dir, verbosity=False):
    prev_no = prev_filenumber([dest_dir])
    if prev_no is not False:
        print 'existing files found, resuming after file #%i' % prev_no
        starting_no = prev_no
    else:
        starting_no = -1

    for idx, url in enumerate(urls):
        if idx > starting_no:
            urllib.urlretrieve(url, os.path.join(dest_dir,"%i.jpg" % idx))

        if verbosity is not False and idx % verbosity == 0:
            print 'downloading... up to file #%i (started at %i)' % (idx, prev_no)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def save_urls_to_file(flickr_api, url_file, tags):
    img_urls = all_img_urls(flickr_api, tags)
    with open(url_file, 'w') as f:
        for url in img_urls:
            f.write(url + '\n')

def download_all_imgs(url_file, img_dir, verbosity=20):
    img_count = 0
    url_len = file_len(url_file)
    print '%i image urls in file' % url_len
    with open(url_file, 'r') as f:
        img_urls = (url for url in f)
        save_imgs_from_urls(img_urls, img_dir, verbosity)
    print 'downloads complete.'
