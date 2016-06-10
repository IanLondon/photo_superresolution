FULL_DIR = 'flickr_faces' #original full images from flickr
CLEAN_DIR = 'clean_patches' #non-blurred patches
LOSSY_DIR = 'lossy_patches' #corresponding blurred patches
PATCH_FILE_EXT = '.png'

RESULT_DIR = 'result_patches'

PATCHES_PER_IMG = 5
WINDOW_SIZE = 33
DOWNSIZE_SIZE = 11

VERBOSITY = 10 #used when printing progress in downloader.py

# Convolutional neural network parameters
EPOCHS = 10
BATCH_SIZE = 32
