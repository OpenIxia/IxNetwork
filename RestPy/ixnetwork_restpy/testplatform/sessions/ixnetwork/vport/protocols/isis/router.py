
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


class Router(Base):
	"""The Router class encapsulates a user managed router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'router'

	def __init__(self, parent):
		super(Router, self).__init__(parent)

	@property
	def CustomTlv(self):
		"""An instance of the CustomTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtlv.CustomTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtlv import CustomTlv
		return CustomTlv(self)

	@property
	def CustomTopology(self):
		"""An instance of the CustomTopology class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopology.CustomTopology)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopology import CustomTopology
		return CustomTopology(self)

	@property
	def DceMulticastIpv4GroupRange(self):
		"""An instance of the DceMulticastIpv4GroupRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv4grouprange.DceMulticastIpv4GroupRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv4grouprange import DceMulticastIpv4GroupRange
		return DceMulticastIpv4GroupRange(self)

	@property
	def DceMulticastIpv6GroupRange(self):
		"""An instance of the DceMulticastIpv6GroupRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv6grouprange.DceMulticastIpv6GroupRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv6grouprange import DceMulticastIpv6GroupRange
		return DceMulticastIpv6GroupRange(self)

	@property
	def DceMulticastMacRange(self):
		"""An instance of the DceMulticastMacRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastmacrange.DceMulticastMacRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastmacrange import DceMulticastMacRange
		return DceMulticastMacRange(self)

	@property
	def DceNetworkRange(self):
		"""An instance of the DceNetworkRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenetworkrange.DceNetworkRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenetworkrange import DceNetworkRange
		return DceNetworkRange(self)

	@property
	def DceTopologyRange(self):
		"""An instance of the DceTopologyRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcetopologyrange.DceTopologyRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcetopologyrange import DceTopologyRange
		return DceTopologyRange(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.interface import Interface
		return Interface(self)

	@property
	def LearnedInformation(self):
		"""An instance of the LearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.learnedinformation.LearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.learnedinformation import LearnedInformation
		return LearnedInformation(self)._select()

	@property
	def NetworkRange(self):
		"""An instance of the NetworkRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.networkrange.NetworkRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.networkrange import NetworkRange
		return NetworkRange(self)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.routerange import RouteRange
		return RouteRange(self)

	@property
	def SpbNetworkRange(self):
		"""An instance of the SpbNetworkRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbnetworkrange.SpbNetworkRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbnetworkrange import SpbNetworkRange
		return SpbNetworkRange(self)

	@property
	def SpbTopologyRange(self):
		"""An instance of the SpbTopologyRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbtopologyrange.SpbTopologyRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbtopologyrange import SpbTopologyRange
		return SpbTopologyRange(self)

	@property
	def TrillPingOam(self):
		"""An instance of the TrillPingOam class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillpingoam.TrillPingOam)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillpingoam import TrillPingOam
		return TrillPingOam(self)._select()

	@property
	def TrillUnicastMacRange(self):
		"""An instance of the TrillUnicastMacRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillunicastmacrange.TrillUnicastMacRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillunicastmacrange import TrillUnicastMacRange
		return TrillUnicastMacRange(self)

	@property
	def AreaAddressList(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('areaAddressList')
	@AreaAddressList.setter
	def AreaAddressList(self, value):
		self._set_attribute('areaAddressList', value)

	@property
	def AreaAuthType(self):
		"""

		Returns:
			str(none|password|md5)
		"""
		return self._get_attribute('areaAuthType')
	@AreaAuthType.setter
	def AreaAuthType(self, value):
		self._set_attribute('areaAuthType', value)

	@property
	def AreaReceivedPasswordList(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('areaReceivedPasswordList')
	@AreaReceivedPasswordList.setter
	def AreaReceivedPasswordList(self, value):
		self._set_attribute('areaReceivedPasswordList', value)

	@property
	def AreaTransmitPassword(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('areaTransmitPassword')
	@AreaTransmitPassword.setter
	def AreaTransmitPassword(self, value):
		self._set_attribute('areaTransmitPassword', value)

	@property
	def BroadcastRootPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('broadcastRootPriority')
	@BroadcastRootPriority.setter
	def BroadcastRootPriority(self, value):
		self._set_attribute('broadcastRootPriority', value)

	@property
	def CapabilityRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('capabilityRouterId')
	@CapabilityRouterId.setter
	def CapabilityRouterId(self, value):
		self._set_attribute('capabilityRouterId', value)

	@property
	def DeviceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('deviceId')
	@DeviceId.setter
	def DeviceId(self, value):
		self._set_attribute('deviceId', value)

	@property
	def DevicePriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('devicePriority')
	@DevicePriority.setter
	def DevicePriority(self, value):
		self._set_attribute('devicePriority', value)

	@property
	def DomainAuthType(self):
		"""

		Returns:
			str(none|password|md5)
		"""
		return self._get_attribute('domainAuthType')
	@DomainAuthType.setter
	def DomainAuthType(self, value):
		self._set_attribute('domainAuthType', value)

	@property
	def DomainReceivedPasswordList(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('domainReceivedPasswordList')
	@DomainReceivedPasswordList.setter
	def DomainReceivedPasswordList(self, value):
		self._set_attribute('domainReceivedPasswordList', value)

	@property
	def DomainTransmitPassword(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('domainTransmitPassword')
	@DomainTransmitPassword.setter
	def DomainTransmitPassword(self, value):
		self._set_attribute('domainTransmitPassword', value)

	@property
	def EnableAttached(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAttached')
	@EnableAttached.setter
	def EnableAttached(self, value):
		self._set_attribute('enableAttached', value)

	@property
	def EnableAutoLoopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoLoopback')
	@EnableAutoLoopback.setter
	def EnableAutoLoopback(self, value):
		self._set_attribute('enableAutoLoopback', value)

	@property
	def EnableDiscardLearnedLsps(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDiscardLearnedLsps')
	@EnableDiscardLearnedLsps.setter
	def EnableDiscardLearnedLsps(self, value):
		self._set_attribute('enableDiscardLearnedLsps', value)

	@property
	def EnableHelloPadding(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHelloPadding')
	@EnableHelloPadding.setter
	def EnableHelloPadding(self, value):
		self._set_attribute('enableHelloPadding', value)

	@property
	def EnableHitlessRestart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHitlessRestart')
	@EnableHitlessRestart.setter
	def EnableHitlessRestart(self, value):
		self._set_attribute('enableHitlessRestart', value)

	@property
	def EnableHostName(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHostName')
	@EnableHostName.setter
	def EnableHostName(self, value):
		self._set_attribute('enableHostName', value)

	@property
	def EnableIgnoreMtPortCapability(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIgnoreMtPortCapability')
	@EnableIgnoreMtPortCapability.setter
	def EnableIgnoreMtPortCapability(self, value):
		self._set_attribute('enableIgnoreMtPortCapability', value)

	@property
	def EnableIgnoreRecvMd5(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIgnoreRecvMd5')
	@EnableIgnoreRecvMd5.setter
	def EnableIgnoreRecvMd5(self, value):
		self._set_attribute('enableIgnoreRecvMd5', value)

	@property
	def EnableMtIpv6(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMtIpv6')
	@EnableMtIpv6.setter
	def EnableMtIpv6(self, value):
		self._set_attribute('enableMtIpv6', value)

	@property
	def EnableMtuProbe(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMtuProbe')
	@EnableMtuProbe.setter
	def EnableMtuProbe(self, value):
		self._set_attribute('enableMtuProbe', value)

	@property
	def EnableMultiTopology(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMultiTopology')
	@EnableMultiTopology.setter
	def EnableMultiTopology(self, value):
		self._set_attribute('enableMultiTopology', value)

	@property
	def EnableOverloaded(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOverloaded')
	@EnableOverloaded.setter
	def EnableOverloaded(self, value):
		self._set_attribute('enableOverloaded', value)

	@property
	def EnablePartitionRepair(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePartitionRepair')
	@EnablePartitionRepair.setter
	def EnablePartitionRepair(self, value):
		self._set_attribute('enablePartitionRepair', value)

	@property
	def EnableTrillOam(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableTrillOam')
	@EnableTrillOam.setter
	def EnableTrillOam(self, value):
		self._set_attribute('enableTrillOam', value)

	@property
	def EnableWideMetric(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableWideMetric')
	@EnableWideMetric.setter
	def EnableWideMetric(self, value):
		self._set_attribute('enableWideMetric', value)

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
	def FTagValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fTagValue')
	@FTagValue.setter
	def FTagValue(self, value):
		self._set_attribute('fTagValue', value)

	@property
	def FilterIpv4MulticastTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterIpv4MulticastTlvs')
	@FilterIpv4MulticastTlvs.setter
	def FilterIpv4MulticastTlvs(self, value):
		self._set_attribute('filterIpv4MulticastTlvs', value)

	@property
	def FilterIpv6MulticastTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterIpv6MulticastTlvs')
	@FilterIpv6MulticastTlvs.setter
	def FilterIpv6MulticastTlvs(self, value):
		self._set_attribute('filterIpv6MulticastTlvs', value)

	@property
	def FilterLearnedIpv4Prefixes(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedIpv4Prefixes')
	@FilterLearnedIpv4Prefixes.setter
	def FilterLearnedIpv4Prefixes(self, value):
		self._set_attribute('filterLearnedIpv4Prefixes', value)

	@property
	def FilterLearnedIpv6Prefixes(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedIpv6Prefixes')
	@FilterLearnedIpv6Prefixes.setter
	def FilterLearnedIpv6Prefixes(self, value):
		self._set_attribute('filterLearnedIpv6Prefixes', value)

	@property
	def FilterLearnedRbridges(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedRbridges')
	@FilterLearnedRbridges.setter
	def FilterLearnedRbridges(self, value):
		self._set_attribute('filterLearnedRbridges', value)

	@property
	def FilterLearnedSpbRbridges(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedSpbRbridges')
	@FilterLearnedSpbRbridges.setter
	def FilterLearnedSpbRbridges(self, value):
		self._set_attribute('filterLearnedSpbRbridges', value)

	@property
	def FilterLearnedTrillMacUnicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedTrillMacUnicast')
	@FilterLearnedTrillMacUnicast.setter
	def FilterLearnedTrillMacUnicast(self, value):
		self._set_attribute('filterLearnedTrillMacUnicast', value)

	@property
	def FilterMacMulticastTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('filterMacMulticastTlvs')
	@FilterMacMulticastTlvs.setter
	def FilterMacMulticastTlvs(self, value):
		self._set_attribute('filterMacMulticastTlvs', value)

	@property
	def HostName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostName')
	@HostName.setter
	def HostName(self, value):
		self._set_attribute('hostName', value)

	@property
	def InterLspMgroupPduBurstGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interLspMgroupPduBurstGap')
	@InterLspMgroupPduBurstGap.setter
	def InterLspMgroupPduBurstGap(self, value):
		self._set_attribute('interLspMgroupPduBurstGap', value)

	@property
	def LspLifeTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspLifeTime')
	@LspLifeTime.setter
	def LspLifeTime(self, value):
		self._set_attribute('lspLifeTime', value)

	@property
	def LspMaxSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspMaxSize')
	@LspMaxSize.setter
	def LspMaxSize(self, value):
		self._set_attribute('lspMaxSize', value)

	@property
	def LspMgroupPduMinTransmissionInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspMgroupPduMinTransmissionInterval')
	@LspMgroupPduMinTransmissionInterval.setter
	def LspMgroupPduMinTransmissionInterval(self, value):
		self._set_attribute('lspMgroupPduMinTransmissionInterval', value)

	@property
	def LspRefreshRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspRefreshRate')
	@LspRefreshRate.setter
	def LspRefreshRate(self, value):
		self._set_attribute('lspRefreshRate', value)

	@property
	def MaxAreaAddresses(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxAreaAddresses')
	@MaxAreaAddresses.setter
	def MaxAreaAddresses(self, value):
		self._set_attribute('maxAreaAddresses', value)

	@property
	def MaxLspMgroupPdusPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxLspMgroupPdusPerBurst')
	@MaxLspMgroupPdusPerBurst.setter
	def MaxLspMgroupPdusPerBurst(self, value):
		self._set_attribute('maxLspMgroupPdusPerBurst', value)

	@property
	def NumberOfMtuProbes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfMtuProbes')
	@NumberOfMtuProbes.setter
	def NumberOfMtuProbes(self, value):
		self._set_attribute('numberOfMtuProbes', value)

	@property
	def NumberOfMultiDestinationTrees(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfMultiDestinationTrees')
	@NumberOfMultiDestinationTrees.setter
	def NumberOfMultiDestinationTrees(self, value):
		self._set_attribute('numberOfMultiDestinationTrees', value)

	@property
	def OriginatingLspBufSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('originatingLspBufSize')
	@OriginatingLspBufSize.setter
	def OriginatingLspBufSize(self, value):
		self._set_attribute('originatingLspBufSize', value)

	@property
	def PsnpInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('psnpInterval')
	@PsnpInterval.setter
	def PsnpInterval(self, value):
		self._set_attribute('psnpInterval', value)

	@property
	def RestartMode(self):
		"""

		Returns:
			str(normalRouter|restartingRouter|startingRouter|helperRouter)
		"""
		return self._get_attribute('restartMode')
	@RestartMode.setter
	def RestartMode(self, value):
		self._set_attribute('restartMode', value)

	@property
	def RestartTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('restartTime')
	@RestartTime.setter
	def RestartTime(self, value):
		self._set_attribute('restartTime', value)

	@property
	def RestartVersion(self):
		"""

		Returns:
			str(version3|version4)
		"""
		return self._get_attribute('restartVersion')
	@RestartVersion.setter
	def RestartVersion(self, value):
		self._set_attribute('restartVersion', value)

	@property
	def StartFtagValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startFtagValue')
	@StartFtagValue.setter
	def StartFtagValue(self, value):
		self._set_attribute('startFtagValue', value)

	@property
	def SwitchId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchId')
	@SwitchId.setter
	def SwitchId(self, value):
		self._set_attribute('switchId', value)

	@property
	def SwitchIdPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchIdPriority')
	@SwitchIdPriority.setter
	def SwitchIdPriority(self, value):
		self._set_attribute('switchIdPriority', value)

	@property
	def SystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('systemId')
	@SystemId.setter
	def SystemId(self, value):
		self._set_attribute('systemId', value)

	@property
	def TeEnable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('teEnable')
	@TeEnable.setter
	def TeEnable(self, value):
		self._set_attribute('teEnable', value)

	@property
	def TeRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('teRouterId')
	@TeRouterId.setter
	def TeRouterId(self, value):
		self._set_attribute('teRouterId', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, AreaAddressList=None, AreaAuthType=None, AreaReceivedPasswordList=None, AreaTransmitPassword=None, BroadcastRootPriority=None, CapabilityRouterId=None, DeviceId=None, DevicePriority=None, DomainAuthType=None, DomainReceivedPasswordList=None, DomainTransmitPassword=None, EnableAttached=None, EnableAutoLoopback=None, EnableDiscardLearnedLsps=None, EnableHelloPadding=None, EnableHitlessRestart=None, EnableHostName=None, EnableIgnoreMtPortCapability=None, EnableIgnoreRecvMd5=None, EnableMtIpv6=None, EnableMtuProbe=None, EnableMultiTopology=None, EnableOverloaded=None, EnablePartitionRepair=None, EnableTrillOam=None, EnableWideMetric=None, Enabled=None, FTagValue=None, FilterIpv4MulticastTlvs=None, FilterIpv6MulticastTlvs=None, FilterLearnedIpv4Prefixes=None, FilterLearnedIpv6Prefixes=None, FilterLearnedRbridges=None, FilterLearnedSpbRbridges=None, FilterLearnedTrillMacUnicast=None, FilterMacMulticastTlvs=None, HostName=None, InterLspMgroupPduBurstGap=None, LspLifeTime=None, LspMaxSize=None, LspMgroupPduMinTransmissionInterval=None, LspRefreshRate=None, MaxAreaAddresses=None, MaxLspMgroupPdusPerBurst=None, NumberOfMtuProbes=None, NumberOfMultiDestinationTrees=None, OriginatingLspBufSize=None, PsnpInterval=None, RestartMode=None, RestartTime=None, RestartVersion=None, StartFtagValue=None, SwitchId=None, SwitchIdPriority=None, SystemId=None, TeEnable=None, TeRouterId=None, TrafficGroupId=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			AreaAddressList (list(str)): 
			AreaAuthType (str(none|password|md5)): 
			AreaReceivedPasswordList (list(str)): 
			AreaTransmitPassword (str): 
			BroadcastRootPriority (number): 
			CapabilityRouterId (str): 
			DeviceId (number): 
			DevicePriority (number): 
			DomainAuthType (str(none|password|md5)): 
			DomainReceivedPasswordList (list(str)): 
			DomainTransmitPassword (str): 
			EnableAttached (bool): 
			EnableAutoLoopback (bool): 
			EnableDiscardLearnedLsps (bool): 
			EnableHelloPadding (bool): 
			EnableHitlessRestart (bool): 
			EnableHostName (bool): 
			EnableIgnoreMtPortCapability (bool): 
			EnableIgnoreRecvMd5 (bool): 
			EnableMtIpv6 (bool): 
			EnableMtuProbe (bool): 
			EnableMultiTopology (bool): 
			EnableOverloaded (bool): 
			EnablePartitionRepair (bool): 
			EnableTrillOam (bool): 
			EnableWideMetric (bool): 
			Enabled (bool): 
			FTagValue (number): 
			FilterIpv4MulticastTlvs (bool): 
			FilterIpv6MulticastTlvs (bool): 
			FilterLearnedIpv4Prefixes (bool): 
			FilterLearnedIpv6Prefixes (bool): 
			FilterLearnedRbridges (bool): 
			FilterLearnedSpbRbridges (bool): 
			FilterLearnedTrillMacUnicast (bool): 
			FilterMacMulticastTlvs (bool): 
			HostName (str): 
			InterLspMgroupPduBurstGap (number): 
			LspLifeTime (number): 
			LspMaxSize (number): 
			LspMgroupPduMinTransmissionInterval (number): 
			LspRefreshRate (number): 
			MaxAreaAddresses (number): 
			MaxLspMgroupPdusPerBurst (number): 
			NumberOfMtuProbes (number): 
			NumberOfMultiDestinationTrees (number): 
			OriginatingLspBufSize (number): 
			PsnpInterval (number): 
			RestartMode (str(normalRouter|restartingRouter|startingRouter|helperRouter)): 
			RestartTime (number): 
			RestartVersion (str(version3|version4)): 
			StartFtagValue (number): 
			SwitchId (number): 
			SwitchIdPriority (number): 
			SystemId (str): 
			TeEnable (bool): 
			TeRouterId (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the router data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AreaAddressList=None, AreaAuthType=None, AreaReceivedPasswordList=None, AreaTransmitPassword=None, BroadcastRootPriority=None, CapabilityRouterId=None, DeviceId=None, DevicePriority=None, DomainAuthType=None, DomainReceivedPasswordList=None, DomainTransmitPassword=None, EnableAttached=None, EnableAutoLoopback=None, EnableDiscardLearnedLsps=None, EnableHelloPadding=None, EnableHitlessRestart=None, EnableHostName=None, EnableIgnoreMtPortCapability=None, EnableIgnoreRecvMd5=None, EnableMtIpv6=None, EnableMtuProbe=None, EnableMultiTopology=None, EnableOverloaded=None, EnablePartitionRepair=None, EnableTrillOam=None, EnableWideMetric=None, Enabled=None, FTagValue=None, FilterIpv4MulticastTlvs=None, FilterIpv6MulticastTlvs=None, FilterLearnedIpv4Prefixes=None, FilterLearnedIpv6Prefixes=None, FilterLearnedRbridges=None, FilterLearnedSpbRbridges=None, FilterLearnedTrillMacUnicast=None, FilterMacMulticastTlvs=None, HostName=None, InterLspMgroupPduBurstGap=None, LspLifeTime=None, LspMaxSize=None, LspMgroupPduMinTransmissionInterval=None, LspRefreshRate=None, MaxAreaAddresses=None, MaxLspMgroupPdusPerBurst=None, NumberOfMtuProbes=None, NumberOfMultiDestinationTrees=None, OriginatingLspBufSize=None, PsnpInterval=None, RestartMode=None, RestartTime=None, RestartVersion=None, StartFtagValue=None, SwitchId=None, SwitchIdPriority=None, SystemId=None, TeEnable=None, TeRouterId=None, TrafficGroupId=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			AreaAddressList (list(str)): 
			AreaAuthType (str(none|password|md5)): 
			AreaReceivedPasswordList (list(str)): 
			AreaTransmitPassword (str): 
			BroadcastRootPriority (number): 
			CapabilityRouterId (str): 
			DeviceId (number): 
			DevicePriority (number): 
			DomainAuthType (str(none|password|md5)): 
			DomainReceivedPasswordList (list(str)): 
			DomainTransmitPassword (str): 
			EnableAttached (bool): 
			EnableAutoLoopback (bool): 
			EnableDiscardLearnedLsps (bool): 
			EnableHelloPadding (bool): 
			EnableHitlessRestart (bool): 
			EnableHostName (bool): 
			EnableIgnoreMtPortCapability (bool): 
			EnableIgnoreRecvMd5 (bool): 
			EnableMtIpv6 (bool): 
			EnableMtuProbe (bool): 
			EnableMultiTopology (bool): 
			EnableOverloaded (bool): 
			EnablePartitionRepair (bool): 
			EnableTrillOam (bool): 
			EnableWideMetric (bool): 
			Enabled (bool): 
			FTagValue (number): 
			FilterIpv4MulticastTlvs (bool): 
			FilterIpv6MulticastTlvs (bool): 
			FilterLearnedIpv4Prefixes (bool): 
			FilterLearnedIpv6Prefixes (bool): 
			FilterLearnedRbridges (bool): 
			FilterLearnedSpbRbridges (bool): 
			FilterLearnedTrillMacUnicast (bool): 
			FilterMacMulticastTlvs (bool): 
			HostName (str): 
			InterLspMgroupPduBurstGap (number): 
			LspLifeTime (number): 
			LspMaxSize (number): 
			LspMgroupPduMinTransmissionInterval (number): 
			LspRefreshRate (number): 
			MaxAreaAddresses (number): 
			MaxLspMgroupPdusPerBurst (number): 
			NumberOfMtuProbes (number): 
			NumberOfMultiDestinationTrees (number): 
			OriginatingLspBufSize (number): 
			PsnpInterval (number): 
			RestartMode (str(normalRouter|restartingRouter|startingRouter|helperRouter)): 
			RestartTime (number): 
			RestartVersion (str(version3|version4)): 
			StartFtagValue (number): 
			SwitchId (number): 
			SwitchIdPriority (number): 
			SystemId (str): 
			TeEnable (bool): 
			TeRouterId (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with matching router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshLearnedInformation(self):
		"""Executes the refreshLearnedInformation operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInformation', payload=locals(), response_object=None)

	def SendTrillOamPing(self):
		"""Executes the sendTrillOamPing operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendTrillOamPing', payload=locals(), response_object=None)
