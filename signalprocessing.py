#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A collection of useful signal processing functions """

# wget http://public.procoders.net/sg_filter/sg_filter.py
import sg_filter
def smooth(signal):
    """ Smoothing a signal using the Savitzky–Golay filter. """
    coeff = sg_filter.calc_coeff(len(signal)/500, 5)
    return sg_filter.smooth(signal, coeff) 

from numpy import real, arctan, pi
from numpy.fft import fft, ifft
def remove_high_frequency_noise(signal, cutoff=15.):
    """
    A Low-pass filter.
    See http://en.wikipedia.org/wiki/Low-pass_filter .
    :param cutoff: defines the limit at which higher frequencies should be removed (from 0. to 100.).
    :type cutoff: float.
    """
    cutoff_range = (1 + len(signal) * cutoff * .01, len(signal) - cutoff * .01 * len(signal))
    spectrum = fft(signal)
    i = 0
    spectrum_cut = []
    for freq in spectrum:
        ### no filter at all:
        #spectrum_cut.append(freq)
        ### sharply defined range cut out:
        if i < cutoff_range[0]:
            spectrum_cut.append(freq)
        elif i < cutoff_range[1]:
            spectrum_cut.append(0.0)
            ### lowpass with linear cut:
            #spectrum_cut.append( freq * ( 2 * cutoff_range[0] - i)/( cutoff_range[1] - cutoff_range[1] ) )
        else:
            #spectrum_cut.append(0.0)
            spectrum_cut.append(freq)
        ### arctan as transfer function
        #spectrum_cut.append(freq * (arctan((-i+cutoff_range[0])/cutoff_range[0]*10)/pi + .5) )
        ### lowpass filter with sharp cutoff:
        #spectrum_cut.append(freq if i < cutoff_range[0] else 0.0)
        i += 1
    return real(ifft(spectrum_cut))

from numpy import sum
def calculate_sum(signal, val_from, val_to, baseline):
    """ A function to calculate the sum of a selection of values from which a baseline value has been substracted. """
    cropped_signal = signal[val_from:val_to+1]
    return sum(cropped_signal) - baseline * (val_to+1 - val_from)
