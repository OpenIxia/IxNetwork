from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InstructionMiss(Base):
	"""The InstructionMiss class encapsulates a required instructionMiss node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InstructionMiss property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'instructionMiss'

	def __init__(self, parent):
		super(InstructionMiss, self).__init__(parent)

	@property
	def ApplyActions(self):
		"""If selected, applies the actions associated with a flow immediately.

		Returns:
			bool
		"""
		return self._get_attribute('applyActions')
	@ApplyActions.setter
	def ApplyActions(self, value):
		self._set_attribute('applyActions', value)

	@property
	def ClearActions(self):
		"""If selected, clears the actions attached with the flow.

		Returns:
			bool
		"""
		return self._get_attribute('clearActions')
	@ClearActions.setter
	def ClearActions(self, value):
		self._set_attribute('clearActions', value)

	@property
	def Experimenter(self):
		"""If selected, gives experimenter instruction.

		Returns:
			bool
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def GoToTable(self):
		"""If selected, forwards the packet to the next table in the pipeline.

		Returns:
			bool
		"""
		return self._get_attribute('goToTable')
	@GoToTable.setter
	def GoToTable(self, value):
		self._set_attribute('goToTable', value)

	@property
	def Meter(self):
		"""If selected, directs a flow to a particular meter.

		Returns:
			bool
		"""
		return self._get_attribute('meter')
	@Meter.setter
	def Meter(self, value):
		self._set_attribute('meter', value)

	@property
	def WriteActions(self):
		"""If selected, appends actions to the existing action set of the packet.

		Returns:
			bool
		"""
		return self._get_attribute('writeActions')
	@WriteActions.setter
	def WriteActions(self, value):
		self._set_attribute('writeActions', value)

	@property
	def WriteMetadata(self):
		"""If selected, writes the masked metadata field to the match.

		Returns:
			bool
		"""
		return self._get_attribute('writeMetadata')
	@WriteMetadata.setter
	def WriteMetadata(self, value):
		self._set_attribute('writeMetadata', value)
