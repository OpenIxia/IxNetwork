
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


class Bridge(Base):
	"""The Bridge class encapsulates a user managed bridge node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bridge property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bridge'

	def __init__(self, parent):
		super(Bridge, self).__init__(parent)

	@property
	def Cist(self):
		"""An instance of the Cist class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.cist.Cist)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.cist import Cist
		return Cist(self)._select()

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.interface import Interface
		return Interface(self)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def Msti(self):
		"""An instance of the Msti class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.msti.Msti)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.msti import Msti
		return Msti(self)

	@property
	def Vlan(self):
		"""An instance of the Vlan class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.vlan.Vlan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.vlan import Vlan
		return Vlan(self)

	@property
	def AutoPickBridgeMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoPickBridgeMac')
	@AutoPickBridgeMac.setter
	def AutoPickBridgeMac(self, value):
		self._set_attribute('autoPickBridgeMac', value)

	@property
	def BridgeMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bridgeMac')
	@BridgeMac.setter
	def BridgeMac(self, value):
		self._set_attribute('bridgeMac', value)

	@property
	def BridgePriority(self):
		"""

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('bridgePriority')
	@BridgePriority.setter
	def BridgePriority(self, value):
		self._set_attribute('bridgePriority', value)

	@property
	def BridgeSystemId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bridgeSystemId')
	@BridgeSystemId.setter
	def BridgeSystemId(self, value):
		self._set_attribute('bridgeSystemId', value)

	@property
	def BridgeType(self):
		"""

		Returns:
			str(bridges|providerBridges)
		"""
		return self._get_attribute('bridgeType')
	@BridgeType.setter
	def BridgeType(self, value):
		self._set_attribute('bridgeType', value)

	@property
	def CistRegRootCost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cistRegRootCost')
	@CistRegRootCost.setter
	def CistRegRootCost(self, value):
		self._set_attribute('cistRegRootCost', value)

	@property
	def CistRegRootMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cistRegRootMac')
	@CistRegRootMac.setter
	def CistRegRootMac(self, value):
		self._set_attribute('cistRegRootMac', value)

	@property
	def CistRegRootPriority(self):
		"""

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('cistRegRootPriority')
	@CistRegRootPriority.setter
	def CistRegRootPriority(self, value):
		self._set_attribute('cistRegRootPriority', value)

	@property
	def CistRemainingHop(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cistRemainingHop')
	@CistRemainingHop.setter
	def CistRemainingHop(self, value):
		self._set_attribute('cistRemainingHop', value)

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
	def ExternalRootCost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('externalRootCost')
	@ExternalRootCost.setter
	def ExternalRootCost(self, value):
		self._set_attribute('externalRootCost', value)

	@property
	def ExternalRootMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('externalRootMac')
	@ExternalRootMac.setter
	def ExternalRootMac(self, value):
		self._set_attribute('externalRootMac', value)

	@property
	def ExternalRootPriority(self):
		"""

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('externalRootPriority')
	@ExternalRootPriority.setter
	def ExternalRootPriority(self, value):
		self._set_attribute('externalRootPriority', value)

	@property
	def ForwardDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('forwardDelay')
	@ForwardDelay.setter
	def ForwardDelay(self, value):
		self._set_attribute('forwardDelay', value)

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
	def IsRefreshComplete(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isRefreshComplete')

	@property
	def MaxAge(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxAge')
	@MaxAge.setter
	def MaxAge(self, value):
		self._set_attribute('maxAge', value)

	@property
	def MessageAge(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('messageAge')
	@MessageAge.setter
	def MessageAge(self, value):
		self._set_attribute('messageAge', value)

	@property
	def Mode(self):
		"""

		Returns:
			str(stp|rstp|mstp|pvst|rpvst|pvstp)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def MstcName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mstcName')
	@MstcName.setter
	def MstcName(self, value):
		self._set_attribute('mstcName', value)

	@property
	def MstcRevisionNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mstcRevisionNumber')
	@MstcRevisionNumber.setter
	def MstcRevisionNumber(self, value):
		self._set_attribute('mstcRevisionNumber', value)

	@property
	def PortPriority(self):
		"""

		Returns:
			str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)
		"""
		return self._get_attribute('portPriority')
	@PortPriority.setter
	def PortPriority(self, value):
		self._set_attribute('portPriority', value)

	@property
	def PvstpMode(self):
		"""

		Returns:
			str(stp|rstp)
		"""
		return self._get_attribute('pvstpMode')
	@PvstpMode.setter
	def PvstpMode(self, value):
		self._set_attribute('pvstpMode', value)

	@property
	def RootCost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rootCost')
	@RootCost.setter
	def RootCost(self, value):
		self._set_attribute('rootCost', value)

	@property
	def RootMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rootMac')
	@RootMac.setter
	def RootMac(self, value):
		self._set_attribute('rootMac', value)

	@property
	def RootPriority(self):
		"""

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('rootPriority')
	@RootPriority.setter
	def RootPriority(self, value):
		self._set_attribute('rootPriority', value)

	@property
	def RootSystemId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rootSystemId')
	@RootSystemId.setter
	def RootSystemId(self, value):
		self._set_attribute('rootSystemId', value)

	@property
	def UpdateRequired(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('updateRequired')
	@UpdateRequired.setter
	def UpdateRequired(self, value):
		self._set_attribute('updateRequired', value)

	@property
	def VlanPortPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanPortPriority')
	@VlanPortPriority.setter
	def VlanPortPriority(self, value):
		self._set_attribute('vlanPortPriority', value)

	@property
	def VlanRootMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanRootMac')
	@VlanRootMac.setter
	def VlanRootMac(self, value):
		self._set_attribute('vlanRootMac', value)

	@property
	def VlanRootPathCost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanRootPathCost')
	@VlanRootPathCost.setter
	def VlanRootPathCost(self, value):
		self._set_attribute('vlanRootPathCost', value)

	@property
	def VlanRootPriority(self):
		"""

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('vlanRootPriority')
	@VlanRootPriority.setter
	def VlanRootPriority(self, value):
		self._set_attribute('vlanRootPriority', value)

	def add(self, AutoPickBridgeMac=None, BridgeMac=None, BridgePriority=None, BridgeSystemId=None, BridgeType=None, CistRegRootCost=None, CistRegRootMac=None, CistRegRootPriority=None, CistRemainingHop=None, Enabled=None, ExternalRootCost=None, ExternalRootMac=None, ExternalRootPriority=None, ForwardDelay=None, HelloInterval=None, MaxAge=None, MessageAge=None, Mode=None, MstcName=None, MstcRevisionNumber=None, PortPriority=None, PvstpMode=None, RootCost=None, RootMac=None, RootPriority=None, RootSystemId=None, UpdateRequired=None, VlanPortPriority=None, VlanRootMac=None, VlanRootPathCost=None, VlanRootPriority=None):
		"""Adds a new bridge node on the server and retrieves it in this instance.

		Args:
			AutoPickBridgeMac (bool): 
			BridgeMac (str): 
			BridgePriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			BridgeSystemId (number): 
			BridgeType (str(bridges|providerBridges)): 
			CistRegRootCost (number): 
			CistRegRootMac (str): 
			CistRegRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			CistRemainingHop (number): 
			Enabled (bool): 
			ExternalRootCost (number): 
			ExternalRootMac (str): 
			ExternalRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			ForwardDelay (number): 
			HelloInterval (number): 
			MaxAge (number): 
			MessageAge (number): 
			Mode (str(stp|rstp|mstp|pvst|rpvst|pvstp)): 
			MstcName (str): 
			MstcRevisionNumber (number): 
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): 
			PvstpMode (str(stp|rstp)): 
			RootCost (number): 
			RootMac (str): 
			RootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			RootSystemId (number): 
			UpdateRequired (number): 
			VlanPortPriority (number): 
			VlanRootMac (str): 
			VlanRootPathCost (number): 
			VlanRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 

		Returns:
			self: This instance with all currently retrieved bridge data using find and the newly added bridge data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bridge data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoPickBridgeMac=None, BridgeMac=None, BridgePriority=None, BridgeSystemId=None, BridgeType=None, CistRegRootCost=None, CistRegRootMac=None, CistRegRootPriority=None, CistRemainingHop=None, Enabled=None, ExternalRootCost=None, ExternalRootMac=None, ExternalRootPriority=None, ForwardDelay=None, HelloInterval=None, IsRefreshComplete=None, MaxAge=None, MessageAge=None, Mode=None, MstcName=None, MstcRevisionNumber=None, PortPriority=None, PvstpMode=None, RootCost=None, RootMac=None, RootPriority=None, RootSystemId=None, UpdateRequired=None, VlanPortPriority=None, VlanRootMac=None, VlanRootPathCost=None, VlanRootPriority=None):
		"""Finds and retrieves bridge data from the server.

		All named parameters support regex and can be used to selectively retrieve bridge data from the server.
		By default the find method takes no parameters and will retrieve all bridge data from the server.

		Args:
			AutoPickBridgeMac (bool): 
			BridgeMac (str): 
			BridgePriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			BridgeSystemId (number): 
			BridgeType (str(bridges|providerBridges)): 
			CistRegRootCost (number): 
			CistRegRootMac (str): 
			CistRegRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			CistRemainingHop (number): 
			Enabled (bool): 
			ExternalRootCost (number): 
			ExternalRootMac (str): 
			ExternalRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			ForwardDelay (number): 
			HelloInterval (number): 
			IsRefreshComplete (bool): 
			MaxAge (number): 
			MessageAge (number): 
			Mode (str(stp|rstp|mstp|pvst|rpvst|pvstp)): 
			MstcName (str): 
			MstcRevisionNumber (number): 
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): 
			PvstpMode (str(stp|rstp)): 
			RootCost (number): 
			RootMac (str): 
			RootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			RootSystemId (number): 
			UpdateRequired (number): 
			VlanPortPriority (number): 
			VlanRootMac (str): 
			VlanRootPathCost (number): 
			VlanRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 

		Returns:
			self: This instance with matching bridge data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bridge data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bridge data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def BridgeTopologyChange(self):
		"""Executes the bridgeTopologyChange operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('BridgeTopologyChange', payload=locals(), response_object=None)

	def CistTopologyChange(self):
		"""Executes the cistTopologyChange operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CistTopologyChange', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)

	def UpdateParameters(self):
		"""Executes the updateParameters operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
