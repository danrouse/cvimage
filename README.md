# CvImage - a Chainable Python Class for OpenCV

CvImage is a chainable wrapper for OpenCV's python bindings.

## Installation
	- Using ``pip``:
	    pip install cvimage

## Usage
	from cvimage import CvImage
    im = CvImage('test.png') \
        .blur(3) \
        .canny(100, 200) \
        .show()
