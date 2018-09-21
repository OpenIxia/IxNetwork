from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OrganizationSpecificOamPduData(Base):
	"""The OrganizationSpecificOamPduData class encapsulates a user managed organizationSpecificOamPduData node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OrganizationSpecificOamPduData property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'organizationSpecificOamPduData'

	def __init__(self, parent):
		super(OrganizationSpecificOamPduData, self).__init__(parent)

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

	def add(self, Oui=None, Value=None):
		"""Adds a new organizationSpecificOamPduData node on the server and retrieves it in this instance.

		Args:
			Oui (str): 
			Value (str): 

		Returns:
			self: This instance with all currently retrieved organizationSpecificOamPduData data using find and the newly added organizationSpecificOamPduData data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the organizationSpecificOamPduData data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Oui=None, Value=None):
		"""Finds and retrieves organizationSpecificOamPduData data from the server.

		All named parameters support regex and can be used to selectively retrieve organizationSpecificOamPduData data from the server.
		By default the find method takes no parameters and will retrieve all organizationSpecificOamPduData data from the server.

		Args:
			Oui (str): 
			Value (str): 

		Returns:
			self: This instance with matching organizationSpecificOamPduData data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of organizationSpecificOamPduData data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the organizationSpecificOamPduData data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
