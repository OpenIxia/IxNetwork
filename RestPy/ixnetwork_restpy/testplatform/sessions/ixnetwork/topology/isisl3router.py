
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


class IsisL3Router(Base):
	"""The IsisL3Router class encapsulates a system managed isisL3Router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IsisL3Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'isisL3Router'

	def __init__(self, parent):
		super(IsisL3Router, self).__init__(parent)

	@property
	def IsisBierSubDomainList(self):
		"""An instance of the IsisBierSubDomainList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisbiersubdomainlist.IsisBierSubDomainList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisbiersubdomainlist import IsisBierSubDomainList
		return IsisBierSubDomainList(self)._select()

	@property
	def IsisMappingServerIPV4List(self):
		"""An instance of the IsisMappingServerIPV4List class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isismappingserveripv4list.IsisMappingServerIPV4List)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isismappingserveripv4list import IsisMappingServerIPV4List
		return IsisMappingServerIPV4List(self)._select()

	@property
	def IsisMappingServerIPV6List(self):
		"""An instance of the IsisMappingServerIPV6List class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isismappingserveripv6list.IsisMappingServerIPV6List)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isismappingserveripv6list import IsisMappingServerIPV6List
		return IsisMappingServerIPV6List(self)._select()

	@property
	def IsisSRAlgorithmList(self):
		"""An instance of the IsisSRAlgorithmList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissralgorithmlist.IsisSRAlgorithmList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissralgorithmlist import IsisSRAlgorithmList
		return IsisSRAlgorithmList(self)

	@property
	def IsisSRGBRangeSubObjectsList(self):
		"""An instance of the IsisSRGBRangeSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissrgbrangesubobjectslist.IsisSRGBRangeSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissrgbrangesubobjectslist import IsisSRGBRangeSubObjectsList
		return IsisSRGBRangeSubObjectsList(self)

	@property
	def IsisSRLBDescriptorList(self):
		"""An instance of the IsisSRLBDescriptorList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissrlbdescriptorlist.IsisSRLBDescriptorList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissrlbdescriptorlist import IsisSRLBDescriptorList
		return IsisSRLBDescriptorList(self)

	@property
	def IsisSRTunnelList(self):
		"""An instance of the IsisSRTunnelList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissrtunnellist.IsisSRTunnelList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissrtunnellist import IsisSRTunnelList
		return IsisSRTunnelList(self)._select()

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
	def BIERNodePrefix(self):
		"""Node Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BIERNodePrefix')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvertiseSRLB(self):
		"""Enables advertisement of Segment Routing Local Block (SRLB) Sub-Tlv in Router Capability Tlv

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseSRLB')

	@property
	def AdvertiseSRMSPreference(self):
		"""Advertise SRMS Preference sub-TLV in Router capability TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseSRMSPreference')

	@property
	def AdvertiseSidAsLocator(self):
		"""If enabled, then the configured IPv6 Node SID gets advertised as a reachable IPv6 prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseSidAsLocator')

	@property
	def Algorithm(self):
		"""Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('algorithm')

	@property
	def AreaAddresses(self):
		"""Area Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaAddresses')

	@property
	def AreaAuthenticationType(self):
		"""Area Authentication Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaAuthenticationType')

	@property
	def AreaTransmitPasswordOrMD5Key(self):
		"""Area Transmit Password / MD5-Key

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaTransmitPasswordOrMD5Key')

	@property
	def Attached(self):
		"""Attached

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('attached')

	@property
	def BIERIPv6NodePrefix(self):
		"""IPv6 Node Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bIERIPv6NodePrefix')

	@property
	def BierNFlag(self):
		"""Nodal prefix flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierNFlag')

	@property
	def BierRFlag(self):
		"""Redistribution flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierRFlag')

	@property
	def CSNPInterval(self):
		"""CSNP Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cSNPInterval')

	@property
	def ConfigureSIDIndexLabel(self):
		"""Configure SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureSIDIndexLabel')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DBit(self):
		"""When the IS-IS Router CAPABILITY TLV is leaked from level-2 to level-1, the D bit MUST be set, else it should be clear

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dBit')

	@property
	def DBitForSRv6Cap(self):
		"""When the IS-IS Router CAPABILITY TLV is leaked from level-2 to level-1, the D bit MUST be set, else it should be clear

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dBitForSRv6Cap')

	@property
	def DBitInsideSRv6SidTLV(self):
		"""When the SID is leaked from level-2 to level-1, the D bit MUST be set. Otherwise, this bit MUST be clear.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dBitInsideSRv6SidTLV')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DiscardLSPs(self):
		"""Discard LSPs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardLSPs')

	@property
	def Distribution(self):
		"""Distribution

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('distribution')

	@property
	def DomainAuthenticationType(self):
		"""Domain Authentication Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domainAuthenticationType')

	@property
	def DomainTransmitPasswordOrMD5Key(self):
		"""Domain Transmit Password / MD5-Key

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domainTransmitPasswordOrMD5Key')

	@property
	def EFlag(self):
		"""Explicit NULL flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlag')

	@property
	def EFlagOfSRv6CapTlv(self):
		"""If set, then router is able to apply T.Encap operation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlagOfSRv6CapTlv')

	@property
	def EnableBIER(self):
		"""Enable BIER

		Returns:
			bool
		"""
		return self._get_attribute('enableBIER')
	@EnableBIER.setter
	def EnableBIER(self, value):
		self._set_attribute('enableBIER', value)

	@property
	def EnableHelloPadding(self):
		"""Enable Hello Padding

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHelloPadding')

	@property
	def EnableHitlessRestart(self):
		"""Enable Hitless Restart

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHitlessRestart')

	@property
	def EnableHostName(self):
		"""Enable Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHostName')

	@property
	def EnableMTIPv6(self):
		"""Enable MT for IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableMTIPv6')

	@property
	def EnableMappingServer(self):
		"""This ensures whether the ISIS router will behave as a Segment Routing Mapping Server (SRMS) or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableMappingServer')

	@property
	def EnableSR(self):
		"""Enable Segment Routing

		Returns:
			bool
		"""
		return self._get_attribute('enableSR')
	@EnableSR.setter
	def EnableSR(self, value):
		self._set_attribute('enableSR', value)

	@property
	def EnableTE(self):
		"""Enable TE

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableTE')

	@property
	def EnableWMforTE(self):
		"""Hidden field is to disable wide Metric, when user disable TE Router conditionally

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableWMforTE')

	@property
	def EnableWideMetric(self):
		"""Enable Wide Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableWideMetric')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def Funcflags(self):
		"""This is the function flags

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('funcflags')

	@property
	def Function(self):
		"""This specifies endpoint function codes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('function')

	@property
	def HitlessRestartMode(self):
		"""Restart Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hitlessRestartMode')

	@property
	def HitlessRestartTime(self):
		"""Restart Time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hitlessRestartTime')

	@property
	def HitlessRestartVersion(self):
		"""Restart Version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hitlessRestartVersion')

	@property
	def HostName(self):
		"""Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostName')

	@property
	def IgnoreReceiveMD5(self):
		"""Ignore Receive MD5

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignoreReceiveMD5')

	@property
	def IncludeMaximumEndDSrhTLV(self):
		"""If set, then include Maximum End D SRH TLV in SRv6 capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMaximumEndDSrhTLV')

	@property
	def IncludeMaximumEndPopSrhTLV(self):
		"""If set, then include Max-End-Pop-SRH TLV in SRv6 capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMaximumEndPopSrhTLV')

	@property
	def IncludeMaximumSLTLV(self):
		"""If set, then include Maximum SL TLV in SRv6 capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMaximumSLTLV')

	@property
	def IncludeMaximumTEncapSrhTLV(self):
		"""If set, then include Maximum T.Encap SRH TLV in SRv6 capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMaximumTEncapSrhTLV')

	@property
	def IncludeMaximumTInsertSrhTLV(self):
		"""If set, then include Maximum T.Insert SRH TLV in SRv6 capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMaximumTInsertSrhTLV')

	@property
	def IncludePrefixAttrFlags(self):
		"""Include Prefix Attributes Flags

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includePrefixAttrFlags')

	@property
	def InterLSPsOrMGroupPDUBurstGap(self):
		"""Inter LSPs/MGROUP-PDUs Burst Gap (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interLSPsOrMGroupPDUBurstGap')

	@property
	def Ipv4Flag(self):
		"""If set, then the router is capable of processing SR MPLS encapsulated IPv4 packets on all interfaces.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Flag')

	@property
	def Ipv6Flag(self):
		"""If set, then the router is capable of processing SR MPLS encapsulated IPv6 packets on all interfaces.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Flag')

	@property
	def Ipv6NodePrefix(self):
		"""IPv6 Node SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6NodePrefix')

	@property
	def Ipv6Srh(self):
		"""This is the SR-IPv6 flag. If set to true, then this enables the SRv6 capability on the router If set to false, then this enables the MPLS SR capability on the router

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Srh')

	@property
	def LFlag(self):
		"""Local Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def LSPLifetime(self):
		"""LSP Rifetime (sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPLifetime')

	@property
	def LSPRefreshRate(self):
		"""LSP Refresh Rate (sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPRefreshRate')

	@property
	def LSPorMGroupPDUMinTransmissionInterval(self):
		"""LSP/MGROUP-PDU Min Transmission Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPorMGroupPDUMinTransmissionInterval')

	@property
	def LocalSystemID(self):
		"""System ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localSystemID')

	@property
	def LocatorPrefixLength(self):
		"""Locator Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('locatorPrefixLength')

	@property
	def Mask(self):
		"""Mask

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mask')

	@property
	def MaxAreaAddresses(self):
		"""Maximum Area Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxAreaAddresses')

	@property
	def MaxEndD(self):
		"""This field specifies the maximum number of SIDs in an SRH when applying End.DX6 and End.DT6 functions. If this field is zero, then the router cannot apply End.DX6 or End.DT6 functions if the extension header right underneath the outer IPv6 header is an SRH.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxEndD')

	@property
	def MaxEndPopSrh(self):
		"""This field specifies the maximum number of SIDs in the top SRH in an SRH stack that the router can apply PSP or USP flavors to. If the value of this field is zero, then the router cannot apply PSP or USP flavors.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxEndPopSrh')

	@property
	def MaxLSPSize(self):
		"""Max LSP Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLSPSize')

	@property
	def MaxLSPsOrMGroupPDUsPerBurst(self):
		"""Max LSPs/MGROUP-PDUs Per Burst

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLSPsOrMGroupPDUsPerBurst')

	@property
	def MaxSL(self):
		"""This field specifies the maximum value of the Segments Left (SL) field in the SRH of a received packet before applying the function associated with a SID.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxSL')

	@property
	def MaxTEncap(self):
		"""This field specifies the maximum number of SIDs that can be included as part of the T.Encap behavior. If this field is zero and the E flag is set, then the router can apply T.Encap by encapsulating the incoming packet in another IPv6 header without SRH the same way IPinIP encapsulation is performed. If the E flag is clear, then this field SHOULD be transmitted as zero and MUST be ignored on receipt.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxTEncap')

	@property
	def MaxTInsert(self):
		"""This field specifies the maximum number of SIDs that can be inserted as part of the T.insert behavior. If the value of this field is zero, then the router cannot apply any variation of the T.insert behavior.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxTInsert')

	@property
	def NFlag(self):
		"""Nodal prefix flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nFlag')

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
	def NoOfBIERSubDomains(self):
		"""Number of BIER Sub Domains

		Returns:
			number
		"""
		return self._get_attribute('noOfBIERSubDomains')
	@NoOfBIERSubDomains.setter
	def NoOfBIERSubDomains(self, value):
		self._set_attribute('noOfBIERSubDomains', value)

	@property
	def NoOfSRTunnels(self):
		"""Number of MPLS SR Tunnels

		Returns:
			number
		"""
		return self._get_attribute('noOfSRTunnels')
	@NoOfSRTunnels.setter
	def NoOfSRTunnels(self, value):
		self._set_attribute('noOfSRTunnels', value)

	@property
	def NodePrefix(self):
		"""Node Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodePrefix')

	@property
	def NumberOfMappingIPV4Ranges(self):
		"""Specifies the number of IPv4 mappings or range TLVs that each router in a DG can advertise.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMappingIPV4Ranges')
	@NumberOfMappingIPV4Ranges.setter
	def NumberOfMappingIPV4Ranges(self, value):
		self._set_attribute('numberOfMappingIPV4Ranges', value)

	@property
	def NumberOfMappingIPV6Ranges(self):
		"""Specifies the number of IPv6 mappings or range TLVs that each router in a DG can advertise.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMappingIPV6Ranges')
	@NumberOfMappingIPV6Ranges.setter
	def NumberOfMappingIPV6Ranges(self, value):
		self._set_attribute('numberOfMappingIPV6Ranges', value)

	@property
	def OFlagOfSRv6CapTlv(self):
		"""If set, it indicates that this packet is an operations and management (OAM) packet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('oFlagOfSRv6CapTlv')

	@property
	def Overloaded(self):
		"""Overloaded

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overloaded')

	@property
	def PFlag(self):
		"""No-PHP flag. If set, then the penultimate hop MUST NOT pop the Prefix-SID before delivering the packet to the node that advertised the Prefix-SID.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlag')

	@property
	def PSNPInterval(self):
		"""PSNP Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pSNPInterval')

	@property
	def PartitionRepair(self):
		"""Partition Repair

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('partitionRepair')

	@property
	def PrefixAdvertisementType(self):
		"""Prefix Advertisement Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixAdvertisementType')

	@property
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def RFlag(self):
		"""Redistribution flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rFlag')

	@property
	def Redistribution(self):
		"""Redistribution

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redistribution')

	@property
	def RedistributionForSRv6(self):
		"""Redistribution

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redistributionForSRv6')

	@property
	def ReservedInsideFlagsOfSRv6SidTLV(self):
		"""This is the reserved field (part of flags field of SRv6 SID TLV)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reservedInsideFlagsOfSRv6SidTLV')

	@property
	def ReservedInsideSRv6CapFlag(self):
		"""This is the reserved field (as part of Flags field of SRv6 Capability TLV)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reservedInsideSRv6CapFlag')

	@property
	def RouteMetric(self):
		"""Route Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routeMetric')

	@property
	def RouteOrigin(self):
		"""Route Origin

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routeOrigin')

	@property
	def RtrcapId(self):
		"""Router Capability Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rtrcapId')

	@property
	def RtrcapIdForSrv6(self):
		"""Router Capability Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rtrcapIdForSrv6')

	@property
	def SBit(self):
		"""Enabling S bit lets the IS-IS Router CAPABILITY TLV to get flooded across the entire routing domain, otherwise the TLV not be leaked between levels

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sBit')

	@property
	def SBitForSRv6Cap(self):
		"""Enabling S bit lets the IS-IS Router CAPABILITY TLV to get flooded across the entire routing domain, otherwise the TLV not be leaked between levels

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sBitForSRv6Cap')

	@property
	def SIDIndexLabel(self):
		"""SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sIDIndexLabel')

	@property
	def SRAlgorithmCount(self):
		"""SR Algorithm Count

		Returns:
			number
		"""
		return self._get_attribute('sRAlgorithmCount')
	@SRAlgorithmCount.setter
	def SRAlgorithmCount(self, value):
		self._set_attribute('sRAlgorithmCount', value)

	@property
	def SRGBRangeCount(self):
		"""SRGB Range Count

		Returns:
			number
		"""
		return self._get_attribute('sRGBRangeCount')
	@SRGBRangeCount.setter
	def SRGBRangeCount(self, value):
		self._set_attribute('sRGBRangeCount', value)

	@property
	def SessionInfo(self):
		"""Logs additional information about the session Information

		Returns:
			list(str[noIfaceUp|up])
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
	def SrlbDescriptorCount(self):
		"""Count of the SRLB descriptor entries, each being a tuple having format {Start SID/Label, SID Count}

		Returns:
			number
		"""
		return self._get_attribute('srlbDescriptorCount')
	@SrlbDescriptorCount.setter
	def SrlbDescriptorCount(self, value):
		self._set_attribute('srlbDescriptorCount', value)

	@property
	def SrlbFlags(self):
		"""This specifies the value of the SRLB flags field

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srlbFlags')

	@property
	def SrmsPreference(self):
		"""This is used to associate a preference with SRMS advertisements and is being advertised as a sub-TLV in Router Capability TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srmsPreference')

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
	def TERouterId(self):
		"""TE Router ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tERouterId')

	@property
	def VFlag(self):
		"""Value Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

	def find(self, Count=None, DescriptiveName=None, EnableBIER=None, EnableSR=None, Errors=None, LocalSystemID=None, Name=None, NoOfBIERSubDomains=None, NoOfSRTunnels=None, NumberOfMappingIPV4Ranges=None, NumberOfMappingIPV6Ranges=None, SRAlgorithmCount=None, SRGBRangeCount=None, SessionInfo=None, SessionStatus=None, SrlbDescriptorCount=None, StateCounts=None, Status=None):
		"""Finds and retrieves isisL3Router data from the server.

		All named parameters support regex and can be used to selectively retrieve isisL3Router data from the server.
		By default the find method takes no parameters and will retrieve all isisL3Router data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableBIER (bool): Enable BIER
			EnableSR (bool): Enable Segment Routing
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			LocalSystemID (list(str)): System ID
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfBIERSubDomains (number): Number of BIER Sub Domains
			NoOfSRTunnels (number): Number of MPLS SR Tunnels
			NumberOfMappingIPV4Ranges (number): Specifies the number of IPv4 mappings or range TLVs that each router in a DG can advertise.
			NumberOfMappingIPV6Ranges (number): Specifies the number of IPv6 mappings or range TLVs that each router in a DG can advertise.
			SRAlgorithmCount (number): SR Algorithm Count
			SRGBRangeCount (number): SRGB Range Count
			SessionInfo (list(str[noIfaceUp|up])): Logs additional information about the session Information
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			SrlbDescriptorCount (number): Count of the SRLB descriptor entries, each being a tuple having format {Start SID/Label, SID Count}
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching isisL3Router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of isisL3Router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the isisL3Router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, BIERNodePrefix=None, Active=None, AdvertiseSRLB=None, AdvertiseSRMSPreference=None, AdvertiseSidAsLocator=None, Algorithm=None, AreaAddresses=None, AreaAuthenticationType=None, AreaTransmitPasswordOrMD5Key=None, Attached=None, BIERIPv6NodePrefix=None, BierNFlag=None, BierRFlag=None, CSNPInterval=None, ConfigureSIDIndexLabel=None, DBit=None, DBitForSRv6Cap=None, DBitInsideSRv6SidTLV=None, DiscardLSPs=None, Distribution=None, DomainAuthenticationType=None, DomainTransmitPasswordOrMD5Key=None, EFlag=None, EFlagOfSRv6CapTlv=None, EnableHelloPadding=None, EnableHitlessRestart=None, EnableHostName=None, EnableMTIPv6=None, EnableMappingServer=None, EnableTE=None, EnableWMforTE=None, EnableWideMetric=None, Funcflags=None, Function=None, HitlessRestartMode=None, HitlessRestartTime=None, HitlessRestartVersion=None, HostName=None, IgnoreReceiveMD5=None, IncludeMaximumEndDSrhTLV=None, IncludeMaximumEndPopSrhTLV=None, IncludeMaximumSLTLV=None, IncludeMaximumTEncapSrhTLV=None, IncludeMaximumTInsertSrhTLV=None, IncludePrefixAttrFlags=None, InterLSPsOrMGroupPDUBurstGap=None, Ipv4Flag=None, Ipv6Flag=None, Ipv6NodePrefix=None, Ipv6Srh=None, LFlag=None, LSPLifetime=None, LSPRefreshRate=None, LSPorMGroupPDUMinTransmissionInterval=None, LocatorPrefixLength=None, Mask=None, MaxAreaAddresses=None, MaxEndD=None, MaxEndPopSrh=None, MaxLSPSize=None, MaxLSPsOrMGroupPDUsPerBurst=None, MaxSL=None, MaxTEncap=None, MaxTInsert=None, NFlag=None, NodePrefix=None, OFlagOfSRv6CapTlv=None, Overloaded=None, PFlag=None, PSNPInterval=None, PartitionRepair=None, PrefixAdvertisementType=None, PrefixLength=None, RFlag=None, Redistribution=None, RedistributionForSRv6=None, ReservedInsideFlagsOfSRv6SidTLV=None, ReservedInsideSRv6CapFlag=None, RouteMetric=None, RouteOrigin=None, RtrcapId=None, RtrcapIdForSrv6=None, SBit=None, SBitForSRv6Cap=None, SIDIndexLabel=None, SrlbFlags=None, SrmsPreference=None, TERouterId=None, VFlag=None):
		"""Base class infrastructure that gets a list of isisL3Router device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BIERNodePrefix (str): optional regex of BIERNodePrefix
			Active (str): optional regex of active
			AdvertiseSRLB (str): optional regex of advertiseSRLB
			AdvertiseSRMSPreference (str): optional regex of advertiseSRMSPreference
			AdvertiseSidAsLocator (str): optional regex of advertiseSidAsLocator
			Algorithm (str): optional regex of algorithm
			AreaAddresses (str): optional regex of areaAddresses
			AreaAuthenticationType (str): optional regex of areaAuthenticationType
			AreaTransmitPasswordOrMD5Key (str): optional regex of areaTransmitPasswordOrMD5Key
			Attached (str): optional regex of attached
			BIERIPv6NodePrefix (str): optional regex of bIERIPv6NodePrefix
			BierNFlag (str): optional regex of bierNFlag
			BierRFlag (str): optional regex of bierRFlag
			CSNPInterval (str): optional regex of cSNPInterval
			ConfigureSIDIndexLabel (str): optional regex of configureSIDIndexLabel
			DBit (str): optional regex of dBit
			DBitForSRv6Cap (str): optional regex of dBitForSRv6Cap
			DBitInsideSRv6SidTLV (str): optional regex of dBitInsideSRv6SidTLV
			DiscardLSPs (str): optional regex of discardLSPs
			Distribution (str): optional regex of distribution
			DomainAuthenticationType (str): optional regex of domainAuthenticationType
			DomainTransmitPasswordOrMD5Key (str): optional regex of domainTransmitPasswordOrMD5Key
			EFlag (str): optional regex of eFlag
			EFlagOfSRv6CapTlv (str): optional regex of eFlagOfSRv6CapTlv
			EnableHelloPadding (str): optional regex of enableHelloPadding
			EnableHitlessRestart (str): optional regex of enableHitlessRestart
			EnableHostName (str): optional regex of enableHostName
			EnableMTIPv6 (str): optional regex of enableMTIPv6
			EnableMappingServer (str): optional regex of enableMappingServer
			EnableTE (str): optional regex of enableTE
			EnableWMforTE (str): optional regex of enableWMforTE
			EnableWideMetric (str): optional regex of enableWideMetric
			Funcflags (str): optional regex of funcflags
			Function (str): optional regex of function
			HitlessRestartMode (str): optional regex of hitlessRestartMode
			HitlessRestartTime (str): optional regex of hitlessRestartTime
			HitlessRestartVersion (str): optional regex of hitlessRestartVersion
			HostName (str): optional regex of hostName
			IgnoreReceiveMD5 (str): optional regex of ignoreReceiveMD5
			IncludeMaximumEndDSrhTLV (str): optional regex of includeMaximumEndDSrhTLV
			IncludeMaximumEndPopSrhTLV (str): optional regex of includeMaximumEndPopSrhTLV
			IncludeMaximumSLTLV (str): optional regex of includeMaximumSLTLV
			IncludeMaximumTEncapSrhTLV (str): optional regex of includeMaximumTEncapSrhTLV
			IncludeMaximumTInsertSrhTLV (str): optional regex of includeMaximumTInsertSrhTLV
			IncludePrefixAttrFlags (str): optional regex of includePrefixAttrFlags
			InterLSPsOrMGroupPDUBurstGap (str): optional regex of interLSPsOrMGroupPDUBurstGap
			Ipv4Flag (str): optional regex of ipv4Flag
			Ipv6Flag (str): optional regex of ipv6Flag
			Ipv6NodePrefix (str): optional regex of ipv6NodePrefix
			Ipv6Srh (str): optional regex of ipv6Srh
			LFlag (str): optional regex of lFlag
			LSPLifetime (str): optional regex of lSPLifetime
			LSPRefreshRate (str): optional regex of lSPRefreshRate
			LSPorMGroupPDUMinTransmissionInterval (str): optional regex of lSPorMGroupPDUMinTransmissionInterval
			LocatorPrefixLength (str): optional regex of locatorPrefixLength
			Mask (str): optional regex of mask
			MaxAreaAddresses (str): optional regex of maxAreaAddresses
			MaxEndD (str): optional regex of maxEndD
			MaxEndPopSrh (str): optional regex of maxEndPopSrh
			MaxLSPSize (str): optional regex of maxLSPSize
			MaxLSPsOrMGroupPDUsPerBurst (str): optional regex of maxLSPsOrMGroupPDUsPerBurst
			MaxSL (str): optional regex of maxSL
			MaxTEncap (str): optional regex of maxTEncap
			MaxTInsert (str): optional regex of maxTInsert
			NFlag (str): optional regex of nFlag
			NodePrefix (str): optional regex of nodePrefix
			OFlagOfSRv6CapTlv (str): optional regex of oFlagOfSRv6CapTlv
			Overloaded (str): optional regex of overloaded
			PFlag (str): optional regex of pFlag
			PSNPInterval (str): optional regex of pSNPInterval
			PartitionRepair (str): optional regex of partitionRepair
			PrefixAdvertisementType (str): optional regex of prefixAdvertisementType
			PrefixLength (str): optional regex of prefixLength
			RFlag (str): optional regex of rFlag
			Redistribution (str): optional regex of redistribution
			RedistributionForSRv6 (str): optional regex of redistributionForSRv6
			ReservedInsideFlagsOfSRv6SidTLV (str): optional regex of reservedInsideFlagsOfSRv6SidTLV
			ReservedInsideSRv6CapFlag (str): optional regex of reservedInsideSRv6CapFlag
			RouteMetric (str): optional regex of routeMetric
			RouteOrigin (str): optional regex of routeOrigin
			RtrcapId (str): optional regex of rtrcapId
			RtrcapIdForSrv6 (str): optional regex of rtrcapIdForSrv6
			SBit (str): optional regex of sBit
			SBitForSRv6Cap (str): optional regex of sBitForSRv6Cap
			SIDIndexLabel (str): optional regex of sIDIndexLabel
			SrlbFlags (str): optional regex of srlbFlags
			SrmsPreference (str): optional regex of srmsPreference
			TERouterId (str): optional regex of tERouterId
			VFlag (str): optional regex of vFlag

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def IsisStartRouter(self):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStartRouter', payload=locals(), response_object=None)

	def IsisStartRouter(self, SessionIndices):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStartRouter', payload=locals(), response_object=None)

	def IsisStartRouter(self, SessionIndices):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStartRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStopRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, SessionIndices):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStopRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, SessionIndices):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStopRouter', payload=locals(), response_object=None)

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
