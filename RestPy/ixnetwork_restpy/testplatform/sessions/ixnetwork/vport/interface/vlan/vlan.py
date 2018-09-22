from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Vlan(Base):
	"""The Vlan class encapsulates a required vlan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Vlan property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'vlan'

	def __init__(self, parent):
		super(Vlan, self).__init__(parent)

	@property
	def Tpid(self):
		"""Tag Protocol Identifier / TPID (hex). The EtherType that identifies the protocol header that follows the VLAN header (tag). (Active only if VLAN has been enabled.)

		Returns:
			str
		"""
		return self._get_attribute('tpid')
	@Tpid.setter
	def Tpid(self, value):
		self._set_attribute('tpid', value)

	@property
	def VlanCount(self):
		"""The number of VLANs configured for this interface.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanEnable(self):
		"""If enabled, a VLAN can be assigned for each of the interfaces.

		Returns:
			bool
		"""
		return self._get_attribute('vlanEnable')
	@VlanEnable.setter
	def VlanEnable(self, value):
		self._set_attribute('vlanEnable', value)

	@property
	def VlanId(self):
		"""If the VLAN option is enabled for the current interface, a VLAN ID may be added to the packet, to identify the VLAN that the packet belongs to. The default is 1. If the VLAN Count is greater than 1 (for stacked VLANs), corresponding multiple entries will appear in the VLAN ID field.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""The user priority of the VLAN tag: a value from 0 through 7. The use and interpretation of this field is defined in ISO/IEC 15802-3.The default is 5.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
