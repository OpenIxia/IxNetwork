from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SourceTrafficRange(Base):
	"""The SourceTrafficRange class encapsulates a user managed sourceTrafficRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SourceTrafficRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'sourceTrafficRange'

	def __init__(self, parent):
		super(SourceTrafficRange, self).__init__(parent)

	@property
	def AddrFamily(self):
		"""The address familyt value.

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('addrFamily')
	@AddrFamily.setter
	def AddrFamily(self, value):
		self._set_attribute('addrFamily', value)

	@property
	def FilterOnGroupAddress(self):
		"""The available filters on group address.

		Returns:
			bool
		"""
		return self._get_attribute('filterOnGroupAddress')
	@FilterOnGroupAddress.setter
	def FilterOnGroupAddress(self, value):
		self._set_attribute('filterOnGroupAddress', value)

	@property
	def GroupAddress(self):
		"""The group address.

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')
	@GroupAddress.setter
	def GroupAddress(self, value):
		self._set_attribute('groupAddress', value)

	@property
	def GrpCountPerLsp(self):
		"""The total group count per LSP.

		Returns:
			number
		"""
		return self._get_attribute('grpCountPerLsp')
	@GrpCountPerLsp.setter
	def GrpCountPerLsp(self, value):
		self._set_attribute('grpCountPerLsp', value)

	@property
	def SourceAddress(self):
		"""The source address.

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')
	@SourceAddress.setter
	def SourceAddress(self, value):
		self._set_attribute('sourceAddress', value)

	@property
	def SrcCountPerLsp(self):
		"""The total source count per LSP.

		Returns:
			number
		"""
		return self._get_attribute('srcCountPerLsp')
	@SrcCountPerLsp.setter
	def SrcCountPerLsp(self, value):
		self._set_attribute('srcCountPerLsp', value)

	def add(self, AddrFamily=None, FilterOnGroupAddress=None, GroupAddress=None, GrpCountPerLsp=None, SourceAddress=None, SrcCountPerLsp=None):
		"""Adds a new sourceTrafficRange node on the server and retrieves it in this instance.

		Args:
			AddrFamily (str(ipv4|ipv6)): The address familyt value.
			FilterOnGroupAddress (bool): The available filters on group address.
			GroupAddress (str): The group address.
			GrpCountPerLsp (number): The total group count per LSP.
			SourceAddress (str): The source address.
			SrcCountPerLsp (number): The total source count per LSP.

		Returns:
			self: This instance with all currently retrieved sourceTrafficRange data using find and the newly added sourceTrafficRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the sourceTrafficRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddrFamily=None, FilterOnGroupAddress=None, GroupAddress=None, GrpCountPerLsp=None, SourceAddress=None, SrcCountPerLsp=None):
		"""Finds and retrieves sourceTrafficRange data from the server.

		All named parameters support regex and can be used to selectively retrieve sourceTrafficRange data from the server.
		By default the find method takes no parameters and will retrieve all sourceTrafficRange data from the server.

		Args:
			AddrFamily (str(ipv4|ipv6)): The address familyt value.
			FilterOnGroupAddress (bool): The available filters on group address.
			GroupAddress (str): The group address.
			GrpCountPerLsp (number): The total group count per LSP.
			SourceAddress (str): The source address.
			SrcCountPerLsp (number): The total source count per LSP.

		Returns:
			self: This instance with matching sourceTrafficRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of sourceTrafficRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the sourceTrafficRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
