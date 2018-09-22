from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MsAllowedEidRange(Base):
	"""The MsAllowedEidRange class encapsulates a user managed msAllowedEidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MsAllowedEidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'msAllowedEidRange'

	def __init__(self, parent):
		super(MsAllowedEidRange, self).__init__(parent)

	@property
	def Address(self):
		"""It gives details about the address

		Returns:
			str
		"""
		return self._get_attribute('address')
	@Address.setter
	def Address(self, value):
		self._set_attribute('address', value)

	@property
	def Count(self):
		"""it gives details about the count

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Enabled(self):
		"""If true, it enables the protocol

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Family(self):
		"""It details about the ip family

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('family')
	@Family.setter
	def Family(self, value):
		self._set_attribute('family', value)

	@property
	def PrefixLength(self):
		"""It gives details about the prefix length

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')
	@PrefixLength.setter
	def PrefixLength(self, value):
		self._set_attribute('prefixLength', value)

	def add(self, Address=None, Count=None, Enabled=None, Family=None, PrefixLength=None):
		"""Adds a new msAllowedEidRange node on the server and retrieves it in this instance.

		Args:
			Address (str): It gives details about the address
			Count (number): it gives details about the count
			Enabled (bool): If true, it enables the protocol
			Family (str(ipv4|ipv6)): It details about the ip family
			PrefixLength (number): It gives details about the prefix length

		Returns:
			self: This instance with all currently retrieved msAllowedEidRange data using find and the newly added msAllowedEidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the msAllowedEidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Address=None, Count=None, Enabled=None, Family=None, PrefixLength=None):
		"""Finds and retrieves msAllowedEidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve msAllowedEidRange data from the server.
		By default the find method takes no parameters and will retrieve all msAllowedEidRange data from the server.

		Args:
			Address (str): It gives details about the address
			Count (number): it gives details about the count
			Enabled (bool): If true, it enables the protocol
			Family (str(ipv4|ipv6)): It details about the ip family
			PrefixLength (number): It gives details about the prefix length

		Returns:
			self: This instance with matching msAllowedEidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of msAllowedEidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the msAllowedEidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
