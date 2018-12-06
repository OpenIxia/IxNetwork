
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


class FlowRange(Base):
	"""The FlowRange class encapsulates a user managed flowRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowRange'

	def __init__(self, parent):
		super(FlowRange, self).__init__(parent)

	@property
	def FlowRangeAction(self):
		"""An instance of the FlowRangeAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrangeaction.FlowRangeAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrangeaction import FlowRangeAction
		return FlowRangeAction(self)

	@property
	def CheckOverlap(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('checkOverlap')
	@CheckOverlap.setter
	def CheckOverlap(self, value):
		self._set_attribute('checkOverlap', value)

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
	def DontAddOnChannelUp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('dontAddOnChannelUp')
	@DontAddOnChannelUp.setter
	def DontAddOnChannelUp(self, value):
		self._set_attribute('dontAddOnChannelUp', value)

	@property
	def EmergencyFlow(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('emergencyFlow')
	@EmergencyFlow.setter
	def EmergencyFlow(self, value):
		self._set_attribute('emergencyFlow', value)

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
	def EthernetDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def FlowModStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('flowModStatus')

	@property
	def HardTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('hardTimeout')
	@HardTimeout.setter
	def HardTimeout(self, value):
		self._set_attribute('hardTimeout', value)

	@property
	def IdleTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('idleTimeout')
	@IdleTimeout.setter
	def IdleTimeout(self, value):
		self._set_attribute('idleTimeout', value)

	@property
	def InPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpProtocol(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def MatchType(self):
		"""

		Returns:
			str(strict|loose)
		"""
		return self._get_attribute('matchType')
	@MatchType.setter
	def MatchType(self, value):
		self._set_attribute('matchType', value)

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
	def SendFlowRemoved(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendFlowRemoved')
	@SendFlowRemoved.setter
	def SendFlowRemoved(self, value):
		self._set_attribute('sendFlowRemoved', value)

	@property
	def TotalFlowCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalFlowCount')
	@TotalFlowCount.setter
	def TotalFlowCount(self, value):
		self._set_attribute('totalFlowCount', value)

	@property
	def TransportDestinationIcmpCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transportDestinationIcmpCode')
	@TransportDestinationIcmpCode.setter
	def TransportDestinationIcmpCode(self, value):
		self._set_attribute('transportDestinationIcmpCode', value)

	@property
	def TransportSourceIcmpType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transportSourceIcmpType')
	@TransportSourceIcmpType.setter
	def TransportSourceIcmpType(self, value):
		self._set_attribute('transportSourceIcmpType', value)

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, CheckOverlap=None, Description=None, DontAddOnChannelUp=None, EmergencyFlow=None, Enabled=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, HardTimeout=None, IdleTimeout=None, InPort=None, IpDscp=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, MatchType=None, Priority=None, SendFlowRemoved=None, TotalFlowCount=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, VlanId=None, VlanPriority=None):
		"""Adds a new flowRange node on the server and retrieves it in this instance.

		Args:
			CheckOverlap (bool): 
			Description (str): 
			DontAddOnChannelUp (bool): 
			EmergencyFlow (bool): 
			Enabled (bool): 
			EthernetDestination (str): 
			EthernetSource (str): 
			EthernetType (str): 
			HardTimeout (number): 
			IdleTimeout (number): 
			InPort (str): 
			IpDscp (str): 
			IpProtocol (str): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			MatchType (str(strict|loose)): 
			Priority (number): 
			SendFlowRemoved (bool): 
			TotalFlowCount (number): 
			TransportDestinationIcmpCode (str): 
			TransportSourceIcmpType (str): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved flowRange data using find and the newly added flowRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CheckOverlap=None, Description=None, DontAddOnChannelUp=None, EmergencyFlow=None, Enabled=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, FlowModStatus=None, HardTimeout=None, IdleTimeout=None, InPort=None, IpDscp=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, MatchType=None, Priority=None, SendFlowRemoved=None, TotalFlowCount=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves flowRange data from the server.

		All named parameters support regex and can be used to selectively retrieve flowRange data from the server.
		By default the find method takes no parameters and will retrieve all flowRange data from the server.

		Args:
			CheckOverlap (bool): 
			Description (str): 
			DontAddOnChannelUp (bool): 
			EmergencyFlow (bool): 
			Enabled (bool): 
			EthernetDestination (str): 
			EthernetSource (str): 
			EthernetType (str): 
			FlowModStatus (str): 
			HardTimeout (number): 
			IdleTimeout (number): 
			InPort (str): 
			IpDscp (str): 
			IpProtocol (str): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			MatchType (str(strict|loose)): 
			Priority (number): 
			SendFlowRemoved (bool): 
			TotalFlowCount (number): 
			TransportDestinationIcmpCode (str): 
			TransportSourceIcmpType (str): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching flowRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateFlowMod(self, Arg2):
		"""Executes the updateFlowMod operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=flowRange)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(sendFlowAdd|sendFlowModify|sendFlowRemove)): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateFlowMod', payload=locals(), response_object=None)
