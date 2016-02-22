import random, math, settings

class Chromosome:
    """
    A class representing a chromosome. It is a simple container for a specified number of genes
    on which we applied crossovers and mutations.
    """

    def __init__(self, genes):
        self.genes = genes
        self.fitness = Chromosome.compute_fitness(genes)
        self.crossover_methods = {
            'one_point_crossover': self.one_point_crossover,
            'two_points_crossover': self.two_points_crossover,
            'special': self.crossover
        }

    @staticmethod
    def hypothesis(genes, x):
        return (
            genes[0] +
            genes[1] * x +
            genes[2] * x * x +
            genes[3] * x * x * x +
            genes[4] * x * x * x * x +
            genes[5] * x * x * x * x * x
        )

    @staticmethod
    def compute_fitness(genes):
        F = 0.0
        for idx in range(settings.size):
            cost = settings.y[idx] - Chromosome.hypothesis(genes, settings.x[idx])
            F += cost * cost
        F = math.sqrt(F)
        return F

    def one_point_crossover(self, parent):
        """
        One point crossover between two parents previously selected.
        """
        pivot = random.randint(0, len(self.genes) - 1)
        child1 = self.genes[:pivot] + parent.genes[pivot:]
        child2 = parent.genes[:pivot] + self.genes[pivot:]
        return (Chromosome(child1), Chromosome(child2))

    def two_points_crossover(self, parent):
        """
        Two points crossover between two parents previously selected.
        """
        pivot1 = random.randint(0, len(self.genes) - 1)
        pivot2 = random.randint(0, len(self.genes) - 1)
        child1 = parent.chromosomes[0:pivot1] + self.chromosomes[pivot1:pivot2] + parent.chromosomes[pivot2:]
        child2 = self.chromosomes[0:pivot1] + parent.chromosomes[pivot1:pivot2] + self.chromosomes[pivot2:]
        return (Chromosome(child1), Chromosome(child2))

    def crossover(self, parent):
        """
        Special crossover between two parents previously selected, looks like a mutation.
        """
        child1 = list(self.genes)
        child2 = list(self.genes)
        child3 = list(self.genes)
        for idx in range(len(self.genes)):
            child1[idx] = 0.5 * self.genes[idx] + 0.5 * parent.genes[idx]
            child2[idx] = 1.5 * self.genes[idx] - 0.5 * parent.genes[idx]
            child3[idx] = -0.5 * self.genes[idx] + 1.5 * parent.genes[idx]
        childs = [Chromosome(child1), Chromosome(child2), Chromosome(child3)]
        return sorted(childs, key=lambda x: x.fitness)[:2]

    def mutate(self, mutation_rate):
        """
        Gene mutation.
        """
        mutated_chromosome = list(self.genes)
        idx = random.randint(0, len(self.genes) - 1)
        mutation = abs(mutation_rate * self.genes[idx])
        if random.random() < 0.5:
            mutation *= -1.0
        mutated_chromosome[idx] += mutation
        return Chromosome(mutated_chromosome)
