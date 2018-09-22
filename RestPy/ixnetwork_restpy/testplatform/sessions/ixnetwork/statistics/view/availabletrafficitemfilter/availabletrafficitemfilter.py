from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableTrafficItemFilter(Base):
	"""The AvailableTrafficItemFilter class encapsulates a system managed availableTrafficItemFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableTrafficItemFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'availableTrafficItemFilter'

	def __init__(self, parent):
		super(AvailableTrafficItemFilter, self).__init__(parent)

	@property
	def Constraints(self):
		"""Lists down the constraints associated with the available traffic item filter list.

		Returns:
			list(str)
		"""
		return self._get_attribute('constraints')

	@property
	def Name(self):
		"""Displays the name of the traffic item filter.

		Returns:
			str
		"""
		return self._get_attribute('name')

	def find(self, Constraints=None, Name=None):
		"""Finds and retrieves availableTrafficItemFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve availableTrafficItemFilter data from the server.
		By default the find method takes no parameters and will retrieve all availableTrafficItemFilter data from the server.

		Args:
			Constraints (list(str)): Lists down the constraints associated with the available traffic item filter list.
			Name (str): Displays the name of the traffic item filter.

		Returns:
			self: This instance with matching availableTrafficItemFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of availableTrafficItemFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the availableTrafficItemFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
