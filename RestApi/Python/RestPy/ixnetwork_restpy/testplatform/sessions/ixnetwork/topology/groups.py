from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Groups(Base):
	"""The Groups class encapsulates a system managed groups node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Groups property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groups'

	def __init__(self, parent):
		super(Groups, self).__init__(parent)

	@property
	def Buckets(self):
		"""An instance of the Buckets class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.buckets.Buckets)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.buckets import Buckets
		return Buckets(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ChannelName(self):
		"""Parent Channel Name

		Returns:
			str
		"""
		return self._get_attribute('channelName')

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
	def GroupAdvertise(self):
		"""If selected, group is advertised when the OpenFlow channel comes up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAdvertise')

	@property
	def GroupDescription(self):
		"""A description of the group.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupDescription')

	@property
	def GroupId(self):
		"""A 32-bit integer uniquely identifying the group.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupId')

	@property
	def GroupType(self):
		"""Select the type of group to determine the group semantics.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupType')

	@property
	def Multiplier(self):
		"""Number of instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

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
	def NumberOfBuckets(self):
		"""Specify the number of Buckets.

		Returns:
			number
		"""
		return self._get_attribute('numberOfBuckets')
	@NumberOfBuckets.setter
	def NumberOfBuckets(self, value):
		self._set_attribute('numberOfBuckets', value)

	@property
	def OfChannel(self):
		"""The OF Channel to which the group belongs.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ofChannel')

	def find(self, ChannelName=None, Count=None, DescriptiveName=None, Multiplier=None, Name=None, NumberOfBuckets=None):
		"""Finds and retrieves groups data from the server.

		All named parameters support regex and can be used to selectively retrieve groups data from the server.
		By default the find method takes no parameters and will retrieve all groups data from the server.

		Args:
			ChannelName (str): Parent Channel Name
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Multiplier (number): Number of instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfBuckets (number): Specify the number of Buckets.

		Returns:
			self: This instance with matching groups data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groups data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groups data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SendAllGroupAdd(self):
		"""Executes the sendAllGroupAdd operation on the server.

		Sends a Group Add on all groups.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendAllGroupAdd', payload=locals(), response_object=None)

	def SendAllGroupRemove(self):
		"""Executes the sendAllGroupRemove operation on the server.

		Sends a Group Remove on all groups.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendAllGroupRemove', payload=locals(), response_object=None)

	def SendGroupAdd(self, Arg2):
		"""Executes the sendGroupAdd operation on the server.

		Sends a Group Add on selected Group.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendGroupAdd', payload=locals(), response_object=None)

	def SendGroupRemove(self, Arg2):
		"""Executes the sendGroupRemove operation on the server.

		Sends a Group Remove on selected Group.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendGroupRemove', payload=locals(), response_object=None)
