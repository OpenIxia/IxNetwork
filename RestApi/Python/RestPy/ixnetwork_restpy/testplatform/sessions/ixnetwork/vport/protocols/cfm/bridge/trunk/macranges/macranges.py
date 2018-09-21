from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MacRanges(Base):
	"""The MacRanges class encapsulates a user managed macRanges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MacRanges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'macRanges'

	def __init__(self, parent):
		super(MacRanges, self).__init__(parent)

	@property
	def CVlanId(self):
		"""The identifier for the C-VLAN for the MAC range. A unique,12-bit VLAN Identifier which specifies the C-VLAN with which this frame is associated.

		Returns:
			number
		"""
		return self._get_attribute('cVlanId')
	@CVlanId.setter
	def CVlanId(self, value):
		self._set_attribute('cVlanId', value)

	@property
	def CVlanPriority(self):
		"""The user priority of the tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

		Returns:
			number
		"""
		return self._get_attribute('cVlanPriority')
	@CVlanPriority.setter
	def CVlanPriority(self, value):
		self._set_attribute('cVlanPriority', value)

	@property
	def CVlanTpId(self):
		"""The Tag Protocol ID. EtherTypes identify the protocol that follows the VLAN header. Select from a list of hex options: 0x8100, 0x9100, 0x9200, 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('cVlanTpId')
	@CVlanTpId.setter
	def CVlanTpId(self, value):
		self._set_attribute('cVlanTpId', value)

	@property
	def Count(self):
		"""The number of times to increment in this MAC range, starting with the address set in macAddress.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def EnableVlan(self):
		"""If true, the VLAN assigned to the MAC range is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def Enabled(self):
		"""If true, the MAC range is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ITagethernetType(self):
		"""(Read-only) The I-Tag Ethernet type for the MAC range. An I-Tag is amultiplexing tag for service instance scaling in Provider Bridged Networks. This value is set to 0x88E7.

		Returns:
			str
		"""
		return self._get_attribute('iTagethernetType')

	@property
	def ITagiSid(self):
		"""The I-Tag service instance identifier, and is a 3 octet field. The default is 0. Min:0 Max: 16777215

		Returns:
			number
		"""
		return self._get_attribute('iTagiSid')
	@ITagiSid.setter
	def ITagiSid(self, value):
		self._set_attribute('iTagiSid', value)

	@property
	def SVlanId(self):
		"""A unique, 12-bit VLAN Identifier which specifies the VLAN with which this frame is associated. Default = 1 Min: 1 Max: 4095

		Returns:
			number
		"""
		return self._get_attribute('sVlanId')
	@SVlanId.setter
	def SVlanId(self, value):
		self._set_attribute('sVlanId', value)

	@property
	def SVlanPriority(self):
		"""The user priority of the tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

		Returns:
			number
		"""
		return self._get_attribute('sVlanPriority')
	@SVlanPriority.setter
	def SVlanPriority(self, value):
		self._set_attribute('sVlanPriority', value)

	@property
	def SVlanTpId(self):
		"""The Tag Protocol ID. EtherTypes identify the protocol that follows the VLAN header. Select from a list of hex options: 0x8100, 0x9100, 0x9200, 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('sVlanTpId')
	@SVlanTpId.setter
	def SVlanTpId(self, value):
		self._set_attribute('sVlanTpId', value)

	@property
	def StartMacAddress(self):
		"""The MAC address of the first entry in the range.

		Returns:
			str
		"""
		return self._get_attribute('startMacAddress')
	@StartMacAddress.setter
	def StartMacAddress(self, value):
		self._set_attribute('startMacAddress', value)

	@property
	def Step(self):
		"""The amount to increment each MAC address in the range.

		Returns:
			str
		"""
		return self._get_attribute('step')
	@Step.setter
	def Step(self, value):
		self._set_attribute('step', value)

	@property
	def TrafficGroupId(self):
		"""Assigns a traffic group to the MAC range. The traffic group must be previously configured.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def Type(self):
		"""Selects the VLAN type, either single or stacked. Stacked VLANS have an inner and outer value. Default = single.

		Returns:
			str(singleVlan|stackedVlan)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, CVlanId=None, CVlanPriority=None, CVlanTpId=None, Count=None, EnableVlan=None, Enabled=None, ITagiSid=None, SVlanId=None, SVlanPriority=None, SVlanTpId=None, StartMacAddress=None, Step=None, TrafficGroupId=None, Type=None):
		"""Adds a new macRanges node on the server and retrieves it in this instance.

		Args:
			CVlanId (number): The identifier for the C-VLAN for the MAC range. A unique,12-bit VLAN Identifier which specifies the C-VLAN with which this frame is associated.
			CVlanPriority (number): The user priority of the tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.
			CVlanTpId (str): The Tag Protocol ID. EtherTypes identify the protocol that follows the VLAN header. Select from a list of hex options: 0x8100, 0x9100, 0x9200, 0x88A8.
			Count (number): The number of times to increment in this MAC range, starting with the address set in macAddress.
			EnableVlan (bool): If true, the VLAN assigned to the MAC range is enabled.
			Enabled (bool): If true, the MAC range is enabled.
			ITagiSid (number): The I-Tag service instance identifier, and is a 3 octet field. The default is 0. Min:0 Max: 16777215
			SVlanId (number): A unique, 12-bit VLAN Identifier which specifies the VLAN with which this frame is associated. Default = 1 Min: 1 Max: 4095
			SVlanPriority (number): The user priority of the tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.
			SVlanTpId (str): The Tag Protocol ID. EtherTypes identify the protocol that follows the VLAN header. Select from a list of hex options: 0x8100, 0x9100, 0x9200, 0x88A8.
			StartMacAddress (str): The MAC address of the first entry in the range.
			Step (str): The amount to increment each MAC address in the range.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Assigns a traffic group to the MAC range. The traffic group must be previously configured.
			Type (str(singleVlan|stackedVlan)): Selects the VLAN type, either single or stacked. Stacked VLANS have an inner and outer value. Default = single.

		Returns:
			self: This instance with all currently retrieved macRanges data using find and the newly added macRanges data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the macRanges data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CVlanId=None, CVlanPriority=None, CVlanTpId=None, Count=None, EnableVlan=None, Enabled=None, ITagethernetType=None, ITagiSid=None, SVlanId=None, SVlanPriority=None, SVlanTpId=None, StartMacAddress=None, Step=None, TrafficGroupId=None, Type=None):
		"""Finds and retrieves macRanges data from the server.

		All named parameters support regex and can be used to selectively retrieve macRanges data from the server.
		By default the find method takes no parameters and will retrieve all macRanges data from the server.

		Args:
			CVlanId (number): The identifier for the C-VLAN for the MAC range. A unique,12-bit VLAN Identifier which specifies the C-VLAN with which this frame is associated.
			CVlanPriority (number): The user priority of the tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.
			CVlanTpId (str): The Tag Protocol ID. EtherTypes identify the protocol that follows the VLAN header. Select from a list of hex options: 0x8100, 0x9100, 0x9200, 0x88A8.
			Count (number): The number of times to increment in this MAC range, starting with the address set in macAddress.
			EnableVlan (bool): If true, the VLAN assigned to the MAC range is enabled.
			Enabled (bool): If true, the MAC range is enabled.
			ITagethernetType (str): (Read-only) The I-Tag Ethernet type for the MAC range. An I-Tag is amultiplexing tag for service instance scaling in Provider Bridged Networks. This value is set to 0x88E7.
			ITagiSid (number): The I-Tag service instance identifier, and is a 3 octet field. The default is 0. Min:0 Max: 16777215
			SVlanId (number): A unique, 12-bit VLAN Identifier which specifies the VLAN with which this frame is associated. Default = 1 Min: 1 Max: 4095
			SVlanPriority (number): The user priority of the tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.
			SVlanTpId (str): The Tag Protocol ID. EtherTypes identify the protocol that follows the VLAN header. Select from a list of hex options: 0x8100, 0x9100, 0x9200, 0x88A8.
			StartMacAddress (str): The MAC address of the first entry in the range.
			Step (str): The amount to increment each MAC address in the range.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Assigns a traffic group to the MAC range. The traffic group must be previously configured.
			Type (str(singleVlan|stackedVlan)): Selects the VLAN type, either single or stacked. Stacked VLANS have an inner and outer value. Default = single.

		Returns:
			self: This instance with matching macRanges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of macRanges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the macRanges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
