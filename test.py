import unittest

import numpy as np
import cv2
from cvimage import CvImage

def gen_sample(dims = (512, 512, 3)):
	return np.uint8(np.random.rand(*dims))

class TestCvMethods(unittest.TestCase):

	def test_filter_chain(self):
		sample = gen_sample()

		b_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
		baseline = sample.copy()
		baseline = cv2.blur(baseline, (3, 3))
		baseline = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
		baseline = cv2.Canny(baseline, 100, 200)
		baseline = cv2.dilate(baseline, b_kernel)

		p_kernel = CvImage.kernel('ellipse', (3, 3))
		patient = CvImage(sample.copy())\
			.blur((3, 3))\
			.cvtColor(cv2.COLOR_BGR2GRAY)\
			.canny(100, 200)\
			.dilate(p_kernel)

		self.assertEqual(str(baseline), str(patient.image))

	def test_data_return(self):
		sample = gen_sample()

		result, threshold = cv2.threshold(sample, 100, 200, cv2.THRESH_BINARY)
		im = CvImage(sample).threshold(100, 200, cv2.THRESH_BINARY)

		self.assertEqual(result, im.data)

	def test_constants(self):
		sample = gen_sample()

		result, threshold = cv2.threshold(sample, 100, 200, cv2.THRESH_BINARY)
		im = CvImage(sample).threshold(100, 200, 'THRESH_BINARY')

		self.assertEqual(str(threshold), str(im.image))

	#def test_kernel(self):
	#def test_contrib_methods(self):


if __name__ == '__main__':
	unittest.main()
