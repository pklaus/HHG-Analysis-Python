#!/usr/bin/env python

from acquisition import read_run_file, dump_structure, get_stage_positions, get_photodiode_scope_channel, get_ion_scope_channel, get_scope_channel, calculate_ion_signal
from plot import plot_multiple, plot
from signalprocessing import calculate_sum, remove_high_frequency_noise, smooth
from numpy import sum

filename = 'HHG_20110818T054235f91_.xml'
#filename = 'HHG2.xml'

run = read_run_file(filename)

print dump_structure(run)

photodiode_ydata = get_photodiode_scope_channel(run)
ion_ydata = get_ion_scope_channel(run)
lowpass_ion_ydata = remove_high_frequency_noise(ion_ydata)
sg_ion_ydata = smooth(ion_ydata)

ion_signals = [ion_ydata, lowpass_ion_ydata, sg_ion_ydata]
#ion_sums = [sum(signal) for signal in ion_signals]
#print ion_sums
ion_corrected_sums = [ calculate_sum(signal, 2900, 4000, 0.00155) for signal in ion_signals]
print ion_corrected_sums

ion_sum=0.0
lowpass_ion_sum=0.0
sg_ion_sum=0.0
sum_diff = []
for i in range(len(ion_ydata)):
    ion_sum += ion_ydata[i]
    lowpass_ion_sum += lowpass_ion_ydata[i]
    sg_ion_sum += sg_ion_ydata[i]
    #sum_diff.append(ion_sum - sg_ion_sum)
    sum_diff.append(ion_sum - lowpass_ion_sum)

#from numpy.fft import fft
plots = [
    ('Photodiode', range(len(photodiode_ydata)), photodiode_ydata),
    ('Ion Detector', range(len(ion_ydata)), ion_ydata),
    #[ range(len(ion_ydata)), fft(ion_ydata)],
    ('Ion Detector (low pass)', range(len(lowpass_ion_ydata)), lowpass_ion_ydata),
    ('Ion Detector (difference direct - low pass)', range(len(sum_diff)), sum_diff),
    ('Ion Detector (SG filter)', range(len(sg_ion_ydata)), sg_ion_ydata),
  ]
plot_multiple( plots )

plot('time', 'photodiode signal', [ range(len(photodiode_ydata)), photodiode_ydata], True)
