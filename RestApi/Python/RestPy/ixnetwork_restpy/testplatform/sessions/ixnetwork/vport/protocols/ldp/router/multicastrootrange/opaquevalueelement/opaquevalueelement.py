from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpaqueValueElement(Base):
	"""The OpaqueValueElement class encapsulates a user managed opaqueValueElement node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpaqueValueElement property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'opaqueValueElement'

	def __init__(self, parent):
		super(OpaqueValueElement, self).__init__(parent)

	@property
	def Increment(self):
		"""It signifies the incremented value.

		Returns:
			str
		"""
		return self._get_attribute('increment')
	@Increment.setter
	def Increment(self, value):
		self._set_attribute('increment', value)

	@property
	def Length(self):
		"""It signifies the length.

		Returns:
			number
		"""
		return self._get_attribute('length')
	@Length.setter
	def Length(self, value):
		self._set_attribute('length', value)

	@property
	def Type(self):
		"""It signifies the type.

		Returns:
			number
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def Value(self):
		"""It signifies the value.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Increment=None, Length=None, Type=None, Value=None):
		"""Adds a new opaqueValueElement node on the server and retrieves it in this instance.

		Args:
			Increment (str): It signifies the incremented value.
			Length (number): It signifies the length.
			Type (number): It signifies the type.
			Value (str): It signifies the value.

		Returns:
			self: This instance with all currently retrieved opaqueValueElement data using find and the newly added opaqueValueElement data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the opaqueValueElement data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Increment=None, Length=None, Type=None, Value=None):
		"""Finds and retrieves opaqueValueElement data from the server.

		All named parameters support regex and can be used to selectively retrieve opaqueValueElement data from the server.
		By default the find method takes no parameters and will retrieve all opaqueValueElement data from the server.

		Args:
			Increment (str): It signifies the incremented value.
			Length (number): It signifies the length.
			Type (number): It signifies the type.
			Value (str): It signifies the value.

		Returns:
			self: This instance with matching opaqueValueElement data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of opaqueValueElement data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the opaqueValueElement data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
