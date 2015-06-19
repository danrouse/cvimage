# CvImage

CvImage is a chainable wrapper for OpenCV's python bindings. This jQuery-like syntax is convenient for performing series of filters and transformations on a single image.

## Usage

- Install from [pip](https://pypi.python.org/pypi/cvimage) (``pip install cvimage``) or [GitHub releases]
All ``cv2`` methods that take an image (numpy array) as their first argument can be called from a ``CvImage`` context. Any of *those* methods that return an image can be chained together. ``cv2`` constants can be passed as strings.

```python
from cvimage import CvImage

im = CvImage('test.png') \
	.blur(3) \
	.threshold(0, 100, 'THRESH_BINARY') \
	.canny(100, 200) \
	.save('test-edges.png')
```

A ``CvImage`` instance can be created with both a pre-existing image (numpy array) or with a filename, which gets passed to ``cv2.imread``. An image can be saved at any time using ``CvImage.save(filename)``, which calls ``cv2.imwrite``.

Method names beginning with a Capital Letter (e.g. ``Canny, Sobel, Laplacian``) are normalized to lowercase (``canny, sobel, laplacian``). On the one hand, they are names of people, on the other hand, it causes an inconsistent API.

Methods that return data as well as an image, such as ``cv2.threshold``, save their data to ``CvImage.data`` - if they are chained together, only the last called method's data is retained.
	
```python
result, threshold = cv2.threshold(src_im, 100, 200, cv2.THRESH_BINARY)
im = CvImage(src_im).threshold(100, 200, cv2.THRESH_BINARY)
# im.data == result
```


# Reference

## CvImage(...)
Main class that wraps cv2 methods. Constructor will create a new ``CvImage`` from any of the following:
- OpenCV-compatible image data (``numpy.ndarray``)
- Filename to pass to ``cv2.imread``
- A previously created ``CvImage`` to copy

### Attributes

name | type | description
-----|:----:|------------
``height`` | int | image height
``width`` | int | image width
``depth`` | int | image depth
``image`` | numpy.ndarray | image data
``data`` | var | temporary data returned from wrapped functions


### Methods
name | description
-----|------------
``show([name])`` | wraps ``cv2.imshow``
``save([filename])`` | wraps ``cv2.imwrite``
``copy()`` | returns a new ``CvImage`` with the same data
``wait([delay])`` | wraps ``cv2.waitKey``
``preview([delay])`` | calls both ``show()`` and ``wait(delay)``
``crop(pt1, pt2)`` | slices the image, cropping from. Accepts floats as a percentage of the image size.
``findContours(...)`` | wraps ``cv2.findContours`` in a non-destructive way

## CvContour(contour)

## cvKernel()

# Changelog
## 0.1.1
- Added constant passing by string, with hinted namespaces (e.g. ``threshold(...,'binary')`` resolves to ``threshold(...,cv2.THRESH_BINARY)``)