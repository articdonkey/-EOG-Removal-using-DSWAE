import datetime
import random

import numpy
import scipy.io

from SAE import trainSAE
from utility import haarDecompose, LEVEL, NOL, gamma, ADDITIONAL_LENGTH

#shuffle the data for what?
def loadData(filename):
    path = '.\\data_EOG\\'+filename
    data = scipy.io.loadmat(path)['data_train']
    indexes = [x for x in range(data.shape[1])]
    random.shuffle(indexes)
    res = data.copy()
    for key, val in enumerate(indexes):
        res[:, key] = data[:, val]
    # print(type(res), res.shape)
    # plt.figure(1)
    # plt.subplot(211)
    # plt.plot(data)
    return res


def wavelet(data, level):
    m, n = data.shape
    res = None
    for i in range(n):
        decomposeData = haarDecompose(data[:, i], level)
        ele = numpy.asarray([])
        for j in range(NOL):
            ele = numpy.concatenate((ele.flatten(), decomposeData[j].flatten()))
        ele = ele.reshape(-1, 1)
        # tmp = ele.shape
        if res is None:
            res = numpy.zeros((ele.shape[0], n), dtype=numpy.float64)
        res[:, i] = ele[:, 0]
    return res * gamma


#if __name__ == '__main__':
def training_SAE(traindata_loc):
#    traindata_loc='traindata14.mat'
    train_data = loadData(traindata_loc)
    train_data = wavelet(train_data, LEVEL)

    time_start = datetime.datetime.now()
    encoder = trainSAE(data=train_data)
    time_end = datetime.datetime.now()
    print("time: ", time_end - time_start)
    theta = encoder.theta

    """ save trained model to .mat file """
    now = datetime.datetime.now()
#    matfile = '_'.join([str(layer.nNode) for layer in encoder.layers]) + now.strftime('_%m-%d-%YT%H%M') + '.mat'
    matfile='my_model.mat'
    scipy.io.savemat('.\\models\\' + matfile, {
        'rho': encoder.rho,
        'lamda': encoder.lamda,
        'beta': encoder.beta,
        'nHiddenLayer': encoder.nHiddenLayer,
        'nNodeArr': [layer.nNode for layer in encoder.layers],
        'theta': theta,
        'gamma': gamma,
        'LEVEL': LEVEL,
        'NOL': NOL,
        'ADDITIONAL_LENGTH': ADDITIONAL_LENGTH
    }
                     )
    print('Save file successfully!', matfile)

    # model = loadModel(matfile)
    # """ Initialize the Autoencoder with the above parameters """
    # # encoder = SAE(nHiddenLayer, nNodeArr, lamda, beta, rho)
    # encoder1 = SAE(model.get('nHiddenLayer'), model.get('nNodeArr'), model.get('lamda'), model.get('beta'),
    #                model.get('rho'))
    # encoder1.extractTheta(model['theta'])
    # encoder1.theta = encoder1.compressTheta()

    # print(encoder1 == encoder)
