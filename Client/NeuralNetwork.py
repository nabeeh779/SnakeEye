import tensorflow as tf
import numpy as np
import random

class neural_network():

    def __init__(self):
        """
        Init the neural network parameters.
        """
        self.n_nodes_data = 10

        self.n_classes = 3

        self.x = tf.placeholder('float', [1, self.n_nodes_data])

        self.move = None
        self.sess = None

    def neural_network_model(self, data):
        """
        Creates the neural network model.

        tf.matmul - Multiply two matricies
        """
        self.output_layer = {'weights': tf.Variable(tf.random_normal([self.n_nodes_data, self.n_classes])),
                        'biases': tf.Variable(tf.random_normal([self.n_classes]))}

        #adding to a graph 
        output = tf.math.sigmoid(tf.add(tf.matmul(data, self.output_layer['weights']), self.output_layer['biases']))

        return output

    def neural_network_model_load(self, data, weigths, biases):
        """
        Loads existing neural network model.
        """
        self.output_layer = {'weights': tf.Variable(weigths),
                        'biases': tf.Variable(biases)}
        #   adding to a graph 
        output = tf.math.sigmoid(tf.add(tf.matmul(data, self.output_layer['weights']), self.output_layer['biases']))

        return output

    def init_neural_network(self):
        """
        Creates session and network model.
        A Session object encapsulates the environment
        in which Operation objects are executed, and Tensor objects are evaluated
        """
        self.sess = tf.Session()
        self.move = self.neural_network_model(self.x)
        self.sess.run(tf.global_variables_initializer())

    def load_neural_network(self, weights, biases):
        """
        Creates session and load network model.
        """
        self.sess = tf.Session()
        self.move = self.neural_network_model_load(self.x, weights, biases)
        self.sess.run(tf.global_variables_initializer())
            
    def get_weight(self, layer):
        """
        Get the weights of one of the input neurons.
        """
        return  self.sess.run(self.output_layer['weights']).tolist()[layer]

    def get_biase(self, layer):
        """
        Get the bias of one of the output neurons.
        """
        return self.sess.run(self.output_layer['biases']).tolist()[layer]

    def mutate(self, chance = 0.2, rate = 0.2):
        """
        Mutate network weights and biases.
        """
        l = [[0] * 3 for _ in range(10)]

        #running on graph 10 by 3 thats mean the 10 nn and 3 classes
        for i in range(10):
            for j in range(3):
                if chance > random.random():
                    l[i][j] = random.uniform( -rate, rate)

        self.sess.run(self.output_layer['weights'].assign_add(l))

        l = [0,0,0]

        for i in range(3):
            if chance > random.random():
                l[i] = random.uniform( -rate, rate)

        self.sess.run(self.output_layer['biases'].assign_add(l))

    def get_move(self, data):
        """
        Run parameters through the model and return move.
        """
        arr = self.sess.run(self.move, feed_dict={self.x: data})[0]

        arr = list(arr)

        return arr.index(max(arr))

    def delete(self):
        """
        Free up bot's memory.
        """
        tf.reset_default_graph()

    def get_network(self):
        """
        Return network weights and biases as dict
        """
        layer = {'weights': self.sess.run(self.output_layer['weights']), 'biases': self.sess.run(self.output_layer['biases'])}
        return layer