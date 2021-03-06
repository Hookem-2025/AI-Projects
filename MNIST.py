# -*- coding: utf-8 -*-
"""Untitled2.ipynb


Original file is located at
    https://colab.research.google.com/drive/1_ipJsTbzRR9aWA0ws_3f5QNZflGP1PeF
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

MNIST_train = '/content/mnist_train.csv'
MNIST_test = '/content/mnist_test.csv'

train = pd.read_csv(MNIST_train)
test = pd.read_csv(MNIST_test)

import matplotlib.pyplot as plt

image_size = 28 # width and length
no_of_different_labels = 10 #  i.e. 0, 1, 2, 3, ..., 9
image_pixels = image_size * image_size

test[:10]

test[test==255]
test.shape

fac = .99/255

new_arr = np.array(train)
new_test = np.array(test)
train_cnv = np.asfarray(new_arr[:, 1:]) * fac + 0.01
test_cnv = np.asfarray(new_test[:, 1:]) * fac + 0.01

train_labels = np.asfarray(new_arr[:, :1]) * fac + 0.01
test_labels = np.asfarray(new_test[:, :1]) * fac + 0.01

lr = np.arange(no_of_different_labels)
train_labels_one_hot = (lr==train_labels).astype(np.float)
test_labels_one_hot = (lr==test_labels).astype(np.float)

train_labels_one_hot[train_labels_one_hot==0] = 0.01
train_labels_one_hot[train_labels_one_hot==1] = 0.99
test_labels_one_hot[test_labels_one_hot==0] = 0.01
test_labels_one_hot[test_labels_one_hot==1] = 0.99

for i in range(10):
    img = train_cnv[i].reshape((28,28))
    plt.imshow(img, cmap="Greys")
    plt.show()

import numpy as np

@np.vectorize
def sigmoid(x):
    return 1 / (1 + np.e ** -x)
activation_function = sigmoid

from scipy.stats import truncnorm

def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, 
                     (upp - mean) / sd, 
                     loc=mean, 
                     scale=sd)


class NeuralNetwork:
    # our neural network takes in number of input nodes (in this case uhh 784), number of output nodes (1), number of hid
    #hidden nodes, and the leanring rate
    def __init__(self, 
                 no_of_in_nodes, 
                 no_of_out_nodes, 
                 no_of_hidden_nodes,
                 learning_rate):
        self.no_of_in_nodes = no_of_in_nodes
        self.no_of_out_nodes = no_of_out_nodes
        self.no_of_hidden_nodes = no_of_hidden_nodes
        self.learning_rate = learning_rate 
        self.create_weight_matrices()
        
    def create_weight_matrices(self):
        """ 
        A method to initialize the weight 
        matrices of the neural network
        """
        rad = 1 / np.sqrt(self.no_of_in_nodes)
        X = truncated_normal(mean=0, 
                             sd=1, 
                             low=-rad, 
                             upp=rad)
        self.wih = X.rvs((self.no_of_hidden_nodes, 
                                       self.no_of_in_nodes))
        rad = 1 / np.sqrt(self.no_of_hidden_nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.who = X.rvs((self.no_of_out_nodes, 
                                         self.no_of_hidden_nodes))
        
    
    def train_single(self, input_vector, target_vector):
        """
        input_vector and target_vector can 
        be tuple, list or ndarray
        """
        
        input_vector = np.array(input_vector, ndmin=2).T
        target_vector = np.array(target_vector, ndmin=2).T
        
        output_vector1 = np.dot(self.wih, 
                                input_vector)
        output_hidden = activation_function(output_vector1)
        
        output_vector2 = np.dot(self.who, 
                                output_hidden)
        output_network = activation_function(output_vector2)
        
        output_errors = target_vector - output_network
        # update the weights:
        tmp = output_errors * output_network \
              * (1.0 - output_network)     
        tmp = self.learning_rate  * np.dot(tmp, 
                                           output_hidden.T)
        self.who += tmp


        # calculate hidden errors:
        hidden_errors = np.dot(self.who.T, 
                               output_errors)
        # update the weights:
        tmp = hidden_errors * output_hidden * \
              (1.0 - output_hidden)
        self.wih += self.learning_rate \
                          * np.dot(tmp, input_vector.T)
        
    def train(self, data_array, 
              labels_one_hot_array,
              epochs=1,
              intermediate_results=False):
        intermediate_weights = []
        for epoch in range(epochs):  
            print("*", end="")
            for i in range(len(data_array)):
                self.train_single(data_array[i], 
                                  labels_one_hot_array[i])
            if intermediate_results:
                intermediate_weights.append((self.wih.copy(), 
                                             self.who.copy()))
        return intermediate_weights 
        
    
    def run(self, input_vector):
        # input_vector can be tuple, list or ndarray
        input_vector = np.array(input_vector, ndmin=2).T

        output_vector = np.dot(self.wih, 
                               input_vector)
        output_vector = activation_function(output_vector)
        
        output_vector = np.dot(self.who, 
                               output_vector)
        output_vector = activation_function(output_vector)
    
        return output_vector
            
    def confusion_matrix(self, data_array, labels):
        cm = np.zeros((10, 10), int)
        for i in range(len(data_array)):
            res = self.run(data_array[i])
            res_max = res.argmax()
            target = labels[i][0]
            cm[res_max, int(target)] += 1
        return cm    

    #precision is out of the number of sick how many did our model classify

    def precision(self, label, confusion_matrix):
        col = confusion_matrix[:, label]
        return confusion_matrix[label, label] / col.np.sum()
    #recall is how many were sick out of the ones u classified? 
    def recall(self, label, confusion_matrix):
        row = confusion_matrix[label, :]
        return confusion_matrix[label, label] / row.np.sum()
        
    #evalutes the model essentially 
    def evaluate(self, data, labels):
        corrects, wrongs = 0, 0
        for i in range(len(data)):
            res = self.run(data[i])
            res_max = res.argmax()
            if res_max == labels[i]:
                corrects += 1
            else:
                wrongs += 1
        return corrects, wrongs

#make our first model
            
Mnist = NeuralNetwork(no_of_in_nodes = image_pixels, 
                    no_of_out_nodes = 10, 
                    no_of_hidden_nodes = 100,
                    learning_rate = 0.1)

for i in range(len(train_cnv)):
    Mnist.train_single(train_cnv[i], train_labels_one_hot[i])

for i in range(20):
    res = Mnist.run(test_cnv[i])
    print(test_labels[i], np.argmax(res), np.max(res))

corrects, wrongs = Mnist.evaluate(train_cnv, train_labels)
print("accuracy train: ", corrects )


cm = Mnist.confusion_matrix(train_cnv, train_labels)
print(cm)

epochs = 10

Mnist = NeuralNetwork(no_of_in_nodes = image_pixels, 
                               no_of_out_nodes = 10, 
                               no_of_hidden_nodes = 100,
                               learning_rate = 0.15)
    
    
 
weights = Mnist.train(train_cnv, 
                    train_labels_one_hot, 
                    epochs=epochs, 
                    intermediate_results=True)

cm = Mnist.confusion_matrix(train_cnv, train_labels)
        
print(Mnist.run(train_cnv[i]))

for i in range(epochs):  
    print("epoch: ", i)
    Mnist.wih = weights[i][0]
    Mnist.who = weights[i][1]
   
    corrects, wrongs = Mnist.evaluate(train_cnv, train_labels)
    print("accuracy train: ", corrects / ( corrects + wrongs))
    corrects, wrongs = Mnist.evaluate(train_cnv, test_labels)
    print("accuracy: test", corrects / ( corrects + wrongs))

