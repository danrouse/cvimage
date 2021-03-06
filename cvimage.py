import cv2
import numpy as np
import inspect

cvSkipMethods = [
	'imread',
	'imreadmulti',
	'imshow',
	'imwrite',
	'imdecode',
	'imencode',
	'findContours'
]

cvChainableRetvals = [
	'dst', '_dst', 'img', 'image', 'edges']

cvMethods = {}
cvConstants = {}
cvNamespaces = {
	'threshold': 'THRESH',
	'morphologyEx': 'MORPH',
	'cvtColor': 'COLOR',
	'matchTemplate': 'TM'
}

def getCvMethods(root, method_dict, constants_dict):
	for method_name, method in inspect.getmembers(root):
		if method_name in cvSkipMethods or method == root:
			continue
		elif inspect.ismodule(method):
			getCvMethods(method, method_dict, constants_dict)
		elif callable(method) and method.__doc__:
			method_type = 'pass'
			method_ret = method.__doc__.split('->')[-1].strip()
			if method_ret in cvChainableRetvals:
				method_type = 'chainable'				
			else:
				ret_values = method_ret.split(',')
				if len(ret_values) > 1:
					if ret_values[-1].strip() in cvChainableRetvals:
						method_type = 'data_chainable'

			# if method_type == 'pass':
			# 	print(method_name, method_ret)

			# normalize first letter to lowercase
			method_name = method_name[0].lower() + method_name[1:]
			
			# resolve submodule conflicts
			if method_name in method_dict:
				method_name = '{}_{}'.format(root.__name__.split('.')[-1], method_name)

			method_dict[method_name] = (method_type, method)
		elif method_name[:2] != '__' or method_name[-2:] != '__':
			constants_dict[method_name] = method

getCvMethods(cv2, cvMethods, cvConstants)


class CvImage:
	"""Chainable wrapper for OpenCV's python bindings."""
	def __init__(self, *args, **kwargs):
		if type(args[0]) is str:
			# initialize from a filename
			self.image = cv2.imread(*args)
		elif type(args[0]) is CvImage:
			self.image = args[0].image
		elif type(args[0]) is np.ndarray:
			# initialize from np array (OpenCV image)
			self.image = args[0]
		else:
			self.image = np.zeros((1,1), np.uint8)

		if 'name' in kwargs:
			self.name = kwargs.name
		else:
			self.name = 'CvImage'

		# set dimensions (width, height, depth)
		shape = self.image.shape
		self.height = shape[0]
		self.width = shape[1]
		if len(shape) == 3:
			self.depth = shape[2]
		else:
			self.depth = 1

	def __repr__(self):
		return repr(self.image)

	def __getattr__(self, key):
		if key in cvMethods:
			return self.wrapCvMethod(key)
		else:
			raise AttributeError(key)

	def __getitem__(self, key):
		return self.image[key]

	def __setitem__(self, key, val):
		self.image[key] = val

	def __delitem__(self, key):
		del self.image[key]

	def __cmp__(self, target):
		if hasattr(target, 'image'):
			return cmp(self.image, target.image)
		else:
			return cmp(self.image, target)

	def wrapCvMethod(self, key):
		method_type, method = cvMethods[key]

		def wrapped(*args, **kwargs):
			args = list(args)
			# allow for constants passed as strings
			namespace = cvNamespaces[method.__name__] if method.__name__ in cvNamespaces else ''
			for i, arg in enumerate(args):
				if type(arg) is str:
					args[i] = CvImage.get_const(arg, namespace)

			will_copy = False
			if 'copy' in kwargs:
				will_copy = kwargs['copy']
				del kwargs['copy']

			if method_type == 'chainable':
				im = method(self.image, *args, **kwargs)

				if will_copy:
					return CvImage(im)
				else:
					self.image = im
					return self
			elif method_type == 'data_chainable':
				ret = method(self.image, *args, **kwargs)
				self.data = ret[:-1]
				if len(self.data) == 1:
					self.data = self.data[0]
				im = ret[-1]

				if will_copy:
					return CvImage(im)
				else:
					self.image = im
					return self
			else:
				return method(self.image, *args, **kwargs)

		return wrapped

	def show(self, name = ''):
		cv2.imshow(name or self.name, self.image)
		return self

	def save(self, filename = ''):
		cv2.imwrite(filename or '{}.png'.format(self.name), self.image)
		return self

	def copy(self):
		return CvImage(self.image.copy())

	def wait(self, delay = 0):
		keycode = cv2.waitKey(delay)
		return self

	def preview(self, delay = 0):
		return self.show().wait(delay)

	def crop(self, pt1, pt2, **kwargs):
		slices = []
		for i, arg in enumerate(pt1 + pt2):
			if type(arg) is float:
				# percentage
				if i % 2:
					arg = int(arg * self.height)
				else:
					arg = int(arg * self.width)
			slices.append(arg)

		im = self.image[slices[1]:slices[3], slices[0]:slices[2]]

		if 'copy' in kwargs and kwargs['copy']:
			return CvImage(im)
		else:
			self.image = im	
			return self

	def findContours(self, *args, **kwargs):
		arg_list = CvImage.get_consts(*args)
		image, contours, hierarchy = cv2.findContours(self.image.copy(), *arg_list)
		return contours, hierarchy


	@staticmethod
	def get_consts(*args, **kwargs):
		namespace = kwargs['namespace'] if 'namespace' in kwargs else ''
		ret = []
		for arg in args:
			ret.append(CvImage.get_const(arg, namespace))

		return ret

	@staticmethod
	def get_const(search_name, namespace = ''):
		name = search_name.upper()
		if search_name in cvConstants:
			return cvConstants[search_name]
		elif name in cvConstants:
			return cvConstants[name]
		else:
			key = '{}_{}'.format(namespace.upper(), name)
			if key in cvConstants:
				return cvConstants[key]

		return search_name

kernel_cache = {}
def cvKernel(key = 'ellipse', size = (3,3)):
	cache_key = key + str(size)
	if cache_key not in kernel_cache:
		cv_key = CvImage.get_const(key, 'morph')
		kernel_cache[cache_key] = cv2.getStructuringElement(cv_key, size)
	return kernel_cache[cache_key]
