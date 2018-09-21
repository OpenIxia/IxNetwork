from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Pattern(Base):
	"""The Pattern class encapsulates a user managed pattern node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Pattern property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'pattern'

	def __init__(self, parent):
		super(Pattern, self).__init__(parent)

	@property
	def BitOffset(self):
		"""Bit offset within a byte. Starting point of the mask.

		Returns:
			number
		"""
		return self._get_attribute('bitOffset')
	@BitOffset.setter
	def BitOffset(self, value):
		self._set_attribute('bitOffset', value)

	@property
	def Enabled(self):
		"""If true, match incoming packets against this pattern.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Mask(self):
		"""Bitmask to match against. Same format as value.

		Returns:
			str
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def Name(self):
		"""Name of pattern.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def Offset(self):
		"""Byte offset from start of L2 frame.

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def Value(self):
		"""The field value to match. For MAC, IPv4, and IPv6 addresses, the value is a formatted address. For all other fields, the value is encoded as a string of hex bytes, most significant byte first, and most significant bit first within each byte. Each hex byte must be exactly two hex digits; A-F and a-f are both accepted. The hex bytes must be separated by a single white space. Example: 00 01 02 FF.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	@property
	def Width(self):
		"""Width of field, in bits.

		Returns:
			number
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)

	def add(self, BitOffset=None, Enabled=None, Mask=None, Name=None, Offset=None, Value=None, Width=None):
		"""Adds a new pattern node on the server and retrieves it in this instance.

		Args:
			BitOffset (number): Bit offset within a byte. Starting point of the mask.
			Enabled (bool): If true, match incoming packets against this pattern.
			Mask (str): Bitmask to match against. Same format as value.
			Name (str): Name of pattern.
			Offset (number): Byte offset from start of L2 frame.
			Value (str): The field value to match. For MAC, IPv4, and IPv6 addresses, the value is a formatted address. For all other fields, the value is encoded as a string of hex bytes, most significant byte first, and most significant bit first within each byte. Each hex byte must be exactly two hex digits; A-F and a-f are both accepted. The hex bytes must be separated by a single white space. Example: 00 01 02 FF.
			Width (number): Width of field, in bits.

		Returns:
			self: This instance with all currently retrieved pattern data using find and the newly added pattern data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the pattern data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BitOffset=None, Enabled=None, Mask=None, Name=None, Offset=None, Value=None, Width=None):
		"""Finds and retrieves pattern data from the server.

		All named parameters support regex and can be used to selectively retrieve pattern data from the server.
		By default the find method takes no parameters and will retrieve all pattern data from the server.

		Args:
			BitOffset (number): Bit offset within a byte. Starting point of the mask.
			Enabled (bool): If true, match incoming packets against this pattern.
			Mask (str): Bitmask to match against. Same format as value.
			Name (str): Name of pattern.
			Offset (number): Byte offset from start of L2 frame.
			Value (str): The field value to match. For MAC, IPv4, and IPv6 addresses, the value is a formatted address. For all other fields, the value is encoded as a string of hex bytes, most significant byte first, and most significant bit first within each byte. Each hex byte must be exactly two hex digits; A-F and a-f are both accepted. The hex bytes must be separated by a single white space. Example: 00 01 02 FF.
			Width (number): Width of field, in bits.

		Returns:
			self: This instance with matching pattern data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pattern data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pattern data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
