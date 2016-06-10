# from load_data import TODO
import persist
import config
import load_data
# from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
# from keras.models import Model

from keras.models import Sequential
from keras.layers.convolutional import Convolution2D

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

subimages_lossy, subimages_clean = load_data.get_subimages()

model.fit(subimages_lossy, subimages_clean, nb_epoch=config.EPOCHS, batch_size=config.BATCH_SIZE)

persist.save_model(model, 'convnet00')

# input_img = Input(shape=(1, 28, 28))
#
# x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(input_img)
# x = MaxPooling2D((2, 2), border_mode='same')(x)
# x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
# x = MaxPooling2D((2, 2), border_mode='same')(x)
# x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
# encoded = MaxPooling2D((2, 2), border_mode='same')(x)
#
# # at this point the representation is (8, 4, 4) i.e. 128-dimensional
#
# x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(encoded)
# x = UpSampling2D((2, 2))(x)
# x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
# x = UpSampling2D((2, 2))(x)
# x = Convolution2D(16, 3, 3, activation='relu')(x)
# x = UpSampling2D((2, 2))(x)
# decoded = Convolution2D(1, 3, 3, activation='sigmoid', border_mode='same')(x)
#
# autoencoder = Model(input_img, decoded)
# autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
#
# x_train, x_test = load_mnist(flatten=False)
#
# epochs = 10
#
# autoencoder.fit(x_train, x_train,
#                 nb_epoch=epochs,
#                 batch_size=128,
#                 shuffle=True,
#                 validation_data=(x_test, x_test))
#
# # encoded_imgs = encoder.predict(x_test)
# decoded_imgs = autoencoder.predict(x_test)
# # decoded_imgs = decoder.predict(encoded_imgs)
#
# persist.save_model(autoencoder, 'conv_autoencoder')
#
# show_mnist_results(decoded_imgs, x_test, 'convolutional')
