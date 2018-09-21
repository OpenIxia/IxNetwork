from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AdvancedFilter(Base):
	"""The AdvancedFilter class encapsulates a user managed advancedFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdvancedFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'advancedFilter'

	def __init__(self, parent):
		super(AdvancedFilter, self).__init__(parent)

	@property
	def Expression(self):
		"""Specifies the filter body. This is a string that must have a specific format.This can be empty (no filter). The available operations and statistics can be obtained from availableAdvancedFilterOptions.

		Returns:
			str
		"""
		return self._get_attribute('expression')
	@Expression.setter
	def Expression(self, value):
		self._set_attribute('expression', value)

	@property
	def Name(self):
		"""Specifies the filter name. It must be unique per view.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def SortingStats(self):
		"""Specifies the list of statistics by which the view will be sorted.

		Returns:
			str
		"""
		return self._get_attribute('sortingStats')
	@SortingStats.setter
	def SortingStats(self, value):
		self._set_attribute('sortingStats', value)

	@property
	def TrackingFilterId(self):
		"""Gets the id of the filter, which is used to add the filter to a view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('trackingFilterId')
	@TrackingFilterId.setter
	def TrackingFilterId(self, value):
		self._set_attribute('trackingFilterId', value)

	def add(self, Expression=None, Name=None, SortingStats=None, TrackingFilterId=None):
		"""Adds a new advancedFilter node on the server and retrieves it in this instance.

		Args:
			Expression (str): Specifies the filter body. This is a string that must have a specific format.This can be empty (no filter). The available operations and statistics can be obtained from availableAdvancedFilterOptions.
			Name (str): Specifies the filter name. It must be unique per view.
			SortingStats (str): Specifies the list of statistics by which the view will be sorted.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Gets the id of the filter, which is used to add the filter to a view.

		Returns:
			self: This instance with all currently retrieved advancedFilter data using find and the newly added advancedFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the advancedFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Expression=None, Name=None, SortingStats=None, TrackingFilterId=None):
		"""Finds and retrieves advancedFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve advancedFilter data from the server.
		By default the find method takes no parameters and will retrieve all advancedFilter data from the server.

		Args:
			Expression (str): Specifies the filter body. This is a string that must have a specific format.This can be empty (no filter). The available operations and statistics can be obtained from availableAdvancedFilterOptions.
			Name (str): Specifies the filter name. It must be unique per view.
			SortingStats (str): Specifies the list of statistics by which the view will be sorted.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Gets the id of the filter, which is used to add the filter to a view.

		Returns:
			self: This instance with matching advancedFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of advancedFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the advancedFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
