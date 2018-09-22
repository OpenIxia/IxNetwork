from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Level(Base):
	"""The Level class encapsulates a system managed level node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Level property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'level'

	def __init__(self, parent):
		super(Level, self).__init__(parent)

	@property
	def NodeCount(self):
		"""Number of Nodes Per Level

		Returns:
			number
		"""
		return self._get_attribute('nodeCount')
	@NodeCount.setter
	def NodeCount(self, value):
		self._set_attribute('nodeCount', value)

	def find(self, NodeCount=None):
		"""Finds and retrieves level data from the server.

		All named parameters support regex and can be used to selectively retrieve level data from the server.
		By default the find method takes no parameters and will retrieve all level data from the server.

		Args:
			NodeCount (number): Number of Nodes Per Level

		Returns:
			self: This instance with matching level data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of level data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the level data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
