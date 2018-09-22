from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AppLibProfile(Base):
	"""The AppLibProfile class encapsulates a user managed appLibProfile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AppLibProfile property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'appLibProfile'

	def __init__(self, parent):
		super(AppLibProfile, self).__init__(parent)

	@property
	def AppLibFlow(self):
		"""An instance of the AppLibFlow class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.applibflow.AppLibFlow)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.applibflow import AppLibFlow
		return AppLibFlow(self)

	@property
	def AvailableFlows(self):
		"""(Read only) All available application library flows.

		Returns:
			list(str[])
		"""
		return self._get_attribute('availableFlows')

	@property
	def ConfiguredFlows(self):
		"""Configured application library flows within profile.

		Returns:
			list(str[])
		"""
		return self._get_attribute('configuredFlows')
	@ConfiguredFlows.setter
	def ConfiguredFlows(self, value):
		self._set_attribute('configuredFlows', value)

	@property
	def EnablePerIPStats(self):
		"""Enable Per IP Stats. When true then Per IP statistic drilldown is available.

		Returns:
			bool
		"""
		return self._get_attribute('enablePerIPStats')
	@EnablePerIPStats.setter
	def EnablePerIPStats(self, value):
		self._set_attribute('enablePerIPStats', value)

	@property
	def ObjectiveDistribution(self):
		"""Objective distribution value.

		Returns:
			str(applyFullObjectiveToEachPort|splitObjectiveEvenlyAmongPorts)
		"""
		return self._get_attribute('objectiveDistribution')
	@ObjectiveDistribution.setter
	def ObjectiveDistribution(self, value):
		self._set_attribute('objectiveDistribution', value)

	@property
	def ObjectiveType(self):
		"""The objective type of the test.A Test Objective is the way the user sets the actual rate of the Application Library Traffic transmission.

		Returns:
			str(simulatedUsers|throughputGbps|throughputKbps|throughputMbps)
		"""
		return self._get_attribute('objectiveType')
	@ObjectiveType.setter
	def ObjectiveType(self, value):
		self._set_attribute('objectiveType', value)

	@property
	def ObjectiveValue(self):
		"""The absolute value of either simulated users or throughput in its measure unit.

		Returns:
			number
		"""
		return self._get_attribute('objectiveValue')
	@ObjectiveValue.setter
	def ObjectiveValue(self, value):
		self._set_attribute('objectiveValue', value)

	@property
	def TrafficState(self):
		"""(Read only) A read-only field which indicates the current state of the traffic item.

		Returns:
			str(Configured|Interim|Running|Unconfigured)
		"""
		return self._get_attribute('trafficState')

	def add(self, ConfiguredFlows=None, EnablePerIPStats=None, ObjectiveDistribution=None, ObjectiveType=None, ObjectiveValue=None):
		"""Adds a new appLibProfile node on the server and retrieves it in this instance.

		Args:
			ConfiguredFlows (list(str[])): Configured application library flows within profile.
			EnablePerIPStats (bool): Enable Per IP Stats. When true then Per IP statistic drilldown is available.
			ObjectiveDistribution (str(applyFullObjectiveToEachPort|splitObjectiveEvenlyAmongPorts)): Objective distribution value.
			ObjectiveType (str(simulatedUsers|throughputGbps|throughputKbps|throughputMbps)): The objective type of the test.A Test Objective is the way the user sets the actual rate of the Application Library Traffic transmission.
			ObjectiveValue (number): The absolute value of either simulated users or throughput in its measure unit.

		Returns:
			self: This instance with all currently retrieved appLibProfile data using find and the newly added appLibProfile data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the appLibProfile data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AvailableFlows=None, ConfiguredFlows=None, EnablePerIPStats=None, ObjectiveDistribution=None, ObjectiveType=None, ObjectiveValue=None, TrafficState=None):
		"""Finds and retrieves appLibProfile data from the server.

		All named parameters support regex and can be used to selectively retrieve appLibProfile data from the server.
		By default the find method takes no parameters and will retrieve all appLibProfile data from the server.

		Args:
			AvailableFlows (list(str[])): (Read only) All available application library flows.
			ConfiguredFlows (list(str[])): Configured application library flows within profile.
			EnablePerIPStats (bool): Enable Per IP Stats. When true then Per IP statistic drilldown is available.
			ObjectiveDistribution (str(applyFullObjectiveToEachPort|splitObjectiveEvenlyAmongPorts)): Objective distribution value.
			ObjectiveType (str(simulatedUsers|throughputGbps|throughputKbps|throughputMbps)): The objective type of the test.A Test Objective is the way the user sets the actual rate of the Application Library Traffic transmission.
			ObjectiveValue (number): The absolute value of either simulated users or throughput in its measure unit.
			TrafficState (str(Configured|Interim|Running|Unconfigured)): (Read only) A read-only field which indicates the current state of the traffic item.

		Returns:
			self: This instance with matching appLibProfile data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of appLibProfile data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the appLibProfile data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddAppLibraryFlow(self, Arg2):
		"""Executes the addAppLibraryFlow operation on the server.

		This exec adds a flow to an application traffic profile.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=appLibProfile)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(str[])): This object specifies the flow(s) to be added.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddAppLibraryFlow', payload=locals(), response_object=None)

	def DistributeFlowsEvenly(self):
		"""Executes the distributeFlowsEvenly operation on the server.

		This exec distributes the percentage for each flow evenly.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=appLibProfile)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DistributeFlowsEvenly', payload=locals(), response_object=None)

	def RemoveAppLibraryFlow(self, Arg2):
		"""Executes the removeAppLibraryFlow operation on the server.

		This exec removes a flow from an application traffic profile.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=appLibProfile)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(str[])): This object specifies the flow(s) to be removed.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RemoveAppLibraryFlow', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		This exec starts running the configured application traffic.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=appLibProfile)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This exec stops the configured application traffic from running.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=appLibProfile)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
