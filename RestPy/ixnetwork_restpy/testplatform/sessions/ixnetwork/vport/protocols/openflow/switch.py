
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


class Switch(Base):
	"""The Switch class encapsulates a user managed switch node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Switch property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'switch'

	def __init__(self, parent):
		super(Switch, self).__init__(parent)

	@property
	def BandTypes(self):
		"""An instance of the BandTypes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.bandtypes.BandTypes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.bandtypes import BandTypes
		return BandTypes(self)._select()

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
	def FlowRemovedMaskMaster(self):
		"""An instance of the FlowRemovedMaskMaster class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowremovedmaskmaster.FlowRemovedMaskMaster)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowremovedmaskmaster import FlowRemovedMaskMaster
		return FlowRemovedMaskMaster(self)._select()

	@property
	def FlowRemovedMaskSlave(self):
		"""An instance of the FlowRemovedMaskSlave class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowremovedmaskslave.FlowRemovedMaskSlave)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowremovedmaskslave import FlowRemovedMaskSlave
		return FlowRemovedMaskSlave(self)._select()

	@property
	def GroupCapabilities(self):
		"""An instance of the GroupCapabilities class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.groupcapabilities.GroupCapabilities)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.groupcapabilities import GroupCapabilities
		return GroupCapabilities(self)._select()

	@property
	def GroupTypes(self):
		"""An instance of the GroupTypes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.grouptypes.GroupTypes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.grouptypes import GroupTypes
		return GroupTypes(self)._select()

	@property
	def MeterCapabilities(self):
		"""An instance of the MeterCapabilities class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.metercapabilities.MeterCapabilities)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.metercapabilities import MeterCapabilities
		return MeterCapabilities(self)._select()

	@property
	def PacketInMaskMaster(self):
		"""An instance of the PacketInMaskMaster class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.packetinmaskmaster.PacketInMaskMaster)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.packetinmaskmaster import PacketInMaskMaster
		return PacketInMaskMaster(self)._select()

	@property
	def PacketInMaskSlave(self):
		"""An instance of the PacketInMaskSlave class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.packetinmaskslave.PacketInMaskSlave)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.packetinmaskslave import PacketInMaskSlave
		return PacketInMaskSlave(self)._select()

	@property
	def PortStatusMaskMaster(self):
		"""An instance of the PortStatusMaskMaster class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.portstatusmaskmaster.PortStatusMaskMaster)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.portstatusmaskmaster import PortStatusMaskMaster
		return PortStatusMaskMaster(self)._select()

	@property
	def PortStatusMaskSlave(self):
		"""An instance of the PortStatusMaskSlave class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.portstatusmaskslave.PortStatusMaskSlave)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.portstatusmaskslave import PortStatusMaskSlave
		return PortStatusMaskSlave(self)._select()

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
	def SwitchGroupFeature(self):
		"""An instance of the SwitchGroupFeature class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchgroupfeature.SwitchGroupFeature)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchgroupfeature import SwitchGroupFeature
		return SwitchGroupFeature(self)

	@property
	def SwitchOfChannel(self):
		"""An instance of the SwitchOfChannel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchofchannel.SwitchOfChannel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchofchannel import SwitchOfChannel
		return SwitchOfChannel(self)

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
	def BarrierReplyDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('barrierReplyDelay')
	@BarrierReplyDelay.setter
	def BarrierReplyDelay(self, value):
		self._set_attribute('barrierReplyDelay', value)

	@property
	def BarrierReplyDelayType(self):
		"""

		Returns:
			str(fixed|random)
		"""
		return self._get_attribute('barrierReplyDelayType')
	@BarrierReplyDelayType.setter
	def BarrierReplyDelayType(self, value):
		self._set_attribute('barrierReplyDelayType', value)

	@property
	def BarrierReplyMaxDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('barrierReplyMaxDelay')
	@BarrierReplyMaxDelay.setter
	def BarrierReplyMaxDelay(self, value):
		self._set_attribute('barrierReplyMaxDelay', value)

	@property
	def CalculateControllerFlowTxRate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('calculateControllerFlowTxRate')
	@CalculateControllerFlowTxRate.setter
	def CalculateControllerFlowTxRate(self, value):
		self._set_attribute('calculateControllerFlowTxRate', value)

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
	def DatapathDescription(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathDescription')
	@DatapathDescription.setter
	def DatapathDescription(self, value):
		self._set_attribute('datapathDescription', value)

	@property
	def DatapathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathId')
	@DatapathId.setter
	def DatapathId(self, value):
		self._set_attribute('datapathId', value)

	@property
	def DatapathIdInHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathIdInHex')
	@DatapathIdInHex.setter
	def DatapathIdInHex(self, value):
		self._set_attribute('datapathIdInHex', value)

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
	def Enable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enable')
	@Enable.setter
	def Enable(self, value):
		self._set_attribute('enable', value)

	@property
	def EnableCalculatePacketOutRxRate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCalculatePacketOutRxRate')
	@EnableCalculatePacketOutRxRate.setter
	def EnableCalculatePacketOutRxRate(self, value):
		self._set_attribute('enableCalculatePacketOutRxRate', value)

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
	def MaxPacketInBytes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxPacketInBytes')
	@MaxPacketInBytes.setter
	def MaxPacketInBytes(self, value):
		self._set_attribute('maxPacketInBytes', value)

	@property
	def MaximumColorValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumColorValue')
	@MaximumColorValue.setter
	def MaximumColorValue(self, value):
		self._set_attribute('maximumColorValue', value)

	@property
	def MaximumNoOfBandsPerMeter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumNoOfBandsPerMeter')
	@MaximumNoOfBandsPerMeter.setter
	def MaximumNoOfBandsPerMeter(self, value):
		self._set_attribute('maximumNoOfBandsPerMeter', value)

	@property
	def MaximumNoOfBucketsPerGroup(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumNoOfBucketsPerGroup')
	@MaximumNoOfBucketsPerGroup.setter
	def MaximumNoOfBucketsPerGroup(self, value):
		self._set_attribute('maximumNoOfBucketsPerGroup', value)

	@property
	def MaximumNoOfMeters(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumNoOfMeters')
	@MaximumNoOfMeters.setter
	def MaximumNoOfMeters(self, value):
		self._set_attribute('maximumNoOfMeters', value)

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
	def SupportPacketForwarding(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportPacketForwarding')
	@SupportPacketForwarding.setter
	def SupportPacketForwarding(self, value):
		self._set_attribute('supportPacketForwarding', value)

	@property
	def TableMissAction(self):
		"""

		Returns:
			str(drop|sendToController)
		"""
		return self._get_attribute('tableMissAction')
	@TableMissAction.setter
	def TableMissAction(self, value):
		self._set_attribute('tableMissAction', value)

	def add(self, BarrierReplyDelay=None, BarrierReplyDelayType=None, BarrierReplyMaxDelay=None, CalculateControllerFlowTxRate=None, CalculatePacketInReplyDelay=None, DatapathDescription=None, DatapathId=None, DatapathIdInHex=None, Description=None, Enable=None, EnableCalculatePacketOutRxRate=None, EnableHelloElement=None, HardwareDescription=None, InterPacketInBurstGap=None, ManufacturerDescription=None, MaxPacketInBytes=None, MaximumColorValue=None, MaximumNoOfBandsPerMeter=None, MaximumNoOfBucketsPerGroup=None, MaximumNoOfMeters=None, NumberOfBuffers=None, PacketInReplyTimeout=None, PacketInTxBurstSize=None, SerialNumber=None, SoftwareDescription=None, StoreFlows=None, SupportPacketForwarding=None, TableMissAction=None):
		"""Adds a new switch node on the server and retrieves it in this instance.

		Args:
			BarrierReplyDelay (number): 
			BarrierReplyDelayType (str(fixed|random)): 
			BarrierReplyMaxDelay (number): 
			CalculateControllerFlowTxRate (bool): 
			CalculatePacketInReplyDelay (bool): 
			DatapathDescription (str): 
			DatapathId (str): 
			DatapathIdInHex (str): 
			Description (str): 
			Enable (bool): 
			EnableCalculatePacketOutRxRate (bool): 
			EnableHelloElement (bool): 
			HardwareDescription (str): 
			InterPacketInBurstGap (number): 
			ManufacturerDescription (str): 
			MaxPacketInBytes (number): 
			MaximumColorValue (number): 
			MaximumNoOfBandsPerMeter (number): 
			MaximumNoOfBucketsPerGroup (number): 
			MaximumNoOfMeters (number): 
			NumberOfBuffers (number): 
			PacketInReplyTimeout (number): 
			PacketInTxBurstSize (number): 
			SerialNumber (str): 
			SoftwareDescription (str): 
			StoreFlows (bool): 
			SupportPacketForwarding (bool): 
			TableMissAction (str(drop|sendToController)): 

		Returns:
			self: This instance with all currently retrieved switch data using find and the newly added switch data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the switch data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BarrierReplyDelay=None, BarrierReplyDelayType=None, BarrierReplyMaxDelay=None, CalculateControllerFlowTxRate=None, CalculatePacketInReplyDelay=None, DatapathDescription=None, DatapathId=None, DatapathIdInHex=None, Description=None, Enable=None, EnableCalculatePacketOutRxRate=None, EnableHelloElement=None, HardwareDescription=None, InterPacketInBurstGap=None, LocalIp=None, ManufacturerDescription=None, MaxPacketInBytes=None, MaximumColorValue=None, MaximumNoOfBandsPerMeter=None, MaximumNoOfBucketsPerGroup=None, MaximumNoOfMeters=None, NumberOfBuffers=None, PacketInReplyTimeout=None, PacketInTxBurstSize=None, SerialNumber=None, SoftwareDescription=None, StoreFlows=None, SupportPacketForwarding=None, TableMissAction=None):
		"""Finds and retrieves switch data from the server.

		All named parameters support regex and can be used to selectively retrieve switch data from the server.
		By default the find method takes no parameters and will retrieve all switch data from the server.

		Args:
			BarrierReplyDelay (number): 
			BarrierReplyDelayType (str(fixed|random)): 
			BarrierReplyMaxDelay (number): 
			CalculateControllerFlowTxRate (bool): 
			CalculatePacketInReplyDelay (bool): 
			DatapathDescription (str): 
			DatapathId (str): 
			DatapathIdInHex (str): 
			Description (str): 
			Enable (bool): 
			EnableCalculatePacketOutRxRate (bool): 
			EnableHelloElement (bool): 
			HardwareDescription (str): 
			InterPacketInBurstGap (number): 
			LocalIp (str): 
			ManufacturerDescription (str): 
			MaxPacketInBytes (number): 
			MaximumColorValue (number): 
			MaximumNoOfBandsPerMeter (number): 
			MaximumNoOfBucketsPerGroup (number): 
			MaximumNoOfMeters (number): 
			NumberOfBuffers (number): 
			PacketInReplyTimeout (number): 
			PacketInTxBurstSize (number): 
			SerialNumber (str): 
			SoftwareDescription (str): 
			StoreFlows (bool): 
			SupportPacketForwarding (bool): 
			TableMissAction (str(drop|sendToController)): 

		Returns:
			self: This instance with matching switch data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switch data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switch data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
