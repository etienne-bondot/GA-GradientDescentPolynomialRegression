#!/usr/bin/env python

import sys, getopt, settings, time
from Population import *

def usage():
    print ''
    print './main.py -f <datafile> [opts]'
    print '-h, --help : help'
    print '-f, --file=... : datafile'
    print '-i, --max-iterations : max iterations'
    print '-p, --population : the number of genes within the population'
    print '-t, --type=<TYPE,TYPE> : type of crossover applied on the population'
    print '-s, --stop : stop when the best fitness is 0, otherwise continue until the max iteration is reach'
    print 'types:'
    print '- default_crossover'
    print '- one_point_crossover'
    print '- two_points_crossover'
    print '- average_crossover'
    print ''
    print 'Example:'
    print '$> python main.py -f data/datfile.dat -t default_crossover -i 1000 -p 1000 -s'
    print ''

def update_progress(progress, population):
    sys.stdout.write('\r')
    sys.stdout.write("[%-40s] %d%% - [%s | %s | %s]%-5s" % ('=' * (progress * 40 / 100),
        progress,
        population.get_best_fitness(),
        population.get_worst_fitness(),
        population.get_average_fitness(), ''))
    sys.stdout.flush()

def main(argv):
    filename = ''
    crossover_methods = []
    max_iterations = 1000
    pop_size = 500
    stop = False

    try:
        opts, args = getopt.getopt(argv, 'hf:i:p:t:s', [
        'help',
        'file=',
        'max-iterations',
        'population',
        'type=',
        's'
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
        elif opt in ('-s', '--stop'):
            stop = True

    start_time = time.time()
    for method in crossover_methods:
        P = Population(pop_size)
        for i in range(max_iterations):
            try:
                P.evolve(method)
            except KeyError, e:
                usage()
                sys.exit()
            update_progress(i * 100 / max_iterations, P)
            if stop == True:
                if int(P.get_best_fitness()) <= 0: break
        update_progress(i * 100 / max_iterations, P)
        print 'processing time: {}'.format(time.time() - start_time)
        P.result()

if __name__ == '__main__':
    main(sys.argv[1:])
