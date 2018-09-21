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
	def AtmEncapsulation(self):
		"""Select the ATM VPI/VCI Name from the list configured in the atm object.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=atm)
		"""
		return self._get_attribute('atmEncapsulation')
	@AtmEncapsulation.setter
	def AtmEncapsulation(self, value):
		self._set_attribute('atmEncapsulation', value)

	@property
	def Count(self):
		"""If the VLAN is enabled, then this is the number of MAC address/VLAN combinations that will be created.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def CountPerVc(self):
		"""The total count per VC in this bundled mode.

		Returns:
			number
		"""
		return self._get_attribute('countPerVc')
	@CountPerVc.setter
	def CountPerVc(self, value):
		self._set_attribute('countPerVc', value)

	@property
	def EnableIncrementMac(self):
		"""Enables the use of multiple MAC addresses, which are incremented for each additional address. The default increment is 00 00 00 00 00 01.

		Returns:
			bool
		"""
		return self._get_attribute('enableIncrementMac')
	@EnableIncrementMac.setter
	def EnableIncrementMac(self, value):
		self._set_attribute('enableIncrementMac', value)

	@property
	def EnableIncrementVlan(self):
		"""Enables the use of multiple VLANs, which are incremented for each additional VLAN. The default increment is 1.

		Returns:
			bool
		"""
		return self._get_attribute('enableIncrementVlan')
	@EnableIncrementVlan.setter
	def EnableIncrementVlan(self, value):
		self._set_attribute('enableIncrementVlan', value)

	@property
	def EnableSiteId(self):
		"""Enables this site identifier (ID).

		Returns:
			bool
		"""
		return self._get_attribute('enableSiteId')
	@EnableSiteId.setter
	def EnableSiteId(self, value):
		self._set_attribute('enableSiteId', value)

	@property
	def EnableVlan(self):
		"""Enables the use of VLANs.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def Enabled(self):
		"""Enables this LAN entry.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FrEncapsulation(self):
		"""Selects the Frame Relay encapsulation for the LAN based on the configuration of the fr object.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=fr)
		"""
		return self._get_attribute('frEncapsulation')
	@FrEncapsulation.setter
	def FrEncapsulation(self, value):
		self._set_attribute('frEncapsulation', value)

	@property
	def IncrementPerVcVlanMode(self):
		"""If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementPerVcVlanMode')
	@IncrementPerVcVlanMode.setter
	def IncrementPerVcVlanMode(self, value):
		self._set_attribute('incrementPerVcVlanMode', value)

	@property
	def IncrementVlanMode(self):
		"""If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementVlanMode')
	@IncrementVlanMode.setter
	def IncrementVlanMode(self, value):
		self._set_attribute('incrementVlanMode', value)

	@property
	def IncremetVlanMode(self):
		"""If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incremetVlanMode')
	@IncremetVlanMode.setter
	def IncremetVlanMode(self, value):
		self._set_attribute('incremetVlanMode', value)

	@property
	def Mac(self):
		"""The first MAC address in the range.

		Returns:
			str
		"""
		return self._get_attribute('mac')
	@Mac.setter
	def Mac(self, value):
		self._set_attribute('mac', value)

	@property
	def MacRangeMode(self):
		"""Indicates the available MAC range mode.

		Returns:
			str(normal|bundled)
		"""
		return self._get_attribute('macRangeMode')
	@MacRangeMode.setter
	def MacRangeMode(self, value):
		self._set_attribute('macRangeMode', value)

	@property
	def NumberOfVcs(self):
		"""The total number of VCs in this mode.

		Returns:
			number
		"""
		return self._get_attribute('numberOfVcs')
	@NumberOfVcs.setter
	def NumberOfVcs(self, value):
		self._set_attribute('numberOfVcs', value)

	@property
	def SiteId(self):
		"""The value of the site identifier (ID). The valid range is 0 to 4,294,967,295. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('siteId')
	@SiteId.setter
	def SiteId(self, value):
		self._set_attribute('siteId', value)

	@property
	def SkipVlanIdZero(self):
		"""Skip the value of vlad id, if the vlan id value is equal to zero.

		Returns:
			bool
		"""
		return self._get_attribute('skipVlanIdZero')
	@SkipVlanIdZero.setter
	def SkipVlanIdZero(self, value):
		self._set_attribute('skipVlanIdZero', value)

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
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

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
		"""The identifier for the first VLAN in the range.

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

	def add(self, AtmEncapsulation=None, Count=None, CountPerVc=None, EnableIncrementMac=None, EnableIncrementVlan=None, EnableSiteId=None, EnableVlan=None, Enabled=None, FrEncapsulation=None, IncrementPerVcVlanMode=None, IncrementVlanMode=None, IncremetVlanMode=None, Mac=None, MacRangeMode=None, NumberOfVcs=None, SiteId=None, SkipVlanIdZero=None, Tpid=None, TrafficGroupId=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new lan node on the server and retrieves it in this instance.

		Args:
			AtmEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=atm)): Select the ATM VPI/VCI Name from the list configured in the atm object.
			Count (number): If the VLAN is enabled, then this is the number of MAC address/VLAN combinations that will be created.
			CountPerVc (number): The total count per VC in this bundled mode.
			EnableIncrementMac (bool): Enables the use of multiple MAC addresses, which are incremented for each additional address. The default increment is 00 00 00 00 00 01.
			EnableIncrementVlan (bool): Enables the use of multiple VLANs, which are incremented for each additional VLAN. The default increment is 1.
			EnableSiteId (bool): Enables this site identifier (ID).
			EnableVlan (bool): Enables the use of VLANs.
			Enabled (bool): Enables this LAN entry.
			FrEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=fr)): Selects the Frame Relay encapsulation for the LAN based on the configuration of the fr object.
			IncrementPerVcVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.
			Mac (str): The first MAC address in the range.
			MacRangeMode (str(normal|bundled)): Indicates the available MAC range mode.
			NumberOfVcs (number): The total number of VCs in this mode.
			SiteId (number): The value of the site identifier (ID). The valid range is 0 to 4,294,967,295. The default is 0.
			SkipVlanIdZero (bool): Skip the value of vlad id, if the vlan id value is equal to zero.
			Tpid (str): Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag).The dropdown list contains the available TPIDs. Choose one of: 0x8100 (the default), 0x88a8, 0x9100, 0x9200.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			VlanCount (number): The number of VLANs created.
			VlanId (str): The identifier for the first VLAN in the range.
			VlanPriority (str): The User Priority for this VLAN. A value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

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

	def find(self, AtmEncapsulation=None, Count=None, CountPerVc=None, EnableIncrementMac=None, EnableIncrementVlan=None, EnableSiteId=None, EnableVlan=None, Enabled=None, FrEncapsulation=None, IncrementPerVcVlanMode=None, IncrementVlanMode=None, IncremetVlanMode=None, Mac=None, MacRangeMode=None, NumberOfVcs=None, SiteId=None, SkipVlanIdZero=None, Tpid=None, TrafficGroupId=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves lan data from the server.

		All named parameters support regex and can be used to selectively retrieve lan data from the server.
		By default the find method takes no parameters and will retrieve all lan data from the server.

		Args:
			AtmEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=atm)): Select the ATM VPI/VCI Name from the list configured in the atm object.
			Count (number): If the VLAN is enabled, then this is the number of MAC address/VLAN combinations that will be created.
			CountPerVc (number): The total count per VC in this bundled mode.
			EnableIncrementMac (bool): Enables the use of multiple MAC addresses, which are incremented for each additional address. The default increment is 00 00 00 00 00 01.
			EnableIncrementVlan (bool): Enables the use of multiple VLANs, which are incremented for each additional VLAN. The default increment is 1.
			EnableSiteId (bool): Enables this site identifier (ID).
			EnableVlan (bool): Enables the use of VLANs.
			Enabled (bool): Enables this LAN entry.
			FrEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=fr)): Selects the Frame Relay encapsulation for the LAN based on the configuration of the fr object.
			IncrementPerVcVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): If true, enables the use of multiple VLANs, which are incremented for each additional VLAN per VC. The default increment is 1.
			Mac (str): The first MAC address in the range.
			MacRangeMode (str(normal|bundled)): Indicates the available MAC range mode.
			NumberOfVcs (number): The total number of VCs in this mode.
			SiteId (number): The value of the site identifier (ID). The valid range is 0 to 4,294,967,295. The default is 0.
			SkipVlanIdZero (bool): Skip the value of vlad id, if the vlan id value is equal to zero.
			Tpid (str): Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag).The dropdown list contains the available TPIDs. Choose one of: 0x8100 (the default), 0x88a8, 0x9100, 0x9200.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			VlanCount (number): The number of VLANs created.
			VlanId (str): The identifier for the first VLAN in the range.
			VlanPriority (str): The User Priority for this VLAN. A value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.

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
