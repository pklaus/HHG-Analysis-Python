# -*- coding: utf-8 -*-

""" A collection of useful mathematical tools and functions. """

import numpy as np

def scoreatpercentile(a, per, limit=()):
    """
    Calculate the score at the given percentile_ `per` of the sequence `a`.

    Largely the same as http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.scoreatpercentile.html .

    .. _percentile: http://en.wikipedia.org/wiki/Percentile"""
    values = np.sort(a, axis=0)
    if limit:
        values = values[(limit[0] <= values) & (values <= limit[1])]
    idx = per /100. * (values.shape[0] - 1)
    if (idx % 1 == 0):
        score = values[idx]
    else:
        score = values[int(idx)] + (idx % 1) * (values[int(idx) + 1] - values[int(idx)])
    return score
