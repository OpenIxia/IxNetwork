
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			str(bfdCvTypeIpUdp|bfdCvTypePwAch)
		"""
		return self._get_attribute('bfdCvType')
	@BfdCvType.setter
	def BfdCvType(self, value):
		self._set_attribute('bfdCvType', value)

	@property
	def BfdDiscriminatorEnd(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bfdDiscriminatorEnd')
	@BfdDiscriminatorEnd.setter
	def BfdDiscriminatorEnd(self, value):
		self._set_attribute('bfdDiscriminatorEnd', value)

	@property
	def BfdDiscriminatorStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bfdDiscriminatorStart')
	@BfdDiscriminatorStart.setter
	def BfdDiscriminatorStart(self, value):
		self._set_attribute('bfdDiscriminatorStart', value)

	@property
	def ControlChannel(self):
		"""

		Returns:
			str(controlChannelRouterAlert|controlChannelPwAch)
		"""
		return self._get_attribute('controlChannel')
	@ControlChannel.setter
	def ControlChannel(self, value):
		self._set_attribute('controlChannel', value)

	@property
	def DestinationAddressIpv4(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationAddressIpv4')
	@DestinationAddressIpv4.setter
	def DestinationAddressIpv4(self, value):
		self._set_attribute('destinationAddressIpv4', value)

	@property
	def DownStreamAddressType(self):
		"""

		Returns:
			str(ipv4Numbered|ipv4UnNumbered|ipv6Numbered|ipv6UnNumbered)
		"""
		return self._get_attribute('downStreamAddressType')
	@DownStreamAddressType.setter
	def DownStreamAddressType(self, value):
		self._set_attribute('downStreamAddressType', value)

	@property
	def DownStreamInterfaceAddress(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('downStreamInterfaceAddress')
	@DownStreamInterfaceAddress.setter
	def DownStreamInterfaceAddress(self, value):
		self._set_attribute('downStreamInterfaceAddress', value)

	@property
	def DownStreamIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downStreamIpAddress')
	@DownStreamIpAddress.setter
	def DownStreamIpAddress(self, value):
		self._set_attribute('downStreamIpAddress', value)

	@property
	def EchoRequestInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoRequestInterval')
	@EchoRequestInterval.setter
	def EchoRequestInterval(self, value):
		self._set_attribute('echoRequestInterval', value)

	@property
	def EchoResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoResponseTimeout')
	@EchoResponseTimeout.setter
	def EchoResponseTimeout(self, value):
		self._set_attribute('echoResponseTimeout', value)

	@property
	def EnableDownStreamMappingTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDownStreamMappingTlv')
	@EnableDownStreamMappingTlv.setter
	def EnableDownStreamMappingTlv(self, value):
		self._set_attribute('enableDownStreamMappingTlv', value)

	@property
	def EnableDsIflag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDsIflag')
	@EnableDsIflag.setter
	def EnableDsIflag(self, value):
		self._set_attribute('enableDsIflag', value)

	@property
	def EnableDsNflag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDsNflag')
	@EnableDsNflag.setter
	def EnableDsNflag(self, value):
		self._set_attribute('enableDsNflag', value)

	@property
	def EnableFecValidation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFecValidation')
	@EnableFecValidation.setter
	def EnableFecValidation(self, value):
		self._set_attribute('enableFecValidation', value)

	@property
	def EnablePeriodicPing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicPing')
	@EnablePeriodicPing.setter
	def EnablePeriodicPing(self, value):
		self._set_attribute('enablePeriodicPing', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FlapTxIntervals(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flapTxIntervals')
	@FlapTxIntervals.setter
	def FlapTxIntervals(self, value):
		self._set_attribute('flapTxIntervals', value)

	@property
	def IncludePadTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includePadTlv')
	@IncludePadTlv.setter
	def IncludePadTlv(self, value):
		self._set_attribute('includePadTlv', value)

	@property
	def IncludeVendorEnterpriseNumberTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeVendorEnterpriseNumberTlv')
	@IncludeVendorEnterpriseNumberTlv.setter
	def IncludeVendorEnterpriseNumberTlv(self, value):
		self._set_attribute('includeVendorEnterpriseNumberTlv', value)

	@property
	def Interfaces(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def MinRxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minRxInterval')
	@MinRxInterval.setter
	def MinRxInterval(self, value):
		self._set_attribute('minRxInterval', value)

	@property
	def Multiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def PadTlvFirstOctet(self):
		"""

		Returns:
			str(dropPadTlvFromReply|copyPadTlvToReply)
		"""
		return self._get_attribute('padTlvFirstOctet')
	@PadTlvFirstOctet.setter
	def PadTlvFirstOctet(self, value):
		self._set_attribute('padTlvFirstOctet', value)

	@property
	def PadTlvLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('padTlvLength')
	@PadTlvLength.setter
	def PadTlvLength(self, value):
		self._set_attribute('padTlvLength', value)

	@property
	def ReplyMode(self):
		"""

		Returns:
			str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)
		"""
		return self._get_attribute('replyMode')
	@ReplyMode.setter
	def ReplyMode(self, value):
		self._set_attribute('replyMode', value)

	@property
	def TxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('txInterval')
	@TxInterval.setter
	def TxInterval(self, value):
		self._set_attribute('txInterval', value)

	@property
	def VendorEnterpriseNumber(self):
		"""

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
			BfdCvType (str(bfdCvTypeIpUdp|bfdCvTypePwAch)): 
			BfdDiscriminatorEnd (number): 
			BfdDiscriminatorStart (number): 
			ControlChannel (str(controlChannelRouterAlert|controlChannelPwAch)): 
			DestinationAddressIpv4 (str): 
			DownStreamAddressType (str(ipv4Numbered|ipv4UnNumbered|ipv6Numbered|ipv6UnNumbered)): 
			DownStreamInterfaceAddress (number): 
			DownStreamIpAddress (str): 
			EchoRequestInterval (number): 
			EchoResponseTimeout (number): 
			EnableDownStreamMappingTlv (bool): 
			EnableDsIflag (bool): 
			EnableDsNflag (bool): 
			EnableFecValidation (bool): 
			EnablePeriodicPing (bool): 
			Enabled (bool): 
			FlapTxIntervals (number): 
			IncludePadTlv (bool): 
			IncludeVendorEnterpriseNumberTlv (bool): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			MinRxInterval (number): 
			Multiplier (number): 
			PadTlvFirstOctet (str(dropPadTlvFromReply|copyPadTlvToReply)): 
			PadTlvLength (number): 
			ReplyMode (str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)): 
			TxInterval (number): 
			VendorEnterpriseNumber (number): 

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
			BfdCvType (str(bfdCvTypeIpUdp|bfdCvTypePwAch)): 
			BfdDiscriminatorEnd (number): 
			BfdDiscriminatorStart (number): 
			ControlChannel (str(controlChannelRouterAlert|controlChannelPwAch)): 
			DestinationAddressIpv4 (str): 
			DownStreamAddressType (str(ipv4Numbered|ipv4UnNumbered|ipv6Numbered|ipv6UnNumbered)): 
			DownStreamInterfaceAddress (number): 
			DownStreamIpAddress (str): 
			EchoRequestInterval (number): 
			EchoResponseTimeout (number): 
			EnableDownStreamMappingTlv (bool): 
			EnableDsIflag (bool): 
			EnableDsNflag (bool): 
			EnableFecValidation (bool): 
			EnablePeriodicPing (bool): 
			Enabled (bool): 
			FlapTxIntervals (number): 
			IncludePadTlv (bool): 
			IncludeVendorEnterpriseNumberTlv (bool): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			MinRxInterval (number): 
			Multiplier (number): 
			PadTlvFirstOctet (str(dropPadTlvFromReply|copyPadTlvToReply)): 
			PadTlvLength (number): 
			ReplyMode (str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)): 
			TxInterval (number): 
			VendorEnterpriseNumber (number): 

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
