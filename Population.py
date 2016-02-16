import random, plotly, math
from plotly import tools
from plotly.graph_objs import Scatter, Layout, Marker
from Gene import *

class Population:

    '''

    A population is composed of an array of n genes.

    '''

    def __init__(self, _nb_genes=2, _nb_chromosomes=6, _min=-1.0, _max=1.0):
        self.nb_genes = _nb_genes
        self.nb_chromosomes = _nb_chromosomes
        self.genes = [Gene(_nb_chromosomes, _min, _max) for _ in range(_nb_genes)]
        self.info()

    def get(self, _ind):
        return self.genes[_ind]

    def gradient_descent(self, inputs, targets, max_iter=1000, alpha=0.001):
        '''
        gradient descent algorithm
        while not converge or max iteration:
            for all j:
                O(j) := O(j) + alpha * (1/m) * (sum(y_i - Hx_i))x_i_J
        '''
        # take only one gene for gradient descent
        G = self.get(0)
        newG = G.copy()
        m = len(inputs)
        fitness = []
        for i in range(max_iter):
            print 'iter: #{}'.format(i)
            for j in range(G.len()):
                newG.set(j, G.get(j) + alpha * G.partial_derivative(inputs, targets))
            G = newG.copy()
            fitness.append(G.fitness(inputs, targets))
        # generate a new set of data
        outputs = [G.hypothesis(x) for x in inputs]
        self.chart(inputs, targets, outputs, fitness)
        return G

    def roulette_wheel_selection(self, inputs, targets, max_iter = 1000, alpha = 0.001):
        self.get(0).fitness(inputs, targets)
        self.get(1).fitness(inputs, targets)
        self.crossover()

    def crossover(self):
        rind = self.get(0).len() / 2
        newG = []
        for i in range(rind):
            newG.append(self.get(0).get(i))
        for i in range(rind, self.get(0).len()):
            newG.append(self.get(1).get(i))
        return newG

    def mutate(self, _min=-10.0, _max=10.0):
        r = random.uniform(_min, _max)
        rind = random.randrange(0, self.get(0).len())

    def select(self, _fitnesses):
        # probability
        P = random.uniform(0, sum(_fitnesses))
        for i, f in enumerate(_fitnesses):
            if P <= 0:
                break
            P -= f
        return i

    def info(self):
        print 'G(genes={}, chromosomes={})['.format(self.nb_genes, self.nb_chromosomes)
        for G in self.genes:
            print '     ',
            G.info()
        print ']'

    def chart(self, _inputs, _targets, _outputs, _fitness):
        plotly.offline.plot({
            'data': [
                Scatter(
                    x = _inputs,
                    y = _outputs,
                    name='solutions',
                    mode='lines+markers',
                    line = dict(
                        color = 'red',
                        width = 1
                    ),
                    marker = Marker(
                        color = 'red',
                        symbol = 'x',
                        size = 2
                    )
                ),
                Scatter(
                    x = _inputs,
                    y = _targets,
                    name = 'inputs',
                    mode = 'markers',
                    marker = Marker(
                        color = 'blue',
                        symbol = 'x',
                        size = 2
                    )
                ),
                Scatter(
                    x = [i for i in range(len(_fitness))],
                    y = _fitness, mode='lines+markers',
                    name = 'fitness',
                    line = dict(
                        color = 'black',
                        width = 1
                    ),
                    marker = Marker(
                        color = 'black',
                        symbol = 'x',
                        size = 2
                    ),
                    xaxis = 'x2',
                    yaxis = 'y2'
                )
            ],
            'layout': Layout(
                title = 'Gradient-Descent algorithm',
                xaxis2 = dict(
                    anchor='y2'
                ),
                yaxis=dict(
                    title='Fx',
                    domain=[0, 0.5]
                ),
                yaxis2=dict(
                    title = 'fitness per epoch',
                    domain=[0.5, 1]
                )
            )
        })
