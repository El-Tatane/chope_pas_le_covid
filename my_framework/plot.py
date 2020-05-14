import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_simple_sir(list_t, list_S, list_I, list_R ):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure()
    ax = fig.add_subplot(facecolor='#dddddd')
    ax.plot(list_t, list_S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(list_t, list_I/1000, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(list_t, list_R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Person Number (10^3)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()


def plot_triple_sir(list_t, list_predict_S, list_predict_I, list_predict_R, list_true_S, list_true_I, list_true_R ):
    list_label = ["Susceptible", "Infected", "Recovered with immunity"]
    for (list_pred, list_true), tilte in zip([[list_predict_S, list_true_S], [list_predict_I, list_true_I], [list_predict_R, list_true_R]], list_label):
            fig = plt.figure()
            ax = fig.add_subplot(facecolor='#dddddd')
            ax.plot(list_t, list_pred/1000, 'b', alpha=0.5, lw=2, label='Predict')
            ax.plot(list_t, list_true/1000, 'r', alpha=0.5, lw=2, label='True')
            ax.set_xlabel('Time (days)')
            ax.set_ylabel('Person Number (10^3)')
            ax.yaxis.set_tick_params(length=0)
            ax.xaxis.set_tick_params(length=0)
            ax.grid(b=True, which='major', c='w', lw=2, ls='-')
            legend = ax.legend()
            legend.get_frame().set_alpha(0.5)
            for spine in ('top', 'right', 'bottom', 'left'):
                ax.spines[spine].set_visible(False)
            fig.suptitle(tilte)
            plt.show()
