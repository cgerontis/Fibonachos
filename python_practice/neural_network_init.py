# first attempt at a neural network!
import numpy as np

# create a neural network class for a two-layer neural network:
class NeuralNetwork:
    def __init__(self,x,y):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1],4)
        self.weights2 = np.random.rand(4,1)
        self.y = y
        self.output = np.zeros(y.shape)

    # output of a simple 2 layer NN: y = sigma(weight2*sigma(weight1*x + bias1)+ bias2)
    # so apparently "training" the neural network is the process of
    # fine-tuning the weights/biases to improve the strength of predictions

    # each iteration of the training process consists of:
        # calculating the predicted output y, known as feedforward
        # updating the weights/biases, known as backpropogation

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    # how do we evaluate the "goodness" of our predictions? Use the loss function
    # (Sum of squares error)
    # our goal is to minimize the value of the loss function

    # find the derivative of the loss function with respect to the weights and biases
    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2
