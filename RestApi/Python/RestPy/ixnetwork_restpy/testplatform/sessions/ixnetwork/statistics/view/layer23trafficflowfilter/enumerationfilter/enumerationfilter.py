from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EnumerationFilter(Base):
	"""The EnumerationFilter class encapsulates a user managed enumerationFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EnumerationFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'enumerationFilter'

	def __init__(self, parent):
		super(EnumerationFilter, self).__init__(parent)

	@property
	def SortDirection(self):
		"""Sets the display order of the view.

		Returns:
			str(ascending|descending)
		"""
		return self._get_attribute('sortDirection')
	@SortDirection.setter
	def SortDirection(self, value):
		self._set_attribute('sortDirection', value)

	@property
	def TrackingFilterId(self):
		"""Selected tracking filters from the availableTrackingFilter list.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)
		"""
		return self._get_attribute('trackingFilterId')
	@TrackingFilterId.setter
	def TrackingFilterId(self, value):
		self._set_attribute('trackingFilterId', value)

	def add(self, SortDirection=None, TrackingFilterId=None):
		"""Adds a new enumerationFilter node on the server and retrieves it in this instance.

		Args:
			SortDirection (str(ascending|descending)): Sets the display order of the view.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.

		Returns:
			self: This instance with all currently retrieved enumerationFilter data using find and the newly added enumerationFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the enumerationFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, SortDirection=None, TrackingFilterId=None):
		"""Finds and retrieves enumerationFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve enumerationFilter data from the server.
		By default the find method takes no parameters and will retrieve all enumerationFilter data from the server.

		Args:
			SortDirection (str(ascending|descending)): Sets the display order of the view.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.

		Returns:
			self: This instance with matching enumerationFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of enumerationFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the enumerationFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
