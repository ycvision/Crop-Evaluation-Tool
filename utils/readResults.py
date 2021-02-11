import pickle
import numpy as np
import glob
import pickle
import os


def read_result(file_path):
    with open(file_path, 'rb') as f:
        r = pickle.load(f)
    return r


if __name__ == "__main__":
    folder = "../QID3_FILE_ID"
    assert os.path.exists(folder)
    file_paths = glob.glob(os.path.join(folder, "*.pkl"))
    numCandidates = len(file_paths)
    data = np.zeros((numCandidates, 7))
    for idx, file_path in enumerate(file_paths):
        r = read_result(file_path)
        res = []
        for i, (k, v) in enumerate(r.items()):
            res.append(v)
        res = np.array(res)
        assert res.shape == (100, 7)
        data[idx] = np.sum(res, axis=0)
    print("Average:\t{}".format(np.average(data, axis=0)))
    print("STD:\t\t{}".format(np.std(data, axis=0)))