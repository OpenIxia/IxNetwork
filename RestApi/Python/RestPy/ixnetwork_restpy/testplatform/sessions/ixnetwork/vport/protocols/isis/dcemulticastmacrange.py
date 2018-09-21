from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceMulticastMacRange(Base):
	"""The DceMulticastMacRange class encapsulates a user managed dceMulticastMacRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceMulticastMacRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceMulticastMacRange'

	def __init__(self, parent):
		super(DceMulticastMacRange, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables the Multicast MAC Range for a particular DCE ISIS route range. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterGroupUnicastMacIncrement(self):
		"""The MAC address format of the Unicast MAC between one or more node groups. (Default = 00 00 00 00 00)

		Returns:
			str
		"""
		return self._get_attribute('interGroupUnicastMacIncrement')
	@InterGroupUnicastMacIncrement.setter
	def InterGroupUnicastMacIncrement(self, value):
		self._set_attribute('interGroupUnicastMacIncrement', value)

	@property
	def IntraGroupUnicastMacIncrement(self):
		"""The MAC address format of the Unicast MAC within a node group. (Default = 00 00 00 00 01)

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastMacIncrement')
	@IntraGroupUnicastMacIncrement.setter
	def IntraGroupUnicastMacIncrement(self, value):
		self._set_attribute('intraGroupUnicastMacIncrement', value)

	@property
	def MulticastMacCount(self):
		"""The number of Multicast MAC addresses. This option takes unsigned integer value ranging from 1 to UINT_MAX.

		Returns:
			number
		"""
		return self._get_attribute('multicastMacCount')
	@MulticastMacCount.setter
	def MulticastMacCount(self, value):
		self._set_attribute('multicastMacCount', value)

	@property
	def MulticastMacStep(self):
		"""The incremental value of Multicast MAC address. (Default = 00 00 00 00 01)

		Returns:
			str
		"""
		return self._get_attribute('multicastMacStep')
	@MulticastMacStep.setter
	def MulticastMacStep(self, value):
		self._set_attribute('multicastMacStep', value)

	@property
	def SourceGroupMapping(self):
		"""The Source Group mapping type.

		Returns:
			str(fullyMeshed|oneToOne|manualMapping)
		"""
		return self._get_attribute('sourceGroupMapping')
	@SourceGroupMapping.setter
	def SourceGroupMapping(self, value):
		self._set_attribute('sourceGroupMapping', value)

	@property
	def StartMulticastMac(self):
		"""The MAC address format of the starting Multicast MAC. (Default = 0x01000000)

		Returns:
			str
		"""
		return self._get_attribute('startMulticastMac')
	@StartMulticastMac.setter
	def StartMulticastMac(self, value):
		self._set_attribute('startMulticastMac', value)

	@property
	def StartUnicastSourceMac(self):
		"""The MAC address format of the starting Unicast Source MAC. (Default = 00 00 00 00 00 00)

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceMac')
	@StartUnicastSourceMac.setter
	def StartUnicastSourceMac(self, value):
		self._set_attribute('startUnicastSourceMac', value)

	@property
	def Topology(self):
		"""The topology identifier to which the corresponding MAC belongs.

		Returns:
			number
		"""
		return self._get_attribute('topology')
	@Topology.setter
	def Topology(self, value):
		self._set_attribute('topology', value)

	@property
	def UnicastSourcesPerMulticastMac(self):
		"""The number of Unicast Source for each Multicast MAC address. This option takes unsigned integer value ranging from 0 to UINT_MAX.

		Returns:
			number
		"""
		return self._get_attribute('unicastSourcesPerMulticastMac')
	@UnicastSourcesPerMulticastMac.setter
	def UnicastSourcesPerMulticastMac(self, value):
		self._set_attribute('unicastSourcesPerMulticastMac', value)

	@property
	def VlanId(self):
		"""The VLAN ID of the enabled Multicast MAC Range. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	def add(self, Enabled=None, InterGroupUnicastMacIncrement=None, IntraGroupUnicastMacIncrement=None, MulticastMacCount=None, MulticastMacStep=None, SourceGroupMapping=None, StartMulticastMac=None, StartUnicastSourceMac=None, Topology=None, UnicastSourcesPerMulticastMac=None, VlanId=None):
		"""Adds a new dceMulticastMacRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true, enables the Multicast MAC Range for a particular DCE ISIS route range. (default = false)
			InterGroupUnicastMacIncrement (str): The MAC address format of the Unicast MAC between one or more node groups. (Default = 00 00 00 00 00)
			IntraGroupUnicastMacIncrement (str): The MAC address format of the Unicast MAC within a node group. (Default = 00 00 00 00 01)
			MulticastMacCount (number): The number of Multicast MAC addresses. This option takes unsigned integer value ranging from 1 to UINT_MAX.
			MulticastMacStep (str): The incremental value of Multicast MAC address. (Default = 00 00 00 00 01)
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): The Source Group mapping type.
			StartMulticastMac (str): The MAC address format of the starting Multicast MAC. (Default = 0x01000000)
			StartUnicastSourceMac (str): The MAC address format of the starting Unicast Source MAC. (Default = 00 00 00 00 00 00)
			Topology (number): The topology identifier to which the corresponding MAC belongs.
			UnicastSourcesPerMulticastMac (number): The number of Unicast Source for each Multicast MAC address. This option takes unsigned integer value ranging from 0 to UINT_MAX.
			VlanId (number): The VLAN ID of the enabled Multicast MAC Range. (default = 1)

		Returns:
			self: This instance with all currently retrieved dceMulticastMacRange data using find and the newly added dceMulticastMacRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceMulticastMacRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InterGroupUnicastMacIncrement=None, IntraGroupUnicastMacIncrement=None, MulticastMacCount=None, MulticastMacStep=None, SourceGroupMapping=None, StartMulticastMac=None, StartUnicastSourceMac=None, Topology=None, UnicastSourcesPerMulticastMac=None, VlanId=None):
		"""Finds and retrieves dceMulticastMacRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceMulticastMacRange data from the server.
		By default the find method takes no parameters and will retrieve all dceMulticastMacRange data from the server.

		Args:
			Enabled (bool): If true, enables the Multicast MAC Range for a particular DCE ISIS route range. (default = false)
			InterGroupUnicastMacIncrement (str): The MAC address format of the Unicast MAC between one or more node groups. (Default = 00 00 00 00 00)
			IntraGroupUnicastMacIncrement (str): The MAC address format of the Unicast MAC within a node group. (Default = 00 00 00 00 01)
			MulticastMacCount (number): The number of Multicast MAC addresses. This option takes unsigned integer value ranging from 1 to UINT_MAX.
			MulticastMacStep (str): The incremental value of Multicast MAC address. (Default = 00 00 00 00 01)
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): The Source Group mapping type.
			StartMulticastMac (str): The MAC address format of the starting Multicast MAC. (Default = 0x01000000)
			StartUnicastSourceMac (str): The MAC address format of the starting Unicast Source MAC. (Default = 00 00 00 00 00 00)
			Topology (number): The topology identifier to which the corresponding MAC belongs.
			UnicastSourcesPerMulticastMac (number): The number of Unicast Source for each Multicast MAC address. This option takes unsigned integer value ranging from 0 to UINT_MAX.
			VlanId (number): The VLAN ID of the enabled Multicast MAC Range. (default = 1)

		Returns:
			self: This instance with matching dceMulticastMacRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceMulticastMacRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceMulticastMacRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
