from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DeadFlowsFilter(Base):
	"""The DeadFlowsFilter class encapsulates a user managed deadFlowsFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DeadFlowsFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'deadFlowsFilter'

	def __init__(self, parent):
		super(DeadFlowsFilter, self).__init__(parent)

	@property
	def NumberOfResults(self):
		"""Number of traffic flows to be displayed.

		Returns:
			number
		"""
		return self._get_attribute('numberOfResults')
	@NumberOfResults.setter
	def NumberOfResults(self, value):
		self._set_attribute('numberOfResults', value)

	@property
	def SortingCondition(self):
		"""Sets the display order of the view.

		Returns:
			str(ascending|descending)
		"""
		return self._get_attribute('sortingCondition')
	@SortingCondition.setter
	def SortingCondition(self, value):
		self._set_attribute('sortingCondition', value)

	def add(self, NumberOfResults=None, SortingCondition=None):
		"""Adds a new deadFlowsFilter node on the server and retrieves it in this instance.

		Args:
			NumberOfResults (number): Number of traffic flows to be displayed.
			SortingCondition (str(ascending|descending)): Sets the display order of the view.

		Returns:
			self: This instance with all currently retrieved deadFlowsFilter data using find and the newly added deadFlowsFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the deadFlowsFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, NumberOfResults=None, SortingCondition=None):
		"""Finds and retrieves deadFlowsFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve deadFlowsFilter data from the server.
		By default the find method takes no parameters and will retrieve all deadFlowsFilter data from the server.

		Args:
			NumberOfResults (number): Number of traffic flows to be displayed.
			SortingCondition (str(ascending|descending)): Sets the display order of the view.

		Returns:
			self: This instance with matching deadFlowsFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of deadFlowsFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the deadFlowsFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
