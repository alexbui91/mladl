import pickle
import os.path as path


def save_file(name, obj):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_file(pathfile):
    if path.exists(pathfile):
        with open(pathfile, 'rb') as f:
            data = pickle.load(f)
        return data 