from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Arp(Base):
	"""The Arp class encapsulates a user managed arp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Arp property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'arp'

	def __init__(self, parent):
		super(Arp, self).__init__(parent)

	@property
	def Enabled(self):
		"""(Non-POS cards only) Enables ARP requests and responses for this port. ARP requests are received at the MAC level.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	def add(self, Enabled=None):
		"""Adds a new arp node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): (Non-POS cards only) Enables ARP requests and responses for this port. ARP requests are received at the MAC level.

		Returns:
			self: This instance with all currently retrieved arp data using find and the newly added arp data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the arp data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None):
		"""Finds and retrieves arp data from the server.

		All named parameters support regex and can be used to selectively retrieve arp data from the server.
		By default the find method takes no parameters and will retrieve all arp data from the server.

		Args:
			Enabled (bool): (Non-POS cards only) Enables ARP requests and responses for this port. ARP requests are received at the MAC level.

		Returns:
			self: This instance with matching arp data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of arp data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the arp data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
