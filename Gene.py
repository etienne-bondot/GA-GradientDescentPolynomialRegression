import random, math, settings

class Gene:

    def __init__(self, _nb_chromosomes=6, _min=-1.0, _max=1.0):
        self.chromosomes = [random.uniform(_min, _max) for _ in range(_nb_chromosomes)]
        self.fitness = 0.0
        self.compute_fitness()

    def hypothesis(self, x):
        return (
            self.chromosomes[0] +
            self.chromosomes[1] * x +
            self.chromosomes[2] * x * x +
            self.chromosomes[3] * x * x * x +
            self.chromosomes[4] * x * x * x * x +
            self.chromosomes[5] * x * x * x * x * x
        )

    def partial_derivative(self):
        D = 0.0
        for index in range(settings.size):
            D += ((settings.y[index] - self.hypothesis(settings.x[index])) * settings.x[index])
        D = D / (float)(settings.size)
        return D

    def gd_fitness(self):
        F = 0.0
        cost = 0.0
        for index in range(settings.size):
            cost += settings.y[index] - self.hypothesis(settings.x[index])
        self.fitness = cost / (2 * settings.size)
        return self.fitness

    def compute_fitness(self):
        F = 0.0
        for index in range(settings.size):
            cost = settings.y[index] - self.hypothesis(settings.x[index])
            F += cost * cost
        self.fitness = math.sqrt(F)

    '''
        One point and two points crossover doesn't seems efficient
    '''

    def one_point_crossover(self, G):
        index = random.randint(1, len(self.chromosomes) - 1)
        childs = [Gene() for _ in range(2)]
        childs[0].chromosomes = list(self.chromosomes)
        childs[1].chromosomes = list(G.chromosomes)
        for i in range(index):
            childs[1].chromosomes[i] = self.chromosomes[i]
        for i in range(index, len(self.chromosomes)):
            childs[0].chromosomes[i] = G.chromosomes[i]
        return childs[0].chromosomes, childs[1].chromosomes

    def two_points_crossover(self, G):
        index_1 = random.randint(1, len(self.chromosomes) - 1)
        index_2 = random.randint(1, len(self.chromosomes) - 1)
        childs = [Gene() for _ in range(2)]
        childs[0].chromosomes = list(self.chromosomes)
        childs[1].chromosomes = list(G.chromosomes)
        for i in range(min(index_1, index_2)):
            childs[0].chromosomes[i] = G.chromosomes[i]
            childs[1].chromosomes[i] = self.chromosomes[i]
        for i in range(max(index_1, index_2), len(self.chromosomes)):
            childs[0].chromosomes[i] = G.chromosomes[i]
            childs[1].chromosomes[i] = self.chromosomes[i]
        return childs[0].chromosomes, childs[1].chromosomes

    '''
        Chromosomes alteration seems more efficient than
        one point or two points crossover.
    '''
    def crossover(self, G):
        childs = [Gene() for _ in range(3)]
        for index in range(len(childs)):
            childs[index].chromosomes = list(self.chromosomes)
        for index in range(len(self.chromosomes)):
            childs[0].chromosomes[index] = 0.5 * self.chromosomes[index] + 0.5 * G.chromosomes[index]
            childs[1].chromosomes[index] = 1.5 * self.chromosomes[index] - 0.5 * G.chromosomes[index]
            childs[2].chromosomes[index] = -0.5 * self.chromosomes[index] + 1.5 * G.chromosomes[index]
        childs = sorted(childs, key=lambda x: x.fitness)[:2]
        return childs[0].chromosomes, childs[1].chromosomes

    def mutate(self):
        index = random.randint(0, len(self.chromosomes) - 1)
        mutation = abs(settings.mutation_rate * self.chromosomes[index])
        if random.random() < 0.5:
            mutation *= -1.0
        self.chromosomes[index] += mutation
