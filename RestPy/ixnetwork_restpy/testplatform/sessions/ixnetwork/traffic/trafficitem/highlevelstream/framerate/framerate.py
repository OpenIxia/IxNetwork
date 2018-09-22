from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FrameRate(Base):
	"""The FrameRate class encapsulates a required frameRate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FrameRate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'frameRate'

	def __init__(self, parent):
		super(FrameRate, self).__init__(parent)

	@property
	def BitRateUnitsType(self):
		"""The rate units for transmitting packet.

		Returns:
			str(bitsPerSec|bytesPerSec|kbitsPerSec|kbytesPerSec|mbitsPerSec|mbytesPerSec)
		"""
		return self._get_attribute('bitRateUnitsType')
	@BitRateUnitsType.setter
	def BitRateUnitsType(self, value):
		self._set_attribute('bitRateUnitsType', value)

	@property
	def EnforceMinimumInterPacketGap(self):
		"""Sets the minimum inter-packet gap allowed for Ethernet ports only. The default is 12 bytes.

		Returns:
			number
		"""
		return self._get_attribute('enforceMinimumInterPacketGap')
	@EnforceMinimumInterPacketGap.setter
	def EnforceMinimumInterPacketGap(self, value):
		self._set_attribute('enforceMinimumInterPacketGap', value)

	@property
	def InterPacketGapUnitsType(self):
		"""The inter-packet gap expressed in units.

		Returns:
			str(bytes|nanoseconds)
		"""
		return self._get_attribute('interPacketGapUnitsType')
	@InterPacketGapUnitsType.setter
	def InterPacketGapUnitsType(self, value):
		self._set_attribute('interPacketGapUnitsType', value)

	@property
	def Rate(self):
		"""The rate at which packet is transmitted.

		Returns:
			number
		"""
		return self._get_attribute('rate')
	@Rate.setter
	def Rate(self, value):
		self._set_attribute('rate', value)

	@property
	def Type(self):
		"""Sets the frame rate types.

		Returns:
			str(bitsPerSecond|framesPerSecond|interPacketGap|percentLineRate)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)
