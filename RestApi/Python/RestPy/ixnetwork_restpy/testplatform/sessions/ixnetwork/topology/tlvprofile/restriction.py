from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Restriction(Base):
	"""The Restriction class encapsulates a system managed restriction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Restriction property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'restriction'

	def __init__(self, parent):
		super(Restriction, self).__init__(parent)

	@property
	def Enum(self):
		"""Internal enumeration type to be used as value options

		Returns:
			str
		"""
		return self._get_attribute('enum')
	@Enum.setter
	def Enum(self, value):
		self._set_attribute('enum', value)

	@property
	def SingleValue(self):
		"""Restricts the field to single value pattern without overlays

		Returns:
			bool
		"""
		return self._get_attribute('singleValue')
	@SingleValue.setter
	def SingleValue(self, value):
		self._set_attribute('singleValue', value)

	def find(self, Enum=None, SingleValue=None):
		"""Finds and retrieves restriction data from the server.

		All named parameters support regex and can be used to selectively retrieve restriction data from the server.
		By default the find method takes no parameters and will retrieve all restriction data from the server.

		Args:
			Enum (str): Internal enumeration type to be used as value options
			SingleValue (bool): Restricts the field to single value pattern without overlays

		Returns:
			self: This instance with matching restriction data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of restriction data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the restriction data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
