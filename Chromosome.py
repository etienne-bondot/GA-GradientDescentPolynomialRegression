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
            'average_crossover': self.average_crossover,
            'default_crossover': self.crossover
        }

    @staticmethod
    def hypothesis(genes, x):
        """
        Hypothesis function, determined for each context and so
        different for each problem.
        """
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
        """
        Compute the fitness of a chromosome.
        """
        F = 0.0
        for idx in range(settings.size):
            cost = settings.y[idx] - Chromosome.hypothesis(genes, settings.x[idx])
            F += cost * cost
        F = math.sqrt(F)
        return F

    def one_point_crossover(self, parent):
        """
        One point crossover between two parents previously selected.
        Return the best fitness between the children and the principal parent.
        """
        pivot = random.randint(1, len(self.genes) - 1)
        child1 = self.genes[pivot:] + parent.genes[:pivot]
        child2 = parent.genes[pivot:] + self.genes[:pivot]
        child3 = list(self.genes)
        childs = [Chromosome(child1), Chromosome(child2), Chromosome(child3)]
        return sorted(childs, key=lambda x: x.fitness)[0]

    def two_points_crossover(self, parent):
        """
        Two points crossover between two parents previously selected.
        Return the best fitness between the children and the principal parent.
        """
        pivot1 = random.randint(1, len(self.genes) - 1)
        pivot2 = random.randint(1, len(self.genes) - 1)
        if pivot1 > pivot2:
            pivot1, pivot2 = pivot2, pivot1
        child1 = parent.genes[:pivot1] + self.genes[pivot1:pivot2] + parent.genes[pivot2:]
        child2 = self.genes[:pivot1] + parent.genes[pivot1:pivot2] + self.genes[pivot2:]
        child3 = list(self.genes)
        childs = [Chromosome(child1), Chromosome(child2), Chromosome(child3)]
        return sorted(childs, key=lambda x: x.fitness)[0]

    def average_crossover(self, parent):
        """
        Average crossover: take the average of the parents genes value to
        make the childs.
        Return the best fitness between the children and the principal parent.
        """
        child1 = list(self.genes)
        child2 = list(self.genes)
        child3 = list(self.genes)
        for idx in range(len(self.genes)):
            child1[idx] = (parent.genes[idx] + self.genes[idx]) * 0.5
            child2[idx] = (parent.genes[idx] + self.genes[idx]) * 0.5 * -1
        childs = [Chromosome(child1), Chromosome(child2), Chromosome(child3)]
        return sorted(childs, key=lambda x: x.fitness)[0]

    def crossover(self, parent):
        """
        Special crossover between two parents previously selected, looks like a mutation.
        Return the best fitness between the children and the principal parent.
        """
        r = random.randint(1, len(self.genes) - 1)
        child1 = self.genes[:r] + [(self.genes[i] + parent.genes[i]) * 0.5 for i in range(r, len(self.genes))]
        child2 = self.genes[:r] + [self.genes[i] + (self.genes[i] - parent.genes[i]) * 0.5 for i in range(r, len(self.genes))]
        child3 = self.genes[:r] + [parent.genes[i] + (parent.genes[i] - self.genes[i]) * 0.5 for i in range(r, len(self.genes))]
        child4 = [(self.genes[i] + parent.genes[i]) * 0.5 for i in range(0, r)] + self.genes[r:]
        child5 = [self.genes[i] + (self.genes[i] - parent.genes[i]) * 0.5 for i in range(0, r)] + self.genes[r:]
        child6 = [parent.genes[i] + (parent.genes[i] - self.genes[i]) * 0.5 for i in range(0, r)] + self.genes[r:]
        childs = [Chromosome(child1), Chromosome(child2), Chromosome(child3), Chromosome(child4), Chromosome(child5), Chromosome(child6)]
        return sorted(childs, key=lambda x: x.fitness)[0]

    def mutate(self, mutation_rate):
        """
        Gene mutation.
        """
        mutated_chromosome = Chromosome(self.genes)
        idx = random.randint(0, len(self.genes) - 1)
        mutation = mutation_rate * self.genes[idx]
        mutated_chromosome.genes[idx] += mutation * -1.0 if random.random() < 0.5 else mutation
        return mutated_chromosome
