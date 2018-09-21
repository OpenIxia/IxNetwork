from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EndpointSet(Base):
	"""The EndpointSet class encapsulates a user managed endpointSet node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EndpointSet property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'endpointSet'

	def __init__(self, parent):
		super(EndpointSet, self).__init__(parent)

	@property
	def AllowEmptyTopologySets(self):
		"""Enable this to allow the setting of sources and destinations without throwing an error even if the combination produces an empty topology set.

		Returns:
			bool
		"""
		return self._get_attribute('allowEmptyTopologySets')
	@AllowEmptyTopologySets.setter
	def AllowEmptyTopologySets(self, value):
		self._set_attribute('allowEmptyTopologySets', value)

	@property
	def DestinationFilter(self):
		"""The list of conditions used for filtering destinations endpoints.

		Returns:
			str
		"""
		return self._get_attribute('destinationFilter')
	@DestinationFilter.setter
	def DestinationFilter(self, value):
		self._set_attribute('destinationFilter', value)

	@property
	def Destinations(self):
		"""Indicates the number of destination endpoints configured.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])
		"""
		return self._get_attribute('destinations')
	@Destinations.setter
	def Destinations(self, value):
		self._set_attribute('destinations', value)

	@property
	def MulticastDestinations(self):
		"""A compact representation of many virtual multicast destinations. Each list item consists of 5 values where the first two, a bool value and enum value, can be defaulted to false and none. The next two values are a starting address and step address which can be either an ipv4, ipv6 or streamId and the last value is a count of addresses.

		Returns:
			list(dict(arg1:bool,arg2:str[igmp|mld|none],arg3:str,arg4:str,arg5:number))
		"""
		return self._get_attribute('multicastDestinations')
	@MulticastDestinations.setter
	def MulticastDestinations(self, value):
		self._set_attribute('multicastDestinations', value)

	@property
	def MulticastReceivers(self):
		"""A list of virtual multicast receivers. Each list item consists of a multicast receiver object reference, port index, host index and group or join/prune index depending on the type of object reference.

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number))
		"""
		return self._get_attribute('multicastReceivers')
	@MulticastReceivers.setter
	def MulticastReceivers(self, value):
		self._set_attribute('multicastReceivers', value)

	@property
	def Name(self):
		"""The name of the endpoint set.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NgpfFilters(self):
		"""The list of next generation structures used to filter endpoints. The structure consists of a string tag and list of integer indexes.

		Returns:
			list(dict(arg1:str,arg2:list[number]))
		"""
		return self._get_attribute('ngpfFilters')
	@NgpfFilters.setter
	def NgpfFilters(self, value):
		self._set_attribute('ngpfFilters', value)

	@property
	def ScalableDestinations(self):
		"""A list of scalable destination structures

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))
		"""
		return self._get_attribute('scalableDestinations')
	@ScalableDestinations.setter
	def ScalableDestinations(self, value):
		self._set_attribute('scalableDestinations', value)

	@property
	def ScalableSources(self):
		"""A list of scalable source structures.

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))
		"""
		return self._get_attribute('scalableSources')
	@ScalableSources.setter
	def ScalableSources(self, value):
		self._set_attribute('scalableSources', value)

	@property
	def SourceFilter(self):
		"""The list of conditions used for filtering source endpoints.

		Returns:
			str
		"""
		return self._get_attribute('sourceFilter')
	@SourceFilter.setter
	def SourceFilter(self, value):
		self._set_attribute('sourceFilter', value)

	@property
	def Sources(self):
		"""Indicates the number of source endpoints configured.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])
		"""
		return self._get_attribute('sources')
	@Sources.setter
	def Sources(self, value):
		self._set_attribute('sources', value)

	@property
	def TrafficGroups(self):
		"""Indicates the traffic groups selected in the source/destination endpoint set.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*])
		"""
		return self._get_attribute('trafficGroups')
	@TrafficGroups.setter
	def TrafficGroups(self, value):
		self._set_attribute('trafficGroups', value)

	def add(self, AllowEmptyTopologySets=None, DestinationFilter=None, Destinations=None, MulticastDestinations=None, MulticastReceivers=None, Name=None, NgpfFilters=None, ScalableDestinations=None, ScalableSources=None, SourceFilter=None, Sources=None, TrafficGroups=None):
		"""Adds a new endpointSet node on the server and retrieves it in this instance.

		Args:
			AllowEmptyTopologySets (bool): Enable this to allow the setting of sources and destinations without throwing an error even if the combination produces an empty topology set.
			DestinationFilter (str): The list of conditions used for filtering destinations endpoints.
			Destinations (list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): Indicates the number of destination endpoints configured.
			MulticastDestinations (list(dict(arg1:bool,arg2:str[igmp|mld|none],arg3:str,arg4:str,arg5:number))): A compact representation of many virtual multicast destinations. Each list item consists of 5 values where the first two, a bool value and enum value, can be defaulted to false and none. The next two values are a starting address and step address which can be either an ipv4, ipv6 or streamId and the last value is a count of addresses.
			MulticastReceivers (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number))): A list of virtual multicast receivers. Each list item consists of a multicast receiver object reference, port index, host index and group or join/prune index depending on the type of object reference.
			Name (str): The name of the endpoint set.
			NgpfFilters (list(dict(arg1:str,arg2:list[number]))): The list of next generation structures used to filter endpoints. The structure consists of a string tag and list of integer indexes.
			ScalableDestinations (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))): A list of scalable destination structures
			ScalableSources (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))): A list of scalable source structures.
			SourceFilter (str): The list of conditions used for filtering source endpoints.
			Sources (list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): Indicates the number of source endpoints configured.
			TrafficGroups (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*])): Indicates the traffic groups selected in the source/destination endpoint set.

		Returns:
			self: This instance with all currently retrieved endpointSet data using find and the newly added endpointSet data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the endpointSet data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AllowEmptyTopologySets=None, DestinationFilter=None, Destinations=None, MulticastDestinations=None, MulticastReceivers=None, Name=None, NgpfFilters=None, ScalableDestinations=None, ScalableSources=None, SourceFilter=None, Sources=None, TrafficGroups=None):
		"""Finds and retrieves endpointSet data from the server.

		All named parameters support regex and can be used to selectively retrieve endpointSet data from the server.
		By default the find method takes no parameters and will retrieve all endpointSet data from the server.

		Args:
			AllowEmptyTopologySets (bool): Enable this to allow the setting of sources and destinations without throwing an error even if the combination produces an empty topology set.
			DestinationFilter (str): The list of conditions used for filtering destinations endpoints.
			Destinations (list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): Indicates the number of destination endpoints configured.
			MulticastDestinations (list(dict(arg1:bool,arg2:str[igmp|mld|none],arg3:str,arg4:str,arg5:number))): A compact representation of many virtual multicast destinations. Each list item consists of 5 values where the first two, a bool value and enum value, can be defaulted to false and none. The next two values are a starting address and step address which can be either an ipv4, ipv6 or streamId and the last value is a count of addresses.
			MulticastReceivers (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number))): A list of virtual multicast receivers. Each list item consists of a multicast receiver object reference, port index, host index and group or join/prune index depending on the type of object reference.
			Name (str): The name of the endpoint set.
			NgpfFilters (list(dict(arg1:str,arg2:list[number]))): The list of next generation structures used to filter endpoints. The structure consists of a string tag and list of integer indexes.
			ScalableDestinations (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))): A list of scalable destination structures
			ScalableSources (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))): A list of scalable source structures.
			SourceFilter (str): The list of conditions used for filtering source endpoints.
			Sources (list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): Indicates the number of source endpoints configured.
			TrafficGroups (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*])): Indicates the traffic groups selected in the source/destination endpoint set.

		Returns:
			self: This instance with matching endpointSet data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of endpointSet data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the endpointSet data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def FindMulticastReceiverGroupIndex(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the findMulticastReceiverGroupIndex operation on the server.

		This will lookup the multicast receiver group index from the multicast provider using the group id start/step/count which can then be used as the group index argument in the endpointSet multicastReceivers struct.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=endpointSet)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): A valid object reference
			Arg3 (str): The multicast group id start value
			Arg4 (str): The multicast group id step value
			Arg5 (number): The multicast group id count value

		Returns:
			number: The index of the multicast group id.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FindMulticastReceiverGroupIndex', payload=locals(), response_object=None)

	def FindMulticastReceiverGroupIndex(self, Arg2, Arg3):
		"""Executes the findMulticastReceiverGroupIndex operation on the server.

		This will lookup the multicast receiver group index from the multicast provider using the group id which can then be used as the group index argument in the endpointSet multicastReceivers struct.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=endpointSet)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/topology)): A valid object reference
			Arg3 (str): The multicast group id which must be an eight digit hex value separated by colons i.e., 00:00:01:01:00:01:01:00.

		Returns:
			number: The index of the multicast group id.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FindMulticastReceiverGroupIndex', payload=locals(), response_object=None)
