from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Vlan(Base):
	"""The Vlan class encapsulates a user managed vlan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Vlan property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'vlan'

	def __init__(self, parent):
		super(Vlan, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def LearnedInterface(self):
		"""An instance of the LearnedInterface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.learnedinterface.learnedinterface.LearnedInterface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.learnedinterface.learnedinterface import LearnedInterface
		return LearnedInterface(self)

	@property
	def Enabled(self):
		"""Enables the use of this STP VLAN. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InternalRootPathCost(self):
		"""Administrative path cost to the root bridge. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('internalRootPathCost')
	@InternalRootPathCost.setter
	def InternalRootPathCost(self, value):
		self._set_attribute('internalRootPathCost', value)

	@property
	def Mac(self):
		"""The 6-byte MAC address of the port. (default = 00:00 :00:00:00:00)

		Returns:
			str
		"""
		return self._get_attribute('mac')
	@Mac.setter
	def Mac(self, value):
		self._set_attribute('mac', value)

	@property
	def PortPriority(self):
		"""The root priority for this port. The valid range is 0 to 61,440, in increments of 4,096. (default = 32,768)

		Returns:
			number
		"""
		return self._get_attribute('portPriority')
	@PortPriority.setter
	def PortPriority(self, value):
		self._set_attribute('portPriority', value)

	@property
	def Priority(self):
		"""The port priority for the emulated port on this PVST+ or RPVST+ bridge that is connected to the VLAN.

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def UpdateRequired(self):
		"""If true, cause the VLAN to update.

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')
	@UpdateRequired.setter
	def UpdateRequired(self, value):
		self._set_attribute('updateRequired', value)

	@property
	def VlanId(self):
		"""The identifier for this VLAN. The valid range is 2 to 4,094. (default = 2)

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	def add(self, Enabled=None, InternalRootPathCost=None, Mac=None, PortPriority=None, Priority=None, UpdateRequired=None, VlanId=None):
		"""Adds a new vlan node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the use of this STP VLAN. (default = disabled)
			InternalRootPathCost (number): Administrative path cost to the root bridge. The default is 0.
			Mac (str): The 6-byte MAC address of the port. (default = 00:00 :00:00:00:00)
			PortPriority (number): The root priority for this port. The valid range is 0 to 61,440, in increments of 4,096. (default = 32,768)
			Priority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The port priority for the emulated port on this PVST+ or RPVST+ bridge that is connected to the VLAN.
			UpdateRequired (bool): If true, cause the VLAN to update.
			VlanId (number): The identifier for this VLAN. The valid range is 2 to 4,094. (default = 2)

		Returns:
			self: This instance with all currently retrieved vlan data using find and the newly added vlan data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the vlan data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InternalRootPathCost=None, Mac=None, PortPriority=None, Priority=None, UpdateRequired=None, VlanId=None):
		"""Finds and retrieves vlan data from the server.

		All named parameters support regex and can be used to selectively retrieve vlan data from the server.
		By default the find method takes no parameters and will retrieve all vlan data from the server.

		Args:
			Enabled (bool): Enables the use of this STP VLAN. (default = disabled)
			InternalRootPathCost (number): Administrative path cost to the root bridge. The default is 0.
			Mac (str): The 6-byte MAC address of the port. (default = 00:00 :00:00:00:00)
			PortPriority (number): The root priority for this port. The valid range is 0 to 61,440, in increments of 4,096. (default = 32,768)
			Priority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The port priority for the emulated port on this PVST+ or RPVST+ bridge that is connected to the VLAN.
			UpdateRequired (bool): If true, cause the VLAN to update.
			VlanId (number): The identifier for this VLAN. The valid range is 2 to 4,094. (default = 2)

		Returns:
			self: This instance with matching vlan data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of vlan data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the vlan data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def TopologyChange(self):
		"""Executes the topologyChange operation on the server.

		This commands checks to see if there has been a topology change for the specified STP VLAN.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)): The method internally set Arg1 to the current href for this instance

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

		Updates the current STP VLAN parameters.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
