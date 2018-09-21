from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Vlans(Base):
	"""The Vlans class encapsulates a user managed vlans node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Vlans property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'vlans'

	def __init__(self, parent):
		super(Vlans, self).__init__(parent)

	@property
	def MacRanges(self):
		"""An instance of the MacRanges class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.vlans.macranges.macranges.MacRanges)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.vlans.macranges.macranges import MacRanges
		return MacRanges(self)

	@property
	def CVlanId(self):
		"""The stacked VLAN identifier.

		Returns:
			number
		"""
		return self._get_attribute('cVlanId')
	@CVlanId.setter
	def CVlanId(self, value):
		self._set_attribute('cVlanId', value)

	@property
	def CVlanPriority(self):
		"""The stacked VLAN priority.

		Returns:
			number
		"""
		return self._get_attribute('cVlanPriority')
	@CVlanPriority.setter
	def CVlanPriority(self, value):
		self._set_attribute('cVlanPriority', value)

	@property
	def CVlanTpId(self):
		"""The stacked VLAN TPID. EtherTypes identify the protocol that follows the VLAN header. Select from: 0x8100, 0x9100, 0x9200, or 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('cVlanTpId')
	@CVlanTpId.setter
	def CVlanTpId(self, value):
		self._set_attribute('cVlanTpId', value)

	@property
	def Enabled(self):
		"""If true, the VLAN is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def SVlanId(self):
		"""The single VLAN identifier.

		Returns:
			number
		"""
		return self._get_attribute('sVlanId')
	@SVlanId.setter
	def SVlanId(self, value):
		self._set_attribute('sVlanId', value)

	@property
	def SVlanPriority(self):
		"""The single VLAN priority.

		Returns:
			number
		"""
		return self._get_attribute('sVlanPriority')
	@SVlanPriority.setter
	def SVlanPriority(self, value):
		self._set_attribute('sVlanPriority', value)

	@property
	def SVlanTpId(self):
		"""The single VLAN TPID. EtherTypes identify the protocol that follows the VLAN header. Select from: 0x8100, 0x9100, 0x9200, or 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('sVlanTpId')
	@SVlanTpId.setter
	def SVlanTpId(self, value):
		self._set_attribute('sVlanTpId', value)

	@property
	def Type(self):
		"""Sets the VLAN type.

		Returns:
			str(singleVlan|stackedVlan)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, CVlanId=None, CVlanPriority=None, CVlanTpId=None, Enabled=None, SVlanId=None, SVlanPriority=None, SVlanTpId=None, Type=None):
		"""Adds a new vlans node on the server and retrieves it in this instance.

		Args:
			CVlanId (number): The stacked VLAN identifier.
			CVlanPriority (number): The stacked VLAN priority.
			CVlanTpId (str): The stacked VLAN TPID. EtherTypes identify the protocol that follows the VLAN header. Select from: 0x8100, 0x9100, 0x9200, or 0x88A8.
			Enabled (bool): If true, the VLAN is enabled.
			SVlanId (number): The single VLAN identifier.
			SVlanPriority (number): The single VLAN priority.
			SVlanTpId (str): The single VLAN TPID. EtherTypes identify the protocol that follows the VLAN header. Select from: 0x8100, 0x9100, 0x9200, or 0x88A8.
			Type (str(singleVlan|stackedVlan)): Sets the VLAN type.

		Returns:
			self: This instance with all currently retrieved vlans data using find and the newly added vlans data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the vlans data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CVlanId=None, CVlanPriority=None, CVlanTpId=None, Enabled=None, SVlanId=None, SVlanPriority=None, SVlanTpId=None, Type=None):
		"""Finds and retrieves vlans data from the server.

		All named parameters support regex and can be used to selectively retrieve vlans data from the server.
		By default the find method takes no parameters and will retrieve all vlans data from the server.

		Args:
			CVlanId (number): The stacked VLAN identifier.
			CVlanPriority (number): The stacked VLAN priority.
			CVlanTpId (str): The stacked VLAN TPID. EtherTypes identify the protocol that follows the VLAN header. Select from: 0x8100, 0x9100, 0x9200, or 0x88A8.
			Enabled (bool): If true, the VLAN is enabled.
			SVlanId (number): The single VLAN identifier.
			SVlanPriority (number): The single VLAN priority.
			SVlanTpId (str): The single VLAN TPID. EtherTypes identify the protocol that follows the VLAN header. Select from: 0x8100, 0x9100, 0x9200, or 0x88A8.
			Type (str(singleVlan|stackedVlan)): Sets the VLAN type.

		Returns:
			self: This instance with matching vlans data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of vlans data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the vlans data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
