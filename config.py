MODE = 'sketch'

print 'config mode: "%s"' % MODE

if MODE == 'sketch':
    MODEL_NAME = 'convnet_sketchy'
    FULL_DIR = 'lfw_faces' #original full images from flickr
    CLEAN_DIR = 'clean_patches_sketchy' #non-blurred patches
    LOSSY_DIR = 'lossy_patches_sketchy' #corresponding blurred patches
    RESULT_DIR = 'result_patches_sketchy'

elif MODE == 'deblur':
    MODEL_NAME = 'convnet00'
    FULL_DIR = 'flickr_faces'
    CLEAN_DIR = 'clean_patches'
    LOSSY_DIR = 'lossy_patches'
    RESULT_DIR = 'result_patches'

else:
    raise ValueError('Config mode not understood: "%s"' % MODE)

# Universal settings for all modes
TEMP_WEIGHTS_DIR = 'temp_weights'
PATCH_FILE_EXT = '.png'

PATCHES_PER_IMG = 5
WINDOW_SIZE = 33
DOWNSIZE_SIZE = 11

VERBOSITY = 10 #used when printing progress in downloader.py

# Convolutional neural network parameters
EPOCHS = 100
BATCH_SIZE = 32
