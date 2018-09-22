from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpaqueValueElement(Base):
	"""The OpaqueValueElement class encapsulates a system managed opaqueValueElement node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpaqueValueElement property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'opaqueValueElement'

	def __init__(self, parent):
		super(OpaqueValueElement, self).__init__(parent)

	@property
	def Length(self):
		"""Signifies the length.

		Returns:
			number
		"""
		return self._get_attribute('length')

	@property
	def Type(self):
		"""Signifies teh type.

		Returns:
			number
		"""
		return self._get_attribute('type')

	@property
	def Value(self):
		"""Signifies the value.

		Returns:
			str
		"""
		return self._get_attribute('value')

	def find(self, Length=None, Type=None, Value=None):
		"""Finds and retrieves opaqueValueElement data from the server.

		All named parameters support regex and can be used to selectively retrieve opaqueValueElement data from the server.
		By default the find method takes no parameters and will retrieve all opaqueValueElement data from the server.

		Args:
			Length (number): Signifies the length.
			Type (number): Signifies teh type.
			Value (str): Signifies the value.

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
