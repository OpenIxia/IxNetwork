from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UserDefinedAfiSafi(Base):
	"""The UserDefinedAfiSafi class encapsulates a user managed userDefinedAfiSafi node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UserDefinedAfiSafi property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'userDefinedAfiSafi'

	def __init__(self, parent):
		super(UserDefinedAfiSafi, self).__init__(parent)

	@property
	def UserDefinedAfiSafiRoutes(self):
		"""An instance of the UserDefinedAfiSafiRoutes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.userdefinedafisafiroutes.UserDefinedAfiSafiRoutes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.userdefinedafisafiroutes import UserDefinedAfiSafiRoutes
		return UserDefinedAfiSafiRoutes(self)

	@property
	def Afi(self):
		"""The 2 byte AFI value.

		Returns:
			number
		"""
		return self._get_attribute('afi')
	@Afi.setter
	def Afi(self, value):
		self._set_attribute('afi', value)

	@property
	def Safi(self):
		"""The 1 byte SAFI value.

		Returns:
			number
		"""
		return self._get_attribute('safi')
	@Safi.setter
	def Safi(self, value):
		self._set_attribute('safi', value)

	def add(self, Afi=None, Safi=None):
		"""Adds a new userDefinedAfiSafi node on the server and retrieves it in this instance.

		Args:
			Afi (number): The 2 byte AFI value.
			Safi (number): The 1 byte SAFI value.

		Returns:
			self: This instance with all currently retrieved userDefinedAfiSafi data using find and the newly added userDefinedAfiSafi data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the userDefinedAfiSafi data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Afi=None, Safi=None):
		"""Finds and retrieves userDefinedAfiSafi data from the server.

		All named parameters support regex and can be used to selectively retrieve userDefinedAfiSafi data from the server.
		By default the find method takes no parameters and will retrieve all userDefinedAfiSafi data from the server.

		Args:
			Afi (number): The 2 byte AFI value.
			Safi (number): The 1 byte SAFI value.

		Returns:
			self: This instance with matching userDefinedAfiSafi data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of userDefinedAfiSafi data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the userDefinedAfiSafi data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
