#!/usr/bin/env python

from xml.etree.ElementTree import parse
from numpy import array
import cv2
import re
import os
from datetime import datetime
from multiprocessing import Pool, Manager
from blobs import find_blobs
from tiff import TIFF
from progress import ProgressMeter
import time


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
        total = len(xmlfiles)
        pm = ProgressMeter(total=total)

        ## Parallel processing of the files
        finished = False
        num_processes = 4
        i = 0
        p = Pool(processes=num_processes)
        manager = Manager()
        queue = manager.Queue()
        result = p.map_async(process_MeasurementPoint_Wrapper, [(xmlfile, queue) for xmlfile in xmlfiles])
        while not finished:
            if not queue.empty():
                #print("Processed XML file %s." % queue.get())
                queue.get()
                i += 1
                if i == total: finished = True
                if i % num_processes == 0: pm.update(4)
            else:
                time.sleep(0.02)
        pm.update(4)
        self.measurementPoints = result.get()
        ## Sequential processing of the files
        #self.measurementPoints = []
        #for xmlfile in xmlfiles:
        #    self.measurementPoints.append(process_MeasurementPoint(xmlfile))
        #    pm.update(1)

        self.after_process()

    def after_process(self):
        """Calculate overall properties
        If they are expensive to calculate, their calculation should be prepared in
        the creation process of the process_MeasurementPoint() call.
        """
        print "Starting after-processing."
        self.minmax = ( min([mp.minmax[0] for mp in self.measurementPoints]),
                        max([mp.minmax[1] for mp in self.measurementPoints]) )
        self.blobs_found = max([len(mp.blobs) for mp in self.measurementPoints]) > 0
        for mp in self.measurementPoints:
            mp.collection = self

def process_MeasurementPoint_Wrapper(args):
    instructions = args[0]
    queue = args[1]
    retval = process_MeasurementPoint(instructions)
    queue.put(instructions['f'])
    return retval

def process_MeasurementPoint(instructions):
    image_file, bg_file = Measurement.other_files_for_xml(instructions['f'])
    return MeasurementPoint(
        instructions['date'],
        instructions['avg'],
        os.path.join(instructions['d'], instructions['f']),
        os.path.join(instructions['d'], image_file),
        os.path.join(instructions['d'], bg_file),
        )

class MeasurementPoint(object):
    PD_SCOPE_CHANNEL = 0
    ION_SCOPE_CHANNEL = 1
    collection = None
    def __init__(self, date, avgnum, xmlfile, imgfile, bgfile=None):
        #print("Reading XML file %s" % xmlfile)
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
        self.img = TIFF(os.path.join(imgfile))
        if bgfile:
            self.img.data -= TIFF(os.path.join(bgfile)).data
        self.minmax = self.img.minmax()
        self.percentiles = self.img.percentiles([1,5,99,99.995])
        self.blobs = find_blobs(self.img.data)
    def display_image(self, rescale=False, rescale_to_global_minmax=False, rescale_to_percentile_and_max=False):
        if rescale:
            i = self.img
            if rescale_to_global_minmax:
                print("Rescaling to global min and max values (%d,%d)" % self.collection.minmax)
                img_data = i.rescale(self.collection.minmax)
            elif rescale_to_percentile_and_max:
                print("Rescaling image using 5 percent percentile to local maximum value: (%d,%d)." % (self.percentiles[5], i.minmax()[1]))
                img_data = i.rescale((self.percentiles[5], i.minmax()[1]))
            else:
                img_data = i.rescale(i.minmax())
        else:
            img_data = self.img.data
        cv2.imshow('test',img_data)
        return cv2.waitKey()
    def __str__(self):
        return "MeasurementPoint: (date: %s, xml: %s, image: %s, bgimage: %s)" % (self.date, self.xmlfile, self.imgfile, self.bgfile)

    def dump_xml_structure(self, level=0):
        output = ''
        for element in self.xml:
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
            output += self.dump_xml_structure(element, level+1)
        return output

    def get_stage_positions(self):
        raise NotImplementedError

    def get_photodiode_scope_channel(self):
        return self.get_scope_channel(self.PD_SCOPE_CHANNEL)

    def get_ion_scope_channel(run):
        return self.get_scope_channel(self.ION_SCOPE_CHANNEL)

    def get_scope_channel(run, channel_no):
        for scope in run:
            if scope.tag == 'NI_TCP_Scope':
                for channel in scope:
                    if channel.tag == 'CH' + str(channel_no):
                        data = channel.text
                        data = [float(value) for value in data.split()]
                        return data
    def calculate_ion_signal(self):
        ion_signal_point = 0.0
        for ion_signal_point in self.get_ion_scope_channel():
            ion_signal += ion_signal_point
        return ion_signal
