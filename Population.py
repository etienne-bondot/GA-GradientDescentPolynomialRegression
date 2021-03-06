import random, math, settings, chart, sys
from Chromosome import *

class Population:
    """
    A class representing a population for a genetic algorithm simulation.
    A population is a collection of chromosomes.
    """

    _tournamentSize = 3
    _genes_per_chromosome = 6

    def __init__(self, size=500, crossover=0.85, elitism=0.01, mutation=0.001):
        # Empirical studies have shown that better results are achieved by a crossover
        # probability of between 0.65 and 0.85, which implies that the probability of
        # a selected chromosome surviving to the next generation unchanged
        # (apart from any changes arising from mutation) ranges from 0.35 to 0.15.
        self.proba_crossover = crossover
        self.proba_mutation = mutation
        self.mutation_rate = 0.00001
        self.elitism = elitism
        self.best_fitness = []
        self.worst_fitness = []
        self.average_fitness = []
        self.progress = -1

        buf = []
        for _ in range(size): buf.append(Chromosome([random.uniform(-10.0, 10.0) for _ in range(Population._genes_per_chromosome)]))
        self.chromosomes = list(sorted(buf, key=lambda x: x.fitness))

    def tournament_selection(self):
        """
        Tournament selection.
        """
        best = self.chromosomes[random.randint(0, len(self.chromosomes) - 1)]
        for _ in range(Population._tournamentSize):
            other = self.chromosomes[random.randint(0, len(self.chromosomes) - 1)]
            if (other.fitness < best.fitness):
                best = other
        return best

    def select_parents(self):
        return self.tournament_selection(), self.tournament_selection()

    def evolve(self, method):
        """
        Algorithm to envolve the population.
        """
        # [elites]: keep a portion of the best chromosomes
        size = len(self.chromosomes)
        idx = int(round(size * self.elitism))
        buf = self.chromosomes[:idx]
        while idx < size:
            # [crossover]
            if random.random() < self.proba_crossover:
                p1, p2 = self.select_parents()
                child = p1.crossover_methods[method](p2)
                # [mutation]
                buf.append(child.mutate(self.mutation_rate) if random.random() <= self.proba_mutation else child)
            else:
                # [mutation]
                buf.append(self.chromosomes[idx].mutate(self.mutation_rate) if random.random() < self.proba_mutation else self.chromosomes[idx])
            idx += 1

        self.chromosomes = sorted(buf, key=lambda x: x.fitness)
        self.best_fitness.append(self.get_best_fitness())
        self.worst_fitness.append(self.get_worst_fitness())
        self.average_fitness.append(self.get_average_fitness())

    def get_best_fitness(self):
        """
        Return the best fitness of the population.
        """
        return self.chromosomes[0].fitness

    def get_worst_fitness(self):
        """
        Return the worst fitness of the population.
        """
        return self.chromosomes[-1].fitness

    def get_average_fitness(self):
        """
        Return the average fitness of the population.
        """
        avg_fitness = 0.0
        for c in self.chromosomes: avg_fitness += c.fitness
        return avg_fitness / (float)(len(self.chromosomes))

    def result(self):
        """
        Display:
        - the best genes of the population,
        - the best fitness of the population,
        - a chart representing the original data compared with the data generated with the best genes,
        - a chart with the best, worst and average fitnesses per epoch
        """
        print ''
        print 'Solutions: '
        print self.chromosomes[0].genes
        print 'fitness: ', self.chromosomes[0].fitness
        outputs = [self.chromosomes[0].hypothesis(self.chromosomes[0].genes, x) for x in settings.x]
        chart.generate_diff_chart(outputs, self.best_fitness)
        chart.generate_fitness_chart(outputs, self.best_fitness, self.worst_fitness, self.average_fitness)
