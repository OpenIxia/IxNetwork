from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchGroupActionLearnedInfo(Base):
	"""The SwitchGroupActionLearnedInfo class encapsulates a system managed switchGroupActionLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchGroupActionLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchGroupActionLearnedInfo'

	def __init__(self, parent):
		super(SwitchGroupActionLearnedInfo, self).__init__(parent)

	@property
	def ActionType(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('actionType')

	@property
	def ArpDestinationHwAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('arpDestinationHwAddress')

	@property
	def ArpDstIpv4Address(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4Address')

	@property
	def ArpOpcode(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('arpOpcode')

	@property
	def ArpSourceHwAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('arpSourceHwAddress')

	@property
	def ArpSrcIpv4Address(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4Address')

	@property
	def EthernetDestination(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetSource(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def EthernetType(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def Experimenter(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenter')

	@property
	def ExperimenterData(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDatalength(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenterDatalength')

	@property
	def GroupId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def Icmpv4Code(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Code')

	@property
	def Icmpv4Type(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Type')

	@property
	def Icmpv6Code(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Code')

	@property
	def Icmpv6Type(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Type')

	@property
	def IpDscp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def IpEcn(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ipEcn')

	@property
	def IpProto(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ipProto')

	@property
	def Ipv4Destination(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')

	@property
	def Ipv6Destination(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv6Destination')

	@property
	def Ipv6ExtHeader(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6FlowLabel(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6NdSll(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')

	@property
	def Ipv6NdTarget(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTarget')

	@property
	def Ipv6NdTll(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTll')

	@property
	def Ipv6Source(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')

	@property
	def MaxByteLength(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')

	@property
	def MplsBos(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('mplsBos')

	@property
	def MplsLabel(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsTc(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('mplsTc')

	@property
	def MplsTtl(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('mplsTtl')

	@property
	def NetworkTtl(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('networkTtl')

	@property
	def OutputPort(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def OutputPortType(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('outputPortType')

	@property
	def PbbIsid(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('pbbIsid')

	@property
	def QueueId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def SctpDestination(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sctpDestination')

	@property
	def SctpSource(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sctpSource')

	@property
	def TcpDestination(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('tcpDestination')

	@property
	def TcpSource(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('tcpSource')

	@property
	def TunnelId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')

	@property
	def UdpDestination(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('udpDestination')

	@property
	def UdpSource(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('udpSource')

	@property
	def VlanId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ActionType=None, ArpDestinationHwAddress=None, ArpDstIpv4Address=None, ArpOpcode=None, ArpSourceHwAddress=None, ArpSrcIpv4Address=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, Experimenter=None, ExperimenterData=None, ExperimenterDatalength=None, GroupId=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IpDscp=None, IpEcn=None, IpProto=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6ExtHeader=None, Ipv6FlowLabel=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6NdTll=None, Ipv6Source=None, MaxByteLength=None, MplsBos=None, MplsLabel=None, MplsTc=None, MplsTtl=None, NetworkTtl=None, OutputPort=None, OutputPortType=None, PbbIsid=None, QueueId=None, SctpDestination=None, SctpSource=None, TcpDestination=None, TcpSource=None, TunnelId=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves switchGroupActionLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchGroupActionLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchGroupActionLearnedInfo data from the server.

		Args:
			ActionType (str): NOT DEFINED
			ArpDestinationHwAddress (str): NOT DEFINED
			ArpDstIpv4Address (str): NOT DEFINED
			ArpOpcode (number): NOT DEFINED
			ArpSourceHwAddress (str): NOT DEFINED
			ArpSrcIpv4Address (str): NOT DEFINED
			EthernetDestination (str): NOT DEFINED
			EthernetSource (str): NOT DEFINED
			EthernetType (str): NOT DEFINED
			Experimenter (number): NOT DEFINED
			ExperimenterData (str): NOT DEFINED
			ExperimenterDatalength (number): NOT DEFINED
			GroupId (number): NOT DEFINED
			Icmpv4Code (number): NOT DEFINED
			Icmpv4Type (number): NOT DEFINED
			Icmpv6Code (number): NOT DEFINED
			Icmpv6Type (number): NOT DEFINED
			IpDscp (str): NOT DEFINED
			IpEcn (number): NOT DEFINED
			IpProto (number): NOT DEFINED
			Ipv4Destination (str): NOT DEFINED
			Ipv4Source (str): NOT DEFINED
			Ipv6Destination (str): NOT DEFINED
			Ipv6ExtHeader (number): NOT DEFINED
			Ipv6FlowLabel (number): NOT DEFINED
			Ipv6NdSll (str): NOT DEFINED
			Ipv6NdTarget (str): NOT DEFINED
			Ipv6NdTll (str): NOT DEFINED
			Ipv6Source (str): NOT DEFINED
			MaxByteLength (number): NOT DEFINED
			MplsBos (number): NOT DEFINED
			MplsLabel (number): NOT DEFINED
			MplsTc (number): NOT DEFINED
			MplsTtl (number): NOT DEFINED
			NetworkTtl (number): NOT DEFINED
			OutputPort (number): NOT DEFINED
			OutputPortType (str): NOT DEFINED
			PbbIsid (number): NOT DEFINED
			QueueId (number): NOT DEFINED
			SctpDestination (number): NOT DEFINED
			SctpSource (number): NOT DEFINED
			TcpDestination (number): NOT DEFINED
			TcpSource (number): NOT DEFINED
			TunnelId (str): NOT DEFINED
			UdpDestination (number): NOT DEFINED
			UdpSource (number): NOT DEFINED
			VlanId (number): NOT DEFINED
			VlanPriority (number): NOT DEFINED

		Returns:
			self: This instance with matching switchGroupActionLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchGroupActionLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchGroupActionLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
