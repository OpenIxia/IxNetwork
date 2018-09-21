from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchTablesList(Base):
	"""The SwitchTablesList class encapsulates a system managed switchTablesList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchTablesList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchTablesList'

	def __init__(self, parent):
		super(SwitchTablesList, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ApplyActions(self):
		"""Select the type of apply action capability that the table will support. The selected actions associated with a flow are applied immediately

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applyActions')

	@property
	def ApplyActionsMiss(self):
		"""Select the type of apply action miss capability that the table miss flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applyActionsMiss')

	@property
	def ApplySetField(self):
		"""Select the type of Apply Set Field capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applySetField')

	@property
	def ApplySetFieldMask(self):
		"""Select the type of Apply Set Field Mask capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applySetFieldMask')

	@property
	def ApplySetFieldMiss(self):
		"""Select the type of Apply Set Field Miss capability that the table miss flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applySetFieldMiss')

	@property
	def ApplySetFieldMissMask(self):
		"""Select the type of Apply Set Field Miss capability that the table miss flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('applySetFieldMissMask')

	@property
	def AutoConfigNextTable(self):
		"""If selected, the Next Table and Next Table Miss are automatically configured

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoConfigNextTable')

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
	def FeaturesSupported(self):
		"""Select the table feature properties to enable them

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('featuresSupported')

	@property
	def Instruction(self):
		"""Select the type of Instructions that the table flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('instruction')

	@property
	def InstructionMiss(self):
		"""Select the type of Instruction miss capabilities that the table miss flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('instructionMiss')

	@property
	def Match(self):
		"""Select the type of match capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('match')

	@property
	def MatchMask(self):
		"""Select the type of match mask capability that the table will support.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('matchMask')

	@property
	def MaxTableEntries(self):
		"""Specify Maximum Entries per Table.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxTableEntries')

	@property
	def MetadataMatch(self):
		"""Specify the bits of Metadata which the table can match

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metadataMatch')

	@property
	def MetadataWrite(self):
		"""Specify the bits of Metadata which the table can write

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metadataWrite')

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
	def NextTable(self):
		"""Specify the next table property (in incrementing order) seperated by , or - (for range) Eg: 1,2,3,4 or 1-4 or 1, 10-20.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nextTable')

	@property
	def NextTableMiss(self):
		"""Specify the next table miss property (in incrementing order) seperated by , or - (for range) Eg: 1,2,3,4 or 1-4 or 1, 10-20.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nextTableMiss')

	@property
	def ParentSwitch(self):
		"""Parent Switch Name

		Returns:
			str
		"""
		return self._get_attribute('parentSwitch')

	@property
	def TableId(self):
		"""Specify the Table Id, {0 - 254}

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableId')

	@property
	def TableName(self):
		"""Specify the name of the Table.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableName')

	@property
	def WildcardFeature(self):
		"""Select the type of wildcard capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('wildcardFeature')

	@property
	def WildcardFeatureMask(self):
		"""Select the type of wildcard mask capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('wildcardFeatureMask')

	@property
	def WriteActions(self):
		"""Select the type of write action capability that the table will support. The selected actions are appended to the existing action set of the packet

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('writeActions')

	@property
	def WriteActionsMiss(self):
		"""Select the type of write action miss capability that the table miss flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('writeActionsMiss')

	@property
	def WriteSetField(self):
		"""Select the type of Write Set Field capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('writeSetField')

	@property
	def WriteSetFieldMask(self):
		"""Select the type of Write Set Field Mask capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('writeSetFieldMask')

	@property
	def WriteSetFieldMiss(self):
		"""Select the type of Write Set Field Miss capability that the table miss flow entry will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('writeSetFieldMiss')

	@property
	def WriteSetFieldMissMask(self):
		"""Select the type of Write Set Field Miss mask capability that the table will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('writeSetFieldMissMask')

	def find(self, Count=None, DescriptiveName=None, Name=None, ParentSwitch=None):
		"""Finds and retrieves switchTablesList data from the server.

		All named parameters support regex and can be used to selectively retrieve switchTablesList data from the server.
		By default the find method takes no parameters and will retrieve all switchTablesList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			ParentSwitch (str): Parent Switch Name

		Returns:
			self: This instance with matching switchTablesList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchTablesList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchTablesList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
