###########################################################################################
""" Normalize the dataset provided as input """
import time
from math import sqrt

import matplotlib.pyplot
import numpy
import scipy.io
import scipy.optimize
# SETTING
from pywt import wavedec, waverec

# vis_patch_side = None
rho = 0.04  # desired average activation of hidden units
lamda = 0.0001  # weight decay parameter
gamma = 0.01 #for wavelet transform to produce new wavelet?
beta = 0.005  # weight of sparsity penalty term
# num_patches = 10000  # number of training examples
max_iterations = 1000  # number of optimization iterations
nHiddenLayer = 5
#nNodeArr = [127, 256, 256, 128, 164, 256, 127]
nNodeArr = [32, 64, 128, 64, 32, 16, 32]
#parameter for playing game dataset
#nNodeArr = [128, 256, 256, 128, 164, 256, 128]
#LENGTH = 128
#MAX_FRE = 128
LENGTH = 128
MAX_FRE = 128 
NOL = 5
LEVEL = 6
ADDITIONAL_LENGTH = 5


def normalizeDataset(dataset):
    """ Remove mean of dataset """

    dataset = dataset - numpy.mean(dataset)

    """ Truncate to +/-3 standard deviations and scale to -1 to 1 """

    std_dev = 3 * numpy.std(dataset)
    dataset = numpy.maximum(numpy.minimum(dataset, std_dev), -std_dev) / std_dev

    """ Rescale from [-1, 1] to [0.1, 0.9] """

    dataset = (dataset + 1) * 0.4 + 0.1

    return dataset


###########################################################################################
""" Randomly samples image patches, normalizes them and returns as dataset """


def loadDataset(num_patches, patch_side):
    """ Load images into numpy array """

    images = scipy.io.loadmat('IMAGES.mat')
    images = images['IMAGES']

    """ Initialize dataset as array of zeros """

    dataset = numpy.zeros((patch_side * patch_side, num_patches))

    """ Initialize random numbers for random sampling of images
        There are 10 images of size 512 X 512 """

    rand = numpy.random.RandomState(int(time.time()))
    image_indices = rand.randint(512 - patch_side, size=(num_patches, 2))
    image_number = rand.randint(10, size=num_patches)

    """ Sample 'num_patches' random image patches """

    for i in range(num_patches):
        """ Initialize indices for patch extraction """

        index1 = image_indices[i, 0]
        index2 = image_indices[i, 1]
        index3 = image_number[i]

        """ Extract patch and store it as a column """

        patch = images[index1:index1 + patch_side, index2:index2 + patch_side, index3]
        patch = patch.flatten()
        dataset[:, i] = patch

    """ Normalize and return the dataset """

    dataset = normalizeDataset(dataset)
    return dataset


###########################################################################################
""" Visualizes the obtained optimal W1 values as images """


def visualize(pos, encoder, title='', nrows=None, ncols=None, npixelX=None, npixelY=None):
    if len(encoder.weights) < pos:
        print('index of weight, which need is not correct!')
        return

    pos = pos - 1
    sizeX = encoder.layers[pos + 1].nNode
    sizeY = encoder.layers[pos].nNode
    weight = encoder.weights[pos]

    weight_square = numpy.zeros(shape=(1, sizeY))
    for i in range(sizeX):
        weight_square += numpy.multiply(weight.W[i], weight.W[i])
    weight_sum_root_square = numpy.sqrt(weight_square)
    # print(weight_sum_root_square)

    """ Add the weights as a matrix of images """
    if nrows is None:
        nrows = int(sqrt(sizeX))
        ncols = nrows
    figure, axes = matplotlib.pyplot.subplots(nrows=nrows,
                                              ncols=ncols)
    index = 0

    for axis in axes.flat:
        tuso = weight.W[index]
        xi = numpy.true_divide(tuso, weight_sum_root_square)
        # print(kq)
        """ Add row of weights as an image to the plot """
        if npixelX is None:
            npixelX = int(sqrt(sizeY))
            npixelY = npixelX

        image = axis.imshow(xi.reshape(npixelX, npixelY),
                            cmap=matplotlib.pyplot.cm.gray, interpolation='nearest')
        axis.set_frame_on(False)
        axis.set_axis_off()
        index += 1

    """ Show the obtained plot """

    figure.suptitle(title, fontsize=16)
    matplotlib.pyplot.show()


def loadSetting():
    return [rho, lamda, beta,
            max_iterations, nHiddenLayer, nNodeArr]


def loadTheta():
    return scipy.io.loadmat('theta.mat')['theta']


def loadData():
    return scipy.io.loadmat('data.mat')['data']


def haarDecompose(data, level):
    coeffs = wavedec(data, 'haar', level=level)
    return coeffs


def haarReconstruct(coeffs):
    res = waverec(coeffs, 'haar')
    return res

#print(new_signal)
#print(new_signal.flatten().shape)