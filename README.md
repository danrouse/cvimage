# CvImage - a Chainable Python Class for OpenCV

## Usage
    import cv2
    from CvImage import CvImage
    
    im = CvImage('test.png') \
        .blur(3)
        .Canny(100, 200)
        .show()

## TODO
- Code coverage
- Better inline docs