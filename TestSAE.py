import matplotlib.pyplot as plt
import numpy
import scipy.io

from SAE import SAE
from utility import haarDecompose, haarReconstruct, visualize


def loadModel(filename):
    path = '.\\models\\' + filename
    tmp = scipy.io.loadmat(path)

    tmp['rho'] = tmp['rho'][0].tolist()[0]
    tmp['NOL'] = tmp['NOL'][0].tolist()[0]
    tmp['LEVEL'] = tmp['LEVEL'][0].tolist()[0]
    tmp['lamda'] = tmp['lamda'][0].tolist()[0]
    tmp['beta'] = tmp['beta'][0].tolist()[0]
    tmp['ADDITIONAL_LENGTH'] = tmp['ADDITIONAL_LENGTH'][0].tolist()[0]
    tmp['nHiddenLayer'] = tmp['nHiddenLayer'][0].tolist()[0]
    tmp['gamma'] = tmp['gamma'][0].tolist()[0]
    tmp['theta'] = tmp['theta'].flatten()
    tmp['nNodeArr'] = tmp['nNodeArr'][0].tolist()
    return tmp


def loadTestData(filename):
    path = '.\\data_EOG\\'+filename
    tmp = scipy.io.loadmat(path)
    return tmp['segments'], tmp['EOGs'], tmp['data_test'], tmp['oriSegments']


def standardize(signal, before_data, after_data):
    res = signal
    if len(before_data) >= 32:
       before_data = before_data[len(before_data) - 32:]
    if len(after_data) >= 32:
       after_data = after_data[:32]

    combine_array = numpy.concatenate((before_data, after_data))
    maxEEG = max(combine_array) * 50 / 100
    minEEG = min(combine_array) * 50 / 100
#    print(res)
    maxSAE = max(res)
    minSAE = min(res)

    for index, val in enumerate(res):
        correctVal = (val - minSAE) / (maxSAE - minSAE) \
                     * (maxEEG - minEEG) + minEEG
        res[index] = correctVal
    return res


#if __name__ == '__main__':
def testing_SAE(testdata_loc):
    model = loadModel('my_model.mat')
    """ Initialize the Autoencoder with the parameters in trained model """
    # encoder = SAE(nHiddenLayer, nNodeArr, lamda, beta, rho)
    encoder = SAE(model.get('nHiddenLayer'), model.get('nNodeArr'), model.get('lamda'), model.get('beta'),
                  model.get('rho'))
    encoder.extractTheta(model['theta'])
    encoder.theta = encoder.compressTheta()
    # print(encoder)
    # visualize(1, encoder, nrows=4, ncols=8, npixelX=4, npixelY=4)
    #segments, EOGs, data, oriSegments = loadTestData('testdata.mat')
    #testdata_loc='testdata01.mat'
    segments, EOGs, data, oriSegments = loadTestData(testdata_loc)
    fixed_data = data.copy().flatten()
    fixed_data1 = data.copy().flatten()
    m, n = EOGs.shape
    for i in range(n):
        """ decompose EOG segment by wavelet level 6"""
        decomposeData = haarDecompose(EOGs[:, i], model.get('LEVEL'))

        """ get wavelet of low frequencies"""
        wavelet = numpy.asarray([])
        for j in range(model.get('NOL')):
            wavelet = numpy.concatenate((wavelet.flatten(), decomposeData[j].flatten()))
        wavelet = wavelet.reshape(-1, 1)
        # tmp = ele.shape
        wavelet = wavelet * model.get('gamma')

        """ use model to predict right signal"""
        new_wavelet = encoder.calcOutput(wavelet) * (1 / model.get('gamma'))
        new_wavelet = new_wavelet.reshape(1, -1)

        """ replace decompose data by new_wavelet """
        # print(new_wavelet)
        new_decomposeData = decomposeData.copy()
        pos = 0
        for j in range(model.get('NOL')):
            new_decomposeData[j] = new_wavelet[0, pos:pos + len(new_decomposeData[j])]
            pos = pos + len(new_decomposeData[j])

        """ reconstruct data by new decompose data"""
        new_signal = haarReconstruct(new_decomposeData)
        
        """ replace new signal to raw data"""
        d, c = segments[i]
        oriD, oriC = oriSegments[i]
        d = d - 1
        c = c - 1
        oriD -= 1
        oriC -= 1
        sP = oriD - d
        addFi = min(sP, model.get('ADDITIONAL_LENGTH'))
        # addFi = min(sP, 5)
        # addLa = min(c - oriC, 5)
        addLa = min(c - oriC, model.get('ADDITIONAL_LENGTH'))
        eP = sP + oriC - oriD
        # print(d, c)
        
        """ calc new signal with quantile function"""
        if i == n - 1:
            new_signal_fixed = standardize(new_signal.flatten()[sP - addFi:eP + addLa],
                                           fixed_data1[:oriD - addFi], fixed_data1[oriC + addLa:])
        else:
            """ calc next segment"""
            d1, c1 = segments[i + 1]
            oriD1, oriC1 = oriSegments[i + 1]
            d1 = d1 - 1
            c1 = c1 - 1
            oriD1 -= 1
            oriC1 -= 1
            sP1 = oriD1 - d1
            addFi1 = min(sP1, model.get('ADDITIONAL_LENGTH'))
            addLa1 = min(c1 - oriC1, model.get('ADDITIONAL_LENGTH'))
            eP1 = sP1 + oriC1 - oriD1
            endP = oriD1 - addFi1
            if oriC + addLa >= endP:
                afte_data = []
            else:
                afte_data = fixed_data1[oriC + addLa:endP]
            new_signal_fixed = standardize(new_signal.flatten()[sP - addFi:eP + addLa],
                                           fixed_data1[:oriD - addFi], afte_data)
        fixed_data1 = numpy.concatenate((fixed_data1[:oriD - addFi],
                                         new_signal_fixed,
                                         fixed_data1[oriC + addLa:]))

    """ plot """
    axs1 = plt.subplot(211)
    plt.plot(data.flatten())
    plt.title('Compare 2 signal')
    plt.ylabel('Raw data')

    plt.subplot(212, sharex=axs1, sharey=axs1)
    plt.plot(fixed_data1)
    plt.xlabel('sample')
    plt.ylabel('Fixed by DWSAE')

    scipy.io.savemat('.\\' + 'SAE.mat', {
        'data': fixed_data1,
    })
    plt.show()
    print('Fix EOGs sucessfully')
    return fixed_data1
 
  
