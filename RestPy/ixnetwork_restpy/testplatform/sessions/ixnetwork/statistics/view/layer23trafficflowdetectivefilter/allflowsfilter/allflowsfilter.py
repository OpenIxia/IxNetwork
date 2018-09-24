from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AllFlowsFilter(Base):
	"""The AllFlowsFilter class encapsulates a user managed allFlowsFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AllFlowsFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'allFlowsFilter'

	def __init__(self, parent):
		super(AllFlowsFilter, self).__init__(parent)

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
	def SortByStatisticId(self):
		"""The reference statistic by which the data will be sorted in created SV.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)
		"""
		return self._get_attribute('sortByStatisticId')
	@SortByStatisticId.setter
	def SortByStatisticId(self, value):
		self._set_attribute('sortByStatisticId', value)

	@property
	def SortingCondition(self):
		"""Sets the display order of the view.

		Returns:
			str(bestPerformers|worstPerformers)
		"""
		return self._get_attribute('sortingCondition')
	@SortingCondition.setter
	def SortingCondition(self, value):
		self._set_attribute('sortingCondition', value)

	def add(self, NumberOfResults=None, SortByStatisticId=None, SortingCondition=None):
		"""Adds a new allFlowsFilter node on the server and retrieves it in this instance.

		Args:
			NumberOfResults (number): Number of traffic flows to be displayed.
			SortByStatisticId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)): The reference statistic by which the data will be sorted in created SV.
			SortingCondition (str(bestPerformers|worstPerformers)): Sets the display order of the view.

		Returns:
			self: This instance with all currently retrieved allFlowsFilter data using find and the newly added allFlowsFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the allFlowsFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, NumberOfResults=None, SortByStatisticId=None, SortingCondition=None):
		"""Finds and retrieves allFlowsFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve allFlowsFilter data from the server.
		By default the find method takes no parameters and will retrieve all allFlowsFilter data from the server.

		Args:
			NumberOfResults (number): Number of traffic flows to be displayed.
			SortByStatisticId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)): The reference statistic by which the data will be sorted in created SV.
			SortingCondition (str(bestPerformers|worstPerformers)): Sets the display order of the view.

		Returns:
			self: This instance with matching allFlowsFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of allFlowsFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the allFlowsFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)