#all: read-test write-test test allegro4 view16
all: opencv

UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
## On Ubuntu / Debian
CV_CFLAGS := $(shell pkg-config --cflags opencv)
CV_LDFLAGS := $(shell pkg-config --libs opencv)
endif
ifeq ($(UNAME), Darwin)
## On Mac OS X
CV_CFLAGS := $(shell pkg-config --cflags opencv)
CV_LDFLAGS := $(shell pkg-config --libs opencv)
endif

CC = g++

opencv: opencv.cpp
	$(CC) opencv.cpp -o opencv $(CV_CFLAGS) $(CV_LDFLAGS)

clean:
	-rm opencv
.PHONY: clean
