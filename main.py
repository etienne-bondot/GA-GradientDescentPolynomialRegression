#!/usr/bin/env python

import sys, getopt, settings
from Population import *

def usage():
    print './main.py -f <datafile> [opts]'
    print '-h, --help : help'
    print '-f, --file= ... : datafile'
    print '-i, --max-iterations : max iterations'
    print '-a, --learning-rate : the learning rate'
    print '-p, --population : the number of genes within the population'
    print '-g, --gradient-descent : gradient descent algorithm'
    print '-d, --default : GA with crossovers and mutations'

def main(argv):
    filename = ''
    alpha = 0.001
    max_iterations = 3000
    population = 500
    chromosomes = 6
    _min = -1000.0
    _max = 1000.0

    try:
        opts, args = getopt.getopt(argv, 'hf:i:a:p:gd', [
        'help',
        'file=',
        'max-iterations',
        'learning-rate',
        'population',
        'gradient-descent',
        'default'
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
            settings.init(filename)
        elif opt in ('-i', '--max-iterations'):
            max_iterations = int(arg)
        elif opt in ('-a', '--learning-rate'):
            alpha = float(arg)
        elif opt in ('-p', '--population'):
            population = int(arg)
        elif opt in ('-g', '--gradient-descent'):
            P = Population(1, chromosomes, _min, _max)
            P.gradient_descent(max_iterations, alpha)
        elif opt in ('-d', '--default'):
            P = Population(population, chromosomes, _min, _max)
            P.GA(max_iterations)

if __name__ == '__main__':
    main(sys.argv[1:])
