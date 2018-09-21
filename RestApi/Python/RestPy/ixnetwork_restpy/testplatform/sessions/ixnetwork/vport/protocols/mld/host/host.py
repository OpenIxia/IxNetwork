from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Host(Base):
	"""The Host class encapsulates a user managed host node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Host property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'host'

	def __init__(self, parent):
		super(Host, self).__init__(parent)

	@property
	def GroupRange(self):
		"""An instance of the GroupRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.grouprange.GroupRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.grouprange import GroupRange
		return GroupRange(self)

	@property
	def EnableImmediateResp(self):
		"""If enabled, the MLD host will ignore the value specified in the maximum response delay in the query message, assume that the delay is always = 0 seconds, and immediately respond to the query by sending a report.

		Returns:
			bool
		"""
		return self._get_attribute('enableImmediateResp')
	@EnableImmediateResp.setter
	def EnableImmediateResp(self, value):
		self._set_attribute('enableImmediateResp', value)

	@property
	def EnableQueryResMode(self):
		"""Enables the simulation for the host to respond to general queries.

		Returns:
			bool
		"""
		return self._get_attribute('enableQueryResMode')
	@EnableQueryResMode.setter
	def EnableQueryResMode(self, value):
		self._set_attribute('enableQueryResMode', value)

	@property
	def EnableRouterAlert(self):
		"""Sets the router alert bit in listener report messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableRouterAlert')
	@EnableRouterAlert.setter
	def EnableRouterAlert(self, value):
		self._set_attribute('enableRouterAlert', value)

	@property
	def EnableSpecificResMode(self):
		"""Enables the simulation for the host to respond to group specific queries.

		Returns:
			bool
		"""
		return self._get_attribute('enableSpecificResMode')
	@EnableSpecificResMode.setter
	def EnableSpecificResMode(self, value):
		self._set_attribute('enableSpecificResMode', value)

	@property
	def EnableSuppressReport(self):
		"""Suppress generation of V2 reports on receipt of v1 reports having common groups. If enabled, it indicates that a host/group member will allow its MLDv2 Membership Record to be 'suppressed by a membership report for Version 1. The suppression will only be for group reports received from another port.

		Returns:
			bool
		"""
		return self._get_attribute('enableSuppressReport')
	@EnableSuppressReport.setter
	def EnableSuppressReport(self, value):
		self._set_attribute('enableSuppressReport', value)

	@property
	def EnableUnsolicitedResMode(self):
		"""If enabled, causes the emulated MLD host to automatically send full membership messages at regular intervals, without waiting for a query message.

		Returns:
			bool
		"""
		return self._get_attribute('enableUnsolicitedResMode')
	@EnableUnsolicitedResMode.setter
	def EnableUnsolicitedResMode(self, value):
		self._set_attribute('enableUnsolicitedResMode', value)

	@property
	def Enabled(self):
		"""Enables the use of the host in the MLD simulation.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this MLD interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this MLD interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""The interfaces that are associated with the selected interface type.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def ProtocolInterface(self):
		"""The name of the protocol interface being used for this emulated MLD Host. There may be multiple IPv6 protocol interfaces to select from.NOTE: Only enabled protocol interfaces configured with IPv6 addresses will be listed here.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def ReportFreq(self):
		"""Can be configured only when the Unsolicited Response Mode option is enabled. Otherwise, it is read-only. When Unsolicited Response Mode is enabled, specifies the frequency, in seconds, with which unsolicited messages are generated.

		Returns:
			number
		"""
		return self._get_attribute('reportFreq')
	@ReportFreq.setter
	def ReportFreq(self, value):
		self._set_attribute('reportFreq', value)

	@property
	def RobustnessVariable(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('robustnessVariable')
	@RobustnessVariable.setter
	def RobustnessVariable(self, value):
		self._set_attribute('robustnessVariable', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def Version(self):
		"""Sets the MLD version number that is to be simulated on the host: 1 or 2.

		Returns:
			str(version1|version2)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, EnableImmediateResp=None, EnableQueryResMode=None, EnableRouterAlert=None, EnableSpecificResMode=None, EnableSuppressReport=None, EnableUnsolicitedResMode=None, Enabled=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ProtocolInterface=None, ReportFreq=None, RobustnessVariable=None, TrafficGroupId=None, Version=None):
		"""Adds a new host node on the server and retrieves it in this instance.

		Args:
			EnableImmediateResp (bool): If enabled, the MLD host will ignore the value specified in the maximum response delay in the query message, assume that the delay is always = 0 seconds, and immediately respond to the query by sending a report.
			EnableQueryResMode (bool): Enables the simulation for the host to respond to general queries.
			EnableRouterAlert (bool): Sets the router alert bit in listener report messages.
			EnableSpecificResMode (bool): Enables the simulation for the host to respond to group specific queries.
			EnableSuppressReport (bool): Suppress generation of V2 reports on receipt of v1 reports having common groups. If enabled, it indicates that a host/group member will allow its MLDv2 Membership Record to be 'suppressed by a membership report for Version 1. The suppression will only be for group reports received from another port.
			EnableUnsolicitedResMode (bool): If enabled, causes the emulated MLD host to automatically send full membership messages at regular intervals, without waiting for a query message.
			Enabled (bool): Enables the use of the host in the MLD simulation.
			InterfaceIndex (number): The assigned protocol interface ID for this MLD interface.
			InterfaceType (str): The type of interface to be selected for this MLD interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The name of the protocol interface being used for this emulated MLD Host. There may be multiple IPv6 protocol interfaces to select from.NOTE: Only enabled protocol interfaces configured with IPv6 addresses will be listed here.
			ReportFreq (number): Can be configured only when the Unsolicited Response Mode option is enabled. Otherwise, it is read-only. When Unsolicited Response Mode is enabled, specifies the frequency, in seconds, with which unsolicited messages are generated.
			RobustnessVariable (number): NOT DEFINED
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			Version (str(version1|version2)): Sets the MLD version number that is to be simulated on the host: 1 or 2.

		Returns:
			self: This instance with all currently retrieved host data using find and the newly added host data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the host data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableImmediateResp=None, EnableQueryResMode=None, EnableRouterAlert=None, EnableSpecificResMode=None, EnableSuppressReport=None, EnableUnsolicitedResMode=None, Enabled=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ProtocolInterface=None, ReportFreq=None, RobustnessVariable=None, TrafficGroupId=None, Version=None):
		"""Finds and retrieves host data from the server.

		All named parameters support regex and can be used to selectively retrieve host data from the server.
		By default the find method takes no parameters and will retrieve all host data from the server.

		Args:
			EnableImmediateResp (bool): If enabled, the MLD host will ignore the value specified in the maximum response delay in the query message, assume that the delay is always = 0 seconds, and immediately respond to the query by sending a report.
			EnableQueryResMode (bool): Enables the simulation for the host to respond to general queries.
			EnableRouterAlert (bool): Sets the router alert bit in listener report messages.
			EnableSpecificResMode (bool): Enables the simulation for the host to respond to group specific queries.
			EnableSuppressReport (bool): Suppress generation of V2 reports on receipt of v1 reports having common groups. If enabled, it indicates that a host/group member will allow its MLDv2 Membership Record to be 'suppressed by a membership report for Version 1. The suppression will only be for group reports received from another port.
			EnableUnsolicitedResMode (bool): If enabled, causes the emulated MLD host to automatically send full membership messages at regular intervals, without waiting for a query message.
			Enabled (bool): Enables the use of the host in the MLD simulation.
			InterfaceIndex (number): The assigned protocol interface ID for this MLD interface.
			InterfaceType (str): The type of interface to be selected for this MLD interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The name of the protocol interface being used for this emulated MLD Host. There may be multiple IPv6 protocol interfaces to select from.NOTE: Only enabled protocol interfaces configured with IPv6 addresses will be listed here.
			ReportFreq (number): Can be configured only when the Unsolicited Response Mode option is enabled. Otherwise, it is read-only. When Unsolicited Response Mode is enabled, specifies the frequency, in seconds, with which unsolicited messages are generated.
			RobustnessVariable (number): NOT DEFINED
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			Version (str(version1|version2)): Sets the MLD version number that is to be simulated on the host: 1 or 2.

		Returns:
			self: This instance with matching host data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of host data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the host data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		Gets the interface accesor Iface list.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=host)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)
