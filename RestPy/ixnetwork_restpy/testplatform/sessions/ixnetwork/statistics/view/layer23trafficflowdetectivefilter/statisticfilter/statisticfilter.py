from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StatisticFilter(Base):
	"""The StatisticFilter class encapsulates a user managed statisticFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the StatisticFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'statisticFilter'

	def __init__(self, parent):
		super(StatisticFilter, self).__init__(parent)

	@property
	def Operator(self):
		"""The logical operation to be performed.

		Returns:
			str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isLike|isNotLike|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

	@property
	def StatisticFilterId(self):
		"""Selected statistic filters from the availableStatisticFilter list.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)
		"""
		return self._get_attribute('statisticFilterId')
	@StatisticFilterId.setter
	def StatisticFilterId(self, value):
		self._set_attribute('statisticFilterId', value)

	@property
	def Value(self):
		"""Value of statistic to be matched based on operator.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Operator=None, StatisticFilterId=None, Value=None):
		"""Adds a new statisticFilter node on the server and retrieves it in this instance.

		Args:
			Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isLike|isNotLike|isSmaller)): The logical operation to be performed.
			StatisticFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)): Selected statistic filters from the availableStatisticFilter list.
			Value (str): Value of statistic to be matched based on operator.

		Returns:
			self: This instance with all currently retrieved statisticFilter data using find and the newly added statisticFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the statisticFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Operator=None, StatisticFilterId=None, Value=None):
		"""Finds and retrieves statisticFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve statisticFilter data from the server.
		By default the find method takes no parameters and will retrieve all statisticFilter data from the server.

		Args:
			Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isLike|isNotLike|isSmaller)): The logical operation to be performed.
			StatisticFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)): Selected statistic filters from the availableStatisticFilter list.
			Value (str): Value of statistic to be matched based on operator.

		Returns:
			self: This instance with matching statisticFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of statisticFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the statisticFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
