from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ControllerTables(Base):
	"""The ControllerTables class encapsulates a user managed controllerTables node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ControllerTables property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'controllerTables'

	def __init__(self, parent):
		super(ControllerTables, self).__init__(parent)

	@property
	def ApplyActions(self):
		"""An instance of the ApplyActions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactions.ApplyActions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactions import ApplyActions
		return ApplyActions(self)._select()

	@property
	def ApplyActionsMiss(self):
		"""An instance of the ApplyActionsMiss class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionsmiss.ApplyActionsMiss)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionsmiss import ApplyActionsMiss
		return ApplyActionsMiss(self)._select()

	@property
	def ApplySetField(self):
		"""An instance of the ApplySetField class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfield.ApplySetField)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfield import ApplySetField
		return ApplySetField(self)._select()

	@property
	def ApplySetFieldMiss(self):
		"""An instance of the ApplySetFieldMiss class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfieldmiss.ApplySetFieldMiss)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfieldmiss import ApplySetFieldMiss
		return ApplySetFieldMiss(self)._select()

	@property
	def ControllerTableFlowRanges(self):
		"""An instance of the ControllerTableFlowRanges class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllertableflowranges.ControllerTableFlowRanges)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllertableflowranges import ControllerTableFlowRanges
		return ControllerTableFlowRanges(self)

	@property
	def FeaturesSupported(self):
		"""An instance of the FeaturesSupported class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.featuressupported.FeaturesSupported)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.featuressupported import FeaturesSupported
		return FeaturesSupported(self)._select()

	@property
	def Instruction(self):
		"""An instance of the Instruction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instruction.Instruction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instruction import Instruction
		return Instruction(self)._select()

	@property
	def InstructionMiss(self):
		"""An instance of the InstructionMiss class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructionmiss.InstructionMiss)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructionmiss import InstructionMiss
		return InstructionMiss(self)._select()

	@property
	def Match(self):
		"""An instance of the Match class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.match.Match)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.match import Match
		return Match(self)._select()

	@property
	def TableModificationTriggerAttributes(self):
		"""An instance of the TableModificationTriggerAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.tablemodificationtriggerattributes.TableModificationTriggerAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.tablemodificationtriggerattributes import TableModificationTriggerAttributes
		return TableModificationTriggerAttributes(self)._select()

	@property
	def Wildcards(self):
		"""An instance of the Wildcards class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.wildcards.Wildcards)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.wildcards import Wildcards
		return Wildcards(self)._select()

	@property
	def WriteActions(self):
		"""An instance of the WriteActions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactions.WriteActions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactions import WriteActions
		return WriteActions(self)._select()

	@property
	def WriteActionsMiss(self):
		"""An instance of the WriteActionsMiss class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactionsmiss.WriteActionsMiss)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactionsmiss import WriteActionsMiss
		return WriteActionsMiss(self)._select()

	@property
	def WriteSetField(self):
		"""An instance of the WriteSetField class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfield.WriteSetField)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfield import WriteSetField
		return WriteSetField(self)._select()

	@property
	def WriteSetFieldMiss(self):
		"""An instance of the WriteSetFieldMiss class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfieldmiss.WriteSetFieldMiss)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfieldmiss import WriteSetFieldMiss
		return WriteSetFieldMiss(self)._select()

	@property
	def ApplyActionExperimenterData(self):
		"""The data of the Apply Action Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('applyActionExperimenterData')
	@ApplyActionExperimenterData.setter
	def ApplyActionExperimenterData(self, value):
		self._set_attribute('applyActionExperimenterData', value)

	@property
	def ApplyActionExperimenterDataLength(self):
		"""The data length of the Apply Action Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('applyActionExperimenterDataLength')
	@ApplyActionExperimenterDataLength.setter
	def ApplyActionExperimenterDataLength(self, value):
		self._set_attribute('applyActionExperimenterDataLength', value)

	@property
	def ApplyActionExperimenterId(self):
		"""The unique identifier for Apply Action Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('applyActionExperimenterId')
	@ApplyActionExperimenterId.setter
	def ApplyActionExperimenterId(self, value):
		self._set_attribute('applyActionExperimenterId', value)

	@property
	def ApplyActionMissExperimenterData(self):
		"""Experimenter Data The data of the apply action for table-miss of Controller Table Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('applyActionMissExperimenterData')
	@ApplyActionMissExperimenterData.setter
	def ApplyActionMissExperimenterData(self, value):
		self._set_attribute('applyActionMissExperimenterData', value)

	@property
	def ApplyActionMissExperimenterDataLength(self):
		"""The data length of the Apply Action Miss Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('applyActionMissExperimenterDataLength')
	@ApplyActionMissExperimenterDataLength.setter
	def ApplyActionMissExperimenterDataLength(self, value):
		self._set_attribute('applyActionMissExperimenterDataLength', value)

	@property
	def ApplyActionMissExperimenterId(self):
		"""The unique identifier for Apply Action Miss Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('applyActionMissExperimenterId')
	@ApplyActionMissExperimenterId.setter
	def ApplyActionMissExperimenterId(self, value):
		self._set_attribute('applyActionMissExperimenterId', value)

	@property
	def Config(self):
		"""Specify the bitmap of OFPTC_* values. The default value is 0.

		Returns:
			number
		"""
		return self._get_attribute('config')
	@Config.setter
	def Config(self, value):
		self._set_attribute('config', value)

	@property
	def Enabled(self):
		"""If selected, this table is used in this controller configuration.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExperimenterData(self):
		"""The data of the Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDataLength(self):
		"""The data length of the Experimenter for table-miss.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')
	@ExperimenterDataLength.setter
	def ExperimenterDataLength(self, value):
		self._set_attribute('experimenterDataLength', value)

	@property
	def ExperimenterId(self):
		"""The unique identifier for the Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('experimenterId')
	@ExperimenterId.setter
	def ExperimenterId(self, value):
		self._set_attribute('experimenterId', value)

	@property
	def ExperimenterMissData(self):
		"""The data of the Experimenter for table-miss.

		Returns:
			str
		"""
		return self._get_attribute('experimenterMissData')
	@ExperimenterMissData.setter
	def ExperimenterMissData(self, value):
		self._set_attribute('experimenterMissData', value)

	@property
	def ExperimenterMissDataLength(self):
		"""The data length of the Experimenter for table-miss.

		Returns:
			number
		"""
		return self._get_attribute('experimenterMissDataLength')
	@ExperimenterMissDataLength.setter
	def ExperimenterMissDataLength(self, value):
		self._set_attribute('experimenterMissDataLength', value)

	@property
	def ExperimenterMissId(self):
		"""The unique identifier for the Experimenter for table-miss.

		Returns:
			number
		"""
		return self._get_attribute('experimenterMissId')
	@ExperimenterMissId.setter
	def ExperimenterMissId(self, value):
		self._set_attribute('experimenterMissId', value)

	@property
	def ExperimenterMissType(self):
		"""The type of experimenter for table-miss.

		Returns:
			number
		"""
		return self._get_attribute('experimenterMissType')
	@ExperimenterMissType.setter
	def ExperimenterMissType(self, value):
		self._set_attribute('experimenterMissType', value)

	@property
	def ExperimenterType(self):
		"""The type of experimenter.

		Returns:
			number
		"""
		return self._get_attribute('experimenterType')
	@ExperimenterType.setter
	def ExperimenterType(self, value):
		self._set_attribute('experimenterType', value)

	@property
	def InstructionExperimenterData(self):
		"""The data of the Instruction Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('instructionExperimenterData')
	@InstructionExperimenterData.setter
	def InstructionExperimenterData(self, value):
		self._set_attribute('instructionExperimenterData', value)

	@property
	def InstructionExperimenterDataLength(self):
		"""The data length of the experimental instruction of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('instructionExperimenterDataLength')
	@InstructionExperimenterDataLength.setter
	def InstructionExperimenterDataLength(self, value):
		self._set_attribute('instructionExperimenterDataLength', value)

	@property
	def InstructionExperimenterId(self):
		"""The unique identifier for the Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('instructionExperimenterId')
	@InstructionExperimenterId.setter
	def InstructionExperimenterId(self, value):
		self._set_attribute('instructionExperimenterId', value)

	@property
	def InstructionMissExperimenterData(self):
		"""The data of the Instruction Miss Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('instructionMissExperimenterData')
	@InstructionMissExperimenterData.setter
	def InstructionMissExperimenterData(self, value):
		self._set_attribute('instructionMissExperimenterData', value)

	@property
	def InstructionMissExperimenterDataLength(self):
		"""It indicates the data length of the Instruction Miss Experimenter

		Returns:
			number
		"""
		return self._get_attribute('instructionMissExperimenterDataLength')
	@InstructionMissExperimenterDataLength.setter
	def InstructionMissExperimenterDataLength(self, value):
		self._set_attribute('instructionMissExperimenterDataLength', value)

	@property
	def InstructionMissExperimenterId(self):
		"""The unique identifier of Instruction Miss Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('instructionMissExperimenterId')
	@InstructionMissExperimenterId.setter
	def InstructionMissExperimenterId(self, value):
		self._set_attribute('instructionMissExperimenterId', value)

	@property
	def MatchExperimenterData(self):
		"""The match data of the Controller Table Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('matchExperimenterData')
	@MatchExperimenterData.setter
	def MatchExperimenterData(self, value):
		self._set_attribute('matchExperimenterData', value)

	@property
	def MatchExperimenterDataLength(self):
		"""The data length of the wildcard experimenter of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('matchExperimenterDataLength')
	@MatchExperimenterDataLength.setter
	def MatchExperimenterDataLength(self, value):
		self._set_attribute('matchExperimenterDataLength', value)

	@property
	def MatchExperimenterField(self):
		"""The identifier for match experimenter of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('matchExperimenterField')
	@MatchExperimenterField.setter
	def MatchExperimenterField(self, value):
		self._set_attribute('matchExperimenterField', value)

	@property
	def MatchExperimenterHasMask(self):
		"""Mask If selected, the match experimenter hash mask field of Controller Table Experimenter is available.

		Returns:
			bool
		"""
		return self._get_attribute('matchExperimenterHasMask')
	@MatchExperimenterHasMask.setter
	def MatchExperimenterHasMask(self, value):
		self._set_attribute('matchExperimenterHasMask', value)

	@property
	def MatchExperimenterId(self):
		"""The unique identifier for wildcard experimenter of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('matchExperimenterId')
	@MatchExperimenterId.setter
	def MatchExperimenterId(self, value):
		self._set_attribute('matchExperimenterId', value)

	@property
	def MaxEntries(self):
		"""Specify the maximum number of entries supported. The default value is 0.

		Returns:
			number
		"""
		return self._get_attribute('maxEntries')
	@MaxEntries.setter
	def MaxEntries(self, value):
		self._set_attribute('maxEntries', value)

	@property
	def MetadataMatch(self):
		"""Specify the bits of metadata table that can match. The default value is 0.

		Returns:
			str
		"""
		return self._get_attribute('metadataMatch')
	@MetadataMatch.setter
	def MetadataMatch(self, value):
		self._set_attribute('metadataMatch', value)

	@property
	def MetadataWrite(self):
		"""Specify the bits of metadata table that can write. The default value is 0.

		Returns:
			str
		"""
		return self._get_attribute('metadataWrite')
	@MetadataWrite.setter
	def MetadataWrite(self, value):
		self._set_attribute('metadataWrite', value)

	@property
	def NextTable(self):
		"""Next table property.

		Returns:
			str
		"""
		return self._get_attribute('nextTable')
	@NextTable.setter
	def NextTable(self, value):
		self._set_attribute('nextTable', value)

	@property
	def NextTableMiss(self):
		"""Next table for table-miss.

		Returns:
			str
		"""
		return self._get_attribute('nextTableMiss')
	@NextTableMiss.setter
	def NextTableMiss(self, value):
		self._set_attribute('nextTableMiss', value)

	@property
	def TableId(self):
		"""Specify the controller table identifier. Lower numbered tables are consulted first.

		Returns:
			number
		"""
		return self._get_attribute('tableId')
	@TableId.setter
	def TableId(self, value):
		self._set_attribute('tableId', value)

	@property
	def TableName(self):
		"""Specify the name of the controller table.

		Returns:
			str
		"""
		return self._get_attribute('tableName')
	@TableName.setter
	def TableName(self, value):
		self._set_attribute('tableName', value)

	@property
	def WildcardExperimenterData(self):
		"""The data of the wildcard experimenter of Controller Table Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('wildcardExperimenterData')
	@WildcardExperimenterData.setter
	def WildcardExperimenterData(self, value):
		self._set_attribute('wildcardExperimenterData', value)

	@property
	def WildcardExperimenterDataLength(self):
		"""The data length of the wildcard experimenter of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('wildcardExperimenterDataLength')
	@WildcardExperimenterDataLength.setter
	def WildcardExperimenterDataLength(self, value):
		self._set_attribute('wildcardExperimenterDataLength', value)

	@property
	def WildcardExperimenterField(self):
		"""The identifier for wildcard experimenter of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('wildcardExperimenterField')
	@WildcardExperimenterField.setter
	def WildcardExperimenterField(self, value):
		self._set_attribute('wildcardExperimenterField', value)

	@property
	def WildcardExperimenterHasMask(self):
		"""Mask If selected, the wildcard experimenter hash mask field of Controller Table Experimenter is available.

		Returns:
			bool
		"""
		return self._get_attribute('wildcardExperimenterHasMask')
	@WildcardExperimenterHasMask.setter
	def WildcardExperimenterHasMask(self, value):
		self._set_attribute('wildcardExperimenterHasMask', value)

	@property
	def WildcardExperimenterId(self):
		"""The unique identifier for wildcard experimenter of Controller Table Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('wildcardExperimenterId')
	@WildcardExperimenterId.setter
	def WildcardExperimenterId(self, value):
		self._set_attribute('wildcardExperimenterId', value)

	@property
	def WriteActionExperimenterData(self):
		"""The data of the Write Action Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('writeActionExperimenterData')
	@WriteActionExperimenterData.setter
	def WriteActionExperimenterData(self, value):
		self._set_attribute('writeActionExperimenterData', value)

	@property
	def WriteActionExperimenterDataLength(self):
		"""The data length of the Write Action Miss Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('writeActionExperimenterDataLength')
	@WriteActionExperimenterDataLength.setter
	def WriteActionExperimenterDataLength(self, value):
		self._set_attribute('writeActionExperimenterDataLength', value)

	@property
	def WriteActionExperimenterId(self):
		"""The unique identifier for Write Action Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('writeActionExperimenterId')
	@WriteActionExperimenterId.setter
	def WriteActionExperimenterId(self, value):
		self._set_attribute('writeActionExperimenterId', value)

	@property
	def WriteActionMissExperimenterData(self):
		"""The data of the Write Action Miss Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('writeActionMissExperimenterData')
	@WriteActionMissExperimenterData.setter
	def WriteActionMissExperimenterData(self, value):
		self._set_attribute('writeActionMissExperimenterData', value)

	@property
	def WriteActionMissExperimenterDataLength(self):
		"""The data length of the Write Action Miss Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('writeActionMissExperimenterDataLength')
	@WriteActionMissExperimenterDataLength.setter
	def WriteActionMissExperimenterDataLength(self, value):
		self._set_attribute('writeActionMissExperimenterDataLength', value)

	@property
	def WriteActionMissExperimenterId(self):
		"""The unique identifier of Write Action Miss Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('writeActionMissExperimenterId')
	@WriteActionMissExperimenterId.setter
	def WriteActionMissExperimenterId(self, value):
		self._set_attribute('writeActionMissExperimenterId', value)

	def add(self, ApplyActionExperimenterData=None, ApplyActionExperimenterDataLength=None, ApplyActionExperimenterId=None, ApplyActionMissExperimenterData=None, ApplyActionMissExperimenterDataLength=None, ApplyActionMissExperimenterId=None, Config=None, Enabled=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterId=None, ExperimenterMissData=None, ExperimenterMissDataLength=None, ExperimenterMissId=None, ExperimenterMissType=None, ExperimenterType=None, InstructionExperimenterData=None, InstructionExperimenterDataLength=None, InstructionExperimenterId=None, InstructionMissExperimenterData=None, InstructionMissExperimenterDataLength=None, InstructionMissExperimenterId=None, MatchExperimenterData=None, MatchExperimenterDataLength=None, MatchExperimenterField=None, MatchExperimenterHasMask=None, MatchExperimenterId=None, MaxEntries=None, MetadataMatch=None, MetadataWrite=None, NextTable=None, NextTableMiss=None, TableId=None, TableName=None, WildcardExperimenterData=None, WildcardExperimenterDataLength=None, WildcardExperimenterField=None, WildcardExperimenterHasMask=None, WildcardExperimenterId=None, WriteActionExperimenterData=None, WriteActionExperimenterDataLength=None, WriteActionExperimenterId=None, WriteActionMissExperimenterData=None, WriteActionMissExperimenterDataLength=None, WriteActionMissExperimenterId=None):
		"""Adds a new controllerTables node on the server and retrieves it in this instance.

		Args:
			ApplyActionExperimenterData (str): The data of the Apply Action Experimenter.
			ApplyActionExperimenterDataLength (number): The data length of the Apply Action Experimenter.
			ApplyActionExperimenterId (number): The unique identifier for Apply Action Experimenter.
			ApplyActionMissExperimenterData (str): Experimenter Data The data of the apply action for table-miss of Controller Table Experimenter.
			ApplyActionMissExperimenterDataLength (number): The data length of the Apply Action Miss Experimenter.
			ApplyActionMissExperimenterId (number): The unique identifier for Apply Action Miss Experimenter.
			Config (number): Specify the bitmap of OFPTC_* values. The default value is 0.
			Enabled (bool): If selected, this table is used in this controller configuration.
			ExperimenterData (str): The data of the Experimenter.
			ExperimenterDataLength (number): The data length of the Experimenter for table-miss.
			ExperimenterId (number): The unique identifier for the Experimenter.
			ExperimenterMissData (str): The data of the Experimenter for table-miss.
			ExperimenterMissDataLength (number): The data length of the Experimenter for table-miss.
			ExperimenterMissId (number): The unique identifier for the Experimenter for table-miss.
			ExperimenterMissType (number): The type of experimenter for table-miss.
			ExperimenterType (number): The type of experimenter.
			InstructionExperimenterData (str): The data of the Instruction Experimenter.
			InstructionExperimenterDataLength (number): The data length of the experimental instruction of Controller Table Experimenter.
			InstructionExperimenterId (number): The unique identifier for the Experimenter.
			InstructionMissExperimenterData (str): The data of the Instruction Miss Experimenter.
			InstructionMissExperimenterDataLength (number): It indicates the data length of the Instruction Miss Experimenter
			InstructionMissExperimenterId (number): The unique identifier of Instruction Miss Experimenter.
			MatchExperimenterData (str): The match data of the Controller Table Experimenter.
			MatchExperimenterDataLength (number): The data length of the wildcard experimenter of Controller Table Experimenter.
			MatchExperimenterField (number): The identifier for match experimenter of Controller Table Experimenter.
			MatchExperimenterHasMask (bool): Mask If selected, the match experimenter hash mask field of Controller Table Experimenter is available.
			MatchExperimenterId (number): The unique identifier for wildcard experimenter of Controller Table Experimenter.
			MaxEntries (number): Specify the maximum number of entries supported. The default value is 0.
			MetadataMatch (str): Specify the bits of metadata table that can match. The default value is 0.
			MetadataWrite (str): Specify the bits of metadata table that can write. The default value is 0.
			NextTable (str): Next table property.
			NextTableMiss (str): Next table for table-miss.
			TableId (number): Specify the controller table identifier. Lower numbered tables are consulted first.
			TableName (str): Specify the name of the controller table.
			WildcardExperimenterData (str): The data of the wildcard experimenter of Controller Table Experimenter.
			WildcardExperimenterDataLength (number): The data length of the wildcard experimenter of Controller Table Experimenter.
			WildcardExperimenterField (number): The identifier for wildcard experimenter of Controller Table Experimenter.
			WildcardExperimenterHasMask (bool): Mask If selected, the wildcard experimenter hash mask field of Controller Table Experimenter is available.
			WildcardExperimenterId (number): The unique identifier for wildcard experimenter of Controller Table Experimenter.
			WriteActionExperimenterData (str): The data of the Write Action Experimenter.
			WriteActionExperimenterDataLength (number): The data length of the Write Action Miss Experimenter.
			WriteActionExperimenterId (number): The unique identifier for Write Action Experimenter.
			WriteActionMissExperimenterData (str): The data of the Write Action Miss Experimenter.
			WriteActionMissExperimenterDataLength (number): The data length of the Write Action Miss Experimenter.
			WriteActionMissExperimenterId (number): The unique identifier of Write Action Miss Experimenter.

		Returns:
			self: This instance with all currently retrieved controllerTables data using find and the newly added controllerTables data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the controllerTables data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ApplyActionExperimenterData=None, ApplyActionExperimenterDataLength=None, ApplyActionExperimenterId=None, ApplyActionMissExperimenterData=None, ApplyActionMissExperimenterDataLength=None, ApplyActionMissExperimenterId=None, Config=None, Enabled=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterId=None, ExperimenterMissData=None, ExperimenterMissDataLength=None, ExperimenterMissId=None, ExperimenterMissType=None, ExperimenterType=None, InstructionExperimenterData=None, InstructionExperimenterDataLength=None, InstructionExperimenterId=None, InstructionMissExperimenterData=None, InstructionMissExperimenterDataLength=None, InstructionMissExperimenterId=None, MatchExperimenterData=None, MatchExperimenterDataLength=None, MatchExperimenterField=None, MatchExperimenterHasMask=None, MatchExperimenterId=None, MaxEntries=None, MetadataMatch=None, MetadataWrite=None, NextTable=None, NextTableMiss=None, TableId=None, TableName=None, WildcardExperimenterData=None, WildcardExperimenterDataLength=None, WildcardExperimenterField=None, WildcardExperimenterHasMask=None, WildcardExperimenterId=None, WriteActionExperimenterData=None, WriteActionExperimenterDataLength=None, WriteActionExperimenterId=None, WriteActionMissExperimenterData=None, WriteActionMissExperimenterDataLength=None, WriteActionMissExperimenterId=None):
		"""Finds and retrieves controllerTables data from the server.

		All named parameters support regex and can be used to selectively retrieve controllerTables data from the server.
		By default the find method takes no parameters and will retrieve all controllerTables data from the server.

		Args:
			ApplyActionExperimenterData (str): The data of the Apply Action Experimenter.
			ApplyActionExperimenterDataLength (number): The data length of the Apply Action Experimenter.
			ApplyActionExperimenterId (number): The unique identifier for Apply Action Experimenter.
			ApplyActionMissExperimenterData (str): Experimenter Data The data of the apply action for table-miss of Controller Table Experimenter.
			ApplyActionMissExperimenterDataLength (number): The data length of the Apply Action Miss Experimenter.
			ApplyActionMissExperimenterId (number): The unique identifier for Apply Action Miss Experimenter.
			Config (number): Specify the bitmap of OFPTC_* values. The default value is 0.
			Enabled (bool): If selected, this table is used in this controller configuration.
			ExperimenterData (str): The data of the Experimenter.
			ExperimenterDataLength (number): The data length of the Experimenter for table-miss.
			ExperimenterId (number): The unique identifier for the Experimenter.
			ExperimenterMissData (str): The data of the Experimenter for table-miss.
			ExperimenterMissDataLength (number): The data length of the Experimenter for table-miss.
			ExperimenterMissId (number): The unique identifier for the Experimenter for table-miss.
			ExperimenterMissType (number): The type of experimenter for table-miss.
			ExperimenterType (number): The type of experimenter.
			InstructionExperimenterData (str): The data of the Instruction Experimenter.
			InstructionExperimenterDataLength (number): The data length of the experimental instruction of Controller Table Experimenter.
			InstructionExperimenterId (number): The unique identifier for the Experimenter.
			InstructionMissExperimenterData (str): The data of the Instruction Miss Experimenter.
			InstructionMissExperimenterDataLength (number): It indicates the data length of the Instruction Miss Experimenter
			InstructionMissExperimenterId (number): The unique identifier of Instruction Miss Experimenter.
			MatchExperimenterData (str): The match data of the Controller Table Experimenter.
			MatchExperimenterDataLength (number): The data length of the wildcard experimenter of Controller Table Experimenter.
			MatchExperimenterField (number): The identifier for match experimenter of Controller Table Experimenter.
			MatchExperimenterHasMask (bool): Mask If selected, the match experimenter hash mask field of Controller Table Experimenter is available.
			MatchExperimenterId (number): The unique identifier for wildcard experimenter of Controller Table Experimenter.
			MaxEntries (number): Specify the maximum number of entries supported. The default value is 0.
			MetadataMatch (str): Specify the bits of metadata table that can match. The default value is 0.
			MetadataWrite (str): Specify the bits of metadata table that can write. The default value is 0.
			NextTable (str): Next table property.
			NextTableMiss (str): Next table for table-miss.
			TableId (number): Specify the controller table identifier. Lower numbered tables are consulted first.
			TableName (str): Specify the name of the controller table.
			WildcardExperimenterData (str): The data of the wildcard experimenter of Controller Table Experimenter.
			WildcardExperimenterDataLength (number): The data length of the wildcard experimenter of Controller Table Experimenter.
			WildcardExperimenterField (number): The identifier for wildcard experimenter of Controller Table Experimenter.
			WildcardExperimenterHasMask (bool): Mask If selected, the wildcard experimenter hash mask field of Controller Table Experimenter is available.
			WildcardExperimenterId (number): The unique identifier for wildcard experimenter of Controller Table Experimenter.
			WriteActionExperimenterData (str): The data of the Write Action Experimenter.
			WriteActionExperimenterDataLength (number): The data length of the Write Action Miss Experimenter.
			WriteActionExperimenterId (number): The unique identifier for Write Action Experimenter.
			WriteActionMissExperimenterData (str): The data of the Write Action Miss Experimenter.
			WriteActionMissExperimenterDataLength (number): The data length of the Write Action Miss Experimenter.
			WriteActionMissExperimenterId (number): The unique identifier of Write Action Miss Experimenter.

		Returns:
			self: This instance with matching controllerTables data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of controllerTables data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the controllerTables data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def TableModificationTrigger(self):
		"""Executes the tableModificationTrigger operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=controllerTables)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('TableModificationTrigger', payload=locals(), response_object=None)
