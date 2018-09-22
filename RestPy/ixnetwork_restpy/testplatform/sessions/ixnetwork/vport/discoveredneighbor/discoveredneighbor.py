from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DiscoveredNeighbor(Base):
	"""The DiscoveredNeighbor class encapsulates a user managed discoveredNeighbor node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DiscoveredNeighbor property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'discoveredNeighbor'

	def __init__(self, parent):
		super(DiscoveredNeighbor, self).__init__(parent)

	@property
	def IsRouter(self):
		"""(read only) Indicates if the neighbor is a router or not.

		Returns:
			str
		"""
		return self._get_attribute('isRouter')

	@property
	def LastUpdate(self):
		"""(read only) Indicates when the last update for the neighbor happened.

		Returns:
			str
		"""
		return self._get_attribute('lastUpdate')

	@property
	def NeighborIp(self):
		"""(read only) The IP address of the neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighborIp')

	@property
	def NeighborMac(self):
		"""(read only) The MAC address of the neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighborMac')

	def add(self):
		"""Adds a new discoveredNeighbor node on the server and retrieves it in this instance.

		Returns:
			self: This instance with all currently retrieved discoveredNeighbor data using find and the newly added discoveredNeighbor data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the discoveredNeighbor data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IsRouter=None, LastUpdate=None, NeighborIp=None, NeighborMac=None):
		"""Finds and retrieves discoveredNeighbor data from the server.

		All named parameters support regex and can be used to selectively retrieve discoveredNeighbor data from the server.
		By default the find method takes no parameters and will retrieve all discoveredNeighbor data from the server.

		Args:
			IsRouter (str): (read only) Indicates if the neighbor is a router or not.
			LastUpdate (str): (read only) Indicates when the last update for the neighbor happened.
			NeighborIp (str): (read only) The IP address of the neighbor.
			NeighborMac (str): (read only) The MAC address of the neighbor.

		Returns:
			self: This instance with matching discoveredNeighbor data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of discoveredNeighbor data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the discoveredNeighbor data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
