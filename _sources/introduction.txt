Introduction
============

The most valuable piece of code of this toolkit at this time is the command line
utility :mod:`walk_folder`. To use it, simply run the follwing command on the
command line (adjust your path to a measurement folder)::

  ./walk_folder.py /some/path/DATA/HHG_00012Ar/

This will load the files in that folder and will let you walk you through the
measurement points using the arrow keys.

Here is an example video that illustrates the usage of these tools:

.. raw:: html

   <video width="640" height="360" controls="controls">
     <source src="_static/screencast_walk-folder_w-subtitles.mp4" type="video/mp4" />
     <source src="_static/screencast_walk-folder_w-subtitles.ogv" type="video/ogg" />
     Your browser does not support the video tag.
   </video>



Requirements
------------

The following requirements have to be met in order to run this software properly:

* OpenCV_ -- An open source computer vision library used to read image files and more.
* NumPy_ -- A fast Python module for number crunching.

Optional dependencies include

* matplotlib_

To create this documentation, you also need:

* Sphinx_

Standard Python modules required for this to work include:

* multiprocessing_
* xml.etree.ElementTree_
* datetime.datetime_
* time_
* re_
* os_
* sys_

.. _OpenCV: http://opencv.willowgarage.com/wiki/
.. _OpenCV-Docs: http://docs.opencv.org/
.. _NumPy: http://numpy.scipy.org/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _Sphinx: http://sphinx.pocoo.org/

.. _multiprocessing: http://docs.python.org/library/multiprocessing.html
.. _xml.etree.ElementTree: http://docs.python.org/library/xml.etree.elementtree.html
.. _datetime.datetime: http://docs.python.org/library/datetime.html#datetime.datetime
.. _time: http://docs.python.org/library/time.html
.. _re: http://docs.python.org/library/re.html
.. _os: http://docs.python.org/library/os.html
.. _sys: http://docs.python.org/library/sys.html


Installation of the Requirements
--------------------------------

On a Mac:

1. Install Homebrew_
2. Install Numpy: ``pip install numpy``
3. Install OpenCV like this: ``brew install opencv``
4. Add these lines to your ``~/.bashrc`` to let Python find it::

    # needed for OpenCV:
    PYTHONPATH="/usr/local/lib/python2.7/site-packages/":"${PYTHONPATH}"
    export PYTHONPATH

On Ubuntu Linux:

1. Install OpenCV (read this: http://opencv.willowgarage.com/wiki/InstallGuide)::

    sudo apt-get install cmake libgtk2.0-dev
    cd ~/Downloads
    wget http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.0/OpenCV-2.4.0.tar.bz2
    tar -xf OpenCV-2.4.0.tar.bz2
    cd OpenCV-2.4.0
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON .
    make
    sudo make install

2. Install Numpy using ``sudo apt-get install python-numpy python-scipy``

.. _Homebrew: http://mxcl.github.com/homebrew/
