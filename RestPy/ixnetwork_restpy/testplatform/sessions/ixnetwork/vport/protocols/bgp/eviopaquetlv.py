from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EviOpaqueTlv(Base):
	"""The EviOpaqueTlv class encapsulates a user managed eviOpaqueTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EviOpaqueTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'eviOpaqueTlv'

	def __init__(self, parent):
		super(EviOpaqueTlv, self).__init__(parent)

	@property
	def Length(self):
		"""The length of the TLV.

		Returns:
			number
		"""
		return self._get_attribute('length')
	@Length.setter
	def Length(self, value):
		self._set_attribute('length', value)

	@property
	def Type(self):
		"""The type of TLV.

		Returns:
			number
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def Value(self):
		"""The value of the TLV.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Length=None, Type=None, Value=None):
		"""Adds a new eviOpaqueTlv node on the server and retrieves it in this instance.

		Args:
			Length (number): The length of the TLV.
			Type (number): The type of TLV.
			Value (str): The value of the TLV.

		Returns:
			self: This instance with all currently retrieved eviOpaqueTlv data using find and the newly added eviOpaqueTlv data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the eviOpaqueTlv data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Length=None, Type=None, Value=None):
		"""Finds and retrieves eviOpaqueTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve eviOpaqueTlv data from the server.
		By default the find method takes no parameters and will retrieve all eviOpaqueTlv data from the server.

		Args:
			Length (number): The length of the TLV.
			Type (number): The type of TLV.
			Value (str): The value of the TLV.

		Returns:
			self: This instance with matching eviOpaqueTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of eviOpaqueTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the eviOpaqueTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
