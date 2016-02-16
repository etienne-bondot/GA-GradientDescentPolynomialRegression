import random, math, copy

class Gene:

    '''

    A gene is an array of n chromosomes.

    '''

    def __init__(self, _nb_chromosomes, _min=-1.0, _max=1.0):
        self.mutation_rate = 0.001
        self.chromosomes = [random.uniform(_min, _max) for _ in range(_nb_chromosomes)]

    def copy(self):
        return copy.copy(self)

    def len(self):
        return len(self.chromosomes)

    def get(self, _ind):
        return self.chromosomes[_ind]

    def getChromosome(self):
        return self.chromosomes

    def set(self, _ind, value):
        self.chromosomes[_ind] = value

    def hypothesis(self, _feature):
        H = self.get(0)
        for i in range(1, self.len()):
            H += self.get(i) * math.pow(_feature, i)
        return H

    def partial_derivative(self, _features, _targets):
        D = 0.0
        m = len(_features)
        for x, y in zip(_features, _targets):
            D += ((y - self.hypothesis(x)) * x)
        D /= m
        return D

    def gd_fitness(self, _features, _targets):
        F = 0.0
        m = len(_features)
        try:
            for x, y in zip(_features, _targets):
                F += math.pow(y - self.hypothesis(x), 2)
            print 'fitness: ', F / (2.0 * m)
        except OverflowError:
            print 'Err: fitness too large, overflow'
            raise
        return F / 2.0

    def fitness(self, _features, _targets):
        F = 0.0
        m = len(_features)
        try:
            for x, y in zip(_features, _targets):
                F += math.pow(y - self.hypothesis(x), 2)
            F = math.sqrt(F)
        except OverflowError:
            print 'Err: fitness too large, overflow'
            raise
        return F

    def one_point_crossover(self, G):
        index = random.randint(1, self.len() - 1)
        G_1 = Gene(self.len())
        G_2 = Gene(self.len())
        for i in range(index):
            G_1.set(i, self.get(i))
        for i in range(index, self.len()):
            G_1.set(i, G.get(i))
        for i in range(index):
            G_2.set(i, G.get(i))
        for i in range(index, self.len()):
            G_2.set(i, self.get(i))
        return G_1.chromosomes, G_2.chromosomes

    def value_changing_mutation(self):
        index = random.randint(0, self.len() - 1)
        mutation = abs(self.mutation_rate * self.get(index))
        mutation *= -1.0 if random.random() < 0.5 else 1.0
        self.set(index, self.get(index) + mutation)

    def info(self):
        print self.chromosomes
