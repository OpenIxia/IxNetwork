from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class L2MacVlanRange(Base):
	"""The L2MacVlanRange class encapsulates a required l2MacVlanRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the L2MacVlanRange property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'l2MacVlanRange'

	def __init__(self, parent):
		super(L2MacVlanRange, self).__init__(parent)

	@property
	def Count(self):
		"""If Enable VLAN is enabled, this it the number of MAC address/VLAN combinations that will be created. If Enabled VLAN is not enabled, this is the number of MAC addresses that will be created.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def EnableRepeatMac(self):
		"""If enabled, and the count is greater than 1, the same address value will be repeated for all MAC addresses.

		Returns:
			bool
		"""
		return self._get_attribute('enableRepeatMac')
	@EnableRepeatMac.setter
	def EnableRepeatMac(self, value):
		self._set_attribute('enableRepeatMac', value)

	@property
	def EnableSameVlan(self):
		"""If enabled, all MAC addresses in the range will be associated with the same VLAN ID. If enabled, all MAC addresses in the range will be associated with different VLAN IDs, where the VLAN IDs will be automatically incremented.

		Returns:
			bool
		"""
		return self._get_attribute('enableSameVlan')
	@EnableSameVlan.setter
	def EnableSameVlan(self, value):
		self._set_attribute('enableSameVlan', value)

	@property
	def EnableVlan(self):
		"""Enables the MAC/VLAN range.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def Enabled(self):
		"""Enables the Layer 2 MAC/VLAN address range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstVlanId(self):
		"""The VLAN ID for the first VLAN in the MAC/VLAN range.

		Returns:
			number
		"""
		return self._get_attribute('firstVlanId')
	@FirstVlanId.setter
	def FirstVlanId(self, value):
		self._set_attribute('firstVlanId', value)

	@property
	def IncrementVlanMode(self):
		"""If true, each additional VLAN in the range is incremented to create unique VLAN IDs.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementVlanMode')
	@IncrementVlanMode.setter
	def IncrementVlanMode(self, value):
		self._set_attribute('incrementVlanMode', value)

	@property
	def IncremetVlanMode(self):
		"""If true, each additional VLAN in the range is incremented to create unique VLAN IDs. The increment value is 1.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incremetVlanMode')
	@IncremetVlanMode.setter
	def IncremetVlanMode(self, value):
		self._set_attribute('incremetVlanMode', value)

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
	def StartMac(self):
		"""The first MAC address in the MAC range.

		Returns:
			str
		"""
		return self._get_attribute('startMac')
	@StartMac.setter
	def StartMac(self, value):
		self._set_attribute('startMac', value)

	@property
	def Tpid(self):
		"""Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag).

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
