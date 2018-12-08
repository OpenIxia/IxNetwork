
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
	def LearnedFilter(self):
		"""An instance of the LearnedFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedfilter.LearnedFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedfilter import LearnedFilter
		return LearnedFilter(self)._select()

	@property
	def LearnedLsa(self):
		"""An instance of the LearnedLsa class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedlsa.LearnedLsa)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedlsa import LearnedLsa
		return LearnedLsa(self)

	@property
	def AdvertiseNetworkRange(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('advertiseNetworkRange')
	@AdvertiseNetworkRange.setter
	def AdvertiseNetworkRange(self, value):
		self._set_attribute('advertiseNetworkRange', value)

	@property
	def AreaId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('areaId')
	@AreaId.setter
	def AreaId(self, value):
		self._set_attribute('areaId', value)

	@property
	def AuthenticationMethods(self):
		"""

		Returns:
			str(null|password|md5)
		"""
		return self._get_attribute('authenticationMethods')
	@AuthenticationMethods.setter
	def AuthenticationMethods(self, value):
		self._set_attribute('authenticationMethods', value)

	@property
	def AuthenticationPassword(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('authenticationPassword')
	@AuthenticationPassword.setter
	def AuthenticationPassword(self, value):
		self._set_attribute('authenticationPassword', value)

	@property
	def BBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('bBit')
	@BBit.setter
	def BBit(self, value):
		self._set_attribute('bBit', value)

	@property
	def ConnectedToDut(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('connectedToDut')
	@ConnectedToDut.setter
	def ConnectedToDut(self, value):
		self._set_attribute('connectedToDut', value)

	@property
	def DeadInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('deadInterval')
	@DeadInterval.setter
	def DeadInterval(self, value):
		self._set_attribute('deadInterval', value)

	@property
	def EBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('eBit')
	@EBit.setter
	def EBit(self, value):
		self._set_attribute('eBit', value)

	@property
	def EnableAdvertiseRouterLsaLoopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvertiseRouterLsaLoopback')
	@EnableAdvertiseRouterLsaLoopback.setter
	def EnableAdvertiseRouterLsaLoopback(self, value):
		self._set_attribute('enableAdvertiseRouterLsaLoopback', value)

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
	def EnableFastHello(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFastHello')
	@EnableFastHello.setter
	def EnableFastHello(self, value):
		self._set_attribute('enableFastHello', value)

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
	def EntryColumn(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('entryColumn')
	@EntryColumn.setter
	def EntryColumn(self, value):
		self._set_attribute('entryColumn', value)

	@property
	def EntryRow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

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
	def HelloMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('helloMultiplier')
	@HelloMultiplier.setter
	def HelloMultiplier(self, value):
		self._set_attribute('helloMultiplier', value)

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
	def InterfaceIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceIpAddress')
	@InterfaceIpAddress.setter
	def InterfaceIpAddress(self, value):
		self._set_attribute('interfaceIpAddress', value)

	@property
	def InterfaceIpMaskAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceIpMaskAddress')
	@InterfaceIpMaskAddress.setter
	def InterfaceIpMaskAddress(self, value):
		self._set_attribute('interfaceIpMaskAddress', value)

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
	def IsLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def LinkTypes(self):
		"""

		Returns:
			str(pointToPoint|transit|stub|virtual)
		"""
		return self._get_attribute('linkTypes')
	@LinkTypes.setter
	def LinkTypes(self, value):
		self._set_attribute('linkTypes', value)

	@property
	def Md5AuthenticationKey(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('md5AuthenticationKey')
	@Md5AuthenticationKey.setter
	def Md5AuthenticationKey(self, value):
		self._set_attribute('md5AuthenticationKey', value)

	@property
	def Md5AuthenticationKeyId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('md5AuthenticationKeyId')
	@Md5AuthenticationKeyId.setter
	def Md5AuthenticationKeyId(self, value):
		self._set_attribute('md5AuthenticationKeyId', value)

	@property
	def Metric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def Mtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def NeighborIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighborIpAddress')
	@NeighborIpAddress.setter
	def NeighborIpAddress(self, value):
		self._set_attribute('neighborIpAddress', value)

	@property
	def NeighborRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighborRouterId')
	@NeighborRouterId.setter
	def NeighborRouterId(self, value):
		self._set_attribute('neighborRouterId', value)

	@property
	def NetworkRangeIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkRangeIp')
	@NetworkRangeIp.setter
	def NetworkRangeIp(self, value):
		self._set_attribute('networkRangeIp', value)

	@property
	def NetworkRangeIpByMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('networkRangeIpByMask')
	@NetworkRangeIpByMask.setter
	def NetworkRangeIpByMask(self, value):
		self._set_attribute('networkRangeIpByMask', value)

	@property
	def NetworkRangeIpIncrementBy(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkRangeIpIncrementBy')
	@NetworkRangeIpIncrementBy.setter
	def NetworkRangeIpIncrementBy(self, value):
		self._set_attribute('networkRangeIpIncrementBy', value)

	@property
	def NetworkRangeIpMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('networkRangeIpMask')
	@NetworkRangeIpMask.setter
	def NetworkRangeIpMask(self, value):
		self._set_attribute('networkRangeIpMask', value)

	@property
	def NetworkRangeLinkType(self):
		"""

		Returns:
			str(broadcast|pointToPoint)
		"""
		return self._get_attribute('networkRangeLinkType')
	@NetworkRangeLinkType.setter
	def NetworkRangeLinkType(self, value):
		self._set_attribute('networkRangeLinkType', value)

	@property
	def NetworkRangeRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkRangeRouterId')
	@NetworkRangeRouterId.setter
	def NetworkRangeRouterId(self, value):
		self._set_attribute('networkRangeRouterId', value)

	@property
	def NetworkRangeRouterIdIncrementBy(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkRangeRouterIdIncrementBy')
	@NetworkRangeRouterIdIncrementBy.setter
	def NetworkRangeRouterIdIncrementBy(self, value):
		self._set_attribute('networkRangeRouterIdIncrementBy', value)

	@property
	def NetworkRangeTeEnable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('networkRangeTeEnable')
	@NetworkRangeTeEnable.setter
	def NetworkRangeTeEnable(self, value):
		self._set_attribute('networkRangeTeEnable', value)

	@property
	def NetworkRangeTeMaxBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('networkRangeTeMaxBandwidth')
	@NetworkRangeTeMaxBandwidth.setter
	def NetworkRangeTeMaxBandwidth(self, value):
		self._set_attribute('networkRangeTeMaxBandwidth', value)

	@property
	def NetworkRangeTeMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('networkRangeTeMetric')
	@NetworkRangeTeMetric.setter
	def NetworkRangeTeMetric(self, value):
		self._set_attribute('networkRangeTeMetric', value)

	@property
	def NetworkRangeTeResMaxBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('networkRangeTeResMaxBandwidth')
	@NetworkRangeTeResMaxBandwidth.setter
	def NetworkRangeTeResMaxBandwidth(self, value):
		self._set_attribute('networkRangeTeResMaxBandwidth', value)

	@property
	def NetworkRangeTeUnreservedBwPriority(self):
		"""

		Returns:
			dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)
		"""
		return self._get_attribute('networkRangeTeUnreservedBwPriority')
	@NetworkRangeTeUnreservedBwPriority.setter
	def NetworkRangeTeUnreservedBwPriority(self, value):
		self._set_attribute('networkRangeTeUnreservedBwPriority', value)

	@property
	def NetworkType(self):
		"""

		Returns:
			str(pointToPoint|broadcast|pointToMultipoint)
		"""
		return self._get_attribute('networkType')
	@NetworkType.setter
	def NetworkType(self, value):
		self._set_attribute('networkType', value)

	@property
	def NoOfCols(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfCols')
	@NoOfCols.setter
	def NoOfCols(self, value):
		self._set_attribute('noOfCols', value)

	@property
	def NoOfRows(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def Options(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('options')
	@Options.setter
	def Options(self, value):
		self._set_attribute('options', value)

	@property
	def Priority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def ProtocolInterface(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def ShowExternal(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showExternal')
	@ShowExternal.setter
	def ShowExternal(self, value):
		self._set_attribute('showExternal', value)

	@property
	def ShowNssa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showNssa')
	@ShowNssa.setter
	def ShowNssa(self, value):
		self._set_attribute('showNssa', value)

	@property
	def TeAdminGroup(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('teAdminGroup')
	@TeAdminGroup.setter
	def TeAdminGroup(self, value):
		self._set_attribute('teAdminGroup', value)

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
	def TeMaxBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('teMaxBandwidth')
	@TeMaxBandwidth.setter
	def TeMaxBandwidth(self, value):
		self._set_attribute('teMaxBandwidth', value)

	@property
	def TeMetricLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('teMetricLevel')
	@TeMetricLevel.setter
	def TeMetricLevel(self, value):
		self._set_attribute('teMetricLevel', value)

	@property
	def TeResMaxBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('teResMaxBandwidth')
	@TeResMaxBandwidth.setter
	def TeResMaxBandwidth(self, value):
		self._set_attribute('teResMaxBandwidth', value)

	@property
	def TeUnreservedBwPriority(self):
		"""

		Returns:
			dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)
		"""
		return self._get_attribute('teUnreservedBwPriority')
	@TeUnreservedBwPriority.setter
	def TeUnreservedBwPriority(self, value):
		self._set_attribute('teUnreservedBwPriority', value)

	@property
	def ValidateReceivedMtuSize(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('validateReceivedMtuSize')
	@ValidateReceivedMtuSize.setter
	def ValidateReceivedMtuSize(self, value):
		self._set_attribute('validateReceivedMtuSize', value)

	def add(self, AdvertiseNetworkRange=None, AreaId=None, AuthenticationMethods=None, AuthenticationPassword=None, BBit=None, ConnectedToDut=None, DeadInterval=None, EBit=None, EnableAdvertiseRouterLsaLoopback=None, EnableBfdRegistration=None, EnableFastHello=None, Enabled=None, EntryColumn=None, EntryRow=None, HelloInterval=None, HelloMultiplier=None, InterfaceIndex=None, InterfaceIpAddress=None, InterfaceIpMaskAddress=None, InterfaceType=None, Interfaces=None, LinkTypes=None, Md5AuthenticationKey=None, Md5AuthenticationKeyId=None, Metric=None, Mtu=None, NeighborIpAddress=None, NeighborRouterId=None, NetworkRangeIp=None, NetworkRangeIpByMask=None, NetworkRangeIpIncrementBy=None, NetworkRangeIpMask=None, NetworkRangeLinkType=None, NetworkRangeRouterId=None, NetworkRangeRouterIdIncrementBy=None, NetworkRangeTeEnable=None, NetworkRangeTeMaxBandwidth=None, NetworkRangeTeMetric=None, NetworkRangeTeResMaxBandwidth=None, NetworkRangeTeUnreservedBwPriority=None, NetworkType=None, NoOfCols=None, NoOfRows=None, Options=None, Priority=None, ProtocolInterface=None, ShowExternal=None, ShowNssa=None, TeAdminGroup=None, TeEnable=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None, ValidateReceivedMtuSize=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AdvertiseNetworkRange (bool): 
			AreaId (number): 
			AuthenticationMethods (str(null|password|md5)): 
			AuthenticationPassword (str): 
			BBit (bool): 
			ConnectedToDut (bool): 
			DeadInterval (number): 
			EBit (bool): 
			EnableAdvertiseRouterLsaLoopback (bool): 
			EnableBfdRegistration (bool): 
			EnableFastHello (bool): 
			Enabled (bool): 
			EntryColumn (number): 
			EntryRow (number): 
			HelloInterval (number): 
			HelloMultiplier (number): 
			InterfaceIndex (number): 
			InterfaceIpAddress (str): 
			InterfaceIpMaskAddress (str): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			LinkTypes (str(pointToPoint|transit|stub|virtual)): 
			Md5AuthenticationKey (str): 
			Md5AuthenticationKeyId (number): 
			Metric (number): 
			Mtu (number): 
			NeighborIpAddress (str): 
			NeighborRouterId (str): 
			NetworkRangeIp (str): 
			NetworkRangeIpByMask (bool): 
			NetworkRangeIpIncrementBy (str): 
			NetworkRangeIpMask (number): 
			NetworkRangeLinkType (str(broadcast|pointToPoint)): 
			NetworkRangeRouterId (str): 
			NetworkRangeRouterIdIncrementBy (str): 
			NetworkRangeTeEnable (bool): 
			NetworkRangeTeMaxBandwidth (number): 
			NetworkRangeTeMetric (number): 
			NetworkRangeTeResMaxBandwidth (number): 
			NetworkRangeTeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): 
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): 
			NoOfCols (number): 
			NoOfRows (number): 
			Options (number): 
			Priority (number): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			ShowExternal (bool): 
			ShowNssa (bool): 
			TeAdminGroup (str): 
			TeEnable (bool): 
			TeMaxBandwidth (number): 
			TeMetricLevel (number): 
			TeResMaxBandwidth (number): 
			TeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): 
			ValidateReceivedMtuSize (bool): 

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

	def find(self, AdvertiseNetworkRange=None, AreaId=None, AuthenticationMethods=None, AuthenticationPassword=None, BBit=None, ConnectedToDut=None, DeadInterval=None, EBit=None, EnableAdvertiseRouterLsaLoopback=None, EnableBfdRegistration=None, EnableFastHello=None, Enabled=None, EntryColumn=None, EntryRow=None, HelloInterval=None, HelloMultiplier=None, InterfaceIndex=None, InterfaceIpAddress=None, InterfaceIpMaskAddress=None, InterfaceType=None, Interfaces=None, IsLearnedInfoRefreshed=None, LinkTypes=None, Md5AuthenticationKey=None, Md5AuthenticationKeyId=None, Metric=None, Mtu=None, NeighborIpAddress=None, NeighborRouterId=None, NetworkRangeIp=None, NetworkRangeIpByMask=None, NetworkRangeIpIncrementBy=None, NetworkRangeIpMask=None, NetworkRangeLinkType=None, NetworkRangeRouterId=None, NetworkRangeRouterIdIncrementBy=None, NetworkRangeTeEnable=None, NetworkRangeTeMaxBandwidth=None, NetworkRangeTeMetric=None, NetworkRangeTeResMaxBandwidth=None, NetworkRangeTeUnreservedBwPriority=None, NetworkType=None, NoOfCols=None, NoOfRows=None, Options=None, Priority=None, ProtocolInterface=None, ShowExternal=None, ShowNssa=None, TeAdminGroup=None, TeEnable=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None, ValidateReceivedMtuSize=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AdvertiseNetworkRange (bool): 
			AreaId (number): 
			AuthenticationMethods (str(null|password|md5)): 
			AuthenticationPassword (str): 
			BBit (bool): 
			ConnectedToDut (bool): 
			DeadInterval (number): 
			EBit (bool): 
			EnableAdvertiseRouterLsaLoopback (bool): 
			EnableBfdRegistration (bool): 
			EnableFastHello (bool): 
			Enabled (bool): 
			EntryColumn (number): 
			EntryRow (number): 
			HelloInterval (number): 
			HelloMultiplier (number): 
			InterfaceIndex (number): 
			InterfaceIpAddress (str): 
			InterfaceIpMaskAddress (str): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IsLearnedInfoRefreshed (bool): 
			LinkTypes (str(pointToPoint|transit|stub|virtual)): 
			Md5AuthenticationKey (str): 
			Md5AuthenticationKeyId (number): 
			Metric (number): 
			Mtu (number): 
			NeighborIpAddress (str): 
			NeighborRouterId (str): 
			NetworkRangeIp (str): 
			NetworkRangeIpByMask (bool): 
			NetworkRangeIpIncrementBy (str): 
			NetworkRangeIpMask (number): 
			NetworkRangeLinkType (str(broadcast|pointToPoint)): 
			NetworkRangeRouterId (str): 
			NetworkRangeRouterIdIncrementBy (str): 
			NetworkRangeTeEnable (bool): 
			NetworkRangeTeMaxBandwidth (number): 
			NetworkRangeTeMetric (number): 
			NetworkRangeTeResMaxBandwidth (number): 
			NetworkRangeTeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): 
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): 
			NoOfCols (number): 
			NoOfRows (number): 
			Options (number): 
			Priority (number): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			ShowExternal (bool): 
			ShowNssa (bool): 
			TeAdminGroup (str): 
			TeEnable (bool): 
			TeMaxBandwidth (number): 
			TeMetricLevel (number): 
			TeResMaxBandwidth (number): 
			TeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): 
			ValidateReceivedMtuSize (bool): 

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

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
