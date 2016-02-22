def init(filename):
    global x, y, size

    # data
    x = []
    y = []

    # parse the data file and store the x/y within a list of tuples
    with open(filename) as f:
        f.readline()
        for line in f.readlines():
            _x, _y = [float(i) for i in line.split()]
            x.append(_x)
            y.append(_y)
        size = len(x)
