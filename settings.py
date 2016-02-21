def init(filename):
    global x, y, size
    global proba_crossover
    global proba_mutation
    global mutation_rate

    # data
    x = []
    y = []

    # Empirical studies have shown that better results are achieved by a crossover
    # probability of between 0.65 and 0.85, which implies that the probability of
    # a selected chromosome surviving to the next generation unchanged
    # (apart from any changes arising from mutation) ranges from 0.35 to 0.15.
    proba_crossover = 0.85
    proba_mutation = 0.001
    mutation_rate = 0.00001

    # parse the data file and store the x/y within a list of tuples
    with open(filename) as f:
        f.readline()
        for line in f.readlines():
            _x, _y = [float(i) for i in line.split()]
            x.append(_x)
            y.append(_y)
        size = len(x)
