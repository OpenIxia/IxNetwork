from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Hex(Base):
	"""The Hex class encapsulates a system managed hex node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Hex property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'hex'

	def __init__(self, parent):
		super(Hex, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter default value.

		Returns:
			str
		"""
		return self._get_attribute('default')

	@property
	def Value(self):
		"""Parameter hex value.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def find(self, Default=None, Value=None):
		"""Finds and retrieves hex data from the server.

		All named parameters support regex and can be used to selectively retrieve hex data from the server.
		By default the find method takes no parameters and will retrieve all hex data from the server.

		Args:
			Default (str): (Read only) Parameter default value.
			Value (str): Parameter hex value.

		Returns:
			self: This instance with matching hex data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of hex data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the hex data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
