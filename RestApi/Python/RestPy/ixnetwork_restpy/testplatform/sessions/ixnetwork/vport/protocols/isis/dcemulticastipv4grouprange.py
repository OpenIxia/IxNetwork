from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceMulticastIpv4GroupRange(Base):
	"""The DceMulticastIpv4GroupRange class encapsulates a user managed dceMulticastIpv4GroupRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceMulticastIpv4GroupRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceMulticastIpv4GroupRange'

	def __init__(self, parent):
		super(DceMulticastIpv4GroupRange, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables the Multicast IPv4 Group Range for a particular DCE ISIS route range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterGroupUnicastIpv4Increment(self):
		"""The IPv4 address format of the Unicast IPv4 between one or more node groups. (Default = 00 00 00 00 00)

		Returns:
			str
		"""
		return self._get_attribute('interGroupUnicastIpv4Increment')
	@InterGroupUnicastIpv4Increment.setter
	def InterGroupUnicastIpv4Increment(self, value):
		self._set_attribute('interGroupUnicastIpv4Increment', value)

	@property
	def IntraGroupUnicastIpv4Increment(self):
		"""The IPv4 address format of the Unicast IPv4 within a node group. (default = 0.0.0.1)

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastIpv4Increment')
	@IntraGroupUnicastIpv4Increment.setter
	def IntraGroupUnicastIpv4Increment(self, value):
		self._set_attribute('intraGroupUnicastIpv4Increment', value)

	@property
	def MulticastIpv4Count(self):
		"""The number of Multicast IPv4 addresses. This field takes unsigned integer value ranging from 1 to UINT_MAX. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('multicastIpv4Count')
	@MulticastIpv4Count.setter
	def MulticastIpv4Count(self, value):
		self._set_attribute('multicastIpv4Count', value)

	@property
	def MulticastIpv4Step(self):
		"""The incremental value of Multicast IPv4 address. (default = 0.0.0.1)

		Returns:
			str
		"""
		return self._get_attribute('multicastIpv4Step')
	@MulticastIpv4Step.setter
	def MulticastIpv4Step(self, value):
		self._set_attribute('multicastIpv4Step', value)

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
	def StartMulticastIpv4(self):
		"""The IP address format of the starting Multicast IPv4 address. (default = 224.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('startMulticastIpv4')
	@StartMulticastIpv4.setter
	def StartMulticastIpv4(self, value):
		self._set_attribute('startMulticastIpv4', value)

	@property
	def StartUnicastSourceIpv4(self):
		"""The IPv4 address format of the starting Unicast Source IPv4. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceIpv4')
	@StartUnicastSourceIpv4.setter
	def StartUnicastSourceIpv4(self, value):
		self._set_attribute('startUnicastSourceIpv4', value)

	@property
	def Topology(self):
		"""The topology identifier to which the corresponding IpV4 belongs.

		Returns:
			number
		"""
		return self._get_attribute('topology')
	@Topology.setter
	def Topology(self, value):
		self._set_attribute('topology', value)

	@property
	def UnicastSourcesPerMulticastIpv4(self):
		"""The number of Unicast Source for each Multicast IPv4 address. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('unicastSourcesPerMulticastIpv4')
	@UnicastSourcesPerMulticastIpv4.setter
	def UnicastSourcesPerMulticastIpv4(self, value):
		self._set_attribute('unicastSourcesPerMulticastIpv4', value)

	@property
	def VlanId(self):
		"""The VLAN ID of the enabled Multicast IPv4 Group Range. (default =1)

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	def add(self, Enabled=None, InterGroupUnicastIpv4Increment=None, IntraGroupUnicastIpv4Increment=None, MulticastIpv4Count=None, MulticastIpv4Step=None, SourceGroupMapping=None, StartMulticastIpv4=None, StartUnicastSourceIpv4=None, Topology=None, UnicastSourcesPerMulticastIpv4=None, VlanId=None):
		"""Adds a new dceMulticastIpv4GroupRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true, enables the Multicast IPv4 Group Range for a particular DCE ISIS route range.
			InterGroupUnicastIpv4Increment (str): The IPv4 address format of the Unicast IPv4 between one or more node groups. (Default = 00 00 00 00 00)
			IntraGroupUnicastIpv4Increment (str): The IPv4 address format of the Unicast IPv4 within a node group. (default = 0.0.0.1)
			MulticastIpv4Count (number): The number of Multicast IPv4 addresses. This field takes unsigned integer value ranging from 1 to UINT_MAX. (default = 1)
			MulticastIpv4Step (str): The incremental value of Multicast IPv4 address. (default = 0.0.0.1)
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): The Source Group mapping type.
			StartMulticastIpv4 (str): The IP address format of the starting Multicast IPv4 address. (default = 224.0.0.0)
			StartUnicastSourceIpv4 (str): The IPv4 address format of the starting Unicast Source IPv4. (default = 0.0.0.0)
			Topology (number): The topology identifier to which the corresponding IpV4 belongs.
			UnicastSourcesPerMulticastIpv4 (number): The number of Unicast Source for each Multicast IPv4 address. (default = 1)
			VlanId (number): The VLAN ID of the enabled Multicast IPv4 Group Range. (default =1)

		Returns:
			self: This instance with all currently retrieved dceMulticastIpv4GroupRange data using find and the newly added dceMulticastIpv4GroupRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceMulticastIpv4GroupRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InterGroupUnicastIpv4Increment=None, IntraGroupUnicastIpv4Increment=None, MulticastIpv4Count=None, MulticastIpv4Step=None, SourceGroupMapping=None, StartMulticastIpv4=None, StartUnicastSourceIpv4=None, Topology=None, UnicastSourcesPerMulticastIpv4=None, VlanId=None):
		"""Finds and retrieves dceMulticastIpv4GroupRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceMulticastIpv4GroupRange data from the server.
		By default the find method takes no parameters and will retrieve all dceMulticastIpv4GroupRange data from the server.

		Args:
			Enabled (bool): If true, enables the Multicast IPv4 Group Range for a particular DCE ISIS route range.
			InterGroupUnicastIpv4Increment (str): The IPv4 address format of the Unicast IPv4 between one or more node groups. (Default = 00 00 00 00 00)
			IntraGroupUnicastIpv4Increment (str): The IPv4 address format of the Unicast IPv4 within a node group. (default = 0.0.0.1)
			MulticastIpv4Count (number): The number of Multicast IPv4 addresses. This field takes unsigned integer value ranging from 1 to UINT_MAX. (default = 1)
			MulticastIpv4Step (str): The incremental value of Multicast IPv4 address. (default = 0.0.0.1)
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): The Source Group mapping type.
			StartMulticastIpv4 (str): The IP address format of the starting Multicast IPv4 address. (default = 224.0.0.0)
			StartUnicastSourceIpv4 (str): The IPv4 address format of the starting Unicast Source IPv4. (default = 0.0.0.0)
			Topology (number): The topology identifier to which the corresponding IpV4 belongs.
			UnicastSourcesPerMulticastIpv4 (number): The number of Unicast Source for each Multicast IPv4 address. (default = 1)
			VlanId (number): The VLAN ID of the enabled Multicast IPv4 Group Range. (default =1)

		Returns:
			self: This instance with matching dceMulticastIpv4GroupRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceMulticastIpv4GroupRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceMulticastIpv4GroupRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
