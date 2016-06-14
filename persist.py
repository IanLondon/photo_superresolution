import os
from keras.models import model_from_json

def save_model(model, modelname, overwrite=True):
    json_string = model.to_json()
    open('%s.json' % modelname, 'w').write(json_string)
    model.save_weights('%s.h5' % modelname, overwrite=overwrite)
    print 'saved "%s" json and 5h files' % modelname

def model_exists(modelname):
    return os.path.isfile('%s.json' % modelname) and os.path.isfile('%s.h5' % modelname)

def load_model(modelname, compile_model=True):
    model = model_from_json(open('%s.json' % modelname).read())
    print 'loaded "%s" json and 5h files' % modelname
    if compile_model:
        # model must be compiled before use
        model.compile(optimizer='adadelta', loss='mse')
    model.load_weights('%s.h5' % modelname)
    return model
