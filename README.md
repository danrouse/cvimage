# CvImage

CvImage is a chainable wrapper for OpenCV's python bindings. This jQuery-like syntax is convenient for performing series of filters and transformations on a single image.

## Installation

- Using ``pip``:

	pip install cvimage


## Usage

All ``cv2`` methods that take an image (numpy array) as their first argument can be called from a ``CvImage`` context. Any of *those* methods that return an image can be chained together. ``cv2`` constants can be passed as strings.


	from cvimage import CvImage

	im = CvImage('test.png') \
		.blur(3) \
		.threshold(0, 100, 'THRESH_BINARY') \
		.canny(100, 200) \
		.save('test-edges.png')


A ``CvImage`` instance can be created with both a pre-existing image (numpy array) or with a filename, which gets passed to ``cv2.imread``. An image can be saved at any time using ``CvImage.save(filename)``, which calls ``cv2.imwrite``.

Method names beginning with a Capital Letter (e.g. ``Canny, Sobel, Laplacian``) are normalized to lowercase (``canny, sobel, laplacian``). On the one hand, they are names of people, on the other hand, it causes an inconsistent API.

Methods that return data as well as an image, such as ``cv2.threshold``, save their data to ``CvImage.data`` - if they are chained together, only the last called method's data is retained.
	

	result, threshold = cv2.threshold(src_im, 100, 200, cv2.THRESH_BINARY)
	im = CvImage(src_im).threshold(100, 200, cv2.THRESH_BINARY)
	# im.data == result

