from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MacAddressRange(Base):
	"""The MacAddressRange class encapsulates a user managed macAddressRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MacAddressRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'macAddressRange'

	def __init__(self, parent):
		super(MacAddressRange, self).__init__(parent)

	@property
	def EnableVlan(self):
		"""If enabled, VLANs will be created and associated with the MAC addresses. The default is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def Enabled(self):
		"""Enables the MAC address range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IncrementVlan(self):
		"""If enabled, each additional VLAN in the range will be incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('incrementVlan')
	@IncrementVlan.setter
	def IncrementVlan(self, value):
		self._set_attribute('incrementVlan', value)

	@property
	def IncrementVlanMode(self):
		"""If enabled, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementVlanMode')
	@IncrementVlanMode.setter
	def IncrementVlanMode(self, value):
		self._set_attribute('incrementVlanMode', value)

	@property
	def IncremetVlanMode(self):
		"""If enabled, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incremetVlanMode')
	@IncremetVlanMode.setter
	def IncremetVlanMode(self, value):
		self._set_attribute('incremetVlanMode', value)

	@property
	def MacCount(self):
		"""The number of MAC addresses to be created for this range. A 4-byte unsigned integer. The default is 1.

		Returns:
			number
		"""
		return self._get_attribute('macCount')
	@MacCount.setter
	def MacCount(self, value):
		self._set_attribute('macCount', value)

	@property
	def MacCountPerL2Site(self):
		"""Signifies the count of MAC values per L2 site

		Returns:
			number
		"""
		return self._get_attribute('macCountPerL2Site')
	@MacCountPerL2Site.setter
	def MacCountPerL2Site(self, value):
		self._set_attribute('macCountPerL2Site', value)

	@property
	def MacIncrement(self):
		"""If enabled, each additional MAC Address in this range of addresses will be incremented by 00 00 00 00 00 01.

		Returns:
			bool
		"""
		return self._get_attribute('macIncrement')
	@MacIncrement.setter
	def MacIncrement(self, value):
		self._set_attribute('macIncrement', value)

	@property
	def SkipVlanIdZero(self):
		"""If enabled, the VLAN ID with zero value will be ignored.

		Returns:
			bool
		"""
		return self._get_attribute('skipVlanIdZero')
	@SkipVlanIdZero.setter
	def SkipVlanIdZero(self, value):
		self._set_attribute('skipVlanIdZero', value)

	@property
	def StartMacAddress(self):
		"""The first 6-byte MAC address in the range of MAC addresses. The default is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('startMacAddress')
	@StartMacAddress.setter
	def StartMacAddress(self, value):
		self._set_attribute('startMacAddress', value)

	@property
	def TotalMacCount(self):
		"""Signifies the total MAC count

		Returns:
			number
		"""
		return self._get_attribute('totalMacCount')

	@property
	def Tpid(self):
		"""Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag).The dropdown list contains the available TPIDs. Choose one of: 0x8100 (the default), 0x88a8, 0x9100, 0x9200.

		Returns:
			str
		"""
		return self._get_attribute('tpid')
	@Tpid.setter
	def Tpid(self, value):
		self._set_attribute('tpid', value)

	@property
	def VlanCount(self):
		"""The number of VLANs created.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""The ID for the first VLAN in a range of VLANs. An 2-byte unsigned integer. The valid range is 0 to 4095. The default is 0.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""The User Priority for this VLAN. A value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, EnableVlan=None, Enabled=None, IncrementVlan=None, IncrementVlanMode=None, IncremetVlanMode=None, MacCount=None, MacCountPerL2Site=None, MacIncrement=None, SkipVlanIdZero=None, StartMacAddress=None, Tpid=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new macAddressRange node on the server and retrieves it in this instance.

		Args:
			EnableVlan (bool): If enabled, VLANs will be created and associated with the MAC addresses. The default is disabled.
			Enabled (bool): Enables the MAC address range.
			IncrementVlan (bool): If enabled, each additional VLAN in the range will be incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If enabled, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If enabled, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.
			MacCount (number): The number of MAC addresses to be created for this range. A 4-byte unsigned integer. The default is 1.
			MacCountPerL2Site (number): Signifies the count of MAC values per L2 site
			MacIncrement (bool): If enabled, each additional MAC Address in this range of addresses will be incremented by 00 00 00 00 00 01.
			SkipVlanIdZero (bool): If enabled, the VLAN ID with zero value will be ignored.
			StartMacAddress (str): The first 6-byte MAC address in the range of MAC addresses. The default is 00 00 00 00 00 00.
			Tpid (str): Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag).The dropdown list contains the available TPIDs. Choose one of: 0x8100 (the default), 0x88a8, 0x9100, 0x9200.
			VlanCount (number): The number of VLANs created.
			VlanId (str): The ID for the first VLAN in a range of VLANs. An 2-byte unsigned integer. The valid range is 0 to 4095. The default is 0.
			VlanPriority (str): The User Priority for this VLAN. A value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

		Returns:
			self: This instance with all currently retrieved macAddressRange data using find and the newly added macAddressRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the macAddressRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableVlan=None, Enabled=None, IncrementVlan=None, IncrementVlanMode=None, IncremetVlanMode=None, MacCount=None, MacCountPerL2Site=None, MacIncrement=None, SkipVlanIdZero=None, StartMacAddress=None, TotalMacCount=None, Tpid=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves macAddressRange data from the server.

		All named parameters support regex and can be used to selectively retrieve macAddressRange data from the server.
		By default the find method takes no parameters and will retrieve all macAddressRange data from the server.

		Args:
			EnableVlan (bool): If enabled, VLANs will be created and associated with the MAC addresses. The default is disabled.
			Enabled (bool): Enables the MAC address range.
			IncrementVlan (bool): If enabled, each additional VLAN in the range will be incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If enabled, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If enabled, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1. The default is disabled.
			MacCount (number): The number of MAC addresses to be created for this range. A 4-byte unsigned integer. The default is 1.
			MacCountPerL2Site (number): Signifies the count of MAC values per L2 site
			MacIncrement (bool): If enabled, each additional MAC Address in this range of addresses will be incremented by 00 00 00 00 00 01.
			SkipVlanIdZero (bool): If enabled, the VLAN ID with zero value will be ignored.
			StartMacAddress (str): The first 6-byte MAC address in the range of MAC addresses. The default is 00 00 00 00 00 00.
			TotalMacCount (number): Signifies the total MAC count
			Tpid (str): Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag).The dropdown list contains the available TPIDs. Choose one of: 0x8100 (the default), 0x88a8, 0x9100, 0x9200.
			VlanCount (number): The number of VLANs created.
			VlanId (str): The ID for the first VLAN in a range of VLANs. An 2-byte unsigned integer. The valid range is 0 to 4095. The default is 0.
			VlanPriority (str): The User Priority for this VLAN. A value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

		Returns:
			self: This instance with matching macAddressRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of macAddressRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the macAddressRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
