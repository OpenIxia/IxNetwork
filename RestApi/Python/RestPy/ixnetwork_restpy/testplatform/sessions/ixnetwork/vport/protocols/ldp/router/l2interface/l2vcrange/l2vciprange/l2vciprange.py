from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class L2VcIpRange(Base):
	"""The L2VcIpRange class encapsulates a required l2VcIpRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the L2VcIpRange property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'l2VcIpRange'

	def __init__(self, parent):
		super(L2VcIpRange, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables the Layer 2 IP address range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IncrementBy(self):
		"""The value to be added for creating each additional L2 VC IP route range.

		Returns:
			number
		"""
		return self._get_attribute('incrementBy')
	@IncrementBy.setter
	def IncrementBy(self, value):
		self._set_attribute('incrementBy', value)

	@property
	def Mask(self):
		"""The number of bits in the mask applied to the network address. The masked bits in the first network address form the address prefix.

		Returns:
			number
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def NumHosts(self):
		"""The number of emulated LDP hosts to be created on this port.

		Returns:
			number
		"""
		return self._get_attribute('numHosts')
	@NumHosts.setter
	def NumHosts(self, value):
		self._set_attribute('numHosts', value)

	@property
	def PeerAddress(self):
		"""The 32-bit IPv4 address of the LDP peer.

		Returns:
			str
		"""
		return self._get_attribute('peerAddress')

	@property
	def StartAddress(self):
		"""The IP address that starts the L2 VC IP range.

		Returns:
			str
		"""
		return self._get_attribute('startAddress')
	@StartAddress.setter
	def StartAddress(self, value):
		self._set_attribute('startAddress', value)
