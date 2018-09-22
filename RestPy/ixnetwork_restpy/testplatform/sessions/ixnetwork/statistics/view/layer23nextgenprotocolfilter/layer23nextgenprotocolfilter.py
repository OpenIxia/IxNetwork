from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23NextGenProtocolFilter(Base):
	"""The Layer23NextGenProtocolFilter class encapsulates a user managed layer23NextGenProtocolFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Layer23NextGenProtocolFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'layer23NextGenProtocolFilter'

	def __init__(self, parent):
		super(Layer23NextGenProtocolFilter, self).__init__(parent)

	@property
	def AdvancedFilter(self):
		"""An instance of the AdvancedFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.advancedfilter.advancedfilter.AdvancedFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.advancedfilter.advancedfilter import AdvancedFilter
		return AdvancedFilter(self)

	@property
	def AvailableAdvancedFilterOptions(self):
		"""An instance of the AvailableAdvancedFilterOptions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.availableadvancedfilteroptions.availableadvancedfilteroptions.AvailableAdvancedFilterOptions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.availableadvancedfilteroptions.availableadvancedfilteroptions import AvailableAdvancedFilterOptions
		return AvailableAdvancedFilterOptions(self)

	@property
	def AdvancedCVFilter(self):
		"""Sets the advanced filter for a custom view. Note: To change the filter on an existing view, you must first disable it.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=advancedCVFilters)
		"""
		return self._get_attribute('advancedCVFilter')
	@AdvancedCVFilter.setter
	def AdvancedCVFilter(self, value):
		self._set_attribute('advancedCVFilter', value)

	@property
	def AdvancedFilterName(self):
		"""Selects an advanced filter from the ones available in the selected drill down view.

		Returns:
			str
		"""
		return self._get_attribute('advancedFilterName')
	@AdvancedFilterName.setter
	def AdvancedFilterName(self, value):
		self._set_attribute('advancedFilterName', value)

	@property
	def AggregationType(self):
		"""Signifies the type of aggregation of next gen protocols

		Returns:
			str(perPort|perSession)
		"""
		return self._get_attribute('aggregationType')
	@AggregationType.setter
	def AggregationType(self, value):
		self._set_attribute('aggregationType', value)

	@property
	def AllAdvancedFilters(self):
		"""Returns a list with all the filters that are present in the selected drill down views. This includes filters that cannot be applied for the current drill down view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('allAdvancedFilters')

	@property
	def MatchingAdvancedFilters(self):
		"""Returns a list that contains only the filters that can be applied on the current drill down view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('matchingAdvancedFilters')

	@property
	def PortFilterIds(self):
		"""Filters the port IDs

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])
		"""
		return self._get_attribute('portFilterIds')
	@PortFilterIds.setter
	def PortFilterIds(self, value):
		self._set_attribute('portFilterIds', value)

	@property
	def ProtocolFilterIds(self):
		"""Filters the protocol IDs

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])
		"""
		return self._get_attribute('protocolFilterIds')
	@ProtocolFilterIds.setter
	def ProtocolFilterIds(self, value):
		self._set_attribute('protocolFilterIds', value)

	def add(self, AdvancedCVFilter=None, AdvancedFilterName=None, AggregationType=None, PortFilterIds=None, ProtocolFilterIds=None):
		"""Adds a new layer23NextGenProtocolFilter node on the server and retrieves it in this instance.

		Args:
			AdvancedCVFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=advancedCVFilters)): Sets the advanced filter for a custom view. Note: To change the filter on an existing view, you must first disable it.
			AdvancedFilterName (str): Selects an advanced filter from the ones available in the selected drill down view.
			AggregationType (str(perPort|perSession)): Signifies the type of aggregation of next gen protocols
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Filters the port IDs
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Filters the protocol IDs

		Returns:
			self: This instance with all currently retrieved layer23NextGenProtocolFilter data using find and the newly added layer23NextGenProtocolFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the layer23NextGenProtocolFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvancedCVFilter=None, AdvancedFilterName=None, AggregationType=None, AllAdvancedFilters=None, MatchingAdvancedFilters=None, PortFilterIds=None, ProtocolFilterIds=None):
		"""Finds and retrieves layer23NextGenProtocolFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve layer23NextGenProtocolFilter data from the server.
		By default the find method takes no parameters and will retrieve all layer23NextGenProtocolFilter data from the server.

		Args:
			AdvancedCVFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=advancedCVFilters)): Sets the advanced filter for a custom view. Note: To change the filter on an existing view, you must first disable it.
			AdvancedFilterName (str): Selects an advanced filter from the ones available in the selected drill down view.
			AggregationType (str(perPort|perSession)): Signifies the type of aggregation of next gen protocols
			AllAdvancedFilters (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Returns a list with all the filters that are present in the selected drill down views. This includes filters that cannot be applied for the current drill down view.
			MatchingAdvancedFilters (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Returns a list that contains only the filters that can be applied on the current drill down view.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Filters the port IDs
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Filters the protocol IDs

		Returns:
			self: This instance with matching layer23NextGenProtocolFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of layer23NextGenProtocolFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the layer23NextGenProtocolFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddAdvancedFilter(self, Arg2):
		"""Executes the addAdvancedFilter operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=layer23NextGenProtocolFilter)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddAdvancedFilter', payload=locals(), response_object=None)

	def RemoveAdvancedFilter(self, Arg2):
		"""Executes the removeAdvancedFilter operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=layer23NextGenProtocolFilter)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RemoveAdvancedFilter', payload=locals(), response_object=None)

	def RemoveAllAdvancedFilters(self):
		"""Executes the removeAllAdvancedFilters operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=layer23NextGenProtocolFilter)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RemoveAllAdvancedFilters', payload=locals(), response_object=None)
