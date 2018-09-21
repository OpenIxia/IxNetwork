from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrackingFilter(Base):
	"""The TrackingFilter class encapsulates a user managed trackingFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrackingFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'trackingFilter'

	def __init__(self, parent):
		super(TrackingFilter, self).__init__(parent)

	@property
	def Operator(self):
		"""The logical operation to be performed.

		Returns:
			str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

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

	@property
	def Value(self):
		"""Value of the object

		Returns:
			list(str)
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Operator=None, TrackingFilterId=None, Value=None):
		"""Adds a new trackingFilter node on the server and retrieves it in this instance.

		Args:
			Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)): The logical operation to be performed.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
			Value (list(str)): Value of the object

		Returns:
			self: This instance with all currently retrieved trackingFilter data using find and the newly added trackingFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the trackingFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Operator=None, TrackingFilterId=None, Value=None):
		"""Finds and retrieves trackingFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve trackingFilter data from the server.
		By default the find method takes no parameters and will retrieve all trackingFilter data from the server.

		Args:
			Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)): The logical operation to be performed.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
			Value (list(str)): Value of the object

		Returns:
			self: This instance with matching trackingFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trackingFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trackingFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
