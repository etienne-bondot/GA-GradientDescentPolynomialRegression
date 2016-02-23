import settings
import matplotlib.pyplot as plt

def plot_that(title, _outputs, _fitness, _worst_fitness, _average_fitness):
    plt.title('Fitness per epoch (_/iteration) - ' + title, fontsize=16)
    plt.ylabel('Fitness')
    plt.xlabel('Epoch')
    plt.semilogy([i for i in range(len(_fitness))], _fitness, 'r', label='Best fitness')
    plt.semilogy([i for i in range(len(_worst_fitness))], _worst_fitness, 'b', label='Worst fitness')
    plt.semilogy([i for i in range(len(_average_fitness))], _average_fitness, 'g', label='Average fitness')
    plt.legend()
    plt.show()

def generate_mpl(title, _outputs, _fitness):
    plt.title('GA applicant processing', fontsize=16)
    plt.ylabel('f(x)')
    plt.xlabel('x')
    data, = plt.plot(settings.x, settings.y, 'b+', label='Original data', linewidth=1)
    solutions, = plt.plot(settings.x, _outputs, 'r-', label='Best solution', linewidth=1)
    plt.legend(handles=[data, solutions], loc=0)
    plt.text(400, 0.65, r'$f(x) = a + bx + cx^2 + dx^3 + ex^4 + fx^5$')
    plt.draw()
    plt.show()
