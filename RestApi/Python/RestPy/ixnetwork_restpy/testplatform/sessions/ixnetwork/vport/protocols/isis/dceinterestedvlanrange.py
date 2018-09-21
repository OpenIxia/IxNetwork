from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceInterestedVlanRange(Base):
	"""The DceInterestedVlanRange class encapsulates a user managed dceInterestedVlanRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceInterestedVlanRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceInterestedVlanRange'

	def __init__(self, parent):
		super(DceInterestedVlanRange, self).__init__(parent)

	@property
	def EnableIncludeInLsp(self):
		"""If true, enable a custom VLAN in the LSP.

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeInLsp')
	@EnableIncludeInLsp.setter
	def EnableIncludeInLsp(self, value):
		self._set_attribute('enableIncludeInLsp', value)

	@property
	def EnableIncludeInMgroupPdu(self):
		"""If true, enable and include VLAN in Mgroup PDU

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeInMgroupPdu')
	@EnableIncludeInMgroupPdu.setter
	def EnableIncludeInMgroupPdu(self, value):
		self._set_attribute('enableIncludeInMgroupPdu', value)

	@property
	def EnableM4Bit(self):
		"""If true, the M4 bit is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enableM4Bit')
	@EnableM4Bit.setter
	def EnableM4Bit(self, value):
		self._set_attribute('enableM4Bit', value)

	@property
	def EnableM6Bit(self):
		"""If true, the M6 bit is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enableM6Bit')
	@EnableM6Bit.setter
	def EnableM6Bit(self, value):
		self._set_attribute('enableM6Bit', value)

	@property
	def Enabled(self):
		"""Signifies if DCE Interested Vlan range is enabled or disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Nickname(self):
		"""The nickname of the VLAN range.

		Returns:
			number
		"""
		return self._get_attribute('nickname')
	@Nickname.setter
	def Nickname(self, value):
		self._set_attribute('nickname', value)

	@property
	def NoOfSpanningTreeRoots(self):
		"""The number of spanning tree roots for the VLAN.

		Returns:
			number
		"""
		return self._get_attribute('noOfSpanningTreeRoots')
	@NoOfSpanningTreeRoots.setter
	def NoOfSpanningTreeRoots(self, value):
		self._set_attribute('noOfSpanningTreeRoots', value)

	@property
	def StartSpanningTreeRootBridgeId(self):
		"""If true, starts the spanning tree root Bridge Id.

		Returns:
			str
		"""
		return self._get_attribute('startSpanningTreeRootBridgeId')
	@StartSpanningTreeRootBridgeId.setter
	def StartSpanningTreeRootBridgeId(self, value):
		self._set_attribute('startSpanningTreeRootBridgeId', value)

	@property
	def StartVlanId(self):
		"""The VLAN Id of first VLAN. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('startVlanId')
	@StartVlanId.setter
	def StartVlanId(self, value):
		self._set_attribute('startVlanId', value)

	@property
	def VlanCount(self):
		"""The count of the VLAN.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanIdStep(self):
		"""It shows the increment step of the VLAN. the default is 1.

		Returns:
			number
		"""
		return self._get_attribute('vlanIdStep')
	@VlanIdStep.setter
	def VlanIdStep(self, value):
		self._set_attribute('vlanIdStep', value)

	def add(self, EnableIncludeInLsp=None, EnableIncludeInMgroupPdu=None, EnableM4Bit=None, EnableM6Bit=None, Enabled=None, Nickname=None, NoOfSpanningTreeRoots=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanCount=None, VlanIdStep=None):
		"""Adds a new dceInterestedVlanRange node on the server and retrieves it in this instance.

		Args:
			EnableIncludeInLsp (bool): If true, enable a custom VLAN in the LSP.
			EnableIncludeInMgroupPdu (bool): If true, enable and include VLAN in Mgroup PDU
			EnableM4Bit (bool): If true, the M4 bit is enabled.
			EnableM6Bit (bool): If true, the M6 bit is enabled.
			Enabled (bool): Signifies if DCE Interested Vlan range is enabled or disabled.
			Nickname (number): The nickname of the VLAN range.
			NoOfSpanningTreeRoots (number): The number of spanning tree roots for the VLAN.
			StartSpanningTreeRootBridgeId (str): If true, starts the spanning tree root Bridge Id.
			StartVlanId (number): The VLAN Id of first VLAN. Default is 1.
			VlanCount (number): The count of the VLAN.
			VlanIdStep (number): It shows the increment step of the VLAN. the default is 1.

		Returns:
			self: This instance with all currently retrieved dceInterestedVlanRange data using find and the newly added dceInterestedVlanRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceInterestedVlanRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableIncludeInLsp=None, EnableIncludeInMgroupPdu=None, EnableM4Bit=None, EnableM6Bit=None, Enabled=None, Nickname=None, NoOfSpanningTreeRoots=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanCount=None, VlanIdStep=None):
		"""Finds and retrieves dceInterestedVlanRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceInterestedVlanRange data from the server.
		By default the find method takes no parameters and will retrieve all dceInterestedVlanRange data from the server.

		Args:
			EnableIncludeInLsp (bool): If true, enable a custom VLAN in the LSP.
			EnableIncludeInMgroupPdu (bool): If true, enable and include VLAN in Mgroup PDU
			EnableM4Bit (bool): If true, the M4 bit is enabled.
			EnableM6Bit (bool): If true, the M6 bit is enabled.
			Enabled (bool): Signifies if DCE Interested Vlan range is enabled or disabled.
			Nickname (number): The nickname of the VLAN range.
			NoOfSpanningTreeRoots (number): The number of spanning tree roots for the VLAN.
			StartSpanningTreeRootBridgeId (str): If true, starts the spanning tree root Bridge Id.
			StartVlanId (number): The VLAN Id of first VLAN. Default is 1.
			VlanCount (number): The count of the VLAN.
			VlanIdStep (number): It shows the increment step of the VLAN. the default is 1.

		Returns:
			self: This instance with matching dceInterestedVlanRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceInterestedVlanRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceInterestedVlanRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
