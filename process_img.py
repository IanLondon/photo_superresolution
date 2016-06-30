import numpy as np
from warnings import warn

def process_img(orig_img, model, stride, window_size):
    """
    Feeds windows of window_size x window_size to the CNN model to get subimages,
    then and combines the subimages together into a resultant image.
    Overlapping windows get pixel values averaged together.

    orig_img : numpy array representing original image. Single channel only!
        For multiple channels, pass them one by one (for now)

    model : trained keras convnet model
    """
    if stride > window_size:
        warn('Stride is bigger than window size, there will be gaps')

    height, width = orig_img.shape
    result = np.zeros(orig_img.shape)

    # Average overlapping subimages together:
    # Keep track of how many subimage values have been added
    # to each pixel so you can divide the pixel by that number later
    # to get the average.
    pixelwise_count = np.zeros(result.shape)
    window_counter = np.ones((window_size,)*2)

    subimages = []

    x_range = range(0, width-window_size+1, stride)
    y_range = range(0, height-window_size+1, stride)

    # make sure to include the "last" patch so there's no gap at the end
    x_last = width - window_size
    y_last = height - window_size

    if x_range[-1] != x_last:
        x_range += [x_last]
    if y_range[-1] != y_last:
        y_range += [y_last]

    # gather all subimages
    for x in x_range:
        for y in y_range:
            window_slice = np.index_exp[y:y+window_size,x:x+window_size]

            subimage = np.array(orig_img[window_slice]).reshape(1,window_size,window_size)
            subimages.append(subimage)

    subimages = np.array(subimages)
    print 'predicting with array', subimages.shape

    new_subimages = model.predict(subimages)
    print 'predicted! mapping to image'

    # add all the subimages to the corresponding position on the result array
    # and keep track of how many values have been added to each pixel
    subimg_no = 0
    for x in x_range:
        for y in y_range:
            window_slice = np.index_exp[y:y+window_size,x:x+window_size]

            result[window_slice] += new_subimages[subimg_no,0,:,:]

            pixelwise_count[window_slice] += window_counter
            subimg_no += 1

    # average the pixels
    result /= pixelwise_count

    return result

if __name__ == '__main__':
    import argparse
    import cv2
    from persist import load_model
    import config

    parser = argparse.ArgumentParser(description='Generate images using a trained model with a sliding window.')
    parser.add_argument('--input', help='Name of input image file')
    parser.add_argument('--output', help='Name of output image file')
    parser.add_argument('--stride', default=config.WINDOW_SIZE, type=int)
    parser.add_argument('--upscale', default=3.0, type=float, help='For deblur mode, scales the image by this factor. Default is 3.0. Ignored in sketch mode.')
    parser.add_argument('--model', default=None, help='Name of model to use.')

    args = parser.parse_args()

    modelname = args.model or config.MODEL_NAME
    print 'loading model "%s"' % modelname
    model = load_model(modelname)
    print 'using stride %i and window size %i' % (args.stride, config.WINDOW_SIZE)

    orig = cv2.imread(args.input)

    if config.MODE == 'sketch':
        print 'resizing image to 250x250 for sketch'
        print 'and just loading the Red channel.'
        orig = orig[:,:,0]
        orig = cv2.resize(orig, dsize=(250,)*2, interpolation=cv2.INTER_CUBIC)
        result = process_img(orig, model, stride=args.stride, window_size=config.WINDOW_SIZE)
    elif config.MODE == 'deblur':
        upscale = args.upscale
        print 'upsizing image by %ix' % upscale
        print 'size was', orig.shape
        orig = cv2.resize(orig, dsize=(0,0), fx=upscale, fy=upscale, interpolation=cv2.INTER_CUBIC)
        print 'resized to', orig.shape

        result_rgb = []
        for channel_no in range(3):
            channel_prediction = process_img(orig[:,:,channel_no], model,
                stride=args.stride, window_size=config.WINDOW_SIZE)
            result_rgb.append(channel_prediction)
            print 'done channel %i' % channel_no

        # reconstuct RGB array from the 3 channels
        result = np.array(result_rgb).swapaxes(0,2).swapaxes(0,1)
    else:
        raise NotImplementedError('Unsupported config mode: "%s"' % config.MODE)

    # write out the result
    cv2.imwrite(args.output, result)
