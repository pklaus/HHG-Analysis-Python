#!/usr/bin/env python

from xml.etree.ElementTree import parse
from numpy import array

def read_run_file(filename):
    file = open(filename, "r")
    tree = parse(file)
    elem = tree.getroot()
    return elem

def dump_structure(run, level=0):
    output = ''
    for element in run:
        output += ''.join(['--' for i in range(level)])
        output += "> " + element.tag
        if element.text != None:
            content = element.text.replace("\n"," ")
            output += " :  "
            if len(content) < 20:
                output += content
            else:
                output += content[:20] + " ..."
        output += "\n"
        output += dump_structure(element, level+1)
    return output

def get_stage_positions(run):
    pass

def get_photodiode_scope_channel(run):
    return get_scope_channel(run, 0)

def get_ion_scope_channel(run):
    return get_scope_channel(run, 1)

def get_scope_channel(run, channel_no):
    for scope in run:
        if scope.tag == 'NI_TCP_Scope':
            for channel in scope:
                if channel.tag == 'CH' + str(channel_no):
                    data = channel.text
                    data = [float(value) for value in data.split()]
                    return data

def calculate_ion_signal(run):
    ion_signal_point = 0.0
    for ion_signal_point in get_ion_scope_channel(run):
        ion_signal += ion_signal_point
    return ion_signal
