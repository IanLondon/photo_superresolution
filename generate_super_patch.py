import os
import config
from load_data import load_images, write_images

def gen_patches(model, input_dir, output_dir, max_out=None):
    img_names = os.listdir(input_dir)

    if max_out is not None:
        img_names = img_names[:max_out]

    lossy_patches = load_images(input_dir, img_names)

    predictions = model.predict(lossy_patches)
    write_images(output_dir, img_names, predictions)

    print 'generated %i images with the CNN' % predictions.shape[0]

if __name__ == '__main__':
    import argparse

    import persist

    parser = argparse.ArgumentParser(description='Generate superpatches for testing CNN from patches in LOSSY_DIR, using parameters in config.py')
    parser.add_argument('--modelname', default='convnet00', help='Name of model, eg convnet00.')
    parser.add_argument('--max_out', type=int, default=None, help='Max number of patches to output. If None, it writes all the images in LOSSY_DIR')

    args = parser.parse_args()

    model = persist.load_model(args.modelname)
    gen_patches(model, config.LOSSY_DIR, config.RESULT_DIR, args.max_out)
    print 'done!'
