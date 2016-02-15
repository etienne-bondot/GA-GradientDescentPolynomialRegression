#!/usr/bin/env python

import plotly, random, math, time, sys, getopt
from plotly import tools
from plotly.graph_objs import Scatter, Layout, Marker

def stochastic_gradient_descent(theta, inputs, targets, max_iter = 1000, alpha = 0.001):
    '''
    stochastic gradient descent algorithm
    while convergence or max iteration:
        for all j:
            O(j) = O(j) - alpha(1/m)(Hx - y)x
    '''
    newT = list(theta)
    m = len(inputs)
    cost_history = []

    for i in range(max_iter):
        for x, y in zip(inputs, targets):
            Fx = hypothesis(theta, x)
            # newT = list(theta[j] - alpha / m * (Fx - y) * x for j in range(len(theta)))
            newT = list(theta[j] - alpha / m * (Fx - y) * math.pow(x, j) for j in range(len(theta)))
            theta = list(newT)
            # print '[#', i, ']', theta
            # print 'F({}) = {} [{}]'.format(x, Fx, y)
            # print ''
            # time.sleep(0.1)
        cost = compute_cost(theta, inputs, targets)
        cost_history.append(cost)
        # print '#{} : cost: {}'.format(i, compute_cost(theta, inputs, targets))
        # print ''

    # generate a new set of data
    outputs = [hypothesis(theta, x) for x in inputs]
    generateChart(inputs, outputs, targets, cost_history)
    return theta

def gradient_descent(theta, inputs, targets, max_iter = 1000, alpha = 0.001):
    '''
    gradient descent algorithm
    while not converge or max iteration:
        for all j:
            tmp(j) := O(j) - alpha(1/m)sum(Hx - y)x
    '''
    newT = list(theta)
    m = len(inputs)
    cost_history = []

    for i in range(max_iter):
        for i in range(len(theta)):
            newT[i] = theta[i] - alpha * J(theta, i, inputs, targets)
        theta = list(newT)
        cost = compute_cost(theta, inputs, targets)
        cost_history.append(cost)

    # generate a new set of data
    outputs = [hypothesis(theta, x) for x in inputs]
    generateChart(inputs, outputs, targets, cost_history)
    return theta

def hypothesis(theta, x):
    '''
    Compute the function according to the variables
    '''
    v = theta[0]
    for i in range(1, len(theta)):
        v += theta[i] * math.pow(x, i)
    return v

def J(theta, indT, inputs, targets):
    '''
    Compute the partial derivative of the cost function
    '''
    loss = 0.0
    m = len(inputs)

    # iterate on every training instance
    for i in range(m):
        loss += (1.0 / m) * (hypothesis(theta, inputs[i]) - targets[i]) * inputs[i]
        # loss += (1.0 / m) * (hypothesis(theta, inputs[i]) - targets[i]) * math.pow(inputs[i], indT)
    return loss

def compute_cost(theta, inputs, targets):
    '''
    Generalized cost function: least squares cost function
    In regression almost always want to fit data well.
    Smallest average distance to points in training data (h(x) close to y for (x,y) in training data)
    Squaring
        - Penalty for positive and negative deviations the sample
        - Penalty for large deviations stronger
    !! Should decrease at every step: this is how gradient descent work !!
    '''
    sse = 0.0
    cost = 0.0
    m = len(inputs)

    # iterate on every training instance
    for i in range(m):
        Fx = hypothesis(theta, inputs[i])
        #
        # display_theta(theta)
        # print 'Fx:      ', Fx
        # print 'target:  ', targets[i]
        # print 'result:  ', (Fx - targets[i])
        # print ''
        #
        sse += math.pow(targets[i] - Fx, 2)
    cost = sse / (2 * m)
    return cost

# generate a chart based on the data
def generateChart(inputs, outputs, targets, cost_history):
    plotly.offline.plot({
        'data': [
            Scatter(
                x = inputs,
                y = outputs,
                name='solutions',
                mode='lines+markers',
                line = dict(
                    color = 'red',
                    width = 1
                ),
                marker = Marker(
                    color = 'red',
                    symbol = 'x',
                    size = 2
                )
            ),
            Scatter(
                x = inputs,
                y = targets,
                name = 'inputs',
                mode = 'markers',
                marker = Marker(
                    color = 'blue',
                    symbol = 'x',
                    size = 2
                )
            ),
            Scatter(
                x = [i for i in range(len(cost_history))],
                y = cost_history, mode='lines+markers',
                name = 'costs',
                line = dict(
                    color = 'black',
                    width = 1
                ),
                marker = Marker(
                    color = 'black',
                    symbol = 'x',
                    size = 2
                ),
                xaxis = 'x2',
                yaxis = 'y2'
            )
        ],
        'layout': Layout(
            title = 'Gradient-Descent algorithm',
            xaxis2 = dict(
                anchor='y2'
            ),
            yaxis=dict(
                title='Fx',
                domain=[0, 0.5]
            ),
            yaxis2=dict(
                title = 'costs per epoch',
                domain=[0.5, 1]
            )
        )
    })

def display_theta(theta):
    print '['
    for t in theta:
        print ' ', t
    print ']'

# parse the data file and store the x/y within a list of tuples
def getData(fname):
    x = []
    y = []
    with open(fname) as f:
        f.readline()
        for line in f.readlines():
            _x, _y = [float(i) for i in line.split()]
            x.append(_x)
            y.append(_y)
    return x, y

def switcher(ind):
    switch = {
        0: gradient_descent,
        1: stochastic_gradient_descent
    }
    return switch.get(ind)

def usage():
    print './main.py -f <datafile> [opts]'
    print '-h, --help : help'
    print '-f, --file= ... : datafile'
    print '-g, --gradient-descent : gradient descent algorithm'
    print '-s, --stochastic : stochastic gradient descent algorithm, prior if -g in same time'

def main(argv):
    '''

    Actually working with
    - a polynome of degree 3
    - a learning rate equals to 0.000000001
    - a max_iteration equals to 1000

    '''

    filename = ''
    theta = [random.uniform(-100, 100) for _ in range (3)] # initial theta
    algo = -1
    max_iteration = 1000
    alpha = 0.000000001

    try:
        opts, args = getopt.getopt(argv, 'hf:gs', ['help', 'file=', 'radient-descent', 'stochastic'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-f', '--file'):
            filename = arg
            inputs, targets = getData(filename)
        elif opt in ('-g', '--gradient-descent'):
            algo = 0
        elif opt in ('-s', '--stochastic'):
            algo = 1

    print switcher(algo)(theta, inputs, targets, max_iteration, alpha)

if __name__ == '__main__':
    main(sys.argv[1:])
