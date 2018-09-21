from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Querier(Base):
	"""The Querier class encapsulates a user managed querier node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Querier property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'querier'

	def __init__(self, parent):
		super(Querier, self).__init__(parent)

	@property
	def LearnedGroupInfo(self):
		"""An instance of the LearnedGroupInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.querier.learnedgroupinfo.learnedgroupinfo.LearnedGroupInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.querier.learnedgroupinfo.learnedgroupinfo import LearnedGroupInfo
		return LearnedGroupInfo(self)

	@property
	def DiscardLearnedInfo(self):
		"""If true, the Querier doesn't maintain any database and only sends periodic general queries. The specific query group/source record information isn't calculated based on any earlier received Report, but solely based on the last received report. If false, the emulated Querier maintains a complete record state for received reports and send queries (based on timer expiry for received groups and sources). Default is true.

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedInfo')
	@DiscardLearnedInfo.setter
	def DiscardLearnedInfo(self, value):
		self._set_attribute('discardLearnedInfo', value)

	@property
	def Enabled(self):
		"""If true, the querier is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GeneralQueryInterval(self):
		"""The amount of time in seconds between IGMP General Query messages sent by the querier. The default query interval is 125 seconds.

		Returns:
			number
		"""
		return self._get_attribute('generalQueryInterval')
	@GeneralQueryInterval.setter
	def GeneralQueryInterval(self, value):
		self._set_attribute('generalQueryInterval', value)

	@property
	def GqResponseInterval(self):
		"""The maximum amount of time in seconds that the IGMP querier waits to receive a response to a General Query message. The default query response interval is 10000 milliseconds and must be less than the query interval.

		Returns:
			number
		"""
		return self._get_attribute('gqResponseInterval')
	@GqResponseInterval.setter
	def GqResponseInterval(self, value):
		self._set_attribute('gqResponseInterval', value)

	@property
	def InterfaceId(self):
		"""The interface associated with the IGMP querier. The interface must be previously configured.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this SM interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""Indicates the type of network for the interface.

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
	def IsQuerier(self):
		"""If true, this IGMP entity is a querier.

		Returns:
			bool
		"""
		return self._get_attribute('isQuerier')

	@property
	def IsRefreshComplete(self):
		"""If true, the querier information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isRefreshComplete')

	@property
	def QuerierAddress(self):
		"""The querier IP address.

		Returns:
			str
		"""
		return self._get_attribute('querierAddress')

	@property
	def QuerierWorkingVersion(self):
		"""The querier working IGMP version.

		Returns:
			number
		"""
		return self._get_attribute('querierWorkingVersion')

	@property
	def RobustnessVariable(self):
		"""Defines the subnet vulnerability to lost packets. IGMP can recover from robustness variable minus 1 lost IGMP packets. The robustness variable should be set to a value of 2 or greater. The default robustness variable value is 2.

		Returns:
			number
		"""
		return self._get_attribute('robustnessVariable')
	@RobustnessVariable.setter
	def RobustnessVariable(self, value):
		self._set_attribute('robustnessVariable', value)

	@property
	def RouterAlert(self):
		"""If true, sets the Send Router Alert bit in the IP header.

		Returns:
			bool
		"""
		return self._get_attribute('routerAlert')
	@RouterAlert.setter
	def RouterAlert(self, value):
		self._set_attribute('routerAlert', value)

	@property
	def SqResponseInterval(self):
		"""The maximum amount of time in seconds that the IGMP querier waits to receive a response to a Specific Query message. The default query response interval is 1000 milliseconds and must be less than the query interval.

		Returns:
			number
		"""
		return self._get_attribute('sqResponseInterval')
	@SqResponseInterval.setter
	def SqResponseInterval(self, value):
		self._set_attribute('sqResponseInterval', value)

	@property
	def SqTransmissionCount(self):
		"""Indicates the total number of specific Query messagessent every Specific Query Response Interval seconds before assuming that there is no interested listener for the particular group/source.

		Returns:
			number
		"""
		return self._get_attribute('sqTransmissionCount')
	@SqTransmissionCount.setter
	def SqTransmissionCount(self, value):
		self._set_attribute('sqTransmissionCount', value)

	@property
	def StartupQueryCount(self):
		"""The number of general query messages sent at startup. The default startup query count is 2.

		Returns:
			number
		"""
		return self._get_attribute('startupQueryCount')
	@StartupQueryCount.setter
	def StartupQueryCount(self, value):
		self._set_attribute('startupQueryCount', value)

	@property
	def SupportElection(self):
		"""If true, indicates whether the Querier participates in querier election or not. If disabled, then all incoming query messages are discarded.

		Returns:
			bool
		"""
		return self._get_attribute('supportElection')
	@SupportElection.setter
	def SupportElection(self, value):
		self._set_attribute('supportElection', value)

	@property
	def SupportOlderVersionHost(self):
		"""If true, indicates whether the Querier will comply to RFC 3376 Section 7.3.2 and RFC 3810 Section 8.3.2. If disabled, all membership reports with version less than the current version are discarded.

		Returns:
			bool
		"""
		return self._get_attribute('supportOlderVersionHost')
	@SupportOlderVersionHost.setter
	def SupportOlderVersionHost(self, value):
		self._set_attribute('supportOlderVersionHost', value)

	@property
	def SupportOlderVersionQuerier(self):
		"""If true, indicates whether the Querier downgrades to the lowest version of received query messages. If disabled, all query messages with version less than the current version are discarded.

		Returns:
			bool
		"""
		return self._get_attribute('supportOlderVersionQuerier')
	@SupportOlderVersionQuerier.setter
	def SupportOlderVersionQuerier(self, value):
		self._set_attribute('supportOlderVersionQuerier', value)

	@property
	def Version(self):
		"""Sets the version for the IGMP querier.

		Returns:
			str(igmpv1|igmpv2|igmpv3)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, DiscardLearnedInfo=None, Enabled=None, GeneralQueryInterval=None, GqResponseInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, RobustnessVariable=None, RouterAlert=None, SqResponseInterval=None, SqTransmissionCount=None, StartupQueryCount=None, SupportElection=None, SupportOlderVersionHost=None, SupportOlderVersionQuerier=None, Version=None):
		"""Adds a new querier node on the server and retrieves it in this instance.

		Args:
			DiscardLearnedInfo (bool): If true, the Querier doesn't maintain any database and only sends periodic general queries. The specific query group/source record information isn't calculated based on any earlier received Report, but solely based on the last received report. If false, the emulated Querier maintains a complete record state for received reports and send queries (based on timer expiry for received groups and sources). Default is true.
			Enabled (bool): If true, the querier is enabled.
			GeneralQueryInterval (number): The amount of time in seconds between IGMP General Query messages sent by the querier. The default query interval is 125 seconds.
			GqResponseInterval (number): The maximum amount of time in seconds that the IGMP querier waits to receive a response to a General Query message. The default query response interval is 10000 milliseconds and must be less than the query interval.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The interface associated with the IGMP querier. The interface must be previously configured.
			InterfaceIndex (number): The assigned protocol interface ID for this SM interface.
			InterfaceType (str): Indicates the type of network for the interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			RobustnessVariable (number): Defines the subnet vulnerability to lost packets. IGMP can recover from robustness variable minus 1 lost IGMP packets. The robustness variable should be set to a value of 2 or greater. The default robustness variable value is 2.
			RouterAlert (bool): If true, sets the Send Router Alert bit in the IP header.
			SqResponseInterval (number): The maximum amount of time in seconds that the IGMP querier waits to receive a response to a Specific Query message. The default query response interval is 1000 milliseconds and must be less than the query interval.
			SqTransmissionCount (number): Indicates the total number of specific Query messagessent every Specific Query Response Interval seconds before assuming that there is no interested listener for the particular group/source.
			StartupQueryCount (number): The number of general query messages sent at startup. The default startup query count is 2.
			SupportElection (bool): If true, indicates whether the Querier participates in querier election or not. If disabled, then all incoming query messages are discarded.
			SupportOlderVersionHost (bool): If true, indicates whether the Querier will comply to RFC 3376 Section 7.3.2 and RFC 3810 Section 8.3.2. If disabled, all membership reports with version less than the current version are discarded.
			SupportOlderVersionQuerier (bool): If true, indicates whether the Querier downgrades to the lowest version of received query messages. If disabled, all query messages with version less than the current version are discarded.
			Version (str(igmpv1|igmpv2|igmpv3)): Sets the version for the IGMP querier.

		Returns:
			self: This instance with all currently retrieved querier data using find and the newly added querier data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the querier data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DiscardLearnedInfo=None, Enabled=None, GeneralQueryInterval=None, GqResponseInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, IsQuerier=None, IsRefreshComplete=None, QuerierAddress=None, QuerierWorkingVersion=None, RobustnessVariable=None, RouterAlert=None, SqResponseInterval=None, SqTransmissionCount=None, StartupQueryCount=None, SupportElection=None, SupportOlderVersionHost=None, SupportOlderVersionQuerier=None, Version=None):
		"""Finds and retrieves querier data from the server.

		All named parameters support regex and can be used to selectively retrieve querier data from the server.
		By default the find method takes no parameters and will retrieve all querier data from the server.

		Args:
			DiscardLearnedInfo (bool): If true, the Querier doesn't maintain any database and only sends periodic general queries. The specific query group/source record information isn't calculated based on any earlier received Report, but solely based on the last received report. If false, the emulated Querier maintains a complete record state for received reports and send queries (based on timer expiry for received groups and sources). Default is true.
			Enabled (bool): If true, the querier is enabled.
			GeneralQueryInterval (number): The amount of time in seconds between IGMP General Query messages sent by the querier. The default query interval is 125 seconds.
			GqResponseInterval (number): The maximum amount of time in seconds that the IGMP querier waits to receive a response to a General Query message. The default query response interval is 10000 milliseconds and must be less than the query interval.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The interface associated with the IGMP querier. The interface must be previously configured.
			InterfaceIndex (number): The assigned protocol interface ID for this SM interface.
			InterfaceType (str): Indicates the type of network for the interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IsQuerier (bool): If true, this IGMP entity is a querier.
			IsRefreshComplete (bool): If true, the querier information is current.
			QuerierAddress (str): The querier IP address.
			QuerierWorkingVersion (number): The querier working IGMP version.
			RobustnessVariable (number): Defines the subnet vulnerability to lost packets. IGMP can recover from robustness variable minus 1 lost IGMP packets. The robustness variable should be set to a value of 2 or greater. The default robustness variable value is 2.
			RouterAlert (bool): If true, sets the Send Router Alert bit in the IP header.
			SqResponseInterval (number): The maximum amount of time in seconds that the IGMP querier waits to receive a response to a Specific Query message. The default query response interval is 1000 milliseconds and must be less than the query interval.
			SqTransmissionCount (number): Indicates the total number of specific Query messagessent every Specific Query Response Interval seconds before assuming that there is no interested listener for the particular group/source.
			StartupQueryCount (number): The number of general query messages sent at startup. The default startup query count is 2.
			SupportElection (bool): If true, indicates whether the Querier participates in querier election or not. If disabled, then all incoming query messages are discarded.
			SupportOlderVersionHost (bool): If true, indicates whether the Querier will comply to RFC 3376 Section 7.3.2 and RFC 3810 Section 8.3.2. If disabled, all membership reports with version less than the current version are discarded.
			SupportOlderVersionQuerier (bool): If true, indicates whether the Querier downgrades to the lowest version of received query messages. If disabled, all query messages with version less than the current version are discarded.
			Version (str(igmpv1|igmpv2|igmpv3)): Sets the version for the IGMP querier.

		Returns:
			self: This instance with matching querier data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of querier data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the querier data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		Fetches interface accessor Iface list.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=querier)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Refreshes the IGMP learned information.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=querier)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
