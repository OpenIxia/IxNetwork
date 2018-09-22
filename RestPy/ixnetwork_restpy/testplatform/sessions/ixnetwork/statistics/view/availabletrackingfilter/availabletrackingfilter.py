from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableTrackingFilter(Base):
	"""The AvailableTrackingFilter class encapsulates a system managed availableTrackingFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableTrackingFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'availableTrackingFilter'

	def __init__(self, parent):
		super(AvailableTrackingFilter, self).__init__(parent)

	@property
	def Constraints(self):
		"""Lists down the constraints associated with the available tracking filter list.

		Returns:
			list(str)
		"""
		return self._get_attribute('constraints')

	@property
	def Name(self):
		"""Displays the name of the tracking filter.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def TrackingType(self):
		"""Indicates the tracking type.

		Returns:
			str
		"""
		return self._get_attribute('trackingType')

	@property
	def ValueType(self):
		"""Value of tracking to be matched based on operator.

		Returns:
			str
		"""
		return self._get_attribute('valueType')

	def find(self, Constraints=None, Name=None, TrackingType=None, ValueType=None):
		"""Finds and retrieves availableTrackingFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve availableTrackingFilter data from the server.
		By default the find method takes no parameters and will retrieve all availableTrackingFilter data from the server.

		Args:
			Constraints (list(str)): Lists down the constraints associated with the available tracking filter list.
			Name (str): Displays the name of the tracking filter.
			TrackingType (str): Indicates the tracking type.
			ValueType (str): Value of tracking to be matched based on operator.

		Returns:
			self: This instance with matching availableTrackingFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of availableTrackingFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the availableTrackingFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
