from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Msti(Base):
	"""The Msti class encapsulates a user managed msti node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Msti property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'msti'

	def __init__(self, parent):
		super(Msti, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def LearnedInterface(self):
		"""An instance of the LearnedInterface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinterface.learnedinterface.LearnedInterface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinterface.learnedinterface import LearnedInterface
		return LearnedInterface(self)

	@property
	def Enabled(self):
		"""Enables the use of this MSTP MSTI. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InternalRootPathCost(self):
		"""The MSTI Internal Root Path Cost. A 4-byte unsigned integer. (default is 0)

		Returns:
			number
		"""
		return self._get_attribute('internalRootPathCost')
	@InternalRootPathCost.setter
	def InternalRootPathCost(self, value):
		self._set_attribute('internalRootPathCost', value)

	@property
	def Mac(self):
		"""The 6-byte MAC address for the MSTI root. This is part of the MSTI regional root identifier.

		Returns:
			str
		"""
		return self._get_attribute('mac')
	@Mac.setter
	def Mac(self, value):
		self._set_attribute('mac', value)

	@property
	def MstiHops(self):
		"""The number of MSTI hops remaining. An unsigned integer. The valid range is 1 to 255. (default = 20)

		Returns:
			number
		"""
		return self._get_attribute('mstiHops')
	@MstiHops.setter
	def MstiHops(self, value):
		self._set_attribute('mstiHops', value)

	@property
	def MstiId(self):
		"""The identifier for this MST Instance (MSTI). The valid range is 1 to 4,094. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('mstiId')
	@MstiId.setter
	def MstiId(self, value):
		self._set_attribute('mstiId', value)

	@property
	def MstiName(self):
		"""The name of the MSTI which is configured from the list of MSTIs. Format: MSTI ID-n. (Editable by the user.)

		Returns:
			str
		"""
		return self._get_attribute('mstiName')
	@MstiName.setter
	def MstiName(self, value):
		self._set_attribute('mstiName', value)

	@property
	def PortPriority(self):
		"""The MSTI Port Priority. This is part of the MSTI Regional Root Identifier. An unsigned integer; a multiple of 16. The valid range is 0 to 240. (default = 0)

		Returns:
			str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)
		"""
		return self._get_attribute('portPriority')
	@PortPriority.setter
	def PortPriority(self, value):
		self._set_attribute('portPriority', value)

	@property
	def Priority(self):
		"""The MSTI Root Priority. This is part of the MSTI Regional Root Identifier. Since MAC address reduction is used, only multiples of 4096 are used.

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def UpdateRequired(self):
		"""If true, causes the MSTI to update.

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')
	@UpdateRequired.setter
	def UpdateRequired(self, value):
		self._set_attribute('updateRequired', value)

	@property
	def VlanStart(self):
		"""The ID for the first VLAN in the VLAN range to which the MSTI is mapped. An unsigned integer. Valid range: 1 to 4094.

		Returns:
			number
		"""
		return self._get_attribute('vlanStart')
	@VlanStart.setter
	def VlanStart(self, value):
		self._set_attribute('vlanStart', value)

	@property
	def VlanStop(self):
		"""The ID for the last VLAN in the VLAN range to which the MSTI is mapped. An unsigned integer. Valid range: 1 to 4094.

		Returns:
			number
		"""
		return self._get_attribute('vlanStop')
	@VlanStop.setter
	def VlanStop(self, value):
		self._set_attribute('vlanStop', value)

	def add(self, Enabled=None, InternalRootPathCost=None, Mac=None, MstiHops=None, MstiId=None, MstiName=None, PortPriority=None, Priority=None, UpdateRequired=None, VlanStart=None, VlanStop=None):
		"""Adds a new msti node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the use of this MSTP MSTI. (default = disabled)
			InternalRootPathCost (number): The MSTI Internal Root Path Cost. A 4-byte unsigned integer. (default is 0)
			Mac (str): The 6-byte MAC address for the MSTI root. This is part of the MSTI regional root identifier.
			MstiHops (number): The number of MSTI hops remaining. An unsigned integer. The valid range is 1 to 255. (default = 20)
			MstiId (number): The identifier for this MST Instance (MSTI). The valid range is 1 to 4,094. (default = 1)
			MstiName (str): The name of the MSTI which is configured from the list of MSTIs. Format: MSTI ID-n. (Editable by the user.)
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): The MSTI Port Priority. This is part of the MSTI Regional Root Identifier. An unsigned integer; a multiple of 16. The valid range is 0 to 240. (default = 0)
			Priority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The MSTI Root Priority. This is part of the MSTI Regional Root Identifier. Since MAC address reduction is used, only multiples of 4096 are used.
			UpdateRequired (bool): If true, causes the MSTI to update.
			VlanStart (number): The ID for the first VLAN in the VLAN range to which the MSTI is mapped. An unsigned integer. Valid range: 1 to 4094.
			VlanStop (number): The ID for the last VLAN in the VLAN range to which the MSTI is mapped. An unsigned integer. Valid range: 1 to 4094.

		Returns:
			self: This instance with all currently retrieved msti data using find and the newly added msti data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the msti data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InternalRootPathCost=None, Mac=None, MstiHops=None, MstiId=None, MstiName=None, PortPriority=None, Priority=None, UpdateRequired=None, VlanStart=None, VlanStop=None):
		"""Finds and retrieves msti data from the server.

		All named parameters support regex and can be used to selectively retrieve msti data from the server.
		By default the find method takes no parameters and will retrieve all msti data from the server.

		Args:
			Enabled (bool): Enables the use of this MSTP MSTI. (default = disabled)
			InternalRootPathCost (number): The MSTI Internal Root Path Cost. A 4-byte unsigned integer. (default is 0)
			Mac (str): The 6-byte MAC address for the MSTI root. This is part of the MSTI regional root identifier.
			MstiHops (number): The number of MSTI hops remaining. An unsigned integer. The valid range is 1 to 255. (default = 20)
			MstiId (number): The identifier for this MST Instance (MSTI). The valid range is 1 to 4,094. (default = 1)
			MstiName (str): The name of the MSTI which is configured from the list of MSTIs. Format: MSTI ID-n. (Editable by the user.)
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): The MSTI Port Priority. This is part of the MSTI Regional Root Identifier. An unsigned integer; a multiple of 16. The valid range is 0 to 240. (default = 0)
			Priority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The MSTI Root Priority. This is part of the MSTI Regional Root Identifier. Since MAC address reduction is used, only multiples of 4096 are used.
			UpdateRequired (bool): If true, causes the MSTI to update.
			VlanStart (number): The ID for the first VLAN in the VLAN range to which the MSTI is mapped. An unsigned integer. Valid range: 1 to 4094.
			VlanStop (number): The ID for the last VLAN in the VLAN range to which the MSTI is mapped. An unsigned integer. Valid range: 1 to 4094.

		Returns:
			self: This instance with matching msti data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of msti data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the msti data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def TopologyChange(self):
		"""Executes the topologyChange operation on the server.

		This command checks to see if a topology change has occurred on the specified STP bridge MSTI.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('TopologyChange', payload=locals(), response_object=None)

	def UpdateParameters(self):
		"""Executes the updateParameters operation on the server.

		Updates the current STP parameters on the specified bridge MSTI.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
