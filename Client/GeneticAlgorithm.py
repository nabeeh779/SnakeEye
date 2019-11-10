import tensorflow as tf
from UIGame import *
import NeuralNetwork as nn
import numpy as np

class GeneticAlgorithm():

        def __init__(self):
                self.pop = []
                #saving the prametrs in a touple struct 
                self.params = {'retain': 0.5, 'mutate_chance': 0.2, 'random_select': 0.1, 'mutate_rate': 0.2}
                self.scoring = {}
                self.evolving = False
                
        def create_population(self, count):
                """Create a population of random networks.
                Args:
                        count (int): Number of networks to generate, aka the
                        size of the population
                """
                self.pop = []
                for _ in range(0, count):
                        # Create a random network.
                        n = nn.neural_network()
                        n.init_neural_network()

                        # Add the network to our population.
                        self.pop.append(n)

                print("Population created!\n")

        def breed(self, mother, father):
                """Make two children as parts of their parents.
                Args:
                        mother (dict): Network parameters
                        father (dict): Network parameters
                """

                children = []
                for _ in range(2):

                        weights = []
                        biases = []
                        for i in range(10):

                                weights.append(random.choice([mother.get_weight(i), father.get_weight(i)]))

                        for i in range(3):
                                
                                biases.append(random.choice([mother.get_biase(i), father.get_biase(i)]))

                        child = nn.neural_network()
                        child.load_neural_network(weights, biases)
                        children.append(child)

                return children

        def grade(self):
                graded = []

                for nn in self.pop:
                        g = Game(nn, False, maxMove=1000, scoring=self.scoring)
                        fitness = g.RunGame()[0]
                        g = Game(nn, False, maxMove=1000, scoring=self.scoring)
                        fitness += g.RunGame()[0]
                        graded.append((fitness, nn))

                # Sort on the scores.
                graded = [x[1] for x in sorted(graded, key=lambda x: x[0], reverse=True)]

                return graded

        def evolve(self):
                """Evolve a population of networks.
                Args:
                        pop (list): A list of network parameters
                """

                # Get scores for each network.
                graded = self.grade()

                print("Population graded!\n")

                # Get the number we want to keep for the next gen.
                retain_length = int(len(graded)*self.params.get('retain'))

                # The parents are every network we want to keep.
                parents = graded[:retain_length]

                # For those we aren't keeping, randomly keep some anyway.
                for individual in graded[retain_length:]:
                        if self.params.get("random_select") > random.random():
                                parents.append(individual)
                        else:
                                individual.delete()

                # Randomly mutate some of the networks we're keeping.
                for individual in parents:
                        individual.mutate(self.params.get('mutate_chance'), self.params.get('mutate_rate'))

                # Now find out how many spots we have left to fill.
                parents_length = len(parents)
                desired_length = len(self.pop) - parents_length
                children = []

                # Add children, which are bred from two remaining networks.
                while len(children) < desired_length:

                        # Get a random mom and dad.
                        male = random.randint(0, parents_length-1)
                        female = random.randint(0, parents_length-1)

                        # Assuming they aren't the same network...
                        if male != female:
                                male = parents[male]
                                female = parents[female]

                                # Breed them.
                                babies = self.breed(male, female)

                                # Add the children one at a time.
                                for baby in babies:
                                        # Don't grow larger than desired length.
                                        if len(children) < desired_length:
                                                children.append(baby)

                parents.extend(children)

                print("Population evolved!\n")
                self.pop = parents

        def save_network(self, path):

                save_data = []

                for netwrok in self.pop:
                        save_data.append(netwrok.get_network())

                np.save(path, save_data)

        def load_network(self, path):

                saved_data = np.load(path)

                self.pop = []

                for network in saved_data:
                        n = nn.neural_network()
                        n.load_neural_network(network.get('weights'), network.get('biases'))
                        self.pop.append(n)