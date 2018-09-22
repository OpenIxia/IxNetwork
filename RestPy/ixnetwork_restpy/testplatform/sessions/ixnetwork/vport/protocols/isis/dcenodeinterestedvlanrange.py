from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceNodeInterestedVlanRange(Base):
	"""The DceNodeInterestedVlanRange class encapsulates a user managed dceNodeInterestedVlanRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceNodeInterestedVlanRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceNodeInterestedVlanRange'

	def __init__(self, parent):
		super(DceNodeInterestedVlanRange, self).__init__(parent)

	@property
	def IncludeInLsp(self):
		"""If true, a custom VLAN is included in the LSP.

		Returns:
			bool
		"""
		return self._get_attribute('includeInLsp')
	@IncludeInLsp.setter
	def IncludeInLsp(self, value):
		self._set_attribute('includeInLsp', value)

	@property
	def IncludeInMgroupPdu(self):
		"""If true, a custom VLAN is included in the MGROUP PDU.

		Returns:
			bool
		"""
		return self._get_attribute('includeInMgroupPdu')
	@IncludeInMgroupPdu.setter
	def IncludeInMgroupPdu(self, value):
		self._set_attribute('includeInMgroupPdu', value)

	@property
	def IncludeInterestedVlan(self):
		"""If true, the interested VLAN is included.

		Returns:
			bool
		"""
		return self._get_attribute('includeInterestedVlan')
	@IncludeInterestedVlan.setter
	def IncludeInterestedVlan(self, value):
		self._set_attribute('includeInterestedVlan', value)

	@property
	def InternodeVlanStep(self):
		"""It shows the Increment Step of internode Vlan ID. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('internodeVlanStep')
	@InternodeVlanStep.setter
	def InternodeVlanStep(self, value):
		self._set_attribute('internodeVlanStep', value)

	@property
	def M4BitEnabled(self):
		"""If true, the M4 bit is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('m4BitEnabled')
	@M4BitEnabled.setter
	def M4BitEnabled(self, value):
		self._set_attribute('m4BitEnabled', value)

	@property
	def M6BitEnabled(self):
		"""If true, the M6 bit is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('m6BitEnabled')
	@M6BitEnabled.setter
	def M6BitEnabled(self, value):
		self._set_attribute('m6BitEnabled', value)

	@property
	def NoOfSpanningTreeRoot(self):
		"""The number of spanning tree roots for the VLAN.

		Returns:
			number
		"""
		return self._get_attribute('noOfSpanningTreeRoot')
	@NoOfSpanningTreeRoot.setter
	def NoOfSpanningTreeRoot(self, value):
		self._set_attribute('noOfSpanningTreeRoot', value)

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
	def VlanIdCount(self):
		"""The count of the VLAN Id.

		Returns:
			number
		"""
		return self._get_attribute('vlanIdCount')
	@VlanIdCount.setter
	def VlanIdCount(self, value):
		self._set_attribute('vlanIdCount', value)

	def add(self, IncludeInLsp=None, IncludeInMgroupPdu=None, IncludeInterestedVlan=None, InternodeVlanStep=None, M4BitEnabled=None, M6BitEnabled=None, NoOfSpanningTreeRoot=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanIdCount=None):
		"""Adds a new dceNodeInterestedVlanRange node on the server and retrieves it in this instance.

		Args:
			IncludeInLsp (bool): If true, a custom VLAN is included in the LSP.
			IncludeInMgroupPdu (bool): If true, a custom VLAN is included in the MGROUP PDU.
			IncludeInterestedVlan (bool): If true, the interested VLAN is included.
			InternodeVlanStep (number): It shows the Increment Step of internode Vlan ID. Default is 1.
			M4BitEnabled (bool): If true, the M4 bit is enabled.
			M6BitEnabled (bool): If true, the M6 bit is enabled.
			NoOfSpanningTreeRoot (number): The number of spanning tree roots for the VLAN.
			StartSpanningTreeRootBridgeId (str): If true, starts the spanning tree root Bridge Id.
			StartVlanId (number): The VLAN Id of first VLAN. Default is 1.
			VlanIdCount (number): The count of the VLAN Id.

		Returns:
			self: This instance with all currently retrieved dceNodeInterestedVlanRange data using find and the newly added dceNodeInterestedVlanRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceNodeInterestedVlanRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeInLsp=None, IncludeInMgroupPdu=None, IncludeInterestedVlan=None, InternodeVlanStep=None, M4BitEnabled=None, M6BitEnabled=None, NoOfSpanningTreeRoot=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanIdCount=None):
		"""Finds and retrieves dceNodeInterestedVlanRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceNodeInterestedVlanRange data from the server.
		By default the find method takes no parameters and will retrieve all dceNodeInterestedVlanRange data from the server.

		Args:
			IncludeInLsp (bool): If true, a custom VLAN is included in the LSP.
			IncludeInMgroupPdu (bool): If true, a custom VLAN is included in the MGROUP PDU.
			IncludeInterestedVlan (bool): If true, the interested VLAN is included.
			InternodeVlanStep (number): It shows the Increment Step of internode Vlan ID. Default is 1.
			M4BitEnabled (bool): If true, the M4 bit is enabled.
			M6BitEnabled (bool): If true, the M6 bit is enabled.
			NoOfSpanningTreeRoot (number): The number of spanning tree roots for the VLAN.
			StartSpanningTreeRootBridgeId (str): If true, starts the spanning tree root Bridge Id.
			StartVlanId (number): The VLAN Id of first VLAN. Default is 1.
			VlanIdCount (number): The count of the VLAN Id.

		Returns:
			self: This instance with matching dceNodeInterestedVlanRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceNodeInterestedVlanRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceNodeInterestedVlanRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
