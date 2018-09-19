from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TxLane(Base):
	"""The TxLane class encapsulates a required txLane node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TxLane property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'txLane'

	def __init__(self, parent):
		super(TxLane, self).__init__(parent)

	@property
	def IsSkewSynchronized(self):
		"""If true, skew value will apply for all the lanes.

		Returns:
			bool
		"""
		return self._get_attribute('isSkewSynchronized')
	@IsSkewSynchronized.setter
	def IsSkewSynchronized(self, value):
		self._set_attribute('isSkewSynchronized', value)

	@property
	def LaneMappingType(self):
		"""Lane Mapping

		Returns:
			str(custom|decrement|default|increment|random)
		"""
		return self._get_attribute('laneMappingType')
	@LaneMappingType.setter
	def LaneMappingType(self, value):
		self._set_attribute('laneMappingType', value)

	@property
	def MaxSkewVal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxSkewVal')

	@property
	def MinSkewVal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minSkewVal')

	@property
	def NoOfLanes(self):
		"""Number of lanes

		Returns:
			number
		"""
		return self._get_attribute('noOfLanes')

	@property
	def PcsLane(self):
		"""Pcs Lane

		Returns:
			list(number)
		"""
		return self._get_attribute('pcsLane')
	@PcsLane.setter
	def PcsLane(self, value):
		self._set_attribute('pcsLane', value)

	@property
	def PhysicalLanes(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('physicalLanes')

	@property
	def Resolution(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('resolution')

	@property
	def SkewValues(self):
		"""Skew Values

		Returns:
			list(number)
		"""
		return self._get_attribute('skewValues')
	@SkewValues.setter
	def SkewValues(self, value):
		self._set_attribute('skewValues', value)

	@property
	def SynchronizedSkewVal(self):
		"""Synchronized Skew Values

		Returns:
			number
		"""
		return self._get_attribute('synchronizedSkewVal')
	@SynchronizedSkewVal.setter
	def SynchronizedSkewVal(self, value):
		self._set_attribute('synchronizedSkewVal', value)
