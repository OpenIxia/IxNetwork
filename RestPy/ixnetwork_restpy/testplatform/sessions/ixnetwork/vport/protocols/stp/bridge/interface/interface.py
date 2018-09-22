from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interface(Base):
	"""The Interface class encapsulates a user managed interface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def AutoPick(self):
		"""If set, then the Auto-Pick Port Number feature is enabled and each STP interface configured for the same bridge will be assigned a unique port number automatically.(default = enabled)

		Returns:
			bool
		"""
		return self._get_attribute('autoPick')
	@AutoPick.setter
	def AutoPick(self, value):
		self._set_attribute('autoPick', value)

	@property
	def BdpuGap(self):
		"""The length of time between transmissions of BPDUs, in milliseconds. The valid range is 0 msec to 60,000 msec. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('bdpuGap')
	@BdpuGap.setter
	def BdpuGap(self, value):
		self._set_attribute('bdpuGap', value)

	@property
	def Cost(self):
		"""The administrative path cost assigned to this interface. The valid range is 0 to 4294967295. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('cost')
	@Cost.setter
	def Cost(self, value):
		self._set_attribute('cost', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of the interface. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterfaceId(self):
		"""The unique identifier for this interface.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def JitterEnabled(self):
		"""Staggered transmit (jitter) for Hello messages. If set, then the jitter feature is enabled. (default = enabled)

		Returns:
			bool
		"""
		return self._get_attribute('jitterEnabled')
	@JitterEnabled.setter
	def JitterEnabled(self, value):
		self._set_attribute('jitterEnabled', value)

	@property
	def JitterPercentage(self):
		"""The maximum percentage of +/- variation (jitter) from the Hello message transmission interval.

		Returns:
			number
		"""
		return self._get_attribute('jitterPercentage')
	@JitterPercentage.setter
	def JitterPercentage(self, value):
		self._set_attribute('jitterPercentage', value)

	@property
	def LinkType(self):
		"""The type of link attached to this interface.

		Returns:
			str(pointToPoint|shared)
		"""
		return self._get_attribute('linkType')
	@LinkType.setter
	def LinkType(self, value):
		self._set_attribute('linkType', value)

	@property
	def MstiOrVlanId(self):
		"""The identifier for this MSTI or the identifier for the first VLAN in the range.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=all|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)
		"""
		return self._get_attribute('mstiOrVlanId')
	@MstiOrVlanId.setter
	def MstiOrVlanId(self, value):
		self._set_attribute('mstiOrVlanId', value)

	@property
	def PortNo(self):
		"""The port number associated with this STP interface. If enableAutoPickPortNum is set, the port number will be automatically assigned (not editable by the user). If enableAutoPickPortNum is not set, the port number can be configured by the user. The valid range is 1 to 4,095. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('portNo')
	@PortNo.setter
	def PortNo(self, value):
		self._set_attribute('portNo', value)

	@property
	def Pvid(self):
		"""The Port VLAN ID. This value must be the same for all ports participating in the PVST+/RPVST+ protocol. The valid range is 1 to 4,094. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('pvid')
	@Pvid.setter
	def Pvid(self, value):
		self._set_attribute('pvid', value)

	def add(self, AutoPick=None, BdpuGap=None, Cost=None, Enabled=None, InterfaceId=None, JitterEnabled=None, JitterPercentage=None, LinkType=None, MstiOrVlanId=None, PortNo=None, Pvid=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AutoPick (bool): If set, then the Auto-Pick Port Number feature is enabled and each STP interface configured for the same bridge will be assigned a unique port number automatically.(default = enabled)
			BdpuGap (number): The length of time between transmissions of BPDUs, in milliseconds. The valid range is 0 msec to 60,000 msec. (default = 0)
			Cost (number): The administrative path cost assigned to this interface. The valid range is 0 to 4294967295. (default = 1)
			Enabled (bool): Enables or disables the use of the interface. (default = disabled)
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The unique identifier for this interface.
			JitterEnabled (bool): Staggered transmit (jitter) for Hello messages. If set, then the jitter feature is enabled. (default = enabled)
			JitterPercentage (number): The maximum percentage of +/- variation (jitter) from the Hello message transmission interval.
			LinkType (str(pointToPoint|shared)): The type of link attached to this interface.
			MstiOrVlanId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=all|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)): The identifier for this MSTI or the identifier for the first VLAN in the range.
			PortNo (number): The port number associated with this STP interface. If enableAutoPickPortNum is set, the port number will be automatically assigned (not editable by the user). If enableAutoPickPortNum is not set, the port number can be configured by the user. The valid range is 1 to 4,095. (default = 1)
			Pvid (number): The Port VLAN ID. This value must be the same for all ports participating in the PVST+/RPVST+ protocol. The valid range is 1 to 4,094. (default = 1)

		Returns:
			self: This instance with all currently retrieved interface data using find and the newly added interface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoPick=None, BdpuGap=None, Cost=None, Enabled=None, InterfaceId=None, JitterEnabled=None, JitterPercentage=None, LinkType=None, MstiOrVlanId=None, PortNo=None, Pvid=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AutoPick (bool): If set, then the Auto-Pick Port Number feature is enabled and each STP interface configured for the same bridge will be assigned a unique port number automatically.(default = enabled)
			BdpuGap (number): The length of time between transmissions of BPDUs, in milliseconds. The valid range is 0 msec to 60,000 msec. (default = 0)
			Cost (number): The administrative path cost assigned to this interface. The valid range is 0 to 4294967295. (default = 1)
			Enabled (bool): Enables or disables the use of the interface. (default = disabled)
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The unique identifier for this interface.
			JitterEnabled (bool): Staggered transmit (jitter) for Hello messages. If set, then the jitter feature is enabled. (default = enabled)
			JitterPercentage (number): The maximum percentage of +/- variation (jitter) from the Hello message transmission interval.
			LinkType (str(pointToPoint|shared)): The type of link attached to this interface.
			MstiOrVlanId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=all|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)): The identifier for this MSTI or the identifier for the first VLAN in the range.
			PortNo (number): The port number associated with this STP interface. If enableAutoPickPortNum is set, the port number will be automatically assigned (not editable by the user). If enableAutoPickPortNum is not set, the port number can be configured by the user. The valid range is 1 to 4,095. (default = 1)
			Pvid (number): The Port VLAN ID. This value must be the same for all ports participating in the PVST+/RPVST+ protocol. The valid range is 1 to 4,094. (default = 1)

		Returns:
			self: This instance with matching interface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateParameters(self):
		"""Executes the updateParameters operation on the server.

		Updates the current STP bridge interface parameters.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
