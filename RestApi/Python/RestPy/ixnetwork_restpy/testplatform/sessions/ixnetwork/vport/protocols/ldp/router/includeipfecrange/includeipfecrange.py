from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IncludeIpFecRange(Base):
	"""The IncludeIpFecRange class encapsulates a user managed includeIpFecRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IncludeIpFecRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'includeIpFecRange'

	def __init__(self, parent):
		super(IncludeIpFecRange, self).__init__(parent)

	@property
	def EnableExactPrefixMatch(self):
		"""Matching for FEC address ranges, for the purpose of filtering.

		Returns:
			bool
		"""
		return self._get_attribute('enableExactPrefixMatch')
	@EnableExactPrefixMatch.setter
	def EnableExactPrefixMatch(self, value):
		self._set_attribute('enableExactPrefixMatch', value)

	@property
	def Enabled(self):
		"""Enables this explicit include FEC range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstNetwork(self):
		"""The first FEC network address in the range (in IP address format).

		Returns:
			str
		"""
		return self._get_attribute('firstNetwork')
	@FirstNetwork.setter
	def FirstNetwork(self, value):
		self._set_attribute('firstNetwork', value)

	@property
	def MaskWidth(self):
		"""The number of bits in the FEC mask applied to the FEC network address. The masked bits in the First Network address form the FEC address prefix.

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def NumberOfNetworks(self):
		"""The number of FEC network addresses to be included in the FEC range. The maximum number of valid possible addresses depends on the values for the first network and the network mask.

		Returns:
			number
		"""
		return self._get_attribute('numberOfNetworks')
	@NumberOfNetworks.setter
	def NumberOfNetworks(self, value):
		self._set_attribute('numberOfNetworks', value)

	def add(self, EnableExactPrefixMatch=None, Enabled=None, FirstNetwork=None, MaskWidth=None, NumberOfNetworks=None):
		"""Adds a new includeIpFecRange node on the server and retrieves it in this instance.

		Args:
			EnableExactPrefixMatch (bool): Matching for FEC address ranges, for the purpose of filtering.
			Enabled (bool): Enables this explicit include FEC range.
			FirstNetwork (str): The first FEC network address in the range (in IP address format).
			MaskWidth (number): The number of bits in the FEC mask applied to the FEC network address. The masked bits in the First Network address form the FEC address prefix.
			NumberOfNetworks (number): The number of FEC network addresses to be included in the FEC range. The maximum number of valid possible addresses depends on the values for the first network and the network mask.

		Returns:
			self: This instance with all currently retrieved includeIpFecRange data using find and the newly added includeIpFecRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the includeIpFecRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableExactPrefixMatch=None, Enabled=None, FirstNetwork=None, MaskWidth=None, NumberOfNetworks=None):
		"""Finds and retrieves includeIpFecRange data from the server.

		All named parameters support regex and can be used to selectively retrieve includeIpFecRange data from the server.
		By default the find method takes no parameters and will retrieve all includeIpFecRange data from the server.

		Args:
			EnableExactPrefixMatch (bool): Matching for FEC address ranges, for the purpose of filtering.
			Enabled (bool): Enables this explicit include FEC range.
			FirstNetwork (str): The first FEC network address in the range (in IP address format).
			MaskWidth (number): The number of bits in the FEC mask applied to the FEC network address. The masked bits in the First Network address form the FEC address prefix.
			NumberOfNetworks (number): The number of FEC network addresses to be included in the FEC range. The maximum number of valid possible addresses depends on the values for the first network and the network mask.

		Returns:
			self: This instance with matching includeIpFecRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of includeIpFecRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the includeIpFecRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
