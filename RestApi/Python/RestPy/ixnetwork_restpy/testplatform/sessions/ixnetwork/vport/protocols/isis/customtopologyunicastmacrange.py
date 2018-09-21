from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologyUnicastMacRange(Base):
	"""The CustomTopologyUnicastMacRange class encapsulates a user managed customTopologyUnicastMacRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyUnicastMacRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyUnicastMacRange'

	def __init__(self, parent):
		super(CustomTopologyUnicastMacRange, self).__init__(parent)

	@property
	def Count(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

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
	def InterNodeMacIncrement(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('interNodeMacIncrement')
	@InterNodeMacIncrement.setter
	def InterNodeMacIncrement(self, value):
		self._set_attribute('interNodeMacIncrement', value)

	@property
	def MacIncrement(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('macIncrement')
	@MacIncrement.setter
	def MacIncrement(self, value):
		self._set_attribute('macIncrement', value)

	@property
	def StartMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startMac')
	@StartMac.setter
	def StartMac(self, value):
		self._set_attribute('startMac', value)

	@property
	def StartVlanId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('startVlanId')
	@StartVlanId.setter
	def StartVlanId(self, value):
		self._set_attribute('startVlanId', value)

	def add(self, Count=None, Enabled=None, InterNodeMacIncrement=None, MacIncrement=None, StartMac=None, StartVlanId=None):
		"""Adds a new customTopologyUnicastMacRange node on the server and retrieves it in this instance.

		Args:
			Count (number): NOT DEFINED
			Enabled (bool): NOT DEFINED
			InterNodeMacIncrement (str): NOT DEFINED
			MacIncrement (str): NOT DEFINED
			StartMac (str): NOT DEFINED
			StartVlanId (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologyUnicastMacRange data using find and the newly added customTopologyUnicastMacRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyUnicastMacRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, Enabled=None, InterNodeMacIncrement=None, MacIncrement=None, StartMac=None, StartVlanId=None):
		"""Finds and retrieves customTopologyUnicastMacRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyUnicastMacRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyUnicastMacRange data from the server.

		Args:
			Count (number): NOT DEFINED
			Enabled (bool): NOT DEFINED
			InterNodeMacIncrement (str): NOT DEFINED
			MacIncrement (str): NOT DEFINED
			StartMac (str): NOT DEFINED
			StartVlanId (number): NOT DEFINED

		Returns:
			self: This instance with matching customTopologyUnicastMacRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyUnicastMacRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyUnicastMacRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
