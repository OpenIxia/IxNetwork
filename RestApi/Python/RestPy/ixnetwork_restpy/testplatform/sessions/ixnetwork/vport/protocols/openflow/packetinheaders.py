from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PacketInHeaders(Base):
	"""The PacketInHeaders class encapsulates a required packetInHeaders node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PacketInHeaders property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'packetInHeaders'

	def __init__(self, parent):
		super(PacketInHeaders, self).__init__(parent)

	@property
	def EthernetDestinationAddress(self):
		"""Indicates the Ethernet destination address for the packet.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestinationAddress')

	@property
	def EthernetSourceAddress(self):
		"""Indicates the ethernet address of the source from which this packet arrived.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSourceAddress')

	@property
	def EthernetType(self):
		"""Indicates the ethernet frame type.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def Ipv4DestinationAddress(self):
		"""Indicates the IPv4 destination address for this packet.

		Returns:
			str
		"""
		return self._get_attribute('ipv4DestinationAddress')

	@property
	def Ipv4Protocol(self):
		"""Defines the protocol used in the data portion of the IP datagram.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Protocol')

	@property
	def Ipv4SourceAddress(self):
		"""Indicates the IPv4 address of the source from which this packet arrived.

		Returns:
			str
		"""
		return self._get_attribute('ipv4SourceAddress')

	@property
	def Ipv6DestinationAddress(self):
		"""Indicates the IPv6 destination address for this packet.

		Returns:
			str
		"""
		return self._get_attribute('ipv6DestinationAddress')

	@property
	def Ipv6FlowLabel(self):
		"""Originally created for giving real-time applications special service.The flow label when set to a non-zero value now serves as a hint to routers and switches with multiple outbound paths that these packets should stay on the same path so that they will not be re-ordered.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6SourceAddress(self):
		"""Indicates the IPv6 address of the source from which this packet arrived.

		Returns:
			str
		"""
		return self._get_attribute('ipv6SourceAddress')

	@property
	def TcpDestinationPort(self):
		"""Identifies the TCP port number of the destination application program.

		Returns:
			str
		"""
		return self._get_attribute('tcpDestinationPort')

	@property
	def TcpSourcePort(self):
		"""Identifies the TCP port number of the source application program.

		Returns:
			str
		"""
		return self._get_attribute('tcpSourcePort')

	@property
	def UdpDestinationPort(self):
		"""Identifies the UDP port number of the destination application program.

		Returns:
			str
		"""
		return self._get_attribute('udpDestinationPort')

	@property
	def UdpSourcePort(self):
		"""Identifies the UDP port number of the source application program.

		Returns:
			str
		"""
		return self._get_attribute('udpSourcePort')

	@property
	def UniquePacketCount(self):
		"""Indicates the packet-in count in this Range.

		Returns:
			str
		"""
		return self._get_attribute('uniquePacketCount')

	@property
	def VlanId(self):
		"""Indicates the field specifying the VLAN to which the frame belongs.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""Indicates the frame priority level.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
