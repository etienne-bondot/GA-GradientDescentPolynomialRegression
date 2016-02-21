import plotly, settings

from plotly import tools
from plotly.graph_objs import Scatter, Layout, Marker

import numpy as np
import matplotlib.pyplot as plt

def generate(_outputs, _fitness):
    plotly.offline.plot({
        'data': [
            Scatter(
                x = settings.x,
                y = _outputs,
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
                x = settings.x,
                y = settings.y,
                name = 'inputs',
                mode = 'markers',
                marker = Marker(
                    color = 'blue',
                    symbol = 'x',
                    size = 2
                )
            ),
            Scatter(
                x = [i for i in range(len(_fitness))],
                y = _fitness, mode='lines+markers',
                name = 'fitness',
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
                title = 'fitness per epoch',
                domain=[0.5, 1]
            )
        )
    })

def generate_mpl(_outputs, _fitness):
    factor = 0.1
    fig = plt.figure()
    fig.suptitle("GA applicant processing", fontsize=16)

    # error
    ax = plt.subplot(2, 1, 1)
    ax.set_title('Fitness per epoch (_/iteration)')
    ax.set_ylabel('Fitness: h0 = sqrt((Fx - y)^2)')
    ax.set_xlabel('Epoch')
    ax.plot([i for i in range(len(_fitness))], _fitness, 'r-')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    new_xlim = (xlim[0] + xlim[1])/2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor)
    new_ylim = (ylim[0] + ylim[1])/2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor)
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)

    # data
    ax = plt.subplot(2, 1, 2)
    ax.set_title('Data graph')
    ax.set_ylabel('f(x) = a + bx + cx^2 + dx^3 + ex^4 + fx^5')
    ax.set_xlabel('x')
    ax.plot(settings.x, settings.y, 'b+')

    # solutions
    ax = plt.subplot(2, 1, 2)
    ax.plot(settings.x, _outputs, 'r-')

    plt.show()
