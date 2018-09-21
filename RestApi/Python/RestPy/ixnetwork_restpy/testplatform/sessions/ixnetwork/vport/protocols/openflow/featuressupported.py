from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FeaturesSupported(Base):
	"""The FeaturesSupported class encapsulates a required featuresSupported node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FeaturesSupported property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'featuresSupported'

	def __init__(self, parent):
		super(FeaturesSupported, self).__init__(parent)

	@property
	def ApplyActions(self):
		"""Select the type of apply action instructions that the table flow entry will support. The selected actions associated with a flow are applied immediately.

		Returns:
			bool
		"""
		return self._get_attribute('applyActions')
	@ApplyActions.setter
	def ApplyActions(self, value):
		self._set_attribute('applyActions', value)

	@property
	def ApplyActionsMiss(self):
		"""Select the type of apply action miss instructions that the table miss flow entry will support.

		Returns:
			bool
		"""
		return self._get_attribute('applyActionsMiss')
	@ApplyActionsMiss.setter
	def ApplyActionsMiss(self, value):
		self._set_attribute('applyActionsMiss', value)

	@property
	def ApplySetField(self):
		"""Apply set field property.

		Returns:
			bool
		"""
		return self._get_attribute('applySetField')
	@ApplySetField.setter
	def ApplySetField(self, value):
		self._set_attribute('applySetField', value)

	@property
	def ApplySetFieldMiss(self):
		"""Apply set field for table-miss.

		Returns:
			bool
		"""
		return self._get_attribute('applySetFieldMiss')
	@ApplySetFieldMiss.setter
	def ApplySetFieldMiss(self, value):
		self._set_attribute('applySetFieldMiss', value)

	@property
	def Experimenter(self):
		"""This view lists all the experimenter properties that can be configured. Experimenter messages provide a standard way for OpenFlow switches to offer additional functionality within the OpenFlow message type space.

		Returns:
			bool
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def ExperimenterMiss(self):
		"""Experimenter for table-miss.

		Returns:
			bool
		"""
		return self._get_attribute('experimenterMiss')
	@ExperimenterMiss.setter
	def ExperimenterMiss(self, value):
		self._set_attribute('experimenterMiss', value)

	@property
	def Instruction(self):
		"""It select the type of instructions that the table flow entry will support

		Returns:
			bool
		"""
		return self._get_attribute('instruction')
	@Instruction.setter
	def Instruction(self, value):
		self._set_attribute('instruction', value)

	@property
	def InstructionMiss(self):
		"""Select the type of instruction miss capabilities that the table miss flow entry will support.

		Returns:
			bool
		"""
		return self._get_attribute('instructionMiss')
	@InstructionMiss.setter
	def InstructionMiss(self, value):
		self._set_attribute('instructionMiss', value)

	@property
	def Match(self):
		"""Select the type of match instructions that the table will support.

		Returns:
			bool
		"""
		return self._get_attribute('match')
	@Match.setter
	def Match(self, value):
		self._set_attribute('match', value)

	@property
	def NextTable(self):
		"""Specify the array of tables that can be directly reached from the present table using the GoTo Table instruction.

		Returns:
			bool
		"""
		return self._get_attribute('nextTable')
	@NextTable.setter
	def NextTable(self, value):
		self._set_attribute('nextTable', value)

	@property
	def NextTableMiss(self):
		"""Specify the Next table Miss value.

		Returns:
			bool
		"""
		return self._get_attribute('nextTableMiss')
	@NextTableMiss.setter
	def NextTableMiss(self, value):
		self._set_attribute('nextTableMiss', value)

	@property
	def Wildcards(self):
		"""Select the type of wildcard instructions that the table will support.

		Returns:
			bool
		"""
		return self._get_attribute('wildcards')
	@Wildcards.setter
	def Wildcards(self, value):
		self._set_attribute('wildcards', value)

	@property
	def WriteActions(self):
		"""Select the type of write action instructions that the table flow entry will support.

		Returns:
			bool
		"""
		return self._get_attribute('writeActions')
	@WriteActions.setter
	def WriteActions(self, value):
		self._set_attribute('writeActions', value)

	@property
	def WriteActionsMiss(self):
		"""Select the type of write action miss instructions that the table miss flow entry will support.

		Returns:
			bool
		"""
		return self._get_attribute('writeActionsMiss')
	@WriteActionsMiss.setter
	def WriteActionsMiss(self, value):
		self._set_attribute('writeActionsMiss', value)

	@property
	def WriteSetField(self):
		"""Apply set field for table-miss.

		Returns:
			bool
		"""
		return self._get_attribute('writeSetField')
	@WriteSetField.setter
	def WriteSetField(self, value):
		self._set_attribute('writeSetField', value)

	@property
	def WriteSetFieldMiss(self):
		"""Write set field for table-miss.

		Returns:
			bool
		"""
		return self._get_attribute('writeSetFieldMiss')
	@WriteSetFieldMiss.setter
	def WriteSetFieldMiss(self, value):
		self._set_attribute('writeSetFieldMiss', value)
