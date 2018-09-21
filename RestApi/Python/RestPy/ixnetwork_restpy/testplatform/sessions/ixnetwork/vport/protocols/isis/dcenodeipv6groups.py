from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceNodeIpv6Groups(Base):
	"""The DceNodeIpv6Groups class encapsulates a user managed dceNodeIpv6Groups node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceNodeIpv6Groups property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceNodeIpv6Groups'

	def __init__(self, parent):
		super(DceNodeIpv6Groups, self).__init__(parent)

	@property
	def IncludeIpv6Groups(self):
		"""If true, includes IPv6 groups for this Network Range.

		Returns:
			bool
		"""
		return self._get_attribute('includeIpv6Groups')
	@IncludeIpv6Groups.setter
	def IncludeIpv6Groups(self, value):
		self._set_attribute('includeIpv6Groups', value)

	@property
	def InterGroupUnicastIpv6Increment(self):
		"""The IPv6 address format of the Unicast IPv6 between one or more node groups.

		Returns:
			str
		"""
		return self._get_attribute('interGroupUnicastIpv6Increment')
	@InterGroupUnicastIpv6Increment.setter
	def InterGroupUnicastIpv6Increment(self, value):
		self._set_attribute('interGroupUnicastIpv6Increment', value)

	@property
	def IntraGroupUnicastIpv6Increment(self):
		"""The IPv6 address format of the Unicast MAC within a node group.

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastIpv6Increment')
	@IntraGroupUnicastIpv6Increment.setter
	def IntraGroupUnicastIpv6Increment(self, value):
		self._set_attribute('intraGroupUnicastIpv6Increment', value)

	@property
	def MulticastAddressNodeStep(self):
		"""The Multicast IPv6 address that configures the increment across the Network Range simulated RBridges.

		Returns:
			str
		"""
		return self._get_attribute('multicastAddressNodeStep')
	@MulticastAddressNodeStep.setter
	def MulticastAddressNodeStep(self, value):
		self._set_attribute('multicastAddressNodeStep', value)

	@property
	def MulticastIpv6Count(self):
		"""The number of Multicast IPv6 addresses.

		Returns:
			number
		"""
		return self._get_attribute('multicastIpv6Count')
	@MulticastIpv6Count.setter
	def MulticastIpv6Count(self, value):
		self._set_attribute('multicastIpv6Count', value)

	@property
	def MulticastIpv6Step(self):
		"""The incremental value of Multicast IPv6 address.

		Returns:
			str
		"""
		return self._get_attribute('multicastIpv6Step')
	@MulticastIpv6Step.setter
	def MulticastIpv6Step(self, value):
		self._set_attribute('multicastIpv6Step', value)

	@property
	def NoOfUnicastScrIpv6sPerMulicastIpv6(self):
		"""The number of Unicast Source for each Multicast IPv6 address.

		Returns:
			number
		"""
		return self._get_attribute('noOfUnicastScrIpv6sPerMulicastIpv6')
	@NoOfUnicastScrIpv6sPerMulicastIpv6.setter
	def NoOfUnicastScrIpv6sPerMulicastIpv6(self, value):
		self._set_attribute('noOfUnicastScrIpv6sPerMulicastIpv6', value)

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
	def StartMulticastIpv6(self):
		"""The IP address format of the starting Multicast IPv6 address.

		Returns:
			str
		"""
		return self._get_attribute('startMulticastIpv6')
	@StartMulticastIpv6.setter
	def StartMulticastIpv6(self, value):
		self._set_attribute('startMulticastIpv6', value)

	@property
	def StartUnicastSourceIpv6(self):
		"""The IPv6 address format of the starting Unicast Source IPv6.

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceIpv6')
	@StartUnicastSourceIpv6.setter
	def StartUnicastSourceIpv6(self, value):
		self._set_attribute('startUnicastSourceIpv6', value)

	@property
	def UnicastAddressNodeStep(self):
		"""The Unicast IPv6 address that configures the increment across the Network Range simulated RBridges.

		Returns:
			str
		"""
		return self._get_attribute('unicastAddressNodeStep')
	@UnicastAddressNodeStep.setter
	def UnicastAddressNodeStep(self, value):
		self._set_attribute('unicastAddressNodeStep', value)

	@property
	def VlanId(self):
		"""The VLAN ID of the enabled Multicast IPv6 Group Range.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	def add(self, IncludeIpv6Groups=None, InterGroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastAddressNodeStep=None, MulticastIpv6Count=None, MulticastIpv6Step=None, NoOfUnicastScrIpv6sPerMulicastIpv6=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Adds a new dceNodeIpv6Groups node on the server and retrieves it in this instance.

		Args:
			IncludeIpv6Groups (bool): If true, includes IPv6 groups for this Network Range.
			InterGroupUnicastIpv6Increment (str): The IPv6 address format of the Unicast IPv6 between one or more node groups.
			IntraGroupUnicastIpv6Increment (str): The IPv6 address format of the Unicast MAC within a node group.
			MulticastAddressNodeStep (str): The Multicast IPv6 address that configures the increment across the Network Range simulated RBridges.
			MulticastIpv6Count (number): The number of Multicast IPv6 addresses.
			MulticastIpv6Step (str): The incremental value of Multicast IPv6 address.
			NoOfUnicastScrIpv6sPerMulicastIpv6 (number): The number of Unicast Source for each Multicast IPv6 address.
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): The Source Group mapping type.
			StartMulticastIpv6 (str): The IP address format of the starting Multicast IPv6 address.
			StartUnicastSourceIpv6 (str): The IPv6 address format of the starting Unicast Source IPv6.
			UnicastAddressNodeStep (str): The Unicast IPv6 address that configures the increment across the Network Range simulated RBridges.
			VlanId (number): The VLAN ID of the enabled Multicast IPv6 Group Range.

		Returns:
			self: This instance with all currently retrieved dceNodeIpv6Groups data using find and the newly added dceNodeIpv6Groups data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceNodeIpv6Groups data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeIpv6Groups=None, InterGroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastAddressNodeStep=None, MulticastIpv6Count=None, MulticastIpv6Step=None, NoOfUnicastScrIpv6sPerMulicastIpv6=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Finds and retrieves dceNodeIpv6Groups data from the server.

		All named parameters support regex and can be used to selectively retrieve dceNodeIpv6Groups data from the server.
		By default the find method takes no parameters and will retrieve all dceNodeIpv6Groups data from the server.

		Args:
			IncludeIpv6Groups (bool): If true, includes IPv6 groups for this Network Range.
			InterGroupUnicastIpv6Increment (str): The IPv6 address format of the Unicast IPv6 between one or more node groups.
			IntraGroupUnicastIpv6Increment (str): The IPv6 address format of the Unicast MAC within a node group.
			MulticastAddressNodeStep (str): The Multicast IPv6 address that configures the increment across the Network Range simulated RBridges.
			MulticastIpv6Count (number): The number of Multicast IPv6 addresses.
			MulticastIpv6Step (str): The incremental value of Multicast IPv6 address.
			NoOfUnicastScrIpv6sPerMulicastIpv6 (number): The number of Unicast Source for each Multicast IPv6 address.
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): The Source Group mapping type.
			StartMulticastIpv6 (str): The IP address format of the starting Multicast IPv6 address.
			StartUnicastSourceIpv6 (str): The IPv6 address format of the starting Unicast Source IPv6.
			UnicastAddressNodeStep (str): The Unicast IPv6 address that configures the increment across the Network Range simulated RBridges.
			VlanId (number): The VLAN ID of the enabled Multicast IPv6 Group Range.

		Returns:
			self: This instance with matching dceNodeIpv6Groups data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceNodeIpv6Groups data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceNodeIpv6Groups data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
