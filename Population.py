import random, math, settings, chart, sys
from Chromosome import *

class Population:
    """
    A class representing a population for a genetic algorithm simulation.
    A population is a collection of chromosomes.
    """

    _tournamentSize = 3
    _genes_per_chromosome = 6

    def __init__(self, size=500, crossover=0.85, elitism=0.1, mutation=0.0001):
        # Empirical studies have shown that better results are achieved by a crossover
        # probability of between 0.65 and 0.85, which implies that the probability of
        # a selected chromosome surviving to the next generation unchanged
        # (apart from any changes arising from mutation) ranges from 0.35 to 0.15.
        self.proba_crossover = crossover
        self.proba_mutation = mutation
        self.mutation_rate = 0.00001
        self.elitism = elitism
        self.fitness = []

        buf = []
        for _ in range(size): buf.append(Chromosome([random.uniform(-1000.0, 1000.0) for _ in range(Population._genes_per_chromosome)]))
        self.chromosomes = list(sorted(buf, key=lambda x: x.fitness))

    def tournament_selection(self):
        best = random.choice(self.chromosomes)
        for _ in range(Population._tournamentSize):
            other = random.choice(self.chromosomes)
            if (other.fitness < best.fitness): best = other
        return best

    def select_parents(self):
        return self.tournament_selection(), self.tournament_selection()

    def evolve(self, method):
        # [elites]: keep a portion of the best chromosomes
        size = len(self.chromosomes)
        idx = int(round(size * self.elitism))
        buf = self.chromosomes[:idx]
        while idx < size:
            # [crossover]
            if random.random() < self.proba_crossover:
                p1, p2 = self.select_parents()
                childs = p1.crossover_methods[method](p2)
                # [mutation]
                for c in childs:
                    if random.random() <= self.proba_mutation:
                        buf.append(c.mutate(self.mutation_rate))
                    else: buf.append(c)
                idx += 2
            else:
                # [mutation]
                if random.random() < self.proba_mutation:
                    buf.append(self.chromosomes[idx].mutate(self.mutation_rate))
                else: buf.append(self.chromosomes[idx])
                idx += 1

        self.chromosomes = sorted(buf, key=lambda x: x.fitness)
        self.fitness.append(self.chromosomes[0].fitness)

    def best_fitness(self):
        return self.chromosomes[0].fitness

    def result(self, method):
        print 'Solution with', method, ' crossover method: '
        print self.chromosomes[0].genes
        print 'fitness: ', self.chromosomes[0].fitness
        outputs = [self.chromosomes[0].hypothesis(self.chromosomes[0].genes, x) for x in settings.x]
        chart.generate_mpl(method, outputs, self.fitness)
