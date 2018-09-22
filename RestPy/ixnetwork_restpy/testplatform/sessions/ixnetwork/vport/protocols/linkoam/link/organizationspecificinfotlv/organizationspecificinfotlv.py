from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OrganizationSpecificInfoTlv(Base):
	"""The OrganizationSpecificInfoTlv class encapsulates a user managed organizationSpecificInfoTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OrganizationSpecificInfoTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'organizationSpecificInfoTlv'

	def __init__(self, parent):
		super(OrganizationSpecificInfoTlv, self).__init__(parent)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Oui(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('oui')
	@Oui.setter
	def Oui(self, value):
		self._set_attribute('oui', value)

	@property
	def Value(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Enabled=None, Oui=None, Value=None):
		"""Adds a new organizationSpecificInfoTlv node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			Oui (str): 
			Value (str): 

		Returns:
			self: This instance with all currently retrieved organizationSpecificInfoTlv data using find and the newly added organizationSpecificInfoTlv data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the organizationSpecificInfoTlv data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, Oui=None, Value=None):
		"""Finds and retrieves organizationSpecificInfoTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve organizationSpecificInfoTlv data from the server.
		By default the find method takes no parameters and will retrieve all organizationSpecificInfoTlv data from the server.

		Args:
			Enabled (bool): 
			Oui (str): 
			Value (str): 

		Returns:
			self: This instance with matching organizationSpecificInfoTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of organizationSpecificInfoTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the organizationSpecificInfoTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
