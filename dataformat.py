#!/usr/bin/env python

from xml.etree.ElementTree import parse
from numpy import array
import re
import os
from datetime import datetime
from multiprocessing import Pool
from tiff import TIFF16bit
import cv2

class Measurement(object):
    avg_folder_match = r'avg_(\d)'
    timestamp_match = r'(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})f(\d{2})'
    image_match = r'HHG_' + timestamp_match + '_\.tif'
    bg_image_match = r'HHG_' + timestamp_match + '_bg\.tif'
    xml_match = r'HHG_' + timestamp_match + '_\.xml'

    def __init__(self, folder):
        self.read_measurement(folder)

    @staticmethod
    def other_files_for_xml(xml_filename):
        "Returns the names of the image and background files that belong to a certain xml file."
        return xml_filename.replace('.xml','.tif'), xml_filename.replace('.xml','bg.tif')

    def read_measurement(self, folder):
        avg_folders = []
        for filename in os.listdir(folder):
            if re.match(self.avg_folder_match, filename):
                avg_folders.append(filename)
        xmlfiles = []
        for avg_folder in avg_folders:
            for dirname, dirnames, filenames in os.walk(os.path.join(folder,avg_folder)):
                for filename in filenames:
                    xmlmatch = re.match(self.xml_match, filename)
                    if xmlmatch:
                        vals = [int(val) for val in xmlmatch.groups()]
                        date = datetime(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6]*10000)
                        image_file, bg_file = Measurement.other_files_for_xml(filename)
                        if not os.path.isfile(os.path.join(dirname, image_file)):
                            raise NameError('No TIFF image found for XML %s.' % filename)
                        if not os.path.isfile(os.path.join(dirname, bg_file)):
                            raise NameError('No background TIFF image found for XML %s.' % filename)
                        xmlfiles.append({'date': date, 'd': dirname, 'f': filename, 'avg': re.match(self.avg_folder_match, avg_folder).groups()[0]})
        if xmlfiles == []:
            raise NameError("This folder doesn't seem to contain measurement data")

        ## Parallel processing of the files
        #p = Pool(processes=4)
        #self.measurementPoints = p.map(process_MeasurementPoint, xmlfiles)
        self.measurementPoints = []
        for xmlfile in xmlfiles:
            self.measurementPoints.append(process_MeasurementPoint(xmlfile))

def process_MeasurementPoint(instructions):
    #print instructions
    image_file, bg_file = Measurement.other_files_for_xml(instructions['f'])
    return MeasurementPoint(
        instructions['date'],
        instructions['avg'],
        os.path.join(instructions['d'], instructions['f']),
        os.path.join(instructions['d'], image_file),
        os.path.join(instructions['d'], bg_file)
        )

class MeasurementPoint(object):
    def __init__(self, date, avgnum, xmlfile, imgfile, bgfile = None):
        print("Reading XML file %s" % xmlfile)
        self.date = date
        self.avgnum = avgnum
        self.read_xml(xmlfile)
        self.read_image(imgfile,bgfile)
    def read_xml(self, xmlfile):
        """ xmlfile should be ('/path/to/folder','filename.xml') """
        self.xmlfile = xmlfile
        f = open(xmlfile, "r")
        tree = parse(f)
        self.xml = tree.getroot()
        f.close()
    def read_image(self, imgfile, bgfile=None):
        """ imgfile and bgfile should be ('/path/to/folder','filename.xml') """
        self.imgfile, self.bgfile = imgfile, bgfile
        self.img = TIFF16bit(os.path.join(imgfile))
        if bgfile:
            self.img.img -= TIFF16bit(os.path.join(bgfile)).img
    def rescale_image(self):
        self.img.rescale()
    def display_image(self):
        cv2.imshow('test',self.img.img)
        print("Press key in OpenCV window to continue / exit.")
        cv2.waitKey()
    def __str__(self):
        return "MeasurementPoint: (date: %s, xml: %s, image: %s, bgimage: %s)" % (self.date, self.xmlfile, self.imgfile, self.bgfile)

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
