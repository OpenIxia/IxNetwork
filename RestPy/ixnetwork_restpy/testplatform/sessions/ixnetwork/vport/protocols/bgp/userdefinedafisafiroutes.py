from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UserDefinedAfiSafiRoutes(Base):
	"""The UserDefinedAfiSafiRoutes class encapsulates a user managed userDefinedAfiSafiRoutes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UserDefinedAfiSafiRoutes property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'userDefinedAfiSafiRoutes'

	def __init__(self, parent):
		super(UserDefinedAfiSafiRoutes, self).__init__(parent)

	@property
	def Data(self):
		"""Data to be transmitted for AFI/SAFI, and regular enable-disable.

		Returns:
			str
		"""
		return self._get_attribute('data')
	@Data.setter
	def Data(self, value):
		self._set_attribute('data', value)

	@property
	def Enabled(self):
		"""If true, the user-defined afi/safi is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Length(self):
		"""The data is padded up to length with left alignment otherwise chopped till length.

		Returns:
			number
		"""
		return self._get_attribute('length')
	@Length.setter
	def Length(self, value):
		self._set_attribute('length', value)

	def add(self, Data=None, Enabled=None, Length=None):
		"""Adds a new userDefinedAfiSafiRoutes node on the server and retrieves it in this instance.

		Args:
			Data (str): Data to be transmitted for AFI/SAFI, and regular enable-disable.
			Enabled (bool): If true, the user-defined afi/safi is enabled.
			Length (number): The data is padded up to length with left alignment otherwise chopped till length.

		Returns:
			self: This instance with all currently retrieved userDefinedAfiSafiRoutes data using find and the newly added userDefinedAfiSafiRoutes data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the userDefinedAfiSafiRoutes data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Data=None, Enabled=None, Length=None):
		"""Finds and retrieves userDefinedAfiSafiRoutes data from the server.

		All named parameters support regex and can be used to selectively retrieve userDefinedAfiSafiRoutes data from the server.
		By default the find method takes no parameters and will retrieve all userDefinedAfiSafiRoutes data from the server.

		Args:
			Data (str): Data to be transmitted for AFI/SAFI, and regular enable-disable.
			Enabled (bool): If true, the user-defined afi/safi is enabled.
			Length (number): The data is padded up to length with left alignment otherwise chopped till length.

		Returns:
			self: This instance with matching userDefinedAfiSafiRoutes data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of userDefinedAfiSafiRoutes data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the userDefinedAfiSafiRoutes data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
