from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTlv(Base):
	"""The CustomTlv class encapsulates a user managed customTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTlv'

	def __init__(self, parent):
		super(CustomTlv, self).__init__(parent)

	@property
	def Enabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IncludeInHello(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeInHello')
	@IncludeInHello.setter
	def IncludeInHello(self, value):
		self._set_attribute('includeInHello', value)

	@property
	def IncludeInLsp(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeInLsp')
	@IncludeInLsp.setter
	def IncludeInLsp(self, value):
		self._set_attribute('includeInLsp', value)

	@property
	def IncludeInNetworkRange(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeInNetworkRange')
	@IncludeInNetworkRange.setter
	def IncludeInNetworkRange(self, value):
		self._set_attribute('includeInNetworkRange', value)

	@property
	def Length(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('length')
	@Length.setter
	def Length(self, value):
		self._set_attribute('length', value)

	@property
	def Type(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def Value(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Enabled=None, IncludeInHello=None, IncludeInLsp=None, IncludeInNetworkRange=None, Length=None, Type=None, Value=None):
		"""Adds a new customTlv node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): NOT DEFINED
			IncludeInHello (bool): NOT DEFINED
			IncludeInLsp (bool): NOT DEFINED
			IncludeInNetworkRange (bool): NOT DEFINED
			Length (number): NOT DEFINED
			Type (number): NOT DEFINED
			Value (str): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTlv data using find and the newly added customTlv data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTlv data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, IncludeInHello=None, IncludeInLsp=None, IncludeInNetworkRange=None, Length=None, Type=None, Value=None):
		"""Finds and retrieves customTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve customTlv data from the server.
		By default the find method takes no parameters and will retrieve all customTlv data from the server.

		Args:
			Enabled (bool): NOT DEFINED
			IncludeInHello (bool): NOT DEFINED
			IncludeInLsp (bool): NOT DEFINED
			IncludeInNetworkRange (bool): NOT DEFINED
			Length (number): NOT DEFINED
			Type (number): NOT DEFINED
			Value (str): NOT DEFINED

		Returns:
			self: This instance with matching customTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
