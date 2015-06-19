import unittest

import numpy as np
import cv2
from cvimage import CvImage

class TestCvMethods(unittest.TestCase):

	def test_filter_chain(self):
		sample = np.random.rand(512, 512, 3)
		sample = np.uint8(sample)

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

	#def test_contrib_methods(self):


if __name__ == '__main__':
	unittest.main()
