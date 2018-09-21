from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RxRateLimit(Base):
	"""The RxRateLimit class encapsulates a required rxRateLimit node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RxRateLimit property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rxRateLimit'

	def __init__(self, parent):
		super(RxRateLimit, self).__init__(parent)

	@property
	def BufferSizeEnabled(self):
		"""Allows user to specify a custom buffer size. Default false

		Returns:
			bool
		"""
		return self._get_attribute('bufferSizeEnabled')
	@BufferSizeEnabled.setter
	def BufferSizeEnabled(self, value):
		self._set_attribute('bufferSizeEnabled', value)

	@property
	def BufferSizeUnits(self):
		"""Units (Kilobytes, Megabytes). Default: Kilobytes

		Returns:
			str(kilobytes|kKilobytes|kMegabytes|megabytes)
		"""
		return self._get_attribute('bufferSizeUnits')
	@BufferSizeUnits.setter
	def BufferSizeUnits(self, value):
		self._set_attribute('bufferSizeUnits', value)

	@property
	def BufferSizeValue(self):
		"""Burst tolerance buffer size. Default value is 32 KB

		Returns:
			number
		"""
		return self._get_attribute('bufferSizeValue')
	@BufferSizeValue.setter
	def BufferSizeValue(self, value):
		self._set_attribute('bufferSizeValue', value)

	@property
	def Enabled(self):
		"""Enable or disable the receive rate limit impairment.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Units(self):
		"""Specify the units for the receive rate limit value.

		Returns:
			str(kilobitsPerSecond|kKilobitsPerSecond|kMegabitsPerSecond|megabitsPerSecond)
		"""
		return self._get_attribute('units')
	@Units.setter
	def Units(self, value):
		self._set_attribute('units', value)

	@property
	def Value(self):
		"""Specify the value of the receive rate limit.

		Returns:
			number
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
