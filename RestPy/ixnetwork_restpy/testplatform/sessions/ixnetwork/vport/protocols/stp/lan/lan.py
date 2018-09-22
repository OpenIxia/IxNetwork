from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Lan(Base):
	"""The Lan class encapsulates a user managed lan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Lan property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'lan'

	def __init__(self, parent):
		super(Lan, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables the use of the STP LAN.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def MacAddress(self):
		"""The first 6-byte MAC Address in the range. (default = 00:00:00:00:00:00)

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MacCount(self):
		"""The number of MAC addresses in the LAN range. The valid range is 1 to 500. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('macCount')
	@MacCount.setter
	def MacCount(self, value):
		self._set_attribute('macCount', value)

	@property
	def MacIncrement(self):
		"""If enabled, a 6-byte increment value will be added for each additional MAC address to create a range of MAC addresses.

		Returns:
			bool
		"""
		return self._get_attribute('macIncrement')
	@MacIncrement.setter
	def MacIncrement(self, value):
		self._set_attribute('macIncrement', value)

	@property
	def TrafficGroupId(self):
		"""References a traffic group identifier as configured by the trafficGroup object.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def VlanEnabled(self):
		"""Enables the use of this STP LAN. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('vlanEnabled')
	@VlanEnabled.setter
	def VlanEnabled(self, value):
		self._set_attribute('vlanEnabled', value)

	@property
	def VlanId(self):
		"""The identifier for the first VLAN in the range. Valid range: 1 to 4094.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanIncrement(self):
		"""If enabled, an increment value will be added for each additional VLAN to create a range of MAC addresses.

		Returns:
			bool
		"""
		return self._get_attribute('vlanIncrement')
	@VlanIncrement.setter
	def VlanIncrement(self, value):
		self._set_attribute('vlanIncrement', value)

	def add(self, Enabled=None, MacAddress=None, MacCount=None, MacIncrement=None, TrafficGroupId=None, VlanEnabled=None, VlanId=None, VlanIncrement=None):
		"""Adds a new lan node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the use of the STP LAN.
			MacAddress (str): The first 6-byte MAC Address in the range. (default = 00:00:00:00:00:00)
			MacCount (number): The number of MAC addresses in the LAN range. The valid range is 1 to 500. (default = 1)
			MacIncrement (bool): If enabled, a 6-byte increment value will be added for each additional MAC address to create a range of MAC addresses.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): References a traffic group identifier as configured by the trafficGroup object.
			VlanEnabled (bool): Enables the use of this STP LAN. (default = disabled)
			VlanId (number): The identifier for the first VLAN in the range. Valid range: 1 to 4094.
			VlanIncrement (bool): If enabled, an increment value will be added for each additional VLAN to create a range of MAC addresses.

		Returns:
			self: This instance with all currently retrieved lan data using find and the newly added lan data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the lan data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, MacAddress=None, MacCount=None, MacIncrement=None, TrafficGroupId=None, VlanEnabled=None, VlanId=None, VlanIncrement=None):
		"""Finds and retrieves lan data from the server.

		All named parameters support regex and can be used to selectively retrieve lan data from the server.
		By default the find method takes no parameters and will retrieve all lan data from the server.

		Args:
			Enabled (bool): Enables the use of the STP LAN.
			MacAddress (str): The first 6-byte MAC Address in the range. (default = 00:00:00:00:00:00)
			MacCount (number): The number of MAC addresses in the LAN range. The valid range is 1 to 500. (default = 1)
			MacIncrement (bool): If enabled, a 6-byte increment value will be added for each additional MAC address to create a range of MAC addresses.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): References a traffic group identifier as configured by the trafficGroup object.
			VlanEnabled (bool): Enables the use of this STP LAN. (default = disabled)
			VlanId (number): The identifier for the first VLAN in the range. Valid range: 1 to 4094.
			VlanIncrement (bool): If enabled, an increment value will be added for each additional VLAN to create a range of MAC addresses.

		Returns:
			self: This instance with matching lan data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lan data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lan data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
