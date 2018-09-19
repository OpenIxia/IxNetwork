from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Latency(Base):
	"""The Latency class encapsulates a required latency node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Latency property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'latency'

	def __init__(self, parent):
		super(Latency, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, latency statistics is enabled and if false, latency statistics is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Mode(self):
		"""Latency statistics is generated according to the mode set if latency is enabled.

		Returns:
			str(cutThrough|forwardingDelay|mef|storeForward)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)
