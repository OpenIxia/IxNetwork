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
	def Group(self):
		"""An instance of the Group class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.host.group.group.Group)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.host.group.group import Group
		return Group(self)

	@property
	def Enabled(self):
		"""Enables the use of the host in the IGMP simulation.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GqResponseMode(self):
		"""If enabled, responds to General Query messages (where the Group Address field and Number of Sources Field = 0). This query message is sent by a multicast router so it can learn about the complete multicast reception state for each of the neighboring interfaces. interfaces.

		Returns:
			bool
		"""
		return self._get_attribute('gqResponseMode')
	@GqResponseMode.setter
	def GqResponseMode(self, value):
		self._set_attribute('gqResponseMode', value)

	@property
	def InterfaceId(self):
		"""This is a local ID and is unique per router.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this IGMP interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this IGMP interface.

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
	def ReportFreq(self):
		"""When the mode is report to all unsolicited, this is the frequency in seconds with unsolicited messages are generated.

		Returns:
			number
		"""
		return self._get_attribute('reportFreq')
	@ReportFreq.setter
	def ReportFreq(self, value):
		self._set_attribute('reportFreq', value)

	@property
	def RespToQueryImmediately(self):
		"""If enabled, the state machine will ignore the value specified in the maximum response delay in the membership query message, assume that the delay is always 0 seconds, and immediately responds to the query by sending a report.

		Returns:
			bool
		"""
		return self._get_attribute('respToQueryImmediately')
	@RespToQueryImmediately.setter
	def RespToQueryImmediately(self, value):
		self._set_attribute('respToQueryImmediately', value)

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
	def RouterAlert(self):
		"""Sets the IP header Send Router Alert bit.

		Returns:
			bool
		"""
		return self._get_attribute('routerAlert')
	@RouterAlert.setter
	def RouterAlert(self, value):
		self._set_attribute('routerAlert', value)

	@property
	def SqResponseMode(self):
		"""If enabled, responds to Group-Specific Query messages. This query message is sent by a multicast router so it can learn about the multicast reception state, concerning one multicast address, for each of the neighboring interfaces; for example, when member leaves a group.

		Returns:
			bool
		"""
		return self._get_attribute('sqResponseMode')
	@SqResponseMode.setter
	def SqResponseMode(self, value):
		self._set_attribute('sqResponseMode', value)

	@property
	def SuppressReports(self):
		"""Suppress generation of V3 reports on receipt of v1/v2 reports having common groups. If enabled, it indicates that a host/group member will allow its IGMPv3 Membership Record to be suppressed by a membership report for Version 1 or 2. The suppression will only be for group reports received from another port.

		Returns:
			bool
		"""
		return self._get_attribute('suppressReports')
	@SuppressReports.setter
	def SuppressReports(self, value):
		self._set_attribute('suppressReports', value)

	@property
	def TrafficGroupId(self):
		"""This object contains the traffic group information configured in the trafficGroup object.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def UpResponseMode(self):
		"""Report to all unsolicited-causes each simulated host to automatically send full memberships messages at regular intervals.

		Returns:
			bool
		"""
		return self._get_attribute('upResponseMode')
	@UpResponseMode.setter
	def UpResponseMode(self, value):
		self._set_attribute('upResponseMode', value)

	@property
	def Version(self):
		"""Sets the IGMP version number that is to be simulated on the host: 1, 2, or 3.

		Returns:
			str(igmpv1|igmpv2|igmpv3)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, Enabled=None, GqResponseMode=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ReportFreq=None, RespToQueryImmediately=None, RobustnessVariable=None, RouterAlert=None, SqResponseMode=None, SuppressReports=None, TrafficGroupId=None, UpResponseMode=None, Version=None):
		"""Adds a new host node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the use of the host in the IGMP simulation.
			GqResponseMode (bool): If enabled, responds to General Query messages (where the Group Address field and Number of Sources Field = 0). This query message is sent by a multicast router so it can learn about the complete multicast reception state for each of the neighboring interfaces. interfaces.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This is a local ID and is unique per router.
			InterfaceIndex (number): The assigned protocol interface ID for this IGMP interface.
			InterfaceType (str): The type of interface to be selected for this IGMP interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			ReportFreq (number): When the mode is report to all unsolicited, this is the frequency in seconds with unsolicited messages are generated.
			RespToQueryImmediately (bool): If enabled, the state machine will ignore the value specified in the maximum response delay in the membership query message, assume that the delay is always 0 seconds, and immediately responds to the query by sending a report.
			RobustnessVariable (number): NOT DEFINED
			RouterAlert (bool): Sets the IP header Send Router Alert bit.
			SqResponseMode (bool): If enabled, responds to Group-Specific Query messages. This query message is sent by a multicast router so it can learn about the multicast reception state, concerning one multicast address, for each of the neighboring interfaces; for example, when member leaves a group.
			SuppressReports (bool): Suppress generation of V3 reports on receipt of v1/v2 reports having common groups. If enabled, it indicates that a host/group member will allow its IGMPv3 Membership Record to be suppressed by a membership report for Version 1 or 2. The suppression will only be for group reports received from another port.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): This object contains the traffic group information configured in the trafficGroup object.
			UpResponseMode (bool): Report to all unsolicited-causes each simulated host to automatically send full memberships messages at regular intervals.
			Version (str(igmpv1|igmpv2|igmpv3)): Sets the IGMP version number that is to be simulated on the host: 1, 2, or 3.

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

	def find(self, Enabled=None, GqResponseMode=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ReportFreq=None, RespToQueryImmediately=None, RobustnessVariable=None, RouterAlert=None, SqResponseMode=None, SuppressReports=None, TrafficGroupId=None, UpResponseMode=None, Version=None):
		"""Finds and retrieves host data from the server.

		All named parameters support regex and can be used to selectively retrieve host data from the server.
		By default the find method takes no parameters and will retrieve all host data from the server.

		Args:
			Enabled (bool): Enables the use of the host in the IGMP simulation.
			GqResponseMode (bool): If enabled, responds to General Query messages (where the Group Address field and Number of Sources Field = 0). This query message is sent by a multicast router so it can learn about the complete multicast reception state for each of the neighboring interfaces. interfaces.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This is a local ID and is unique per router.
			InterfaceIndex (number): The assigned protocol interface ID for this IGMP interface.
			InterfaceType (str): The type of interface to be selected for this IGMP interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			ReportFreq (number): When the mode is report to all unsolicited, this is the frequency in seconds with unsolicited messages are generated.
			RespToQueryImmediately (bool): If enabled, the state machine will ignore the value specified in the maximum response delay in the membership query message, assume that the delay is always 0 seconds, and immediately responds to the query by sending a report.
			RobustnessVariable (number): NOT DEFINED
			RouterAlert (bool): Sets the IP header Send Router Alert bit.
			SqResponseMode (bool): If enabled, responds to Group-Specific Query messages. This query message is sent by a multicast router so it can learn about the multicast reception state, concerning one multicast address, for each of the neighboring interfaces; for example, when member leaves a group.
			SuppressReports (bool): Suppress generation of V3 reports on receipt of v1/v2 reports having common groups. If enabled, it indicates that a host/group member will allow its IGMPv3 Membership Record to be suppressed by a membership report for Version 1 or 2. The suppression will only be for group reports received from another port.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): This object contains the traffic group information configured in the trafficGroup object.
			UpResponseMode (bool): Report to all unsolicited-causes each simulated host to automatically send full memberships messages at regular intervals.
			Version (str(igmpv1|igmpv2|igmpv3)): Sets the IGMP version number that is to be simulated on the host: 1, 2, or 3.

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

		Fetches interface accessor Iface list.

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
