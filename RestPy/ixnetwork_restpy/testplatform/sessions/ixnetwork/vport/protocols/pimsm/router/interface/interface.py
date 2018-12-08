
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
	def CrpRange(self):
		"""An instance of the CrpRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.crprange.crprange.CrpRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.crprange.crprange import CrpRange
		return CrpRange(self)

	@property
	def DataMdt(self):
		"""An instance of the DataMdt class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.datamdt.datamdt.DataMdt)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.datamdt.datamdt import DataMdt
		return DataMdt(self)

	@property
	def JoinPrune(self):
		"""An instance of the JoinPrune class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.joinprune.JoinPrune)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.joinprune import JoinPrune
		return JoinPrune(self)

	@property
	def LearnedBsrInfo(self):
		"""An instance of the LearnedBsrInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedbsrinfo.learnedbsrinfo.LearnedBsrInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedbsrinfo.learnedbsrinfo import LearnedBsrInfo
		return LearnedBsrInfo(self)

	@property
	def LearnedCrpInfo(self):
		"""An instance of the LearnedCrpInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedcrpinfo.learnedcrpinfo.LearnedCrpInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedcrpinfo.learnedcrpinfo import LearnedCrpInfo
		return LearnedCrpInfo(self)

	@property
	def LearnedMdtInfo(self):
		"""An instance of the LearnedMdtInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedmdtinfo.learnedmdtinfo.LearnedMdtInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedmdtinfo.learnedmdtinfo import LearnedMdtInfo
		return LearnedMdtInfo(self)

	@property
	def Source(self):
		"""An instance of the Source class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.source.source.Source)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.source.source import Source
		return Source(self)

	@property
	def AddressFamily(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('addressFamily')
	@AddressFamily.setter
	def AddressFamily(self, value):
		self._set_attribute('addressFamily', value)

	@property
	def AutoPickUpstreamNeighbor(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoPickUpstreamNeighbor')
	@AutoPickUpstreamNeighbor.setter
	def AutoPickUpstreamNeighbor(self, value):
		self._set_attribute('autoPickUpstreamNeighbor', value)

	@property
	def BootstrapEnable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('bootstrapEnable')
	@BootstrapEnable.setter
	def BootstrapEnable(self, value):
		self._set_attribute('bootstrapEnable', value)

	@property
	def BootstrapHashMaskLen(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bootstrapHashMaskLen')
	@BootstrapHashMaskLen.setter
	def BootstrapHashMaskLen(self, value):
		self._set_attribute('bootstrapHashMaskLen', value)

	@property
	def BootstrapInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bootstrapInterval')
	@BootstrapInterval.setter
	def BootstrapInterval(self, value):
		self._set_attribute('bootstrapInterval', value)

	@property
	def BootstrapPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bootstrapPriority')
	@BootstrapPriority.setter
	def BootstrapPriority(self, value):
		self._set_attribute('bootstrapPriority', value)

	@property
	def BootstrapTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bootstrapTimeout')
	@BootstrapTimeout.setter
	def BootstrapTimeout(self, value):
		self._set_attribute('bootstrapTimeout', value)

	@property
	def DisableTriggeredHello(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('disableTriggeredHello')
	@DisableTriggeredHello.setter
	def DisableTriggeredHello(self, value):
		self._set_attribute('disableTriggeredHello', value)

	@property
	def DiscardDataMdtTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardDataMdtTlv')
	@DiscardDataMdtTlv.setter
	def DiscardDataMdtTlv(self, value):
		self._set_attribute('discardDataMdtTlv', value)

	@property
	def DiscardLearnedRpInfo(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedRpInfo')
	@DiscardLearnedRpInfo.setter
	def DiscardLearnedRpInfo(self, value):
		self._set_attribute('discardLearnedRpInfo', value)

	@property
	def EnableBfdRegistration(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableV4MappedV6Address(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableV4MappedV6Address')
	@EnableV4MappedV6Address.setter
	def EnableV4MappedV6Address(self, value):
		self._set_attribute('enableV4MappedV6Address', value)

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
	def ForceSemanticFragmentation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('forceSemanticFragmentation')
	@ForceSemanticFragmentation.setter
	def ForceSemanticFragmentation(self, value):
		self._set_attribute('forceSemanticFragmentation', value)

	@property
	def GenerationIdMode(self):
		"""

		Returns:
			str(incremental|random|constant)
		"""
		return self._get_attribute('generationIdMode')
	@GenerationIdMode.setter
	def GenerationIdMode(self, value):
		self._set_attribute('generationIdMode', value)

	@property
	def HelloHoldTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('helloHoldTime')
	@HelloHoldTime.setter
	def HelloHoldTime(self, value):
		self._set_attribute('helloHoldTime', value)

	@property
	def HelloInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def InterfaceId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def IsRefreshRpSetComplete(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isRefreshRpSetComplete')

	@property
	def LanPruneDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lanPruneDelay')
	@LanPruneDelay.setter
	def LanPruneDelay(self, value):
		self._set_attribute('lanPruneDelay', value)

	@property
	def LanPruneDelayTBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('lanPruneDelayTBit')
	@LanPruneDelayTBit.setter
	def LanPruneDelayTBit(self, value):
		self._set_attribute('lanPruneDelayTBit', value)

	@property
	def LearnSelectedRpSet(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('learnSelectedRpSet')
	@LearnSelectedRpSet.setter
	def LearnSelectedRpSet(self, value):
		self._set_attribute('learnSelectedRpSet', value)

	@property
	def OverrideInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('overrideInterval')
	@OverrideInterval.setter
	def OverrideInterval(self, value):
		self._set_attribute('overrideInterval', value)

	@property
	def SendBiDirCapableOption(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendBiDirCapableOption')
	@SendBiDirCapableOption.setter
	def SendBiDirCapableOption(self, value):
		self._set_attribute('sendBiDirCapableOption', value)

	@property
	def SendGenIdOption(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendGenIdOption')
	@SendGenIdOption.setter
	def SendGenIdOption(self, value):
		self._set_attribute('sendGenIdOption', value)

	@property
	def SendHelloLanPruneDelayOption(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendHelloLanPruneDelayOption')
	@SendHelloLanPruneDelayOption.setter
	def SendHelloLanPruneDelayOption(self, value):
		self._set_attribute('sendHelloLanPruneDelayOption', value)

	@property
	def ShowSelectedRpSetOnly(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showSelectedRpSetOnly')
	@ShowSelectedRpSetOnly.setter
	def ShowSelectedRpSetOnly(self, value):
		self._set_attribute('showSelectedRpSetOnly', value)

	@property
	def SupportUnicastBootstrap(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportUnicastBootstrap')
	@SupportUnicastBootstrap.setter
	def SupportUnicastBootstrap(self, value):
		self._set_attribute('supportUnicastBootstrap', value)

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

	@property
	def TriggeredHelloDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('triggeredHelloDelay')
	@TriggeredHelloDelay.setter
	def TriggeredHelloDelay(self, value):
		self._set_attribute('triggeredHelloDelay', value)

	@property
	def UpstreamNeighbor(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('upstreamNeighbor')
	@UpstreamNeighbor.setter
	def UpstreamNeighbor(self, value):
		self._set_attribute('upstreamNeighbor', value)

	def add(self, AddressFamily=None, AutoPickUpstreamNeighbor=None, BootstrapEnable=None, BootstrapHashMaskLen=None, BootstrapInterval=None, BootstrapPriority=None, BootstrapTimeout=None, DisableTriggeredHello=None, DiscardDataMdtTlv=None, DiscardLearnedRpInfo=None, EnableBfdRegistration=None, EnableV4MappedV6Address=None, Enabled=None, ForceSemanticFragmentation=None, GenerationIdMode=None, HelloHoldTime=None, HelloInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, LanPruneDelay=None, LanPruneDelayTBit=None, LearnSelectedRpSet=None, OverrideInterval=None, SendBiDirCapableOption=None, SendGenIdOption=None, SendHelloLanPruneDelayOption=None, ShowSelectedRpSetOnly=None, SupportUnicastBootstrap=None, TrafficGroupId=None, TriggeredHelloDelay=None, UpstreamNeighbor=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AddressFamily (str(ipv4|ipv6)): 
			AutoPickUpstreamNeighbor (bool): 
			BootstrapEnable (bool): 
			BootstrapHashMaskLen (number): 
			BootstrapInterval (number): 
			BootstrapPriority (number): 
			BootstrapTimeout (number): 
			DisableTriggeredHello (bool): 
			DiscardDataMdtTlv (bool): 
			DiscardLearnedRpInfo (bool): 
			EnableBfdRegistration (bool): 
			EnableV4MappedV6Address (bool): 
			Enabled (bool): 
			ForceSemanticFragmentation (bool): 
			GenerationIdMode (str(incremental|random|constant)): 
			HelloHoldTime (number): 
			HelloInterval (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			LanPruneDelay (number): 
			LanPruneDelayTBit (bool): 
			LearnSelectedRpSet (bool): 
			OverrideInterval (number): 
			SendBiDirCapableOption (bool): 
			SendGenIdOption (bool): 
			SendHelloLanPruneDelayOption (bool): 
			ShowSelectedRpSetOnly (bool): 
			SupportUnicastBootstrap (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TriggeredHelloDelay (number): 
			UpstreamNeighbor (str): 

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

	def find(self, AddressFamily=None, AutoPickUpstreamNeighbor=None, BootstrapEnable=None, BootstrapHashMaskLen=None, BootstrapInterval=None, BootstrapPriority=None, BootstrapTimeout=None, DisableTriggeredHello=None, DiscardDataMdtTlv=None, DiscardLearnedRpInfo=None, EnableBfdRegistration=None, EnableV4MappedV6Address=None, Enabled=None, ForceSemanticFragmentation=None, GenerationIdMode=None, HelloHoldTime=None, HelloInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, IsRefreshRpSetComplete=None, LanPruneDelay=None, LanPruneDelayTBit=None, LearnSelectedRpSet=None, OverrideInterval=None, SendBiDirCapableOption=None, SendGenIdOption=None, SendHelloLanPruneDelayOption=None, ShowSelectedRpSetOnly=None, SupportUnicastBootstrap=None, TrafficGroupId=None, TriggeredHelloDelay=None, UpstreamNeighbor=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AddressFamily (str(ipv4|ipv6)): 
			AutoPickUpstreamNeighbor (bool): 
			BootstrapEnable (bool): 
			BootstrapHashMaskLen (number): 
			BootstrapInterval (number): 
			BootstrapPriority (number): 
			BootstrapTimeout (number): 
			DisableTriggeredHello (bool): 
			DiscardDataMdtTlv (bool): 
			DiscardLearnedRpInfo (bool): 
			EnableBfdRegistration (bool): 
			EnableV4MappedV6Address (bool): 
			Enabled (bool): 
			ForceSemanticFragmentation (bool): 
			GenerationIdMode (str(incremental|random|constant)): 
			HelloHoldTime (number): 
			HelloInterval (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IsRefreshRpSetComplete (bool): 
			LanPruneDelay (number): 
			LanPruneDelayTBit (bool): 
			LearnSelectedRpSet (bool): 
			OverrideInterval (number): 
			SendBiDirCapableOption (bool): 
			SendGenIdOption (bool): 
			SendHelloLanPruneDelayOption (bool): 
			ShowSelectedRpSetOnly (bool): 
			SupportUnicastBootstrap (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TriggeredHelloDelay (number): 
			UpstreamNeighbor (str): 

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

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def RefreshCrpBsrLearnedInfo(self):
		"""Executes the refreshCrpBsrLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshCrpBsrLearnedInfo', payload=locals(), response_object=None)
