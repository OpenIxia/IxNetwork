from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FrameSize(Base):
	"""The FrameSize class encapsulates a required frameSize node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FrameSize property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'frameSize'

	def __init__(self, parent):
		super(FrameSize, self).__init__(parent)

	@property
	def FixedSize(self):
		"""Sets all frames to a constant specified size.

		Returns:
			number
		"""
		return self._get_attribute('fixedSize')
	@FixedSize.setter
	def FixedSize(self, value):
		self._set_attribute('fixedSize', value)

	@property
	def IncrementFrom(self):
		"""Specifies the Start Value if the Frame Size is incremented.

		Returns:
			number
		"""
		return self._get_attribute('incrementFrom')
	@IncrementFrom.setter
	def IncrementFrom(self, value):
		self._set_attribute('incrementFrom', value)

	@property
	def IncrementStep(self):
		"""Specifies the Step Value if the Frame Size is Increment.

		Returns:
			number
		"""
		return self._get_attribute('incrementStep')
	@IncrementStep.setter
	def IncrementStep(self, value):
		self._set_attribute('incrementStep', value)

	@property
	def IncrementTo(self):
		"""Specifies the Final Value if the Frame Size is Increment.

		Returns:
			number
		"""
		return self._get_attribute('incrementTo')
	@IncrementTo.setter
	def IncrementTo(self, value):
		self._set_attribute('incrementTo', value)

	@property
	def PresetDistribution(self):
		"""If set, Frame Size is set to IMIX.

		Returns:
			str(cisco|imix|ipSecImix|ipV6Imix|rprQuar|rprTri|standardImix|tcpImix|tolly)
		"""
		return self._get_attribute('presetDistribution')
	@PresetDistribution.setter
	def PresetDistribution(self, value):
		self._set_attribute('presetDistribution', value)

	@property
	def QuadGaussian(self):
		"""This option allows to set frames to use a calculated distribution of Frame sizes. Quad Gaussian is the superposition of four Gaussian distributions. The user can specify the center (or mean), width of half maximum, and weight of each Gaussian distribution. The distribution is then normalized to a single distribution and generates the random numbers according to the normalized distribution.

		Returns:
			list(number)
		"""
		return self._get_attribute('quadGaussian')
	@QuadGaussian.setter
	def QuadGaussian(self, value):
		self._set_attribute('quadGaussian', value)

	@property
	def RandomMax(self):
		"""Sets frame size to maximum length in bytes. The maximum length is 1518 bytes.

		Returns:
			number
		"""
		return self._get_attribute('randomMax')
	@RandomMax.setter
	def RandomMax(self, value):
		self._set_attribute('randomMax', value)

	@property
	def RandomMin(self):
		"""Sets frame size to minimum length in bytes. The maximum length is 64 bytes.

		Returns:
			number
		"""
		return self._get_attribute('randomMin')
	@RandomMin.setter
	def RandomMin(self, value):
		self._set_attribute('randomMin', value)

	@property
	def Type(self):
		"""Sets the type of Frame Size.

		Returns:
			str(auto|fixed|increment|presetDistribution|quadGaussian|random|weightedPairs)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def WeightedPairs(self):
		"""Defines the values for the weight pairs.

		Returns:
			list(number)
		"""
		return self._get_attribute('weightedPairs')
	@WeightedPairs.setter
	def WeightedPairs(self, value):
		self._set_attribute('weightedPairs', value)

	@property
	def WeightedRangePairs(self):
		"""A list of structures that define the weighted range.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:number))
		"""
		return self._get_attribute('weightedRangePairs')
	@WeightedRangePairs.setter
	def WeightedRangePairs(self, value):
		self._set_attribute('weightedRangePairs', value)
