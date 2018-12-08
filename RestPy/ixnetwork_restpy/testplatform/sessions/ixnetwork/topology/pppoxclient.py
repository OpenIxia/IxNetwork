
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


class Pppoxclient(Base):
	"""The Pppoxclient class encapsulates a user managed pppoxclient node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Pppoxclient property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'pppoxclient'

	def __init__(self, parent):
		super(Pppoxclient, self).__init__(parent)

	@property
	def Bfdv4Interface(self):
		"""An instance of the Bfdv4Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv4interface.Bfdv4Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv4interface import Bfdv4Interface
		return Bfdv4Interface(self)

	@property
	def Bfdv6Interface(self):
		"""An instance of the Bfdv6Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6interface.Bfdv6Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6interface import Bfdv6Interface
		return Bfdv6Interface(self)

	@property
	def BgpIpv4Peer(self):
		"""An instance of the BgpIpv4Peer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4peer.BgpIpv4Peer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4peer import BgpIpv4Peer
		return BgpIpv4Peer(self)

	@property
	def BgpIpv6Peer(self):
		"""An instance of the BgpIpv6Peer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv6peer.BgpIpv6Peer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv6peer import BgpIpv6Peer
		return BgpIpv6Peer(self)

	@property
	def Connector(self):
		"""An instance of the Connector class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return Connector(self)

	@property
	def Dhcpv6client(self):
		"""An instance of the Dhcpv6client class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client.Dhcpv6client)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client import Dhcpv6client
		return Dhcpv6client(self)

	@property
	def Geneve(self):
		"""An instance of the Geneve class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.geneve.Geneve)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.geneve import Geneve
		return Geneve(self)

	@property
	def IgmpHost(self):
		"""An instance of the IgmpHost class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmphost.IgmpHost)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmphost import IgmpHost
		return IgmpHost(self)

	@property
	def IgmpQuerier(self):
		"""An instance of the IgmpQuerier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpquerier.IgmpQuerier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpquerier import IgmpQuerier
		return IgmpQuerier(self)

	@property
	def MldHost(self):
		"""An instance of the MldHost class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldhost.MldHost)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldhost import MldHost
		return MldHost(self)

	@property
	def MldQuerier(self):
		"""An instance of the MldQuerier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldquerier.MldQuerier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldquerier import MldQuerier
		return MldQuerier(self)

	@property
	def MplsOam(self):
		"""An instance of the MplsOam class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplsoam.MplsOam)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplsoam import MplsOam
		return MplsOam(self)

	@property
	def NetconfClient(self):
		"""An instance of the NetconfClient class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfclient.NetconfClient)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfclient import NetconfClient
		return NetconfClient(self)

	@property
	def NetconfServer(self):
		"""An instance of the NetconfServer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfserver.NetconfServer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfserver import NetconfServer
		return NetconfServer(self)

	@property
	def Ospfv2(self):
		"""An instance of the Ospfv2 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv2.Ospfv2)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv2 import Ospfv2
		return Ospfv2(self)

	@property
	def Ospfv3(self):
		"""An instance of the Ospfv3 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3.Ospfv3)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3 import Ospfv3
		return Ospfv3(self)

	@property
	def Pcc(self):
		"""An instance of the Pcc class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcc.Pcc)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcc import Pcc
		return Pcc(self)

	@property
	def Pce(self):
		"""An instance of the Pce class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pce.Pce)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pce import Pce
		return Pce(self)

	@property
	def PimV4Interface(self):
		"""An instance of the PimV4Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv4interface.PimV4Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv4interface import PimV4Interface
		return PimV4Interface(self)

	@property
	def PimV6Interface(self):
		"""An instance of the PimV6Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv6interface.PimV6Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv6interface import PimV6Interface
		return PimV6Interface(self)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def Vxlan(self):
		"""An instance of the Vxlan class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vxlan.Vxlan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vxlan import Vxlan
		return Vxlan(self)

	@property
	def AcMatchMac(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acMatchMac')

	@property
	def AcMatchName(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acMatchName')

	@property
	def AcOptions(self):
		"""Indicates PPPoE AC retrieval mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acOptions')

	@property
	def ActualRateDownstream(self):
		"""This parameter specifies the value to be included in the vendor specific PPPoE tag. It is the actual downstream data rate (sub-option 0x81), in kbps.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actualRateDownstream')

	@property
	def ActualRateUpstream(self):
		"""This parameter specifies the value to be included in the vendor specific PPPoE tag. It is the actual upstream data rate (sub-option 0x82), in kbps.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actualRateUpstream')

	@property
	def AgentAccessAggregationCircuitId(self):
		"""The value to be inserted into the Agent Access-Aggregation-Circuit-ID-ASCII-Value field of the PPPoX tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('agentAccessAggregationCircuitId')

	@property
	def AgentCircuitId(self):
		"""The value to be inserted into the Agent Circuit ID field of the PPPoX tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('agentCircuitId')

	@property
	def AgentRemoteId(self):
		"""The value to be inserted into the Agent Remote ID field of the PPPoX tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('agentRemoteId')

	@property
	def AuthRetries(self):
		"""Number of PPP authentication retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authRetries')

	@property
	def AuthTimeout(self):
		"""Timeout for PPP authentication, in seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authTimeout')

	@property
	def AuthType(self):
		"""The authentication type to use during link setup.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authType')

	@property
	def ChapName(self):
		"""User name when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapName')

	@property
	def ChapSecret(self):
		"""Secret when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapSecret')

	@property
	def ClientDnsOptions(self):
		"""The client DNS options.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientDnsOptions')

	@property
	def ClientLocalIp(self):
		"""The requested IPv4 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientLocalIp')

	@property
	def ClientLocalIpv6Iid(self):
		"""The requested IPv6 Interface Identifier (IID).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientLocalIpv6Iid')

	@property
	def ClientNcpOptions(self):
		"""The NCP configuration mode for IPv4 addressing.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientNcpOptions')

	@property
	def ClientNetmask(self):
		"""The netmask that the client will use with the assigned IP address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientNetmask')

	@property
	def ClientNetmaskOptions(self):
		"""The client netmask option.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientNetmaskOptions')

	@property
	def ClientPrimaryDnsAddress(self):
		"""This is the primary DNS server address that the client requests from the server when the value of the Client DNS Options field is set to 'Request Primary only' or 'Request Primary and Secondary'.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientPrimaryDnsAddress')

	@property
	def ClientSecondaryDnsAddress(self):
		"""This is the secondary DNS server address that the client requests from the server when the value of the Client DNS Options field is set to 'Request Primary and Secondary'.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSecondaryDnsAddress')

	@property
	def ClientSignalIWF(self):
		"""This parameter enables or disables the insertion of sub-option 0xFE (signaling of interworked sessions) into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalIWF')

	@property
	def ClientSignalLoopChar(self):
		"""This parameter enables or disables the insertion of sub-options 0x81 and 0x82 into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalLoopChar')

	@property
	def ClientSignalLoopEncapsulation(self):
		"""This parameter enables or disables the insertion of sub-option 0x90 into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalLoopEncapsulation')

	@property
	def ClientSignalLoopId(self):
		"""This parameter enables or disables the insertion of sub-options 0x01 , 0x02, 0x03 (Remote ID,Circuit ID and Access Aggregation Circuit ID) into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalLoopId')

	@property
	def ClientV6NcpOptions(self):
		"""The NCP configuration mode for IPv6 addressing.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientV6NcpOptions')

	@property
	def ClientWinsOptions(self):
		"""Specifies the mode in which WINS host addresses are configured.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientWinsOptions')

	@property
	def ClientWinsPrimaryAddress(self):
		"""Specifies the primary WINS address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientWinsPrimaryAddress')

	@property
	def ClientWinsSecondaryAddress(self):
		"""Specifies the secondary WINS address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientWinsSecondaryAddress')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DataLink(self):
		"""A one-byte field included with sub-option 0x90.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dataLink')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DiscoveredIpv4Addresses(self):
		"""The discovered IPv4 addresses.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredIpv4Addresses')

	@property
	def DiscoveredIpv6Addresses(self):
		"""The discovered IPv6 addresses.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredIpv6Addresses')

	@property
	def DiscoveredMacs(self):
		"""The discovered remote MAC address.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredMacs')

	@property
	def DiscoveredRemoteSessionIds(self):
		"""Remote session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteSessionIds')

	@property
	def DiscoveredRemoteTunnelIds(self):
		"""Remote tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteTunnelIds')

	@property
	def DiscoveredSessionIds(self):
		"""The negotiated session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredSessionIds')

	@property
	def DiscoveredTunnelIPs(self):
		"""The discovered remote tunnel IP.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredTunnelIPs')

	@property
	def DiscoveredTunnelIds(self):
		"""The negotiated tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredTunnelIds')

	@property
	def DomainList(self):
		"""Configure domain group settings

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domainList')

	@property
	def DslTypeTlv(self):
		"""DSL Type to be advertised in PPPoE VSA Tag. For undefined DSL type user has to select User-defined DSL Type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dslTypeTlv')

	@property
	def EchoReqInterval(self):
		"""Keep alive interval, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoReqInterval')

	@property
	def EnableDomainGroups(self):
		"""Enable domain groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDomainGroups')

	@property
	def EnableEchoReq(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEchoReq')

	@property
	def EnableEchoRsp(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEchoRsp')

	@property
	def EnableHostUniq(self):
		"""Enables PPPoE Host-Uniq tag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHostUniq')

	@property
	def EnableMaxPayload(self):
		"""Enables PPPoE Max Payload tag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableMaxPayload')

	@property
	def EnableRedial(self):
		"""If checked, PPPoE redial is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRedial')

	@property
	def Encaps1(self):
		"""A one-byte field included with sub-option 0x90.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('encaps1')

	@property
	def Encaps2(self):
		"""A one-byte field included with sub-option 0x90.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('encaps2')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def HostUniq(self):
		"""Indicates Host-Uniq Tag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostUniq')

	@property
	def HostUniqLength(self):
		"""Host-Uniq Length, in bytes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostUniqLength')

	@property
	def LcpAccm(self):
		"""Async-Control-Character-Map

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpAccm')

	@property
	def LcpEnableAccm(self):
		"""Enable Async-Control-Character-Map

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpEnableAccm')

	@property
	def LcpMaxFailure(self):
		"""Number of Configure-Nak packets sent without sending a Configure-Ack before assuming that configuration is not converging. Any further Configure-Nak packets for peer requested options are converted to Configure-Reject packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpMaxFailure')

	@property
	def LcpRetries(self):
		"""Number of LCP retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpRetries')

	@property
	def LcpStartDelay(self):
		"""Delay time in milliseconds to wait before sending LCP Config Request packet

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpStartDelay')

	@property
	def LcpTermRetries(self):
		"""Number of LCP Termination Retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpTermRetries')

	@property
	def LcpTimeout(self):
		"""Timeout for LCP phase, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpTimeout')

	@property
	def MaxPayload(self):
		"""Max Payload

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxPayload')

	@property
	def MruNegotiation(self):
		"""Enable MRU Negotiation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mruNegotiation')

	@property
	def Mtu(self):
		"""Max Transmit Unit for PPP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mtu')

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NcpRetries(self):
		"""Number of NCP retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ncpRetries')

	@property
	def NcpTimeout(self):
		"""Timeout for NCP phase, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ncpTimeout')

	@property
	def NcpType(self):
		"""IP address type (IPv4 or IPv6) for Network Control Protocol

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ncpType')

	@property
	def PadiRetries(self):
		"""Number of PADI Retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padiRetries')

	@property
	def PadiTimeout(self):
		"""Timeout for PADI no response, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padiTimeout')

	@property
	def PadrRetries(self):
		"""Number of PADR Retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padrRetries')

	@property
	def PadrTimeout(self):
		"""Timeout for PADR no response, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padrTimeout')

	@property
	def PapPassword(self):
		"""Password when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papPassword')

	@property
	def PapUser(self):
		"""User name when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papUser')

	@property
	def PonTypeTlv(self):
		"""PON Type to be advertised in PPPoE VSA Tag. For undefined PON type user has to select User-defined PON Type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ponTypeTlv')

	@property
	def RedialMax(self):
		"""Maximum number of PPPoE redials

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redialMax')

	@property
	def RedialTimeout(self):
		"""PPPoE redial timeout, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redialTimeout')

	@property
	def ServiceName(self):
		"""Access Concentrator Service Name - this option is only available for PPP servers.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serviceName')

	@property
	def ServiceOptions(self):
		"""Indicates PPPoE service retrieval mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serviceOptions')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[cLS_CFG_REJ_AUTH|cLS_CHAP_PEER_DET_FAIL|cLS_CHAP_PEER_RESP_BAD|cLS_CODE_REJ_IPCP|cLS_CODE_REJ_IPV6CP|cLS_CODE_REJ_LCP|cLS_ERR_PPP_NO_BUF|cLS_ERR_PPP_SEND_PKT|cLS_LINK_DISABLE|cLS_LOC_IPADDR_BROADCAST|cLS_LOC_IPADDR_CLASS_E|cLS_LOC_IPADDR_INVAL_ACKS_0|cLS_LOC_IPADDR_INVAL_ACKS_DIFF|cLS_LOC_IPADDR_LOOPBACK|cLS_LOC_IPADDR_PEER_MATCH_LOC|cLS_LOC_IPADDR_PEER_NO_GIVE|cLS_LOC_IPADDR_PEER_NO_HELP|cLS_LOC_IPADDR_PEER_NO_TAKE|cLS_LOC_IPADDR_PEER_REJ|cLS_LOOPBACK_DETECT|cLS_NO_NCP|cLS_NONE|cLS_PAP_BAD_PASSWD|cLS_PEER_DISCONNECTED|cLS_PEER_DISCONNECTED_NEGO|cLS_PEER_IPADDR_MATCH_LOC|cLS_PEER_IPADDR_PEER_NO_SET|cLS_PPOE_AC_SYSTEM_ERROR|cLS_PPOE_GENERIC_ERROR|cLS_PPP_DISABLE|cLS_PPPOE_NO_HOST_UNIQ|cLS_PPPOE_PADI_TIMEOUT|cLS_PPPOE_PADO_TIMEOUT|cLS_PPPOE_PADR_TIMEOUT|cLS_PROTO_REJ_IPCP|cLS_PROTO_REJ_IPv6CP|cLS_TIMEOUT_CHAP_CHAL|cLS_TIMEOUT_CHAP_RESP|cLS_TIMEOUT_IPCP_CFG_REQ|cLS_TIMEOUT_IPV6CP_CFG_REQ|cLS_TIMEOUT_IPV6CP_RA|cLS_TIMEOUT_LCP_CFG_REQ|cLS_TIMEOUT_LCP_ECHO_REQ|cLS_TIMEOUT_PAP_AUTH_REQ|cLS_TUN_AUTH_FAILED|cLS_TUN_NO_RESOURCES|cLS_TUN_TIMEOUT_ICRQ|cLS_TUN_TIMEOUT_SCCRQ|cLS_TUN_VENDOR_SPECIFIC_ERR])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def UnlimitedRedialAttempts(self):
		"""If checked, PPPoE unlimited redial attempts is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unlimitedRedialAttempts')

	@property
	def UserDefinedDslType(self):
		"""User Defined DSL-Type Value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('userDefinedDslType')

	@property
	def UserDefinedPonType(self):
		"""User Defined PON-Type Value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('userDefinedPonType')

	def add(self, ConnectedVia=None, Multiplier=None, Name=None, StackedLayers=None):
		"""Adds a new pppoxclient node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved pppoxclient data using find and the newly added pppoxclient data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the pppoxclient data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, DiscoveredIpv4Addresses=None, DiscoveredIpv6Addresses=None, DiscoveredMacs=None, DiscoveredRemoteSessionIds=None, DiscoveredRemoteTunnelIds=None, DiscoveredSessionIds=None, DiscoveredTunnelIPs=None, DiscoveredTunnelIds=None, Errors=None, Multiplier=None, Name=None, SessionInfo=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves pppoxclient data from the server.

		All named parameters support regex and can be used to selectively retrieve pppoxclient data from the server.
		By default the find method takes no parameters and will retrieve all pppoxclient data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			DiscoveredIpv4Addresses (list(str)): The discovered IPv4 addresses.
			DiscoveredIpv6Addresses (list(str)): The discovered IPv6 addresses.
			DiscoveredMacs (list(str)): The discovered remote MAC address.
			DiscoveredRemoteSessionIds (list(number)): Remote session ID.
			DiscoveredRemoteTunnelIds (list(number)): Remote tunnel ID.
			DiscoveredSessionIds (list(number)): The negotiated session ID.
			DiscoveredTunnelIPs (list(str)): The discovered remote tunnel IP.
			DiscoveredTunnelIds (list(number)): The negotiated tunnel ID.
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SessionInfo (list(str[cLS_CFG_REJ_AUTH|cLS_CHAP_PEER_DET_FAIL|cLS_CHAP_PEER_RESP_BAD|cLS_CODE_REJ_IPCP|cLS_CODE_REJ_IPV6CP|cLS_CODE_REJ_LCP|cLS_ERR_PPP_NO_BUF|cLS_ERR_PPP_SEND_PKT|cLS_LINK_DISABLE|cLS_LOC_IPADDR_BROADCAST|cLS_LOC_IPADDR_CLASS_E|cLS_LOC_IPADDR_INVAL_ACKS_0|cLS_LOC_IPADDR_INVAL_ACKS_DIFF|cLS_LOC_IPADDR_LOOPBACK|cLS_LOC_IPADDR_PEER_MATCH_LOC|cLS_LOC_IPADDR_PEER_NO_GIVE|cLS_LOC_IPADDR_PEER_NO_HELP|cLS_LOC_IPADDR_PEER_NO_TAKE|cLS_LOC_IPADDR_PEER_REJ|cLS_LOOPBACK_DETECT|cLS_NO_NCP|cLS_NONE|cLS_PAP_BAD_PASSWD|cLS_PEER_DISCONNECTED|cLS_PEER_DISCONNECTED_NEGO|cLS_PEER_IPADDR_MATCH_LOC|cLS_PEER_IPADDR_PEER_NO_SET|cLS_PPOE_AC_SYSTEM_ERROR|cLS_PPOE_GENERIC_ERROR|cLS_PPP_DISABLE|cLS_PPPOE_NO_HOST_UNIQ|cLS_PPPOE_PADI_TIMEOUT|cLS_PPPOE_PADO_TIMEOUT|cLS_PPPOE_PADR_TIMEOUT|cLS_PROTO_REJ_IPCP|cLS_PROTO_REJ_IPv6CP|cLS_TIMEOUT_CHAP_CHAL|cLS_TIMEOUT_CHAP_RESP|cLS_TIMEOUT_IPCP_CFG_REQ|cLS_TIMEOUT_IPV6CP_CFG_REQ|cLS_TIMEOUT_IPV6CP_RA|cLS_TIMEOUT_LCP_CFG_REQ|cLS_TIMEOUT_LCP_ECHO_REQ|cLS_TIMEOUT_PAP_AUTH_REQ|cLS_TUN_AUTH_FAILED|cLS_TUN_NO_RESOURCES|cLS_TUN_TIMEOUT_ICRQ|cLS_TUN_TIMEOUT_SCCRQ|cLS_TUN_VENDOR_SPECIFIC_ERR])): Logs additional information about the session state
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching pppoxclient data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pppoxclient data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pppoxclient data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, AcMatchMac=None, AcMatchName=None, AcOptions=None, ActualRateDownstream=None, ActualRateUpstream=None, AgentAccessAggregationCircuitId=None, AgentCircuitId=None, AgentRemoteId=None, AuthRetries=None, AuthTimeout=None, AuthType=None, ChapName=None, ChapSecret=None, ClientDnsOptions=None, ClientLocalIp=None, ClientLocalIpv6Iid=None, ClientNcpOptions=None, ClientNetmask=None, ClientNetmaskOptions=None, ClientPrimaryDnsAddress=None, ClientSecondaryDnsAddress=None, ClientSignalIWF=None, ClientSignalLoopChar=None, ClientSignalLoopEncapsulation=None, ClientSignalLoopId=None, ClientV6NcpOptions=None, ClientWinsOptions=None, ClientWinsPrimaryAddress=None, ClientWinsSecondaryAddress=None, DataLink=None, DomainList=None, DslTypeTlv=None, EchoReqInterval=None, EnableDomainGroups=None, EnableEchoReq=None, EnableEchoRsp=None, EnableHostUniq=None, EnableMaxPayload=None, EnableRedial=None, Encaps1=None, Encaps2=None, HostUniq=None, HostUniqLength=None, LcpAccm=None, LcpEnableAccm=None, LcpMaxFailure=None, LcpRetries=None, LcpStartDelay=None, LcpTermRetries=None, LcpTimeout=None, MaxPayload=None, MruNegotiation=None, Mtu=None, NcpRetries=None, NcpTimeout=None, NcpType=None, PadiRetries=None, PadiTimeout=None, PadrRetries=None, PadrTimeout=None, PapPassword=None, PapUser=None, PonTypeTlv=None, RedialMax=None, RedialTimeout=None, ServiceName=None, ServiceOptions=None, UnlimitedRedialAttempts=None, UserDefinedDslType=None, UserDefinedPonType=None):
		"""Base class infrastructure that gets a list of pppoxclient device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AcMatchMac (str): optional regex of acMatchMac
			AcMatchName (str): optional regex of acMatchName
			AcOptions (str): optional regex of acOptions
			ActualRateDownstream (str): optional regex of actualRateDownstream
			ActualRateUpstream (str): optional regex of actualRateUpstream
			AgentAccessAggregationCircuitId (str): optional regex of agentAccessAggregationCircuitId
			AgentCircuitId (str): optional regex of agentCircuitId
			AgentRemoteId (str): optional regex of agentRemoteId
			AuthRetries (str): optional regex of authRetries
			AuthTimeout (str): optional regex of authTimeout
			AuthType (str): optional regex of authType
			ChapName (str): optional regex of chapName
			ChapSecret (str): optional regex of chapSecret
			ClientDnsOptions (str): optional regex of clientDnsOptions
			ClientLocalIp (str): optional regex of clientLocalIp
			ClientLocalIpv6Iid (str): optional regex of clientLocalIpv6Iid
			ClientNcpOptions (str): optional regex of clientNcpOptions
			ClientNetmask (str): optional regex of clientNetmask
			ClientNetmaskOptions (str): optional regex of clientNetmaskOptions
			ClientPrimaryDnsAddress (str): optional regex of clientPrimaryDnsAddress
			ClientSecondaryDnsAddress (str): optional regex of clientSecondaryDnsAddress
			ClientSignalIWF (str): optional regex of clientSignalIWF
			ClientSignalLoopChar (str): optional regex of clientSignalLoopChar
			ClientSignalLoopEncapsulation (str): optional regex of clientSignalLoopEncapsulation
			ClientSignalLoopId (str): optional regex of clientSignalLoopId
			ClientV6NcpOptions (str): optional regex of clientV6NcpOptions
			ClientWinsOptions (str): optional regex of clientWinsOptions
			ClientWinsPrimaryAddress (str): optional regex of clientWinsPrimaryAddress
			ClientWinsSecondaryAddress (str): optional regex of clientWinsSecondaryAddress
			DataLink (str): optional regex of dataLink
			DomainList (str): optional regex of domainList
			DslTypeTlv (str): optional regex of dslTypeTlv
			EchoReqInterval (str): optional regex of echoReqInterval
			EnableDomainGroups (str): optional regex of enableDomainGroups
			EnableEchoReq (str): optional regex of enableEchoReq
			EnableEchoRsp (str): optional regex of enableEchoRsp
			EnableHostUniq (str): optional regex of enableHostUniq
			EnableMaxPayload (str): optional regex of enableMaxPayload
			EnableRedial (str): optional regex of enableRedial
			Encaps1 (str): optional regex of encaps1
			Encaps2 (str): optional regex of encaps2
			HostUniq (str): optional regex of hostUniq
			HostUniqLength (str): optional regex of hostUniqLength
			LcpAccm (str): optional regex of lcpAccm
			LcpEnableAccm (str): optional regex of lcpEnableAccm
			LcpMaxFailure (str): optional regex of lcpMaxFailure
			LcpRetries (str): optional regex of lcpRetries
			LcpStartDelay (str): optional regex of lcpStartDelay
			LcpTermRetries (str): optional regex of lcpTermRetries
			LcpTimeout (str): optional regex of lcpTimeout
			MaxPayload (str): optional regex of maxPayload
			MruNegotiation (str): optional regex of mruNegotiation
			Mtu (str): optional regex of mtu
			NcpRetries (str): optional regex of ncpRetries
			NcpTimeout (str): optional regex of ncpTimeout
			NcpType (str): optional regex of ncpType
			PadiRetries (str): optional regex of padiRetries
			PadiTimeout (str): optional regex of padiTimeout
			PadrRetries (str): optional regex of padrRetries
			PadrTimeout (str): optional regex of padrTimeout
			PapPassword (str): optional regex of papPassword
			PapUser (str): optional regex of papUser
			PonTypeTlv (str): optional regex of ponTypeTlv
			RedialMax (str): optional regex of redialMax
			RedialTimeout (str): optional regex of redialTimeout
			ServiceName (str): optional regex of serviceName
			ServiceOptions (str): optional regex of serviceOptions
			UnlimitedRedialAttempts (str): optional regex of unlimitedRedialAttempts
			UserDefinedDslType (str): optional regex of userDefinedDslType
			UserDefinedPonType (str): optional regex of userDefinedPonType

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def CloseIpcp(self):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CloseIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CloseIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CloseIpcp', payload=locals(), response_object=None)

	def CloseIpv6cp(self):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CloseIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CloseIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CloseIpv6cp', payload=locals(), response_object=None)

	def OpenIpcp(self):
		"""Executes the openIpcp operation on the server.

		Open IPCP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('OpenIpcp', payload=locals(), response_object=None)

	def OpenIpcp(self, SessionIndices):
		"""Executes the openIpcp operation on the server.

		Open IPCP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('OpenIpcp', payload=locals(), response_object=None)

	def OpenIpcp(self, SessionIndices):
		"""Executes the openIpcp operation on the server.

		Open IPCP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('OpenIpcp', payload=locals(), response_object=None)

	def OpenIpv6cp(self):
		"""Executes the openIpv6cp operation on the server.

		Open IPv6CP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('OpenIpv6cp', payload=locals(), response_object=None)

	def OpenIpv6cp(self, SessionIndices):
		"""Executes the openIpv6cp operation on the server.

		Open IPv6CP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('OpenIpv6cp', payload=locals(), response_object=None)

	def OpenIpv6cp(self, SessionIndices):
		"""Executes the openIpv6cp operation on the server.

		Open IPv6CP for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('OpenIpv6cp', payload=locals(), response_object=None)

	def RestartDown(self):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def SendPing(self, DestIp):
		"""Executes the sendPing operation on the server.

		Send Ping IPv4 for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			DestIp (str): This parameter requires a destIp of type kString

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPing', payload=locals(), response_object=None)

	def SendPing(self, DestIp, SessionIndices):
		"""Executes the sendPing operation on the server.

		Send Ping IPv4 for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			DestIp (str): This parameter requires a destIp of type kString
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPing', payload=locals(), response_object=None)

	def SendPing(self, SessionIndices, DestIp):
		"""Executes the sendPing operation on the server.

		Send Ping IPv4 for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a destIp of type kString
			DestIp (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPing', payload=locals(), response_object=None)

	def SendPing6(self, DestIp):
		"""Executes the sendPing6 operation on the server.

		Send Ping IPv6 for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			DestIp (str): This parameter requires a destIp of type kString

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPing6', payload=locals(), response_object=None)

	def SendPing6(self, DestIp, SessionIndices):
		"""Executes the sendPing6 operation on the server.

		Send Ping IPv6 for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			DestIp (str): This parameter requires a destIp of type kString
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPing6', payload=locals(), response_object=None)

	def SendPing6(self, SessionIndices, DestIp):
		"""Executes the sendPing6 operation on the server.

		Send Ping IPv6 for selected PPPoX items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a destIp of type kString
			DestIp (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPing6', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
