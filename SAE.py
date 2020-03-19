import math
import time

import numpy
import scipy.optimize

from utility import loadSetting


class Layer:
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + numpy.exp(-x))

    def __init__(self, nNode):
        self.nNode = nNode
        self.input = None
        self.output = None

    def setInput(self, value):
        self.input = value

    def calOutput(self):
        raise NotImplementedError


class HiddenLayer(Layer):
    def calOutput(self):
        self.output = self.sigmoid(self.input)


class InputLayer(Layer):
    def calOutput(self):
        self.output = self.input


class OutputLayer(Layer):
    def calOutput(self):
        self.output = self.sigmoid(self.input)


class Weight:
    def __init__(self, sizeX, sizeY):
        r = math.sqrt(6) / math.sqrt(sizeX + sizeY + 1) #why square(6)?
        rand = numpy.random.RandomState(int(time.time()))
        self.W = numpy.asarray(rand.uniform(low=-r, high=r, size=(sizeX, sizeY)))

    def setW(self, value):
        self.W = value

    def getSize(self):
        return self.W.shape


class Bias:
    def __init__(self, size):
        self.b = numpy.zeros((size, 1))

    def setB(self, value):
        self.b = value


class SAE:
    def __init__(self, nHiddenLayer, nNodeArr, lamda, beta, rho):
        self.lamda = lamda
        self.beta = beta
        self.rho = rho
        self.nHiddenLayer = nHiddenLayer
        self.layers = []
        self.initLayer(nHiddenLayer, nNodeArr)
        self.weights = []
        self.initWeight(nHiddenLayer)
        self.biases = []
        self.initBias(nHiddenLayer)
        self.theta = self.compressTheta()

    def costFunction(self, theta, inputData):
        """ Extract weights and biases from 'theta' inputData """

        self.extractTheta(theta)

        """ Compute output layers by performing a feedforward pass
            Computation is done for all the training inputs simultaneously """

        self.layers[0].setInput(inputData)
        for index, layer in enumerate(self.layers):
            layer.calOutput()
            if index != self.nHiddenLayer + 1:
                nextInput = numpy.dot(self.weights[index].W, layer.output) + self.biases[index].b
                self.layers[index + 1].setInput(nextInput)

        """ Estimate the average activation value of the hidden layers """

        rho_caps = []
        for hidden_layer in self.layers:
            if isinstance(hidden_layer, HiddenLayer):
                rho_caps.append(numpy.sum(hidden_layer.output, axis=1) / inputData.shape[1])

        """ Compute intermediate difference values using Backpropagation algorithm """

        diff = self.layers[-1].output - inputData

        sum_of_squares_error = 0.5 * numpy.sum(numpy.multiply(diff, diff)) / inputData.shape[1]

        weight_decay = 0
        for weight in self.weights:
            weight_decay += numpy.sum(numpy.multiply(weight.W, weight.W))

        weight_decay = 0.5 * self.lamda * weight_decay

        KL_divergence = []
        for rho_cap in rho_caps:
            element = self.beta * numpy.sum(self.rho * numpy.log(self.rho / rho_cap) +
                                            (1 - self.rho) * numpy.log((1 - self.rho) / (1 - rho_cap)))
            KL_divergence.append(element)

        cost = sum_of_squares_error + weight_decay + numpy.sum(KL_divergence)

        KL_div_grads = []
        for rho_cap in rho_caps:
            element = self.beta * (-(self.rho / rho_cap) + ((1 - self.rho) / (1 - rho_cap)))
            KL_div_grads.append(element)

        deltas = []
        for index, layer in enumerate(reversed(self.layers)):
            if isinstance(layer, InputLayer):
                continue
            if isinstance(layer, OutputLayer):
                delta = numpy.multiply(diff, numpy.multiply(layer.output, 1 - layer.output))
            else:
                delta = numpy.multiply(numpy.dot(numpy.transpose(self.weights[self.nHiddenLayer - index + 1].W),
                                                 deltas[index - 1])
                                       + numpy.transpose(numpy.matrix(KL_div_grads[self.nHiddenLayer - index])),
                                       numpy.multiply(layer.output, 1 - layer.output))
            deltas.append(delta)
        deltas.reverse()

        """ Compute the gradient values by averaging partial derivatives
            Partial derivatives are averaged over all training examples """
        W_grads = []
        b_grads = []
        for index in range(len(self.weights)):
            W_grad = numpy.dot(deltas[index], numpy.transpose(self.layers[index].output))
            W_grads.append(W_grad)

        for index in range(len(self.biases)):
            b_grad = numpy.sum(deltas[index], axis=1)
            b_grads.append(b_grad)

        for index in range(len(W_grads)):
            W_grads[index] = W_grads[index] / inputData.shape[1] + self.lamda * self.weights[index].W

        for index in range(len(b_grads)):
            b_grads[index] = b_grads[index] / inputData.shape[1]

        """ Transform numpy matrices into arrays """

        for index in range(len(W_grads)):
            W_grads[index] = numpy.array(W_grads[index])

        for index in range(len(b_grads)):
            b_grads[index] = numpy.array(b_grads[index])

        """ Unroll the gradient values and return as 'theta' gradient """

        theta_grad = self.compress(W_grads, b_grads)

        return [cost, theta_grad]

    def initLayer(self, nHiddenLayer, nNodeArr):
        self.layers = self.layers + [InputLayer(nNodeArr[0])]
        for i in range(nHiddenLayer):
            layer = HiddenLayer(nNodeArr[i + 1])
            self.layers = self.layers + [layer]
        self.layers = self.layers + [OutputLayer(nNodeArr[-1])]

    def initWeight(self, nHiddenLayer):
        nLayer = nHiddenLayer + 2
        for i in range(nLayer - 1):
            self.weights = self.weights + [Weight(self.layers[i + 1].nNode, self.layers[i].nNode)]

    def initBias(self, nHiddenLayer):
        nLayer = nHiddenLayer + 2
        for i in range(nLayer - 1):
            self.biases = self.biases + [Bias(self.layers[i + 1].nNode)]

    @staticmethod
    def compress(weights, biases):
        res = numpy.array([])
        res = res.flatten()
        for weight in weights:
            res = numpy.concatenate((res, weight.flatten()))

        for bias in biases:
            res = numpy.concatenate((res, bias.flatten()))
        return res

    def compressTheta(self):
        weights = []
        biases = []
        for weight in self.weights:
            weights.append(weight.W)

        for bias in self.biases:
            biases.append(bias.b)
        return self.compress(weights, biases)

    def extractTheta(self, theta):
        pos = 0
        for index, weight in enumerate(self.weights):
            (sizeX, sizeY) = weight.W.shape
            W = theta[pos: pos + sizeX * sizeY].reshape(self.layers[index + 1].nNode, self.layers[index].nNode)
            weight.setW(W)
            pos = pos + sizeX * sizeY

        for index, bias in enumerate(self.biases):
            (sizeX, sizeY) = bias.b.shape
            b = theta[pos: pos + sizeX * sizeY].reshape(self.layers[index + 1].nNode, 1)
            bias.setB(b)
            pos = pos + sizeX * sizeY

    def calcOutput(self, inputData):
        self.layers[0].setInput(inputData)
        for index, layer in enumerate(self.layers):
            layer.calOutput()
            if index != self.nHiddenLayer + 1:
                nextInput = numpy.dot(self.weights[index].W, layer.output) + self.biases[index].b
                self.layers[index + 1].setInput(nextInput)
        return self.layers[-1].output


def trainSAE(theta=None, data=None):
    [rho, lamda, beta,
     max_iterations, nHiddenLayer, nNodeArr] = loadSetting()

    """ Initialize the Autoencoder with the above parameters """
    encoder = SAE(nHiddenLayer, nNodeArr, lamda, beta, rho)
    if theta is None:
        theta = encoder.theta
    """ Run the L-BFGS algorithm to get the optimal parameter values """

    scipy.optimize.minimize(encoder.costFunction, theta,
                            args=(data,), method='L-BFGS-B',
                            jac=True, options={'maxiter': max_iterations})
    return encoder

