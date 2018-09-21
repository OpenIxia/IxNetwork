from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrillPingOam(Base):
	"""The TrillPingOam class encapsulates a required trillPingOam node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrillPingOam property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'trillPingOam'

	def __init__(self, parent):
		super(TrillPingOam, self).__init__(parent)

	@property
	def AlertFlag(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('alertFlag')
	@AlertFlag.setter
	def AlertFlag(self, value):
		self._set_attribute('alertFlag', value)

	@property
	def DestinationNickname(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('destinationNickname')
	@DestinationNickname.setter
	def DestinationNickname(self, value):
		self._set_attribute('destinationNickname', value)

	@property
	def EtherType(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('etherType')
	@EtherType.setter
	def EtherType(self, value):
		self._set_attribute('etherType', value)

	@property
	def HopCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('hopCount')
	@HopCount.setter
	def HopCount(self, value):
		self._set_attribute('hopCount', value)

	@property
	def NativeFlag(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('nativeFlag')
	@NativeFlag.setter
	def NativeFlag(self, value):
		self._set_attribute('nativeFlag', value)

	@property
	def NoOfPingRequests(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('noOfPingRequests')
	@NoOfPingRequests.setter
	def NoOfPingRequests(self, value):
		self._set_attribute('noOfPingRequests', value)

	@property
	def SilentFlag(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('silentFlag')
	@SilentFlag.setter
	def SilentFlag(self, value):
		self._set_attribute('silentFlag', value)

	@property
	def SourceNickname(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sourceNickname')
	@SourceNickname.setter
	def SourceNickname(self, value):
		self._set_attribute('sourceNickname', value)

	@property
	def TimeOut(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('timeOut')
	@TimeOut.setter
	def TimeOut(self, value):
		self._set_attribute('timeOut', value)
