from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23TrafficFlowDetectiveFilter(Base):
	"""The Layer23TrafficFlowDetectiveFilter class encapsulates a user managed layer23TrafficFlowDetectiveFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Layer23TrafficFlowDetectiveFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'layer23TrafficFlowDetectiveFilter'

	def __init__(self, parent):
		super(Layer23TrafficFlowDetectiveFilter, self).__init__(parent)

	@property
	def AllFlowsFilter(self):
		"""An instance of the AllFlowsFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.allflowsfilter.allflowsfilter.AllFlowsFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.allflowsfilter.allflowsfilter import AllFlowsFilter
		return AllFlowsFilter(self)

	@property
	def DeadFlowsFilter(self):
		"""An instance of the DeadFlowsFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.deadflowsfilter.deadflowsfilter.DeadFlowsFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.deadflowsfilter.deadflowsfilter import DeadFlowsFilter
		return DeadFlowsFilter(self)

	@property
	def LiveFlowsFilter(self):
		"""An instance of the LiveFlowsFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.liveflowsfilter.liveflowsfilter.LiveFlowsFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.liveflowsfilter.liveflowsfilter import LiveFlowsFilter
		return LiveFlowsFilter(self)

	@property
	def StatisticFilter(self):
		"""An instance of the StatisticFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.statisticfilter.statisticfilter.StatisticFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.statisticfilter.statisticfilter import StatisticFilter
		return StatisticFilter(self)

	@property
	def TrackingFilter(self):
		"""An instance of the TrackingFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.trackingfilter.trackingfilter.TrackingFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.trackingfilter.trackingfilter import TrackingFilter
		return TrackingFilter(self)

	@property
	def DeadFlowsCount(self):
		"""The number of flows declared dead. A flow is declared dead if no traffic is received for a specified number of seconds. To change this threshold use the deadFlowsThreshold attribute.

		Returns:
			number
		"""
		return self._get_attribute('deadFlowsCount')

	@property
	def DeadFlowsThreshold(self):
		"""Threshold in seconds after which the flows are declared dead if there are no packets received for a specified number of seconds. This is a global attibute and hence the latest value entered takes precedence over previous values in all the custom views.

		Returns:
			number
		"""
		return self._get_attribute('deadFlowsThreshold')
	@DeadFlowsThreshold.setter
	def DeadFlowsThreshold(self, value):
		self._set_attribute('deadFlowsThreshold', value)

	@property
	def FlowFilterType(self):
		"""Indicates the flow detective filter settings.

		Returns:
			str(allFlows|deadFlows|liveFlows)
		"""
		return self._get_attribute('flowFilterType')
	@FlowFilterType.setter
	def FlowFilterType(self, value):
		self._set_attribute('flowFilterType', value)

	@property
	def PortFilterIds(self):
		"""Selected port filters from the availablePortFilter list.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])
		"""
		return self._get_attribute('portFilterIds')
	@PortFilterIds.setter
	def PortFilterIds(self, value):
		self._set_attribute('portFilterIds', value)

	@property
	def ShowEgressFlows(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('showEgressFlows')
	@ShowEgressFlows.setter
	def ShowEgressFlows(self, value):
		self._set_attribute('showEgressFlows', value)

	@property
	def TrafficItemFilterId(self):
		"""Selected traffic flow detective filter from the availableTrafficItemFilter list.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)
		"""
		return self._get_attribute('trafficItemFilterId')
	@TrafficItemFilterId.setter
	def TrafficItemFilterId(self, value):
		self._set_attribute('trafficItemFilterId', value)

	@property
	def TrafficItemFilterIds(self):
		"""Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])
		"""
		return self._get_attribute('trafficItemFilterIds')
	@TrafficItemFilterIds.setter
	def TrafficItemFilterIds(self, value):
		self._set_attribute('trafficItemFilterIds', value)

	def add(self, DeadFlowsThreshold=None, FlowFilterType=None, PortFilterIds=None, ShowEgressFlows=None, TrafficItemFilterId=None, TrafficItemFilterIds=None):
		"""Adds a new layer23TrafficFlowDetectiveFilter node on the server and retrieves it in this instance.

		Args:
			DeadFlowsThreshold (number): Threshold in seconds after which the flows are declared dead if there are no packets received for a specified number of seconds. This is a global attibute and hence the latest value entered takes precedence over previous values in all the custom views.
			FlowFilterType (str(allFlows|deadFlows|liveFlows)): Indicates the flow detective filter settings.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.
			ShowEgressFlows (bool): NOT DEFINED
			TrafficItemFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)): Selected traffic flow detective filter from the availableTrafficItemFilter list.
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			self: This instance with all currently retrieved layer23TrafficFlowDetectiveFilter data using find and the newly added layer23TrafficFlowDetectiveFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the layer23TrafficFlowDetectiveFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DeadFlowsCount=None, DeadFlowsThreshold=None, FlowFilterType=None, PortFilterIds=None, ShowEgressFlows=None, TrafficItemFilterId=None, TrafficItemFilterIds=None):
		"""Finds and retrieves layer23TrafficFlowDetectiveFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve layer23TrafficFlowDetectiveFilter data from the server.
		By default the find method takes no parameters and will retrieve all layer23TrafficFlowDetectiveFilter data from the server.

		Args:
			DeadFlowsCount (number): The number of flows declared dead. A flow is declared dead if no traffic is received for a specified number of seconds. To change this threshold use the deadFlowsThreshold attribute.
			DeadFlowsThreshold (number): Threshold in seconds after which the flows are declared dead if there are no packets received for a specified number of seconds. This is a global attibute and hence the latest value entered takes precedence over previous values in all the custom views.
			FlowFilterType (str(allFlows|deadFlows|liveFlows)): Indicates the flow detective filter settings.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.
			ShowEgressFlows (bool): NOT DEFINED
			TrafficItemFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)): Selected traffic flow detective filter from the availableTrafficItemFilter list.
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			self: This instance with matching layer23TrafficFlowDetectiveFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of layer23TrafficFlowDetectiveFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the layer23TrafficFlowDetectiveFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
