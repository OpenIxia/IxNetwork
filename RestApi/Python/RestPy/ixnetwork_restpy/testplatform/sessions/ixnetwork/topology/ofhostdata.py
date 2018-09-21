from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfHostData(Base):
	"""The OfHostData class encapsulates a user managed ofHostData node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfHostData property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ofHostData'

	def __init__(self, parent):
		super(OfHostData, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NumberOfHostPorts(self):
		"""number of Host Ports per OF Switch.

		Returns:
			number
		"""
		return self._get_attribute('numberOfHostPorts')
	@NumberOfHostPorts.setter
	def NumberOfHostPorts(self, value):
		self._set_attribute('numberOfHostPorts', value)

	@property
	def NumberOfHostsPerPort(self):
		"""Number of Host Groups for each Host Port. Configure Number of Hosts Per Host Group using the Count field in Encapsulations Tab

		Returns:
			number
		"""
		return self._get_attribute('numberOfHostsPerPort')
	@NumberOfHostsPerPort.setter
	def NumberOfHostsPerPort(self, value):
		self._set_attribute('numberOfHostsPerPort', value)

	@property
	def ParentSwitchPortName(self):
		"""Description of the parent Switch Port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('parentSwitchPortName')

	def add(self, Name=None, NumberOfHostPorts=None, NumberOfHostsPerPort=None):
		"""Adds a new ofHostData node on the server and retrieves it in this instance.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfHostPorts (number): number of Host Ports per OF Switch.
			NumberOfHostsPerPort (number): Number of Host Groups for each Host Port. Configure Number of Hosts Per Host Group using the Count field in Encapsulations Tab

		Returns:
			self: This instance with all currently retrieved ofHostData data using find and the newly added ofHostData data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ofHostData data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, DescriptiveName=None, Name=None, NumberOfHostPorts=None, NumberOfHostsPerPort=None):
		"""Finds and retrieves ofHostData data from the server.

		All named parameters support regex and can be used to selectively retrieve ofHostData data from the server.
		By default the find method takes no parameters and will retrieve all ofHostData data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfHostPorts (number): number of Host Ports per OF Switch.
			NumberOfHostsPerPort (number): Number of Host Groups for each Host Port. Configure Number of Hosts Per Host Group using the Count field in Encapsulations Tab

		Returns:
			self: This instance with matching ofHostData data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofHostData data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofHostData data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SendPacketWithTraverseLI(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7, Arg8, Arg9):
		"""Executes the sendPacketWithTraverseLI operation on the server.

		Send an Host Packet (ARP/PING/CUSTOM) from the given device instance to the given destination instance.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the device group for the corresponding device instances whose IP addresses are used as the source of the request messages.
			Arg3 (number): Destination Host index.
			Arg4 (str(aRP|custom|pING)): Packet Type.
			Arg5 (number): Encapsulation index.
			Arg6 (number): Response Timeout.
			Arg7 (bool): Periodic.
			Arg8 (number): Periodic Interval.
			Arg9 (number): Number of Iteration.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPacketWithTraverseLI', payload=locals(), response_object=None)
