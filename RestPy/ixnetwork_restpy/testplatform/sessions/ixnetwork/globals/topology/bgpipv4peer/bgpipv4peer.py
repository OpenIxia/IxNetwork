
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


class BgpIpv4Peer(Base):
	"""The BgpIpv4Peer class encapsulates a required bgpIpv4Peer node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpIpv4Peer property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpIpv4Peer'

	def __init__(self, parent):
		super(BgpIpv4Peer, self).__init__(parent)

	@property
	def StartRate(self):
		"""An instance of the StartRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.startrate.startrate.StartRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.startrate.startrate import StartRate
		return StartRate(self)._select()

	@property
	def StopRate(self):
		"""An instance of the StopRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.stoprate.stoprate.StopRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.stoprate.stoprate import StopRate
		return StopRate(self)._select()

	@property
	def TlvEditor(self):
		"""An instance of the TlvEditor class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlveditor.TlvEditor)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlveditor import TlvEditor
		return TlvEditor(self)

	@property
	def BIERTunnelType(self):
		"""BIER Tunnel Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BIERTunnelType')

	@property
	def LLGRCapabilityCode(self):
		"""Long Live Graceful Restart Capability Code

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('LLGRCapabilityCode')

	@property
	def BgpConfMemType(self):
		"""BGP Confederation Member Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpConfMemType')

	@property
	def BgpRouterId(self):
		"""BGP Router-ID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpRouterId')

	@property
	def BindingType(self):
		"""Binding Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bindingType')

	@property
	def ColorType(self):
		"""Color Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorType')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DisableReceivedUpdateValidation(self):
		"""Disable Received Update Validation (Enabled for High Performance)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('disableReceivedUpdateValidation')

	@property
	def EnLenthForPolicyNLRI(self):
		"""Include Length Field in SR TE Policy NLRI

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enLenthForPolicyNLRI')

	@property
	def EnableAdVplsPrefixLength(self):
		"""Enable AD VPLS Prefix Length in Bits

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAdVplsPrefixLength')

	@property
	def IBgpTester4BytesAsNumber(self):
		"""Tester 4 Byte AS# for iBGP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('iBgpTester4BytesAsNumber')

	@property
	def IBgpTesterAsNumber(self):
		"""Tester AS# for iBGP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('iBgpTesterAsNumber')

	@property
	def InitiateEbgpActiveConnection(self):
		"""Initiate eBGP Active Connection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initiateEbgpActiveConnection')

	@property
	def InitiateIbgpActiveConnection(self):
		"""Initiate iBGP Active Connection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initiateIbgpActiveConnection')

	@property
	def Ipv4AddrIndexType(self):
		"""IPv4 Address + Index Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4AddrIndexType')

	@property
	def Ipv4LocRemoteAddrType(self):
		"""IPv4 Local and Remote Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4LocRemoteAddrType')

	@property
	def Ipv4NodeAddrType(self):
		"""IPv4 Node Address Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4NodeAddrType')

	@property
	def Ipv6AddrIndexType(self):
		"""IPv6 Address + Index Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6AddrIndexType')

	@property
	def Ipv6LocRemoteAddrType(self):
		"""IPv6 Local and Remote Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6LocRemoteAddrType')

	@property
	def Ipv6NodeAddrType(self):
		"""IPv6 Node Address Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6NodeAddrType')

	@property
	def Ipv6SIDType(self):
		"""IPv6 SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6SIDType')

	@property
	def LenthForPolicyNLRI(self):
		"""Length Unit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lenthForPolicyNLRI')

	@property
	def MldpP2mpFecType(self):
		"""MLDP P2MP FEC Type (Hex)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mldpP2mpFecType')

	@property
	def MplsSIDType(self):
		"""MPLS SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mplsSIDType')

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
	def PeerAdjSidType(self):
		"""Peer-Adj-SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerAdjSidType')

	@property
	def PeerNodeSidType(self):
		"""Peer-Node-SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerNodeSidType')

	@property
	def PeerSetSidType(self):
		"""Peer-Set-SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerSetSidType')

	@property
	def PreferenceType(self):
		"""Preference Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('preferenceType')

	@property
	def PrefixSIDAttrType(self):
		"""Prefix SID Attr Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixSIDAttrType')

	@property
	def ProtoclIdType(self):
		"""Protocol-ID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protoclIdType')

	@property
	def RemoteEndpointType(self):
		"""Remote Endpoint Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteEndpointType')

	@property
	def RequestVpnLabelExchangeOverLsp(self):
		"""Request VPN Label Exchange over LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestVpnLabelExchangeOverLsp')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def SRv6VPNSIDTLVType(self):
		"""SRv6-VPN SID TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sRv6VPNSIDTLVType')

	@property
	def SegmentListType(self):
		"""Segment List Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('segmentListType')

	@property
	def SrtePolicyAttrType(self):
		"""Tunnel Encaps Attribute Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srtePolicyAttrType')

	@property
	def SrtePolicySAFI(self):
		"""SR TE Policy SAFI

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srtePolicySAFI')

	@property
	def SrtePolicyType(self):
		"""Tunnel Type for SR Policy

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srtePolicyType')

	@property
	def TriggerVplsPwInitiation(self):
		"""Trigger VPLS PW Initiation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('triggerVplsPwInitiation')

	@property
	def UdpDestinationPort(self):
		"""UDP Destination Port for VXLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('udpDestinationPort')

	@property
	def UseUnicastDestMacForBierTraffic(self):
		"""Use Unicast Dst MAC for Traffic

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useUnicastDestMacForBierTraffic')

	@property
	def VPNSIDType(self):
		"""L3VPN SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vPNSIDType')

	@property
	def VrfRouteImportExtendedCommunitySubType(self):
		"""VRF Route Import Extended Community Sub Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vrfRouteImportExtendedCommunitySubType')

	@property
	def WeightType(self):
		"""Weight Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weightType')

	def get_device_ids(self, PortNames=None, BIERTunnelType=None, LLGRCapabilityCode=None, BgpConfMemType=None, BgpRouterId=None, BindingType=None, ColorType=None, DisableReceivedUpdateValidation=None, EnLenthForPolicyNLRI=None, EnableAdVplsPrefixLength=None, IBgpTester4BytesAsNumber=None, IBgpTesterAsNumber=None, InitiateEbgpActiveConnection=None, InitiateIbgpActiveConnection=None, Ipv4AddrIndexType=None, Ipv4LocRemoteAddrType=None, Ipv4NodeAddrType=None, Ipv6AddrIndexType=None, Ipv6LocRemoteAddrType=None, Ipv6NodeAddrType=None, Ipv6SIDType=None, LenthForPolicyNLRI=None, MldpP2mpFecType=None, MplsSIDType=None, PeerAdjSidType=None, PeerNodeSidType=None, PeerSetSidType=None, PreferenceType=None, PrefixSIDAttrType=None, ProtoclIdType=None, RemoteEndpointType=None, RequestVpnLabelExchangeOverLsp=None, SRv6VPNSIDTLVType=None, SegmentListType=None, SrtePolicyAttrType=None, SrtePolicySAFI=None, SrtePolicyType=None, TriggerVplsPwInitiation=None, UdpDestinationPort=None, UseUnicastDestMacForBierTraffic=None, VPNSIDType=None, VrfRouteImportExtendedCommunitySubType=None, WeightType=None):
		"""Base class infrastructure that gets a list of bgpIpv4Peer device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BIERTunnelType (str): optional regex of BIERTunnelType
			LLGRCapabilityCode (str): optional regex of LLGRCapabilityCode
			BgpConfMemType (str): optional regex of bgpConfMemType
			BgpRouterId (str): optional regex of bgpRouterId
			BindingType (str): optional regex of bindingType
			ColorType (str): optional regex of colorType
			DisableReceivedUpdateValidation (str): optional regex of disableReceivedUpdateValidation
			EnLenthForPolicyNLRI (str): optional regex of enLenthForPolicyNLRI
			EnableAdVplsPrefixLength (str): optional regex of enableAdVplsPrefixLength
			IBgpTester4BytesAsNumber (str): optional regex of iBgpTester4BytesAsNumber
			IBgpTesterAsNumber (str): optional regex of iBgpTesterAsNumber
			InitiateEbgpActiveConnection (str): optional regex of initiateEbgpActiveConnection
			InitiateIbgpActiveConnection (str): optional regex of initiateIbgpActiveConnection
			Ipv4AddrIndexType (str): optional regex of ipv4AddrIndexType
			Ipv4LocRemoteAddrType (str): optional regex of ipv4LocRemoteAddrType
			Ipv4NodeAddrType (str): optional regex of ipv4NodeAddrType
			Ipv6AddrIndexType (str): optional regex of ipv6AddrIndexType
			Ipv6LocRemoteAddrType (str): optional regex of ipv6LocRemoteAddrType
			Ipv6NodeAddrType (str): optional regex of ipv6NodeAddrType
			Ipv6SIDType (str): optional regex of ipv6SIDType
			LenthForPolicyNLRI (str): optional regex of lenthForPolicyNLRI
			MldpP2mpFecType (str): optional regex of mldpP2mpFecType
			MplsSIDType (str): optional regex of mplsSIDType
			PeerAdjSidType (str): optional regex of peerAdjSidType
			PeerNodeSidType (str): optional regex of peerNodeSidType
			PeerSetSidType (str): optional regex of peerSetSidType
			PreferenceType (str): optional regex of preferenceType
			PrefixSIDAttrType (str): optional regex of prefixSIDAttrType
			ProtoclIdType (str): optional regex of protoclIdType
			RemoteEndpointType (str): optional regex of remoteEndpointType
			RequestVpnLabelExchangeOverLsp (str): optional regex of requestVpnLabelExchangeOverLsp
			SRv6VPNSIDTLVType (str): optional regex of sRv6VPNSIDTLVType
			SegmentListType (str): optional regex of segmentListType
			SrtePolicyAttrType (str): optional regex of srtePolicyAttrType
			SrtePolicySAFI (str): optional regex of srtePolicySAFI
			SrtePolicyType (str): optional regex of srtePolicyType
			TriggerVplsPwInitiation (str): optional regex of triggerVplsPwInitiation
			UdpDestinationPort (str): optional regex of udpDestinationPort
			UseUnicastDestMacForBierTraffic (str): optional regex of useUnicastDestMacForBierTraffic
			VPNSIDType (str): optional regex of vPNSIDType
			VrfRouteImportExtendedCommunitySubType (str): optional regex of vrfRouteImportExtendedCommunitySubType
			WeightType (str): optional regex of weightType

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
