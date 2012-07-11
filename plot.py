#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def plot_multiple(data):
    num = len(data)
    i = 1
    for dataset in data:
        plt.subplot(num*100 + 10 + i)
        plt.suptitle(dataset[0],y=0.89-.825*float(i-1)/num)
        #plt.figtext(.5,.9,dataset[0], fontsize=10, ha='center')
        #plt.title(dataset[0])
        plot('x','y',dataset[1:],False)
        i += 1
    plt.show()

def plot(x_label, y_label, data, show = False):
    """See <http://www.scipy.org/Cookbook/Matplotlib/CustomLogLabels> for example code."""
    #ax = subplot(111)
    #ax.scatter(data[0], data[1], s=40, c='b', marker='s', faceted=False)
    plt.plot(data[0], data[1])
    plt.title(y_label)
    if show: plt.show()
    #xlabel(x_label, fontsize = 12)
    #ylabel(y_label, fontsize = 12)
