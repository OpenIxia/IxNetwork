from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchLearnedInformation(Base):
	"""The SwitchLearnedInformation class encapsulates a required switchLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchLearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'switchLearnedInformation'

	def __init__(self, parent):
		super(SwitchLearnedInformation, self).__init__(parent)

	@property
	def OfChannelSwitchLearnedInfo(self):
		"""An instance of the OfChannelSwitchLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelswitchlearnedinfo.OfChannelSwitchLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelswitchlearnedinfo import OfChannelSwitchLearnedInfo
		return OfChannelSwitchLearnedInfo(self)

	@property
	def SwitchFlow131TriggerAttributes(self):
		"""An instance of the SwitchFlow131TriggerAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflow131triggerattributes.SwitchFlow131TriggerAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflow131triggerattributes import SwitchFlow131TriggerAttributes
		return SwitchFlow131TriggerAttributes(self)._select()

	@property
	def SwitchFlowLearnedInfo(self):
		"""An instance of the SwitchFlowLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflowlearnedinfo.SwitchFlowLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflowlearnedinfo import SwitchFlowLearnedInfo
		return SwitchFlowLearnedInfo(self)

	@property
	def SwitchFlowMatchCriteria131TriggerAttributes(self):
		"""An instance of the SwitchFlowMatchCriteria131TriggerAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflowmatchcriteria131triggerattributes.SwitchFlowMatchCriteria131TriggerAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflowmatchcriteria131triggerattributes import SwitchFlowMatchCriteria131TriggerAttributes
		return SwitchFlowMatchCriteria131TriggerAttributes(self)._select()

	@property
	def SwitchGroupLearnedInfo(self):
		"""An instance of the SwitchGroupLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchgrouplearnedinfo.SwitchGroupLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchgrouplearnedinfo import SwitchGroupLearnedInfo
		return SwitchGroupLearnedInfo(self)

	@property
	def SwitchMeterLearnedInfo(self):
		"""An instance of the SwitchMeterLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchmeterlearnedinfo.SwitchMeterLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchmeterlearnedinfo import SwitchMeterLearnedInfo
		return SwitchMeterLearnedInfo(self)

	@property
	def SwitchTableFeaturesStatLearnedInfo(self):
		"""An instance of the SwitchTableFeaturesStatLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchtablefeaturesstatlearnedinfo.SwitchTableFeaturesStatLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchtablefeaturesstatlearnedinfo import SwitchTableFeaturesStatLearnedInfo
		return SwitchTableFeaturesStatLearnedInfo(self)

	@property
	def EnableVendorExperimenterMessage(self):
		"""If true, the vendor message trigger configuration parameters are available.

		Returns:
			bool
		"""
		return self._get_attribute('enableVendorExperimenterMessage')
	@EnableVendorExperimenterMessage.setter
	def EnableVendorExperimenterMessage(self, value):
		self._set_attribute('enableVendorExperimenterMessage', value)

	@property
	def EthernetDestination(self):
		"""This describes the flow match value for ethernet destination address field.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""This describes the flow match value for ethernet source address field.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""This describes the Ethernet type of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def InPort(self):
		"""This describes the flow match value for input port field

		Returns:
			str
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""This describes the flow match value for IP ToS field.

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpProtocol(self):
		"""This describes the flow match value for IP Protocol field.

		Returns:
			str
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Source(self):
		"""This describes the flow match value for IPv4 source address field.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv4destination(self):
		"""This describes the flow match value for IPv4 destination address field.

		Returns:
			str
		"""
		return self._get_attribute('ipv4destination')
	@Ipv4destination.setter
	def Ipv4destination(self, value):
		self._set_attribute('ipv4destination', value)

	@property
	def IsOfChannelLearnedInformationRefreshed(self):
		"""If true, it denotes that the Learned Info for the OF Channels is received.

		Returns:
			bool
		"""
		return self._get_attribute('isOfChannelLearnedInformationRefreshed')

	@property
	def IsOfFlowsLearnedInformationRefreshed(self):
		"""If true, it denotes that the Flow Learned Info for the OF Channels is received.

		Returns:
			bool
		"""
		return self._get_attribute('isOfFlowsLearnedInformationRefreshed')

	@property
	def OutPort(self):
		"""This describes the flow match value for output port field.

		Returns:
			number
		"""
		return self._get_attribute('outPort')
	@OutPort.setter
	def OutPort(self, value):
		self._set_attribute('outPort', value)

	@property
	def OutPortInputMode(self):
		"""This describes the output port type.

		Returns:
			str(ofppMax|ofppInPort|ofppTable|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal|ofppNone|outPortCustom)
		"""
		return self._get_attribute('outPortInputMode')
	@OutPortInputMode.setter
	def OutPortInputMode(self, value):
		self._set_attribute('outPortInputMode', value)

	@property
	def TableId(self):
		"""This describes the table identifier. It indicates the next table in the packet processing pipeline.

		Returns:
			number
		"""
		return self._get_attribute('tableId')
	@TableId.setter
	def TableId(self, value):
		self._set_attribute('tableId', value)

	@property
	def TableIdInputMode(self):
		"""This describes the type of table from which flow statistics will be sought.

		Returns:
			str(allTables|emergency|tableIdCustom)
		"""
		return self._get_attribute('tableIdInputMode')
	@TableIdInputMode.setter
	def TableIdInputMode(self, value):
		self._set_attribute('tableIdInputMode', value)

	@property
	def TansportSource(self):
		"""This describes the flow match value for transport source field.

		Returns:
			str
		"""
		return self._get_attribute('tansportSource')
	@TansportSource.setter
	def TansportSource(self, value):
		self._set_attribute('tansportSource', value)

	@property
	def TransportDestination(self):
		"""This describes the flow match value for transport destination field.

		Returns:
			str
		"""
		return self._get_attribute('transportDestination')
	@TransportDestination.setter
	def TransportDestination(self, value):
		self._set_attribute('transportDestination', value)

	@property
	def VendorExperimenterId(self):
		"""This describes the ID of the vendor for which vendor message is triggered.

		Returns:
			number
		"""
		return self._get_attribute('vendorExperimenterId')
	@VendorExperimenterId.setter
	def VendorExperimenterId(self, value):
		self._set_attribute('vendorExperimenterId', value)

	@property
	def VendorExperimenterType(self):
		"""This describes the Type of experimenter only for v 1.3.

		Returns:
			number
		"""
		return self._get_attribute('vendorExperimenterType')
	@VendorExperimenterType.setter
	def VendorExperimenterType(self, value):
		self._set_attribute('vendorExperimenterType', value)

	@property
	def VendorMessage(self):
		"""This describes the vendor data of the vendor message trigger.

		Returns:
			str
		"""
		return self._get_attribute('vendorMessage')
	@VendorMessage.setter
	def VendorMessage(self, value):
		self._set_attribute('vendorMessage', value)

	@property
	def VendorMessageLength(self):
		"""This describes the length of vendor data of the vendor message trigger.

		Returns:
			number
		"""
		return self._get_attribute('vendorMessageLength')
	@VendorMessageLength.setter
	def VendorMessageLength(self, value):
		self._set_attribute('vendorMessageLength', value)

	@property
	def VlanId(self):
		"""This describes the flow match value for VLAN ID field.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""This describes the flow match value for VLAN Priority field.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def ClearRecordsForTrigger(self):
		"""Executes the clearRecordsForTrigger operation on the server.

		API to clear records for any trigger.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearRecordsForTrigger', payload=locals(), response_object=None)

	def RefreshFlows(self):
		"""Executes the refreshFlows operation on the server.

		This describes that the flows learned information is refreshed.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshFlows', payload=locals(), response_object=None)

	def RefreshGroupLearnedInformation(self):
		"""Executes the refreshGroupLearnedInformation operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshGroupLearnedInformation', payload=locals(), response_object=None)

	def RefreshMeterLearnedInformation(self):
		"""Executes the refreshMeterLearnedInformation operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshMeterLearnedInformation', payload=locals(), response_object=None)

	def RefreshOfChannelLearnedInformation(self):
		"""Executes the refreshOfChannelLearnedInformation operation on the server.

		This describes that the ofChannellearned information is refreshed.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshOfChannelLearnedInformation', payload=locals(), response_object=None)

	def RefreshTableFeature(self):
		"""Executes the refreshTableFeature operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshTableFeature', payload=locals(), response_object=None)

	def Trigger(self):
		"""Executes the trigger operation on the server.

		API to send Trigger.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			number: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Trigger', payload=locals(), response_object=None)
