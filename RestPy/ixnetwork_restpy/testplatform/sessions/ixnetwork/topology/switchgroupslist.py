from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchGroupsList(Base):
	"""The SwitchGroupsList class encapsulates a system managed switchGroupsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchGroupsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchGroupsList'

	def __init__(self, parent):
		super(SwitchGroupsList, self).__init__(parent)

	@property
	def Active(self):
		"""Checked or Unchecked based on the Group Type selections in Groups tab under OF Switch tab-page.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ApplyGroup(self):
		"""Group Action:Apply Group.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applyGroup')

	@property
	def CopyTtlIn(self):
		"""Group Action:Copy TTL inwards from outermost to next-to-outermost.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('copyTtlIn')

	@property
	def CopyTtlOut(self):
		"""Group Action:Copy TTL outwards from next-to-outermost to outermost.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('copyTtlOut')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DecrementMplsTtl(self):
		"""Group Action:Decrement MPLS TTL.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('decrementMplsTtl')

	@property
	def DecrementNetwork(self):
		"""Group Action:Decrement IP TTL.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('decrementNetwork')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def GroupType(self):
		"""Can be of the following types per switch: 1)All: Execute all buckets in the group. 2)Select:Execute one bucket in the group. 3)Indirect:Execute the one defined bucket in this group. 4)Fast Failover:Execute the first live bucket.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupType')

	@property
	def MaxNumberOfGroups(self):
		"""Maximum number of groups for each group type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxNumberOfGroups')

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
	def Output(self):
		"""Group Action:Output to switch port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('output')

	@property
	def ParentSwitch(self):
		"""Parent Switch Name.

		Returns:
			str
		"""
		return self._get_attribute('parentSwitch')

	@property
	def PopMpls(self):
		"""Group Action:Pop the outer MPLS tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('popMpls')

	@property
	def PopPbb(self):
		"""Group Action:Pop the outer PBB service tag (I-TAG).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('popPbb')

	@property
	def PopVlan(self):
		"""Group Action:Pop the outer VLAN tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('popVlan')

	@property
	def PushMpls(self):
		"""Group Action:Push a new MPLS tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pushMpls')

	@property
	def PushPbb(self):
		"""Group Action:Push a new PBB service tag (I-TAG).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pushPbb')

	@property
	def PushVlan(self):
		"""Group Action:Push a new VLAN tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pushVlan')

	@property
	def SetField(self):
		"""Group Action:Set a header field using OXM TLV format.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setField')

	@property
	def SetMplsTtl(self):
		"""Group Action:Set MPLS TTL.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setMplsTtl')

	@property
	def SetNetwork(self):
		"""Group Action:Set IP TTL.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setNetwork')

	@property
	def SetQueue(self):
		"""Group Action:Set queue id when outputting to a port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setQueue')

	def find(self, Count=None, DescriptiveName=None, Name=None, ParentSwitch=None):
		"""Finds and retrieves switchGroupsList data from the server.

		All named parameters support regex and can be used to selectively retrieve switchGroupsList data from the server.
		By default the find method takes no parameters and will retrieve all switchGroupsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			ParentSwitch (str): Parent Switch Name.

		Returns:
			self: This instance with matching switchGroupsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchGroupsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchGroupsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
