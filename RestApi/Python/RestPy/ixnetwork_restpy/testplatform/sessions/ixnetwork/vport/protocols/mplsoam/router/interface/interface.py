from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interface(Base):
	"""The Interface class encapsulates a user managed interface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def BfdCvType(self):
		"""This signifies the BFD Connectivity Verification type. Possible values include:

		Returns:
			str(bfdCvTypeIpUdp|bfdCvTypePwAch)
		"""
		return self._get_attribute('bfdCvType')
	@BfdCvType.setter
	def BfdCvType(self, value):
		self._set_attribute('bfdCvType', value)

	@property
	def BfdDiscriminatorEnd(self):
		"""This signifies the last BFD Discriminator value. This value should be greater than the BFD.

		Returns:
			number
		"""
		return self._get_attribute('bfdDiscriminatorEnd')
	@BfdDiscriminatorEnd.setter
	def BfdDiscriminatorEnd(self, value):
		self._set_attribute('bfdDiscriminatorEnd', value)

	@property
	def BfdDiscriminatorStart(self):
		"""This signifies the first BFD Discriminator value. The default value is 5000.

		Returns:
			number
		"""
		return self._get_attribute('bfdDiscriminatorStart')
	@BfdDiscriminatorStart.setter
	def BfdDiscriminatorStart(self, value):
		self._set_attribute('bfdDiscriminatorStart', value)

	@property
	def ControlChannel(self):
		"""This signifies the communication control channel. Possible values include

		Returns:
			str(controlChannelRouterAlert|controlChannelPwAch)
		"""
		return self._get_attribute('controlChannel')
	@ControlChannel.setter
	def ControlChannel(self, value):
		self._set_attribute('controlChannel', value)

	@property
	def DestinationAddressIpv4(self):
		"""This signifies the destination IPv4 address.

		Returns:
			str
		"""
		return self._get_attribute('destinationAddressIpv4')
	@DestinationAddressIpv4.setter
	def DestinationAddressIpv4(self, value):
		self._set_attribute('destinationAddressIpv4', value)

	@property
	def DownStreamAddressType(self):
		"""This signifies the address type of the downstream traffic. Possible values include:

		Returns:
			str(ipv4Numbered|ipv4UnNumbered|ipv6Numbered|ipv6UnNumbered)
		"""
		return self._get_attribute('downStreamAddressType')
	@DownStreamAddressType.setter
	def DownStreamAddressType(self, value):
		self._set_attribute('downStreamAddressType', value)

	@property
	def DownStreamInterfaceAddress(self):
		"""This signifies the interface address of the downstream traffic.

		Returns:
			number
		"""
		return self._get_attribute('downStreamInterfaceAddress')
	@DownStreamInterfaceAddress.setter
	def DownStreamInterfaceAddress(self, value):
		self._set_attribute('downStreamInterfaceAddress', value)

	@property
	def DownStreamIpAddress(self):
		"""This signifies the IPv4/IPv6 address of the downstream traffic.

		Returns:
			str
		"""
		return self._get_attribute('downStreamIpAddress')
	@DownStreamIpAddress.setter
	def DownStreamIpAddress(self, value):
		self._set_attribute('downStreamIpAddress', value)

	@property
	def EchoRequestInterval(self):
		"""This signifies the minimum interval, in milliseconds, between received Echo packets that this interface is capable of supporting.

		Returns:
			number
		"""
		return self._get_attribute('echoRequestInterval')
	@EchoRequestInterval.setter
	def EchoRequestInterval(self, value):
		self._set_attribute('echoRequestInterval', value)

	@property
	def EchoResponseTimeout(self):
		"""This signifies the minimum tiomeout interval, in milliseconds, between received Echo packets that this interface is capable of supporting.

		Returns:
			number
		"""
		return self._get_attribute('echoResponseTimeout')
	@EchoResponseTimeout.setter
	def EchoResponseTimeout(self, value):
		self._set_attribute('echoResponseTimeout', value)

	@property
	def EnableDownStreamMappingTlv(self):
		"""This signifies the enablement of downstream mapping TLV.

		Returns:
			bool
		"""
		return self._get_attribute('enableDownStreamMappingTlv')
	@EnableDownStreamMappingTlv.setter
	def EnableDownStreamMappingTlv(self, value):
		self._set_attribute('enableDownStreamMappingTlv', value)

	@property
	def EnableDsIflag(self):
		"""This signifies the activation of the DS I Flag.

		Returns:
			bool
		"""
		return self._get_attribute('enableDsIflag')
	@EnableDsIflag.setter
	def EnableDsIflag(self, value):
		self._set_attribute('enableDsIflag', value)

	@property
	def EnableDsNflag(self):
		"""This signifies the activation of the DS N Flag.

		Returns:
			bool
		"""
		return self._get_attribute('enableDsNflag')
	@EnableDsNflag.setter
	def EnableDsNflag(self, value):
		self._set_attribute('enableDsNflag', value)

	@property
	def EnableFecValidation(self):
		"""This signifies the selection of the check box to enable FEC validation.

		Returns:
			bool
		"""
		return self._get_attribute('enableFecValidation')
	@EnableFecValidation.setter
	def EnableFecValidation(self, value):
		self._set_attribute('enableFecValidation', value)

	@property
	def EnablePeriodicPing(self):
		"""If true, the router is pinged at regular intervals.

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicPing')
	@EnablePeriodicPing.setter
	def EnablePeriodicPing(self, value):
		self._set_attribute('enablePeriodicPing', value)

	@property
	def Enabled(self):
		"""If true, it enables or disables the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FlapTxIntervals(self):
		"""This signifies the number of seconds between route flaps for BFD. A value of zero means no flapping.

		Returns:
			number
		"""
		return self._get_attribute('flapTxIntervals')
	@FlapTxIntervals.setter
	def FlapTxIntervals(self, value):
		self._set_attribute('flapTxIntervals', value)

	@property
	def IncludePadTlv(self):
		"""If true, includes Pad TLV in triggered ping.

		Returns:
			bool
		"""
		return self._get_attribute('includePadTlv')
	@IncludePadTlv.setter
	def IncludePadTlv(self, value):
		self._set_attribute('includePadTlv', value)

	@property
	def IncludeVendorEnterpriseNumberTlv(self):
		"""If true, includes the TLV number of the vendor, in triggered ping.

		Returns:
			bool
		"""
		return self._get_attribute('includeVendorEnterpriseNumberTlv')
	@IncludeVendorEnterpriseNumberTlv.setter
	def IncludeVendorEnterpriseNumberTlv(self, value):
		self._set_attribute('includeVendorEnterpriseNumberTlv', value)

	@property
	def Interfaces(self):
		"""This signifies the interfaces that are associated with the selected interface type.Object references are:

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def MinRxInterval(self):
		"""This signifies the minimum interval, in milliseconds, between received BFD Control packets that this interface is capable of supporting.

		Returns:
			number
		"""
		return self._get_attribute('minRxInterval')
	@MinRxInterval.setter
	def MinRxInterval(self, value):
		self._set_attribute('minRxInterval', value)

	@property
	def Multiplier(self):
		"""This signifies the negotiated transmit interval, multiplied by this value, provides the detection time for the interface.

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def PadTlvFirstOctet(self):
		"""This signifies the selection of the first octate of the Pad TLV. Possible values include:

		Returns:
			str(dropPadTlvFromReply|copyPadTlvToReply)
		"""
		return self._get_attribute('padTlvFirstOctet')
	@PadTlvFirstOctet.setter
	def PadTlvFirstOctet(self, value):
		self._set_attribute('padTlvFirstOctet', value)

	@property
	def PadTlvLength(self):
		"""This signifies the specification of the length of the Pad TLV.

		Returns:
			number
		"""
		return self._get_attribute('padTlvLength')
	@PadTlvLength.setter
	def PadTlvLength(self, value):
		self._set_attribute('padTlvLength', value)

	@property
	def ReplyMode(self):
		"""This signifies the selecion of the mode of reply.Possible values include DoNotReply, ReplyViaApplicationLevelControlChannel, ReplyViaIpv4Ipv6UdpPacket and ReplyViaIpv4Ipv6UdpPacketWithRouterAlert.

		Returns:
			str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)
		"""
		return self._get_attribute('replyMode')
	@ReplyMode.setter
	def ReplyMode(self, value):
		self._set_attribute('replyMode', value)

	@property
	def TxInterval(self):
		"""This signifies the minimum interval, in milliseconds, that the interface would like to use when transmitting BFD Control packets.

		Returns:
			number
		"""
		return self._get_attribute('txInterval')
	@TxInterval.setter
	def TxInterval(self, value):
		self._set_attribute('txInterval', value)

	@property
	def VendorEnterpriseNumber(self):
		"""This signifies the specification of the enterprise number of the vendor.

		Returns:
			number
		"""
		return self._get_attribute('vendorEnterpriseNumber')
	@VendorEnterpriseNumber.setter
	def VendorEnterpriseNumber(self, value):
		self._set_attribute('vendorEnterpriseNumber', value)

	def add(self, BfdCvType=None, BfdDiscriminatorEnd=None, BfdDiscriminatorStart=None, ControlChannel=None, DestinationAddressIpv4=None, DownStreamAddressType=None, DownStreamInterfaceAddress=None, DownStreamIpAddress=None, EchoRequestInterval=None, EchoResponseTimeout=None, EnableDownStreamMappingTlv=None, EnableDsIflag=None, EnableDsNflag=None, EnableFecValidation=None, EnablePeriodicPing=None, Enabled=None, FlapTxIntervals=None, IncludePadTlv=None, IncludeVendorEnterpriseNumberTlv=None, Interfaces=None, MinRxInterval=None, Multiplier=None, PadTlvFirstOctet=None, PadTlvLength=None, ReplyMode=None, TxInterval=None, VendorEnterpriseNumber=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			BfdCvType (str(bfdCvTypeIpUdp|bfdCvTypePwAch)): This signifies the BFD Connectivity Verification type. Possible values include:
			BfdDiscriminatorEnd (number): This signifies the last BFD Discriminator value. This value should be greater than the BFD.
			BfdDiscriminatorStart (number): This signifies the first BFD Discriminator value. The default value is 5000.
			ControlChannel (str(controlChannelRouterAlert|controlChannelPwAch)): This signifies the communication control channel. Possible values include
			DestinationAddressIpv4 (str): This signifies the destination IPv4 address.
			DownStreamAddressType (str(ipv4Numbered|ipv4UnNumbered|ipv6Numbered|ipv6UnNumbered)): This signifies the address type of the downstream traffic. Possible values include:
			DownStreamInterfaceAddress (number): This signifies the interface address of the downstream traffic.
			DownStreamIpAddress (str): This signifies the IPv4/IPv6 address of the downstream traffic.
			EchoRequestInterval (number): This signifies the minimum interval, in milliseconds, between received Echo packets that this interface is capable of supporting.
			EchoResponseTimeout (number): This signifies the minimum tiomeout interval, in milliseconds, between received Echo packets that this interface is capable of supporting.
			EnableDownStreamMappingTlv (bool): This signifies the enablement of downstream mapping TLV.
			EnableDsIflag (bool): This signifies the activation of the DS I Flag.
			EnableDsNflag (bool): This signifies the activation of the DS N Flag.
			EnableFecValidation (bool): This signifies the selection of the check box to enable FEC validation.
			EnablePeriodicPing (bool): If true, the router is pinged at regular intervals.
			Enabled (bool): If true, it enables or disables the simulated router.
			FlapTxIntervals (number): This signifies the number of seconds between route flaps for BFD. A value of zero means no flapping.
			IncludePadTlv (bool): If true, includes Pad TLV in triggered ping.
			IncludeVendorEnterpriseNumberTlv (bool): If true, includes the TLV number of the vendor, in triggered ping.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This signifies the interfaces that are associated with the selected interface type.Object references are:
			MinRxInterval (number): This signifies the minimum interval, in milliseconds, between received BFD Control packets that this interface is capable of supporting.
			Multiplier (number): This signifies the negotiated transmit interval, multiplied by this value, provides the detection time for the interface.
			PadTlvFirstOctet (str(dropPadTlvFromReply|copyPadTlvToReply)): This signifies the selection of the first octate of the Pad TLV. Possible values include:
			PadTlvLength (number): This signifies the specification of the length of the Pad TLV.
			ReplyMode (str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)): This signifies the selecion of the mode of reply.Possible values include DoNotReply, ReplyViaApplicationLevelControlChannel, ReplyViaIpv4Ipv6UdpPacket and ReplyViaIpv4Ipv6UdpPacketWithRouterAlert.
			TxInterval (number): This signifies the minimum interval, in milliseconds, that the interface would like to use when transmitting BFD Control packets.
			VendorEnterpriseNumber (number): This signifies the specification of the enterprise number of the vendor.

		Returns:
			self: This instance with all currently retrieved interface data using find and the newly added interface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BfdCvType=None, BfdDiscriminatorEnd=None, BfdDiscriminatorStart=None, ControlChannel=None, DestinationAddressIpv4=None, DownStreamAddressType=None, DownStreamInterfaceAddress=None, DownStreamIpAddress=None, EchoRequestInterval=None, EchoResponseTimeout=None, EnableDownStreamMappingTlv=None, EnableDsIflag=None, EnableDsNflag=None, EnableFecValidation=None, EnablePeriodicPing=None, Enabled=None, FlapTxIntervals=None, IncludePadTlv=None, IncludeVendorEnterpriseNumberTlv=None, Interfaces=None, MinRxInterval=None, Multiplier=None, PadTlvFirstOctet=None, PadTlvLength=None, ReplyMode=None, TxInterval=None, VendorEnterpriseNumber=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			BfdCvType (str(bfdCvTypeIpUdp|bfdCvTypePwAch)): This signifies the BFD Connectivity Verification type. Possible values include:
			BfdDiscriminatorEnd (number): This signifies the last BFD Discriminator value. This value should be greater than the BFD.
			BfdDiscriminatorStart (number): This signifies the first BFD Discriminator value. The default value is 5000.
			ControlChannel (str(controlChannelRouterAlert|controlChannelPwAch)): This signifies the communication control channel. Possible values include
			DestinationAddressIpv4 (str): This signifies the destination IPv4 address.
			DownStreamAddressType (str(ipv4Numbered|ipv4UnNumbered|ipv6Numbered|ipv6UnNumbered)): This signifies the address type of the downstream traffic. Possible values include:
			DownStreamInterfaceAddress (number): This signifies the interface address of the downstream traffic.
			DownStreamIpAddress (str): This signifies the IPv4/IPv6 address of the downstream traffic.
			EchoRequestInterval (number): This signifies the minimum interval, in milliseconds, between received Echo packets that this interface is capable of supporting.
			EchoResponseTimeout (number): This signifies the minimum tiomeout interval, in milliseconds, between received Echo packets that this interface is capable of supporting.
			EnableDownStreamMappingTlv (bool): This signifies the enablement of downstream mapping TLV.
			EnableDsIflag (bool): This signifies the activation of the DS I Flag.
			EnableDsNflag (bool): This signifies the activation of the DS N Flag.
			EnableFecValidation (bool): This signifies the selection of the check box to enable FEC validation.
			EnablePeriodicPing (bool): If true, the router is pinged at regular intervals.
			Enabled (bool): If true, it enables or disables the simulated router.
			FlapTxIntervals (number): This signifies the number of seconds between route flaps for BFD. A value of zero means no flapping.
			IncludePadTlv (bool): If true, includes Pad TLV in triggered ping.
			IncludeVendorEnterpriseNumberTlv (bool): If true, includes the TLV number of the vendor, in triggered ping.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This signifies the interfaces that are associated with the selected interface type.Object references are:
			MinRxInterval (number): This signifies the minimum interval, in milliseconds, between received BFD Control packets that this interface is capable of supporting.
			Multiplier (number): This signifies the negotiated transmit interval, multiplied by this value, provides the detection time for the interface.
			PadTlvFirstOctet (str(dropPadTlvFromReply|copyPadTlvToReply)): This signifies the selection of the first octate of the Pad TLV. Possible values include:
			PadTlvLength (number): This signifies the specification of the length of the Pad TLV.
			ReplyMode (str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)): This signifies the selecion of the mode of reply.Possible values include DoNotReply, ReplyViaApplicationLevelControlChannel, ReplyViaIpv4Ipv6UdpPacket and ReplyViaIpv4Ipv6UdpPacketWithRouterAlert.
			TxInterval (number): This signifies the minimum interval, in milliseconds, that the interface would like to use when transmitting BFD Control packets.
			VendorEnterpriseNumber (number): This signifies the specification of the enterprise number of the vendor.

		Returns:
			self: This instance with matching interface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
