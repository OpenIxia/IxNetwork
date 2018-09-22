from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowRangeAction(Base):
	"""The FlowRangeAction class encapsulates a user managed flowRangeAction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowRangeAction property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowRangeAction'

	def __init__(self, parent):
		super(FlowRangeAction, self).__init__(parent)

	@property
	def EthDestination(self):
		"""Specifies the destination address of the Ethernet port. This attribute value is applicable only when the typeOfAction selected is setEthernetDst.

		Returns:
			str
		"""
		return self._get_attribute('ethDestination')
	@EthDestination.setter
	def EthDestination(self, value):
		self._set_attribute('ethDestination', value)

	@property
	def EthSource(self):
		"""Specifies the source address of the Ethernet port. This attribute value is applicable only when the typeOfAction selected is setEthernetSrc.

		Returns:
			str
		"""
		return self._get_attribute('ethSource')
	@EthSource.setter
	def EthSource(self, value):
		self._set_attribute('ethSource', value)

	@property
	def IpDscp(self):
		"""Specifies the IP DSCP value. This attribute value is applicable only when the typeOfAction selected is setIpv4TosBits.

		Returns:
			number
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def Ipv4Destination(self):
		"""Specifies the destination IPv4 address for this flow range. This attribute value is applicable only when the typeOfAction selected is setIpv4DstAddress.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""Specifies the source IPv4 address for this flow range. This attribute value is applicable only when the typeOfAction selected is setIpv4SrcAddress.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def MaxByteLength(self):
		"""Indicates the maximum length in bytes.

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')
	@MaxByteLength.setter
	def MaxByteLength(self, value):
		self._set_attribute('maxByteLength', value)

	@property
	def OutputPort(self):
		"""Specifies the number of Output ports used. This attribute value is applicable only when the typeOfOutPort selected is ofppManual.

		Returns:
			number
		"""
		return self._get_attribute('outputPort')
	@OutputPort.setter
	def OutputPort(self, value):
		self._set_attribute('outputPort', value)

	@property
	def QueueId(self):
		"""Indicates the Queue ID for this Flow Range. This attribute value is applicable only when the typeOfAction selected is enqueue.

		Returns:
			number
		"""
		return self._get_attribute('queueId')
	@QueueId.setter
	def QueueId(self, value):
		self._set_attribute('queueId', value)

	@property
	def TransportDestination(self):
		"""Specifies the transport destination address. This attribute value is applicable only when the typeOfAction selected is setTransportDestination.

		Returns:
			number
		"""
		return self._get_attribute('transportDestination')
	@TransportDestination.setter
	def TransportDestination(self, value):
		self._set_attribute('transportDestination', value)

	@property
	def TransportSource(self):
		"""Specifies the Transport source address. This attribute value is applicable only when the typeOfAction selected is setTransportSource.

		Returns:
			number
		"""
		return self._get_attribute('transportSource')
	@TransportSource.setter
	def TransportSource(self, value):
		self._set_attribute('transportSource', value)

	@property
	def TypeOfAction(self):
		"""Indicates the action type associated with this Flow Range.

		Returns:
			str(none|output|enqueue|setVlanId|setVlanPriority|stripVlanHeader|setEthernetSrc|setEthernetDst|setIpv4TosBits|setIpv4SrcAddress|setIpv4DstAddress|setTransportSource|setTransportDestination|setVendorAction)
		"""
		return self._get_attribute('typeOfAction')
	@TypeOfAction.setter
	def TypeOfAction(self, value):
		self._set_attribute('typeOfAction', value)

	@property
	def TypeOfOutPort(self):
		"""Specifies the Output Port Type for this Flow Range. This attribute value is applicable only when the typeOfAction selected is output

		Returns:
			str(ofppManual|ofppAll|ofppController|ofppInPort|ofppLocal|ofppNormal|ofppFlood)
		"""
		return self._get_attribute('typeOfOutPort')
	@TypeOfOutPort.setter
	def TypeOfOutPort(self, value):
		self._set_attribute('typeOfOutPort', value)

	@property
	def VendorData(self):
		"""Specifies the data of the Vendor. This attribute value is applicable only when the typeOfAction selected is setVendorAction.

		Returns:
			str
		"""
		return self._get_attribute('vendorData')
	@VendorData.setter
	def VendorData(self, value):
		self._set_attribute('vendorData', value)

	@property
	def VendorDataLength(self):
		"""Specifies the data length of the Vendor. This attribute value is applicable only when the typeOfAction selected is setVendorAction.

		Returns:
			number
		"""
		return self._get_attribute('vendorDataLength')
	@VendorDataLength.setter
	def VendorDataLength(self, value):
		self._set_attribute('vendorDataLength', value)

	@property
	def VendorId(self):
		"""Specifies the unique Vendor identifier. This attribute value is applicable only when the typeOfAction selected is setVendorAction.

		Returns:
			number
		"""
		return self._get_attribute('vendorId')
	@VendorId.setter
	def VendorId(self, value):
		self._set_attribute('vendorId', value)

	@property
	def VlanId(self):
		"""Specifies the unique VLAN Identifier for this VLAN. This attribute value is applicable only when the typeOfAction selected is setVlanId.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Specifies the User Priority for this VLAN. This attribute value is applicable only when the typeOfAction selected is setVlanPriority.

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, EthDestination=None, EthSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, MaxByteLength=None, OutputPort=None, QueueId=None, TransportDestination=None, TransportSource=None, TypeOfAction=None, TypeOfOutPort=None, VendorData=None, VendorDataLength=None, VendorId=None, VlanId=None, VlanPriority=None):
		"""Adds a new flowRangeAction node on the server and retrieves it in this instance.

		Args:
			EthDestination (str): Specifies the destination address of the Ethernet port. This attribute value is applicable only when the typeOfAction selected is setEthernetDst.
			EthSource (str): Specifies the source address of the Ethernet port. This attribute value is applicable only when the typeOfAction selected is setEthernetSrc.
			IpDscp (number): Specifies the IP DSCP value. This attribute value is applicable only when the typeOfAction selected is setIpv4TosBits.
			Ipv4Destination (str): Specifies the destination IPv4 address for this flow range. This attribute value is applicable only when the typeOfAction selected is setIpv4DstAddress.
			Ipv4Source (str): Specifies the source IPv4 address for this flow range. This attribute value is applicable only when the typeOfAction selected is setIpv4SrcAddress.
			MaxByteLength (number): Indicates the maximum length in bytes.
			OutputPort (number): Specifies the number of Output ports used. This attribute value is applicable only when the typeOfOutPort selected is ofppManual.
			QueueId (number): Indicates the Queue ID for this Flow Range. This attribute value is applicable only when the typeOfAction selected is enqueue.
			TransportDestination (number): Specifies the transport destination address. This attribute value is applicable only when the typeOfAction selected is setTransportDestination.
			TransportSource (number): Specifies the Transport source address. This attribute value is applicable only when the typeOfAction selected is setTransportSource.
			TypeOfAction (str(none|output|enqueue|setVlanId|setVlanPriority|stripVlanHeader|setEthernetSrc|setEthernetDst|setIpv4TosBits|setIpv4SrcAddress|setIpv4DstAddress|setTransportSource|setTransportDestination|setVendorAction)): Indicates the action type associated with this Flow Range.
			TypeOfOutPort (str(ofppManual|ofppAll|ofppController|ofppInPort|ofppLocal|ofppNormal|ofppFlood)): Specifies the Output Port Type for this Flow Range. This attribute value is applicable only when the typeOfAction selected is output
			VendorData (str): Specifies the data of the Vendor. This attribute value is applicable only when the typeOfAction selected is setVendorAction.
			VendorDataLength (number): Specifies the data length of the Vendor. This attribute value is applicable only when the typeOfAction selected is setVendorAction.
			VendorId (number): Specifies the unique Vendor identifier. This attribute value is applicable only when the typeOfAction selected is setVendorAction.
			VlanId (number): Specifies the unique VLAN Identifier for this VLAN. This attribute value is applicable only when the typeOfAction selected is setVlanId.
			VlanPriority (number): Specifies the User Priority for this VLAN. This attribute value is applicable only when the typeOfAction selected is setVlanPriority.

		Returns:
			self: This instance with all currently retrieved flowRangeAction data using find and the newly added flowRangeAction data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowRangeAction data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EthDestination=None, EthSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, MaxByteLength=None, OutputPort=None, QueueId=None, TransportDestination=None, TransportSource=None, TypeOfAction=None, TypeOfOutPort=None, VendorData=None, VendorDataLength=None, VendorId=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves flowRangeAction data from the server.

		All named parameters support regex and can be used to selectively retrieve flowRangeAction data from the server.
		By default the find method takes no parameters and will retrieve all flowRangeAction data from the server.

		Args:
			EthDestination (str): Specifies the destination address of the Ethernet port. This attribute value is applicable only when the typeOfAction selected is setEthernetDst.
			EthSource (str): Specifies the source address of the Ethernet port. This attribute value is applicable only when the typeOfAction selected is setEthernetSrc.
			IpDscp (number): Specifies the IP DSCP value. This attribute value is applicable only when the typeOfAction selected is setIpv4TosBits.
			Ipv4Destination (str): Specifies the destination IPv4 address for this flow range. This attribute value is applicable only when the typeOfAction selected is setIpv4DstAddress.
			Ipv4Source (str): Specifies the source IPv4 address for this flow range. This attribute value is applicable only when the typeOfAction selected is setIpv4SrcAddress.
			MaxByteLength (number): Indicates the maximum length in bytes.
			OutputPort (number): Specifies the number of Output ports used. This attribute value is applicable only when the typeOfOutPort selected is ofppManual.
			QueueId (number): Indicates the Queue ID for this Flow Range. This attribute value is applicable only when the typeOfAction selected is enqueue.
			TransportDestination (number): Specifies the transport destination address. This attribute value is applicable only when the typeOfAction selected is setTransportDestination.
			TransportSource (number): Specifies the Transport source address. This attribute value is applicable only when the typeOfAction selected is setTransportSource.
			TypeOfAction (str(none|output|enqueue|setVlanId|setVlanPriority|stripVlanHeader|setEthernetSrc|setEthernetDst|setIpv4TosBits|setIpv4SrcAddress|setIpv4DstAddress|setTransportSource|setTransportDestination|setVendorAction)): Indicates the action type associated with this Flow Range.
			TypeOfOutPort (str(ofppManual|ofppAll|ofppController|ofppInPort|ofppLocal|ofppNormal|ofppFlood)): Specifies the Output Port Type for this Flow Range. This attribute value is applicable only when the typeOfAction selected is output
			VendorData (str): Specifies the data of the Vendor. This attribute value is applicable only when the typeOfAction selected is setVendorAction.
			VendorDataLength (number): Specifies the data length of the Vendor. This attribute value is applicable only when the typeOfAction selected is setVendorAction.
			VendorId (number): Specifies the unique Vendor identifier. This attribute value is applicable only when the typeOfAction selected is setVendorAction.
			VlanId (number): Specifies the unique VLAN Identifier for this VLAN. This attribute value is applicable only when the typeOfAction selected is setVlanId.
			VlanPriority (number): Specifies the User Priority for this VLAN. This attribute value is applicable only when the typeOfAction selected is setVlanPriority.

		Returns:
			self: This instance with matching flowRangeAction data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowRangeAction data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowRangeAction data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
