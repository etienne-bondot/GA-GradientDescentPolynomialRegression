#!/usr/bin/env python

import sys, getopt, settings, time, chart
from Population import *

def usage():
    print './main.py -f <datafile> [opts]'
    print '-h, --help : help'
    print '-f, --file= ... : datafile'
    print '-i, --max-iterations : max iterations'
    print '-p, --population : the number of genes within the population'
    print '-t, --type= [special,one_point_crossover,two_points_crossover] : type of crossover applied on the population'

def update_progress(progress, population):
    sys.stdout.write('\r')
    sys.stdout.write("[%-40s] %d%% - [%s | %s | %s]" % ('=' * (progress * 40 / 100), progress, population.get_best_fitness(), population.get_worst_fitness(), population.get_average_fitness()))
    sys.stdout.flush()
    if progress % 10 == 0:
        population.store_fitnesses(progress)

def main(argv):
    filename = ''
    crossover_methods = []
    max_iterations = 1000
    pop_size = 500

    try:
        opts, args = getopt.getopt(argv, 'hf:i:p:t:', [
        'help',
        'file=',
        'max-iterations',
        'population',
        'type='
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
        elif opt in ('-p', '--population'):
            pop_size = int(arg)
        elif opt in ('-t', '--type'):
            crossover_methods = arg.split(',')
            print crossover_methods

    start_time = time.time()
    # testing special crossover
    if not crossover_methods or 'special' in crossover_methods:
        P = Population(pop_size)
        for i in range(max_iterations):
            update_progress(i * 100 / max_iterations, P)
            P.evolve('special')
            if P.get_best_fitness() == 0: break

        P.result('special')
        print 'processing time: {}'.format(time.time() - start_time)

    # testing one point crossover
    if not crossover_methods or 'one_point_crossover' in crossover_methods:
        P = Population(pop_size)
        for i in range(max_iterations):
            update_progress(i * 100 / max_iterations, P)
            P.evolve('one_point_crossover')
            if P.get_best_fitness() == 0: break

        P.result('one_point_crossover')
        print 'processing time: {}'.format(time.time() - start_time)

    # testing two points crossover
    if not crossover_methods or 'two_points_crossover' in crossover_methods:
        P = Population(pop_size)
        for i in range(max_iterations):
            update_progress(i * 100 / max_iterations, P)
            P.evolve('two_points_crossover')
            if P.get_best_fitness() == 0: break

        P.result('two_points_crossover')
        print 'processing time: {}'.format(time.time() - start_time)

    # testing average crossover
    if not crossover_methods or 'average_crossover' in crossover_methods:
        P = Population(pop_size)
        for i in range(max_iterations):
            update_progress(i * 100 / max_iterations, P)
            P.evolve('average_crossover')
            if P.get_best_fitness() == 0: break

        P.result('average_crossover')
        print 'processing time: {}'.format(time.time() - start_time)

if __name__ == '__main__':
    main(sys.argv[1:])
