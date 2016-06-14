import os
import persist
import config
import load_data
# from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
# from keras.models import Model

from keras.models import Sequential
from keras.layers.convolutional import Convolution2D
from keras.callbacks import ModelCheckpoint

model_name = config.MODEL_NAME

print 'training model "%s"' % (model_name)
print 'NOTE: If model was terminated early, you have to manually replace the weights'
print '(looks at %s.h5 in current dir for weights to resume with)' % model_name

if persist.model_exists(model_name):
    print 'found existing model for "%s", continuing training...' % model_name
    model = persist.load_model(model_name)
else:
    print 'no persisted model found, starting from scratch.'
    channels = 1 # greyscale
    # each sub-image is a square, of WINDOW_SIZE x WINDOW_SIZE pixels.
    input_shape = (channels, config.WINDOW_SIZE, config.WINDOW_SIZE)

    model = Sequential()
    # 9x9 convolution with 64 filters to get patches representation
    model.add(Convolution2D(64, 9, 9, border_mode='same', activation='relu', input_shape=input_shape))
    # 1x1 convolution with 32 filters, add some nonlinearity
    model.add(Convolution2D(32, 1, 1, border_mode='same', activation='relu'))
    # 5x5 convolution with 1 filter for greyscale or 3 filters for RGB
    # for linear flattening, "averaging" the patches
    model.add(Convolution2D(channels, 5, 5, border_mode='same', activation='linear'))

    model.compile(loss='mean_squared_error', optimizer='adadelta')

print 'loading images into memory (if this hangs, use a generator instead)'
subimages_lossy, subimages_clean = load_data.get_subimages()

print 'training model...'
temp_weights_path = os.path.join(config.TEMP_WEIGHTS_DIR, '%s_{epoch}.h5' % model_name)
backups = ModelCheckpoint(filepath=temp_weights_path, verbose=1)
current_checkpoint = ModelCheckpoint(filepath='%s.h5' % model_name, verbose=1)

model.fit(subimages_lossy, subimages_clean, nb_epoch=config.EPOCHS,
    batch_size=config.BATCH_SIZE, callbacks=[backups, current_checkpoint])

# save the final weights
persist.save_model(model, model_name)
