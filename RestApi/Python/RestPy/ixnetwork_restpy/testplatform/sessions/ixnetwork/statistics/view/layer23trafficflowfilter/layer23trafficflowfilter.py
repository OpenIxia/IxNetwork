from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23TrafficFlowFilter(Base):
	"""The Layer23TrafficFlowFilter class encapsulates a user managed layer23TrafficFlowFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Layer23TrafficFlowFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'layer23TrafficFlowFilter'

	def __init__(self, parent):
		super(Layer23TrafficFlowFilter, self).__init__(parent)

	@property
	def EnumerationFilter(self):
		"""An instance of the EnumerationFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.enumerationfilter.enumerationfilter.EnumerationFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.enumerationfilter.enumerationfilter import EnumerationFilter
		return EnumerationFilter(self)

	@property
	def TrackingFilter(self):
		"""An instance of the TrackingFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.trackingfilter.trackingfilter.TrackingFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.trackingfilter.trackingfilter import TrackingFilter
		return TrackingFilter(self)

	@property
	def AggregatedAcrossPorts(self):
		"""If true, displays aggregated stat value across ports selected by portFilterIds. Default = false

		Returns:
			bool
		"""
		return self._get_attribute('aggregatedAcrossPorts')
	@AggregatedAcrossPorts.setter
	def AggregatedAcrossPorts(self, value):
		self._set_attribute('aggregatedAcrossPorts', value)

	@property
	def EgressLatencyBinDisplayOption(self):
		"""Emulates Latency Bin SV or Egress Tracking SV.

		Returns:
			str(none|showEgressFlatView|showEgressRows|showLatencyBinStats)
		"""
		return self._get_attribute('egressLatencyBinDisplayOption')
	@EgressLatencyBinDisplayOption.setter
	def EgressLatencyBinDisplayOption(self, value):
		self._set_attribute('egressLatencyBinDisplayOption', value)

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
	def TrafficItemFilterId(self):
		"""Selected traffic item filter from the availableTrafficItemFilter list.

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

	def add(self, AggregatedAcrossPorts=None, EgressLatencyBinDisplayOption=None, PortFilterIds=None, TrafficItemFilterId=None, TrafficItemFilterIds=None):
		"""Adds a new layer23TrafficFlowFilter node on the server and retrieves it in this instance.

		Args:
			AggregatedAcrossPorts (bool): If true, displays aggregated stat value across ports selected by portFilterIds. Default = false
			EgressLatencyBinDisplayOption (str(none|showEgressFlatView|showEgressRows|showLatencyBinStats)): Emulates Latency Bin SV or Egress Tracking SV.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.
			TrafficItemFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)): Selected traffic item filter from the availableTrafficItemFilter list.
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			self: This instance with all currently retrieved layer23TrafficFlowFilter data using find and the newly added layer23TrafficFlowFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the layer23TrafficFlowFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AggregatedAcrossPorts=None, EgressLatencyBinDisplayOption=None, PortFilterIds=None, TrafficItemFilterId=None, TrafficItemFilterIds=None):
		"""Finds and retrieves layer23TrafficFlowFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve layer23TrafficFlowFilter data from the server.
		By default the find method takes no parameters and will retrieve all layer23TrafficFlowFilter data from the server.

		Args:
			AggregatedAcrossPorts (bool): If true, displays aggregated stat value across ports selected by portFilterIds. Default = false
			EgressLatencyBinDisplayOption (str(none|showEgressFlatView|showEgressRows|showLatencyBinStats)): Emulates Latency Bin SV or Egress Tracking SV.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.
			TrafficItemFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)): Selected traffic item filter from the availableTrafficItemFilter list.
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			self: This instance with matching layer23TrafficFlowFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of layer23TrafficFlowFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the layer23TrafficFlowFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
