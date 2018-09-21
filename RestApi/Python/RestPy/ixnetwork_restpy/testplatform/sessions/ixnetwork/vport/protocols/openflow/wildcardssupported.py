from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class WildcardsSupported(Base):
	"""The WildcardsSupported class encapsulates a required wildcardsSupported node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the WildcardsSupported property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'wildcardsSupported'

	def __init__(self, parent):
		super(WildcardsSupported, self).__init__(parent)

	@property
	def EthernetDestinationAddress(self):
		"""Indicates that the Ethernet destination address is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetDestinationAddress')
	@EthernetDestinationAddress.setter
	def EthernetDestinationAddress(self, value):
		self._set_attribute('ethernetDestinationAddress', value)

	@property
	def EthernetFrameType(self):
		"""Indicates that the Ethernet frame type is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetFrameType')
	@EthernetFrameType.setter
	def EthernetFrameType(self, value):
		self._set_attribute('ethernetFrameType', value)

	@property
	def EthernetSourceAddress(self):
		"""Indicates that the Ethernet source address is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetSourceAddress')
	@EthernetSourceAddress.setter
	def EthernetSourceAddress(self, value):
		self._set_attribute('ethernetSourceAddress', value)

	@property
	def IpDestinationAddress(self):
		"""Indicates that the IP destination address is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipDestinationAddress')
	@IpDestinationAddress.setter
	def IpDestinationAddress(self, value):
		self._set_attribute('ipDestinationAddress', value)

	@property
	def IpProtocol(self):
		"""Indicates that the IP protocol is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def IpSourceAddress(self):
		"""Indicates that the IP source address is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipSourceAddress')
	@IpSourceAddress.setter
	def IpSourceAddress(self, value):
		self._set_attribute('ipSourceAddress', value)

	@property
	def IpTos(self):
		"""Indicates that the IP ToS (DSCP field, 6 bits) is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipTos')
	@IpTos.setter
	def IpTos(self, value):
		self._set_attribute('ipTos', value)

	@property
	def SwitchInputPort(self):
		"""Indicates that the Switch input port is supported.

		Returns:
			bool
		"""
		return self._get_attribute('switchInputPort')
	@SwitchInputPort.setter
	def SwitchInputPort(self, value):
		self._set_attribute('switchInputPort', value)

	@property
	def TcpUdpDestinationPort(self):
		"""Indicates that the TCP/UDP destination port is supported.

		Returns:
			bool
		"""
		return self._get_attribute('tcpUdpDestinationPort')
	@TcpUdpDestinationPort.setter
	def TcpUdpDestinationPort(self, value):
		self._set_attribute('tcpUdpDestinationPort', value)

	@property
	def TcpUdpSourcePort(self):
		"""Indicates that the TCP/UDP source port is supported.

		Returns:
			bool
		"""
		return self._get_attribute('tcpUdpSourcePort')
	@TcpUdpSourcePort.setter
	def TcpUdpSourcePort(self, value):
		self._set_attribute('tcpUdpSourcePort', value)

	@property
	def VlanId(self):
		"""Indicates that the VLAN id is supported.

		Returns:
			bool
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Indicates that the VLAN priority is supported.

		Returns:
			bool
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
