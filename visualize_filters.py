import os
import numpy as np
import cv2
from sklearn.preprocessing import MinMaxScaler

def visualize_filters(model, layer_no=0, filter_dir='filters', final_size=(250,250)):
    """
    Save 2d filters as image files in the filter_dir directory.
    """
    weights = model.layers[layer_no].get_weights()[0]
    scaler = MinMaxScaler((0,255))
    print 'weights.shape:', weights.shape
    assert weights[0].shape[0] == 1, ('Expected 1-deep dimension for each weight, do you have 3d instead of 2d?')
    filters = [scaler.fit_transform(filter_array[0,:,:]) for filter_array in weights]
    # sort by variance
    # filters.sort(key=np.var)
    for idx, filt in enumerate(filters):
        assert len(filt.shape) == 2, ('Expected 2D filter, got:', filt.shape)
        img_path = os.path.join(filter_dir, str(idx)) + '.png'
        # scale up filter so you can see it on presentation slides, etc
        final = cv2.resize(filt, dsize=final_size, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(img_path, final, )
    print 'wrote %i filters to directory %s/.' % (len(filters), filter_dir)

if __name__ == '__main__':
    import persist
    model = persist.load_model('convnet00')
    visualize_filters(model)
