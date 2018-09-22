from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterfaceLearnedInfo(Base):
	"""The InterfaceLearnedInfo class encapsulates a required interfaceLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InterfaceLearnedInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interfaceLearnedInfo'

	def __init__(self, parent):
		super(InterfaceLearnedInfo, self).__init__(parent)

	@property
	def GatewayIp(self):
		"""The IP address of the Gateway to the network, typically an interface on the DUT.

		Returns:
			str
		"""
		return self._get_attribute('gatewayIp')

	@property
	def IpType(self):
		"""The IP version used with this option set: IPv4 or IPv6.

		Returns:
			str(kIpv4|kIpv6)
		"""
		return self._get_attribute('ipType')

	@property
	def OwnIp(self):
		"""The own ip type.

		Returns:
			str
		"""
		return self._get_attribute('ownIp')

	@property
	def PrefixLength(self):
		"""A learned/allocated IPv4 address prefix length (mask) for this interface.

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')
