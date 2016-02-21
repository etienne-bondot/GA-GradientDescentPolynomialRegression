import random, math, time, settings, chart, sys
from Gene import *

class Population:

    def __init__(self, _nb_genes=1000, _nb_chromosomes=6, _min=-1.0, _max=1.0):
        self.nb_genes = _nb_genes
        self.nb_chromosomes = _nb_chromosomes
        self.genes = [Gene(_nb_chromosomes, _min, _max) for _ in range(_nb_genes)]

    def gradient_descent(self, max_iter=1000, alpha=0.001):
        '''
        gradient descent algorithm
        while not converge or max iteration:
            for all j:
                O(j) := O(j) + alpha * (1/m) * (sum(y_i - Hx_i))x_i_J
        '''
        # take only one gene for gradient descent
        G = self.genes[0]
        newG = Gene()
        newG.chromosomes = list(G.chromosomes)
        fitness = []
        for _iter in range(max_iter):
            print '{}%: {}\t{}'.format(_iter * 100 / max_iter, G.chromosomes, G.fitness)
            for j in range(len(G.chromosomes)):
                newG.chromosomes[j] = G.chromosomes[j] + alpha * G.partial_derivative()
            G.chromosomes = list(newG.chromosomes)
            fitness.append(G.gd_fitness())

        # generate a new set of data
        outputs = [G.hypothesis(x) for x in settings.x]
        chart.generate(outputs, fitness)

    def GA(self, max_iter = 1000):
        fitness = []
        start_time = time.time()
        self.genes = sorted(self.genes, key=lambda x: x.fitness)
        for _iter in range(max_iter):
            update_progress(_iter * 100 / max_iter, self.genes[0].fitness)
            # print '{}%: {}\t{}'.format(_iter * 100 / max_iter, self.genes[0].chromosomes, self.genes[0].fitness)
            newGs = []
            newGs.append(self.genes[0])
            for index in range(len(self.genes) / 2):
                G = [Gene(), Gene()]
                G[0].chromosomes = list(self.genes[index * 2].chromosomes)
                G[1].chromosomes = list(self.genes[index * 2 + 1].chromosomes)
                if random.random() < settings.proba_crossover:
                    G[0].chromosomes, G[1].chromosomes = G[0].crossover(G[1])
                if random.random() < settings.proba_mutation:
                    G[0].mutate()
                if random.random() < settings.proba_mutation:
                    G[1].mutate()
                newGs.extend(G)
            self.genes = list(newGs)
            for index in range(len(self.genes)):
                self.genes[index].compute_fitness()
            self.genes = sorted(self.genes, key=lambda x: x.fitness)
            fitness.append(self.genes[0].fitness)

        # generate a new set of data
        print 'Solution: '
        print self.genes[0].chromosomes
        print 'fitness: ', self.genes[0].fitness
        print 'processing time: {}'.format(time.time() - start_time)
        outputs = [self.genes[0].hypothesis(x) for x in settings.x]
        chart.generate_mpl(outputs, fitness)

    def GA_second(self, max_iter = 1000):
        fitness = []
        start_time = time.time()
        self.genes = sorted(self.genes, key=lambda x: x.fitness)
        for _iter in range(max_iter):
            update_progress(_iter * 100 / max_iter, self.genes[0].fitness)
            # print '{}%: {}\t{}'.format(_iter * 100 / max_iter, self.genes[0].chromosomes, self.genes[0].fitness)
            G_elites = []
            new_pop = []

            # [elites]: keep the half better genes
            for index in range(len(self.genes) / 2):
                G = Gene()
                G.chromosomes = list(self.genes[index].chromosomes)
                G_elites.append(G)
            new_pop.extend(G_elites)

            # [crossover] with the newGs as parents The higher the
            # fitness value the higher the probability of that chromosome being
            # selected for reproduction.
            for index in range(len(G_elites) / 2):
                G = [Gene(), Gene()]
                G[0].chromosomes = list(G_elites[index * 2].chromosomes)
                G[1].chromosomes = list(G_elites[index * 2 + 1].chromosomes)
                if random.random() < settings.proba_crossover:
                    # should we keep them only if they're better ?
                    .chromosomes, G[1].chromosomes = G[0].crossover(G[1])

                # [mutation]
                if random.random() < settings.proba_mutation:
                    G[0].mutate()
                if random.random() < settings.proba_mutation:
                    G[1].mutate()

                new_pop.extend(G)

            self.genes = list(new_pop)
            for index in range(len(self.genes)):
                self.genes[index].compute_fitness()
            self.genes = sorted(self.genes, key=lambda x: x.fitness)
            fitness.append(self.genes[0].fitness)

        # generate a new set of data
        print 'Solution: '
        print self.genes[0].chromosomes
        print 'fitness: ', self.genes[0].fitness
        print 'processing time: {}'.format(time.time() - start_time)
        outputs = [self.genes[0].hypothesis(x) for x in settings.x]
        chart.generate_mpl(outputs, fitness)

    def select(self, _fitnesses):
        # probability
        P = random.uniform(0, sum(_fitnesses))
        for i, f in enumerate(_fitnesses):
            if P <= 0:
                break
            P -= f
        return i

def update_progress(progress, last_fitness):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-40s] %d%% - Last fitness: %s" % ('=' * (progress * 40 / 100), progress, last_fitness))
    sys.stdout.flush()
