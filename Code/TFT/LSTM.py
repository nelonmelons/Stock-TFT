# ---------------------------------------------------#
#
#   File       : LSTM.py
#   Author     : Soham Deshpande
#   Date       : October 2021
#   Description: Long-Short Term Memory Block
#
#
#
# ----------------------------------------------------#

import matplotlib.pyplot as plt
import numpy as np
from Activation_functions import *
import torch
import torch.nn as nn
from torch.autograd import Variable


class LSTM(nn.Module):

    """
    Long-Short Term Memory

    LSTM(t) = tanh(s)*sigma(b+sum{U*x}+sum{W*h})

    Args:
        int num_classes = number of classes
        int num_layers  = number of layers
        int input_size  = size of input layer
        int hidden_size = size of hidden layer
        int seq_length  = sequence length

    """
    def __init__(self, num_classes, input_size, hidden_size, num_layers,
            seq_length):
        super(LSTM, self).__init__()
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.seq_length = seq_length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                          num_layers=num_layers, batch_first=True) #lstm
        self.fc_1 =  nn.Linear(hidden_size, 128) #fully connected 1
        self.fc = nn.Linear(128, num_classes) #fully connected last layer

        self.relu = nn.ReLU()

    def forward(self,x):
        h_0 = Variable(torch.zeros(self.num_layers,x.size(0),
            self.hidden_size)) #hidden state
        c_0 =Variable( torch.zeros(self.num_layers, x.size(0),
            self.hidden_size)) #internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input,
        # hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for
        # Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.fc(out) #Final Output
        return out


#x = lstm(1,1,2,2,2)
#print(x)

#test = LSTM(1,1,2,2,2)
#print(test)
#a = torch.Tensor([[0,1,2],[3,4,5],[6,7,8]])
#a.unsqueeze_(-1)
#a = a.expand(3,3,1)
#print(a)
#print(test.forward(a))







#Vanilla  LSTM :

INPUT = 28
HIDDEN = 128
OUTPUT = 10

INPUT += HIDDEN

ALPHA = 0.001
BATCH_SIZE = 64

ITER_NUM = 1000
LOG_ITER = ITER_NUM // 10
PLOT_ITER = ITER_NUM // 200

#x = Sinh()
#print(x.sinh_deriv(1))
#const = 1
#tanh = (x.sinh(const)) / (x.sinh_deriv(const))
#print(tanh)


class Test_LSTM:
    """
    Basic Vanilla LSTM from scratch to test functionality and to help
    with understanding

    """
    def __init__(self, input, hidden, output, alpha, batch_size, iter_num,
            log_iter, plot_iter):
        self.input = input
        self.hidden = hidden
        self.output = output
        self.alpha = alpha
        self.batch_size = batch_size
        self.iter_num = iter_num
        self.log_iter = log_iter
        self.plot_iter = plot_iter
        self.sigmoid = Sigmoid()
        self.sinh = Sinh()
       # self.softmax

    def weights_biases(self, input, hidden):
        """
        Setting up neurons and weights

        wf = weight for neuron f
        bf = bias for neuron f
        """
        wf, wi, wc, wo, wy = 0
        dwf, dwi, dwc, dwo, dwy = 0

        bf, bi, bc, bo, by = 0
        dbf, dwi, dbc, dbo, dby = 0

        weights = [wf, wi, wc, wo, wy]
        biases = [bf, bi, bc, bo, by]
        dweights = [dwf, dwi, dwc, dwo, dwy]
        dbiases = [dbf, dwi, dbc, dbo, dby]

        for weight in weights(0, 4):
            weight = np.random.randn(input, hidden) / np.sqrt(input * 0.5)
        weights[-1] = weights[np.random.randn(hidden, input) / np.sqrt(hidden * 0.5)]

        dweights = [np.zeros_like(dweight) for dweight in dweights]

        for bias in biases(0, 4):
            bias = np.random.randn(input, hidden) / np.sqrt(input * 0.5)
        biases[-1] = biases[np.random.randn(hidden, input) / np.sqrt(hidden * 0.5)]

        dbiases = [np.zeros_like(dbias) for dbias in dbiases]

    def lstm_block(self, sigmoid, input_val, weights, biases):
        batch_num = input_val.shape[1]

        caches = []
        states = [[np.zeros([batch_num, self.hidden]),
            np.zeros([batch_num, self.hidden])]]

        for x in input_val:
            c_prev, h_prev = states[-1]

            x = np.column_stack([x, h_prev])
            hf = sigmoid(np.dot(x, weights[0]) + biases[0])
            hi = sigmoid(np.dot(x, weights[1]) + biases[1])
            hc = tanh(np.dot(x, weights[2]) + biases[2])
            ho = sigmoid(np.dot(x, weights[3]) + biases[3])

            c = hf * c_prev + hi * hc
            h = ho * tanh(c)

            states.append([c, h])
            caches.append([x, hf, hi, ho, hc])

        return caches, states

    def backpropogation(self, caches, states):
        """
        Backpropagation algorithm

        Refer to write up for algorithm with relevant proofs
        """
        for i in range(ITER_NUM + 1):
            X, Y = iterator.get_next()
            Y = tf.one_hot(Y, 10)
            Xt = np.transpose(X, [1, 0, 2])

            caches, states = self.lstm_block(Xt)
            c, h = states[-1]

            out = np.dot(h, wy) + by
            pred = softmax(out)
            entropy = cross_entropy(pred, Y)


        dout = pred - Y
        dwy = np.dot(h.T, dout)
        dby = np.sum(dout, axis=0)

        dc_next = np.zeros_like(c)
        dh_next = np.zeros_like(h)

        for t in range(Xt.shape[0]):
            c, h = states[-t - 1]
            c_prev, h_prev = states[-t - 2]

            x, hf, hi, ho, hc = caches[-t - 1]

            tc = tanh(c)
            dh = np.dot(dout, wy.T) + dh_next

            dc = dh * ho * deriv_tanh(tc)
            dc = dc + dc_next

            dho = dh * tc
            dho = dho * deriv_sigmoid(ho)

            dhf = dc * c_prev
            dhf = dhf * deriv_sigmoid(hf)

            dhi = dc * hc
            dhi = dhi * deriv_sigmoid(hi)

            dhc = dc * hi
            dhc = dhc * deriv_tanh(hc)

            dwf += np.dot(x.T, dhf)
            dbf += np.sum(dhf, axis=0)
            dXf = np.dot(dhf, wf.T)

            dwi += np.dot(x.T, dhi)
            dbi += np.sum(dhi, axis=0)
            dXi = np.dot(dhi, wi.T)

            dwo += np.dot(x.T, dho)
            dbo += np.sum(dho, axis=0)
            dXo = np.dot(dho, wo.T)

            dwc += np.dot(x.T, dhc)
            dbc += np.sum(dhc, axis=0)
            dXc = np.dot(dhc, wc.T)

            dX = dXf + dXi + dXo + dXc

            dc_next = hf * dc
            dh_next = dX[:, -HIDDEN:]

        # Update weights
        wf -= ALPHA * dwf
        wi -= ALPHA * dwi
        wc -= ALPHA * dwc
        wo -= ALPHA * dwo
        wy -= ALPHA * dwy

        bf -= ALPHA * dbf
        bi -= ALPHA * dbi
        bc -= ALPHA * dbc
        bo -= ALPHA * dbo
        by -= ALPHA * dby

        # Initialize delta values
        dwf *= 0
        dwi *= 0
        dwc *= 0
        dwo *= 0
        dwy *= 0

        dbf *= 0
        dbi *= 0
        dbc *= 0
        dbo *= 0
        dby *= 0



