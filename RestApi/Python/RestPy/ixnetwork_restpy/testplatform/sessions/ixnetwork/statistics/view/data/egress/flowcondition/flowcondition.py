from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowCondition(Base):
	"""The FlowCondition class encapsulates a user managed flowCondition node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowCondition property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowCondition'

	def __init__(self, parent):
		super(FlowCondition, self).__init__(parent)

	@property
	def Operator(self):
		"""

		Returns:
			str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

	@property
	def ShowFirstMatchingSet(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showFirstMatchingSet')
	@ShowFirstMatchingSet.setter
	def ShowFirstMatchingSet(self, value):
		self._set_attribute('showFirstMatchingSet', value)

	@property
	def TrackingFilterId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)
		"""
		return self._get_attribute('trackingFilterId')
	@TrackingFilterId.setter
	def TrackingFilterId(self, value):
		self._set_attribute('trackingFilterId', value)

	@property
	def Values(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)

	def add(self, Operator=None, ShowFirstMatchingSet=None, TrackingFilterId=None, Values=None):
		"""Adds a new flowCondition node on the server and retrieves it in this instance.

		Args:
			Operator (str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)): 
			ShowFirstMatchingSet (bool): 
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): 
			Values (list(number)): 

		Returns:
			self: This instance with all currently retrieved flowCondition data using find and the newly added flowCondition data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowCondition data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Operator=None, ShowFirstMatchingSet=None, TrackingFilterId=None, Values=None):
		"""Finds and retrieves flowCondition data from the server.

		All named parameters support regex and can be used to selectively retrieve flowCondition data from the server.
		By default the find method takes no parameters and will retrieve all flowCondition data from the server.

		Args:
			Operator (str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)): 
			ShowFirstMatchingSet (bool): 
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): 
			Values (list(number)): 

		Returns:
			self: This instance with matching flowCondition data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowCondition data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowCondition data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
