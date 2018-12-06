
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
	def CircuitAuthType(self):
		"""

		Returns:
			str(none|password|md5)
		"""
		return self._get_attribute('circuitAuthType')
	@CircuitAuthType.setter
	def CircuitAuthType(self, value):
		self._set_attribute('circuitAuthType', value)

	@property
	def CircuitReceivedPasswordList(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('circuitReceivedPasswordList')
	@CircuitReceivedPasswordList.setter
	def CircuitReceivedPasswordList(self, value):
		self._set_attribute('circuitReceivedPasswordList', value)

	@property
	def CircuitTransmitPassword(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('circuitTransmitPassword')
	@CircuitTransmitPassword.setter
	def CircuitTransmitPassword(self, value):
		self._set_attribute('circuitTransmitPassword', value)

	@property
	def ConfiguredHoldTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('configuredHoldTime')
	@ConfiguredHoldTime.setter
	def ConfiguredHoldTime(self, value):
		self._set_attribute('configuredHoldTime', value)

	@property
	def Enable3WayHandshake(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enable3WayHandshake')
	@Enable3WayHandshake.setter
	def Enable3WayHandshake(self, value):
		self._set_attribute('enable3WayHandshake', value)

	@property
	def EnableAutoAdjustArea(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoAdjustArea')
	@EnableAutoAdjustArea.setter
	def EnableAutoAdjustArea(self, value):
		self._set_attribute('enableAutoAdjustArea', value)

	@property
	def EnableAutoAdjustMtu(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoAdjustMtu')
	@EnableAutoAdjustMtu.setter
	def EnableAutoAdjustMtu(self, value):
		self._set_attribute('enableAutoAdjustMtu', value)

	@property
	def EnableAutoAdjustProtocolsSupported(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoAdjustProtocolsSupported')
	@EnableAutoAdjustProtocolsSupported.setter
	def EnableAutoAdjustProtocolsSupported(self, value):
		self._set_attribute('enableAutoAdjustProtocolsSupported', value)

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
	def EnableConfiguredHoldTime(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableConfiguredHoldTime')
	@EnableConfiguredHoldTime.setter
	def EnableConfiguredHoldTime(self, value):
		self._set_attribute('enableConfiguredHoldTime', value)

	@property
	def EnableConnectedToDut(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableConnectedToDut')
	@EnableConnectedToDut.setter
	def EnableConnectedToDut(self, value):
		self._set_attribute('enableConnectedToDut', value)

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
	def ExtendedCircuitId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('extendedCircuitId')
	@ExtendedCircuitId.setter
	def ExtendedCircuitId(self, value):
		self._set_attribute('extendedCircuitId', value)

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
	def InterfaceIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceIp')
	@InterfaceIp.setter
	def InterfaceIp(self, value):
		self._set_attribute('interfaceIp', value)

	@property
	def InterfaceIpMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceIpMask')
	@InterfaceIpMask.setter
	def InterfaceIpMask(self, value):
		self._set_attribute('interfaceIpMask', value)

	@property
	def Ipv6MtMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MtMetric')
	@Ipv6MtMetric.setter
	def Ipv6MtMetric(self, value):
		self._set_attribute('ipv6MtMetric', value)

	@property
	def Level(self):
		"""

		Returns:
			str(level1|level2|level1Level2)
		"""
		return self._get_attribute('level')
	@Level.setter
	def Level(self, value):
		self._set_attribute('level', value)

	@property
	def Level1DeadTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('level1DeadTime')
	@Level1DeadTime.setter
	def Level1DeadTime(self, value):
		self._set_attribute('level1DeadTime', value)

	@property
	def Level1HelloTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('level1HelloTime')
	@Level1HelloTime.setter
	def Level1HelloTime(self, value):
		self._set_attribute('level1HelloTime', value)

	@property
	def Level2DeadTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('level2DeadTime')
	@Level2DeadTime.setter
	def Level2DeadTime(self, value):
		self._set_attribute('level2DeadTime', value)

	@property
	def Level2HelloTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('level2HelloTime')
	@Level2HelloTime.setter
	def Level2HelloTime(self, value):
		self._set_attribute('level2HelloTime', value)

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
	def PriorityLevel1(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priorityLevel1')
	@PriorityLevel1.setter
	def PriorityLevel1(self, value):
		self._set_attribute('priorityLevel1', value)

	@property
	def PriorityLevel2(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priorityLevel2')
	@PriorityLevel2.setter
	def PriorityLevel2(self, value):
		self._set_attribute('priorityLevel2', value)

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
			list(number)
		"""
		return self._get_attribute('teUnreservedBwPriority')
	@TeUnreservedBwPriority.setter
	def TeUnreservedBwPriority(self, value):
		self._set_attribute('teUnreservedBwPriority', value)

	def add(self, CircuitAuthType=None, CircuitReceivedPasswordList=None, CircuitTransmitPassword=None, ConfiguredHoldTime=None, Enable3WayHandshake=None, EnableAutoAdjustArea=None, EnableAutoAdjustMtu=None, EnableAutoAdjustProtocolsSupported=None, EnableBfdRegistration=None, EnableConfiguredHoldTime=None, EnableConnectedToDut=None, Enabled=None, ExtendedCircuitId=None, InterfaceId=None, InterfaceIp=None, InterfaceIpMask=None, Ipv6MtMetric=None, Level=None, Level1DeadTime=None, Level1HelloTime=None, Level2DeadTime=None, Level2HelloTime=None, Metric=None, NetworkType=None, PriorityLevel1=None, PriorityLevel2=None, TeAdminGroup=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			CircuitAuthType (str(none|password|md5)): 
			CircuitReceivedPasswordList (list(str)): 
			CircuitTransmitPassword (str): 
			ConfiguredHoldTime (number): 
			Enable3WayHandshake (bool): 
			EnableAutoAdjustArea (bool): 
			EnableAutoAdjustMtu (bool): 
			EnableAutoAdjustProtocolsSupported (bool): 
			EnableBfdRegistration (bool): 
			EnableConfiguredHoldTime (bool): 
			EnableConnectedToDut (bool): 
			Enabled (bool): 
			ExtendedCircuitId (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIp (str): 
			InterfaceIpMask (str): 
			Ipv6MtMetric (number): 
			Level (str(level1|level2|level1Level2)): 
			Level1DeadTime (number): 
			Level1HelloTime (number): 
			Level2DeadTime (number): 
			Level2HelloTime (number): 
			Metric (number): 
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): 
			PriorityLevel1 (number): 
			PriorityLevel2 (number): 
			TeAdminGroup (str): 
			TeMaxBandwidth (number): 
			TeMetricLevel (number): 
			TeResMaxBandwidth (number): 
			TeUnreservedBwPriority (list(number)): 

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

	def find(self, CircuitAuthType=None, CircuitReceivedPasswordList=None, CircuitTransmitPassword=None, ConfiguredHoldTime=None, Enable3WayHandshake=None, EnableAutoAdjustArea=None, EnableAutoAdjustMtu=None, EnableAutoAdjustProtocolsSupported=None, EnableBfdRegistration=None, EnableConfiguredHoldTime=None, EnableConnectedToDut=None, Enabled=None, ExtendedCircuitId=None, InterfaceId=None, InterfaceIp=None, InterfaceIpMask=None, Ipv6MtMetric=None, Level=None, Level1DeadTime=None, Level1HelloTime=None, Level2DeadTime=None, Level2HelloTime=None, Metric=None, NetworkType=None, PriorityLevel1=None, PriorityLevel2=None, TeAdminGroup=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			CircuitAuthType (str(none|password|md5)): 
			CircuitReceivedPasswordList (list(str)): 
			CircuitTransmitPassword (str): 
			ConfiguredHoldTime (number): 
			Enable3WayHandshake (bool): 
			EnableAutoAdjustArea (bool): 
			EnableAutoAdjustMtu (bool): 
			EnableAutoAdjustProtocolsSupported (bool): 
			EnableBfdRegistration (bool): 
			EnableConfiguredHoldTime (bool): 
			EnableConnectedToDut (bool): 
			Enabled (bool): 
			ExtendedCircuitId (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIp (str): 
			InterfaceIpMask (str): 
			Ipv6MtMetric (number): 
			Level (str(level1|level2|level1Level2)): 
			Level1DeadTime (number): 
			Level1HelloTime (number): 
			Level2DeadTime (number): 
			Level2HelloTime (number): 
			Metric (number): 
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): 
			PriorityLevel1 (number): 
			PriorityLevel2 (number): 
			TeAdminGroup (str): 
			TeMaxBandwidth (number): 
			TeMetricLevel (number): 
			TeResMaxBandwidth (number): 
			TeUnreservedBwPriority (list(number)): 

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
