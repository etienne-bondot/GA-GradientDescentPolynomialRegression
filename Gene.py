import random, math, copy

class Gene:

    '''

    A gene is an array of n chromosomes.

    '''

    def __init__(self, _nb_chromosomes, _min=-1.0, _max=1.0):
        self.chromosomes = [random.uniform(_min, _max) for _ in range(_nb_chromosomes)]

    def copy(self):
        return copy.copy(self)

    def len(self):
        return len(self.chromosomes)

    def get(self, _ind):
        return self.chromosomes[_ind]

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

    def fitness(self, _features, _targets):
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

    def info(self):
        print self.chromosomes
