
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


class OfChannel(Base):
	"""The OfChannel class encapsulates a user managed ofChannel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ofChannel'

	def __init__(self, parent):
		super(OfChannel, self).__init__(parent)

	@property
	def Capabilities(self):
		"""An instance of the Capabilities class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.capabilities.Capabilities)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.capabilities import Capabilities
		return Capabilities(self)._select()

	@property
	def ControllerTables(self):
		"""An instance of the ControllerTables class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllertables.ControllerTables)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllertables import ControllerTables
		return ControllerTables(self)

	@property
	def FlowRange(self):
		"""An instance of the FlowRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrange.FlowRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrange import FlowRange
		return FlowRange(self)

	@property
	def Group(self):
		"""An instance of the Group class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.group.Group)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.group import Group
		return Group(self)

	@property
	def Meter(self):
		"""An instance of the Meter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meter.Meter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meter import Meter
		return Meter(self)

	@property
	def SupportedActions(self):
		"""An instance of the SupportedActions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.supportedactions.SupportedActions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.supportedactions import SupportedActions
		return SupportedActions(self)._select()

	@property
	def SwitchPacketIn(self):
		"""An instance of the SwitchPacketIn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchpacketin.SwitchPacketIn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchpacketin import SwitchPacketIn
		return SwitchPacketIn(self)

	@property
	def SwitchPorts(self):
		"""An instance of the SwitchPorts class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchports.SwitchPorts)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchports import SwitchPorts
		return SwitchPorts(self)

	@property
	def SwitchTables(self):
		"""An instance of the SwitchTables class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchtables.SwitchTables)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchtables import SwitchTables
		return SwitchTables(self)

	@property
	def CalculateFlows(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('calculateFlows')
	@CalculateFlows.setter
	def CalculateFlows(self, value):
		self._set_attribute('calculateFlows', value)

	@property
	def CalculatePacketInReplyDelay(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('calculatePacketInReplyDelay')
	@CalculatePacketInReplyDelay.setter
	def CalculatePacketInReplyDelay(self, value):
		self._set_attribute('calculatePacketInReplyDelay', value)

	@property
	def DataPathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')
	@DataPathId.setter
	def DataPathId(self, value):
		self._set_attribute('dataPathId', value)

	@property
	def DataPathIdInHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdInHex')
	@DataPathIdInHex.setter
	def DataPathIdInHex(self, value):
		self._set_attribute('dataPathIdInHex', value)

	@property
	def DatapathDescritpion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathDescritpion')
	@DatapathDescritpion.setter
	def DatapathDescritpion(self, value):
		self._set_attribute('datapathDescritpion', value)

	@property
	def Description(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def EnableCalculateFlowsPerSecondUsingBarrierReq(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCalculateFlowsPerSecondUsingBarrierReq')
	@EnableCalculateFlowsPerSecondUsingBarrierReq.setter
	def EnableCalculateFlowsPerSecondUsingBarrierReq(self, value):
		self._set_attribute('enableCalculateFlowsPerSecondUsingBarrierReq', value)

	@property
	def EnableHelloElement(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHelloElement')
	@EnableHelloElement.setter
	def EnableHelloElement(self, value):
		self._set_attribute('enableHelloElement', value)

	@property
	def EnableStartupEmptyTableFeatureRequest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableStartupEmptyTableFeatureRequest')
	@EnableStartupEmptyTableFeatureRequest.setter
	def EnableStartupEmptyTableFeatureRequest(self, value):
		self._set_attribute('enableStartupEmptyTableFeatureRequest', value)

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
	def FlowTxBurstSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowTxBurstSize')
	@FlowTxBurstSize.setter
	def FlowTxBurstSize(self, value):
		self._set_attribute('flowTxBurstSize', value)

	@property
	def HardwareDescription(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hardwareDescription')
	@HardwareDescription.setter
	def HardwareDescription(self, value):
		self._set_attribute('hardwareDescription', value)

	@property
	def InterFlowBurstGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interFlowBurstGap')
	@InterFlowBurstGap.setter
	def InterFlowBurstGap(self, value):
		self._set_attribute('interFlowBurstGap', value)

	@property
	def InterPacketInBurstGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interPacketInBurstGap')
	@InterPacketInBurstGap.setter
	def InterPacketInBurstGap(self, value):
		self._set_attribute('interPacketInBurstGap', value)

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def ManufacturerDescription(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('manufacturerDescription')
	@ManufacturerDescription.setter
	def ManufacturerDescription(self, value):
		self._set_attribute('manufacturerDescription', value)

	@property
	def MaximumNumberOfFlowsProcessed(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumNumberOfFlowsProcessed')
	@MaximumNumberOfFlowsProcessed.setter
	def MaximumNumberOfFlowsProcessed(self, value):
		self._set_attribute('maximumNumberOfFlowsProcessed', value)

	@property
	def MaximumPacketInBytes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumPacketInBytes')
	@MaximumPacketInBytes.setter
	def MaximumPacketInBytes(self, value):
		self._set_attribute('maximumPacketInBytes', value)

	@property
	def NumberOfBuffers(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfBuffers')
	@NumberOfBuffers.setter
	def NumberOfBuffers(self, value):
		self._set_attribute('numberOfBuffers', value)

	@property
	def PacketInReplyTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetInReplyTimeout')
	@PacketInReplyTimeout.setter
	def PacketInReplyTimeout(self, value):
		self._set_attribute('packetInReplyTimeout', value)

	@property
	def PacketInTxBurstSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetInTxBurstSize')
	@PacketInTxBurstSize.setter
	def PacketInTxBurstSize(self, value):
		self._set_attribute('packetInTxBurstSize', value)

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')
	@RemoteIp.setter
	def RemoteIp(self, value):
		self._set_attribute('remoteIp', value)

	@property
	def SerialNumber(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('serialNumber')
	@SerialNumber.setter
	def SerialNumber(self, value):
		self._set_attribute('serialNumber', value)

	@property
	def SoftwareDescription(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('softwareDescription')
	@SoftwareDescription.setter
	def SoftwareDescription(self, value):
		self._set_attribute('softwareDescription', value)

	@property
	def StartUpGenerationId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startUpGenerationId')
	@StartUpGenerationId.setter
	def StartUpGenerationId(self, value):
		self._set_attribute('startUpGenerationId', value)

	@property
	def StartUpRoleRequest(self):
		"""

		Returns:
			str(noRoleRequest|master|slave)
		"""
		return self._get_attribute('startUpRoleRequest')
	@StartUpRoleRequest.setter
	def StartUpRoleRequest(self, value):
		self._set_attribute('startUpRoleRequest', value)

	@property
	def StartupFeatureRequest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('startupFeatureRequest')
	@StartupFeatureRequest.setter
	def StartupFeatureRequest(self, value):
		self._set_attribute('startupFeatureRequest', value)

	@property
	def StoreFlows(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('storeFlows')
	@StoreFlows.setter
	def StoreFlows(self, value):
		self._set_attribute('storeFlows', value)

	@property
	def UseDataPathIdAsChannelIdentifier(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useDataPathIdAsChannelIdentifier')
	@UseDataPathIdAsChannelIdentifier.setter
	def UseDataPathIdAsChannelIdentifier(self, value):
		self._set_attribute('useDataPathIdAsChannelIdentifier', value)

	@property
	def UseDatapathId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useDatapathId')
	@UseDatapathId.setter
	def UseDatapathId(self, value):
		self._set_attribute('useDatapathId', value)

	def add(self, CalculateFlows=None, CalculatePacketInReplyDelay=None, DataPathId=None, DataPathIdInHex=None, DatapathDescritpion=None, Description=None, EnableCalculateFlowsPerSecondUsingBarrierReq=None, EnableHelloElement=None, EnableStartupEmptyTableFeatureRequest=None, Enabled=None, FlowTxBurstSize=None, HardwareDescription=None, InterFlowBurstGap=None, InterPacketInBurstGap=None, ManufacturerDescription=None, MaximumNumberOfFlowsProcessed=None, MaximumPacketInBytes=None, NumberOfBuffers=None, PacketInReplyTimeout=None, PacketInTxBurstSize=None, RemoteIp=None, SerialNumber=None, SoftwareDescription=None, StartUpGenerationId=None, StartUpRoleRequest=None, StartupFeatureRequest=None, StoreFlows=None, UseDataPathIdAsChannelIdentifier=None, UseDatapathId=None):
		"""Adds a new ofChannel node on the server and retrieves it in this instance.

		Args:
			CalculateFlows (bool): 
			CalculatePacketInReplyDelay (bool): 
			DataPathId (str): 
			DataPathIdInHex (str): 
			DatapathDescritpion (str): 
			Description (str): 
			EnableCalculateFlowsPerSecondUsingBarrierReq (bool): 
			EnableHelloElement (bool): 
			EnableStartupEmptyTableFeatureRequest (bool): 
			Enabled (bool): 
			FlowTxBurstSize (number): 
			HardwareDescription (str): 
			InterFlowBurstGap (number): 
			InterPacketInBurstGap (number): 
			ManufacturerDescription (str): 
			MaximumNumberOfFlowsProcessed (number): 
			MaximumPacketInBytes (number): 
			NumberOfBuffers (number): 
			PacketInReplyTimeout (number): 
			PacketInTxBurstSize (number): 
			RemoteIp (str): 
			SerialNumber (str): 
			SoftwareDescription (str): 
			StartUpGenerationId (str): 
			StartUpRoleRequest (str(noRoleRequest|master|slave)): 
			StartupFeatureRequest (bool): 
			StoreFlows (bool): 
			UseDataPathIdAsChannelIdentifier (bool): 
			UseDatapathId (bool): 

		Returns:
			self: This instance with all currently retrieved ofChannel data using find and the newly added ofChannel data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ofChannel data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CalculateFlows=None, CalculatePacketInReplyDelay=None, DataPathId=None, DataPathIdInHex=None, DatapathDescritpion=None, Description=None, EnableCalculateFlowsPerSecondUsingBarrierReq=None, EnableHelloElement=None, EnableStartupEmptyTableFeatureRequest=None, Enabled=None, FlowTxBurstSize=None, HardwareDescription=None, InterFlowBurstGap=None, InterPacketInBurstGap=None, LocalIp=None, ManufacturerDescription=None, MaximumNumberOfFlowsProcessed=None, MaximumPacketInBytes=None, NumberOfBuffers=None, PacketInReplyTimeout=None, PacketInTxBurstSize=None, RemoteIp=None, SerialNumber=None, SoftwareDescription=None, StartUpGenerationId=None, StartUpRoleRequest=None, StartupFeatureRequest=None, StoreFlows=None, UseDataPathIdAsChannelIdentifier=None, UseDatapathId=None):
		"""Finds and retrieves ofChannel data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannel data from the server.
		By default the find method takes no parameters and will retrieve all ofChannel data from the server.

		Args:
			CalculateFlows (bool): 
			CalculatePacketInReplyDelay (bool): 
			DataPathId (str): 
			DataPathIdInHex (str): 
			DatapathDescritpion (str): 
			Description (str): 
			EnableCalculateFlowsPerSecondUsingBarrierReq (bool): 
			EnableHelloElement (bool): 
			EnableStartupEmptyTableFeatureRequest (bool): 
			Enabled (bool): 
			FlowTxBurstSize (number): 
			HardwareDescription (str): 
			InterFlowBurstGap (number): 
			InterPacketInBurstGap (number): 
			LocalIp (str): 
			ManufacturerDescription (str): 
			MaximumNumberOfFlowsProcessed (number): 
			MaximumPacketInBytes (number): 
			NumberOfBuffers (number): 
			PacketInReplyTimeout (number): 
			PacketInTxBurstSize (number): 
			RemoteIp (str): 
			SerialNumber (str): 
			SoftwareDescription (str): 
			StartUpGenerationId (str): 
			StartUpRoleRequest (str(noRoleRequest|master|slave)): 
			StartupFeatureRequest (bool): 
			StoreFlows (bool): 
			UseDataPathIdAsChannelIdentifier (bool): 
			UseDatapathId (bool): 

		Returns:
			self: This instance with matching ofChannel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateRole(self):
		"""Executes the updateRole operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannel)): The method internally sets Arg1 to the current href for this instance

		Returns:
			number: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateRole', payload=locals(), response_object=None)
