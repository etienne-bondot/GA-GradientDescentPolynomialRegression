#!/usr/bin/env python

from Wheel import *
import sys, getopt, random

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
        1: stochastic_gradient_descent,
        2: roulette_wheel_selection
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

    Actually, gradient descent algorithm is working with
    - a polynome of degree 3
    - a learning rate equals to 0.000000001
    - a max_iteration equals to 1000

    '''

    filename = ''
    max_iterations = 1000
    alpha = 0.001

    try:
        opts, args = getopt.getopt(argv, 'hf:gsri:a:', [
        'help',
        'file=',
        'radient-descent',
        'stochastic',
        'roulette-wheel',
        'max-iterations',
        'learning-rate'
    ])
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
        elif opt in ('-i', '--max-iterations'):
            max_iterations = arg
        elif opt in ('-a', '--learning-rate'):
            alpha = float(arg)
        elif opt in ('-g', '--gradient-descent'):
            P = Population(1, 3, -100.0, 100.0)
            P.gradient_descent(inputs, targets, max_iterations, alpha)
        elif opt in ('-r', '--roulette-wheel'):
            P = Population(1, 3, -100.0, 100.0)
            P.roulette_wheel_selection(inputs, targets, max_iterations, alpha)


if __name__ == '__main__':
    main(sys.argv[1:])
