
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			str
		"""
		return self._get_attribute('applyActionExperimenterData')
	@ApplyActionExperimenterData.setter
	def ApplyActionExperimenterData(self, value):
		self._set_attribute('applyActionExperimenterData', value)

	@property
	def ApplyActionExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('applyActionExperimenterDataLength')
	@ApplyActionExperimenterDataLength.setter
	def ApplyActionExperimenterDataLength(self, value):
		self._set_attribute('applyActionExperimenterDataLength', value)

	@property
	def ApplyActionExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('applyActionExperimenterId')
	@ApplyActionExperimenterId.setter
	def ApplyActionExperimenterId(self, value):
		self._set_attribute('applyActionExperimenterId', value)

	@property
	def ApplyActionMissExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('applyActionMissExperimenterData')
	@ApplyActionMissExperimenterData.setter
	def ApplyActionMissExperimenterData(self, value):
		self._set_attribute('applyActionMissExperimenterData', value)

	@property
	def ApplyActionMissExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('applyActionMissExperimenterDataLength')
	@ApplyActionMissExperimenterDataLength.setter
	def ApplyActionMissExperimenterDataLength(self, value):
		self._set_attribute('applyActionMissExperimenterDataLength', value)

	@property
	def ApplyActionMissExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('applyActionMissExperimenterId')
	@ApplyActionMissExperimenterId.setter
	def ApplyActionMissExperimenterId(self, value):
		self._set_attribute('applyActionMissExperimenterId', value)

	@property
	def Config(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('config')
	@Config.setter
	def Config(self, value):
		self._set_attribute('config', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')
	@ExperimenterDataLength.setter
	def ExperimenterDataLength(self, value):
		self._set_attribute('experimenterDataLength', value)

	@property
	def ExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterId')
	@ExperimenterId.setter
	def ExperimenterId(self, value):
		self._set_attribute('experimenterId', value)

	@property
	def ExperimenterMissData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterMissData')
	@ExperimenterMissData.setter
	def ExperimenterMissData(self, value):
		self._set_attribute('experimenterMissData', value)

	@property
	def ExperimenterMissDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterMissDataLength')
	@ExperimenterMissDataLength.setter
	def ExperimenterMissDataLength(self, value):
		self._set_attribute('experimenterMissDataLength', value)

	@property
	def ExperimenterMissId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterMissId')
	@ExperimenterMissId.setter
	def ExperimenterMissId(self, value):
		self._set_attribute('experimenterMissId', value)

	@property
	def ExperimenterMissType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterMissType')
	@ExperimenterMissType.setter
	def ExperimenterMissType(self, value):
		self._set_attribute('experimenterMissType', value)

	@property
	def ExperimenterType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterType')
	@ExperimenterType.setter
	def ExperimenterType(self, value):
		self._set_attribute('experimenterType', value)

	@property
	def InstructionExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('instructionExperimenterData')
	@InstructionExperimenterData.setter
	def InstructionExperimenterData(self, value):
		self._set_attribute('instructionExperimenterData', value)

	@property
	def InstructionExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instructionExperimenterDataLength')
	@InstructionExperimenterDataLength.setter
	def InstructionExperimenterDataLength(self, value):
		self._set_attribute('instructionExperimenterDataLength', value)

	@property
	def InstructionExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instructionExperimenterId')
	@InstructionExperimenterId.setter
	def InstructionExperimenterId(self, value):
		self._set_attribute('instructionExperimenterId', value)

	@property
	def InstructionMissExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('instructionMissExperimenterData')
	@InstructionMissExperimenterData.setter
	def InstructionMissExperimenterData(self, value):
		self._set_attribute('instructionMissExperimenterData', value)

	@property
	def InstructionMissExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instructionMissExperimenterDataLength')
	@InstructionMissExperimenterDataLength.setter
	def InstructionMissExperimenterDataLength(self, value):
		self._set_attribute('instructionMissExperimenterDataLength', value)

	@property
	def InstructionMissExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instructionMissExperimenterId')
	@InstructionMissExperimenterId.setter
	def InstructionMissExperimenterId(self, value):
		self._set_attribute('instructionMissExperimenterId', value)

	@property
	def MatchExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('matchExperimenterData')
	@MatchExperimenterData.setter
	def MatchExperimenterData(self, value):
		self._set_attribute('matchExperimenterData', value)

	@property
	def MatchExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('matchExperimenterDataLength')
	@MatchExperimenterDataLength.setter
	def MatchExperimenterDataLength(self, value):
		self._set_attribute('matchExperimenterDataLength', value)

	@property
	def MatchExperimenterField(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('matchExperimenterField')
	@MatchExperimenterField.setter
	def MatchExperimenterField(self, value):
		self._set_attribute('matchExperimenterField', value)

	@property
	def MatchExperimenterHasMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('matchExperimenterHasMask')
	@MatchExperimenterHasMask.setter
	def MatchExperimenterHasMask(self, value):
		self._set_attribute('matchExperimenterHasMask', value)

	@property
	def MatchExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('matchExperimenterId')
	@MatchExperimenterId.setter
	def MatchExperimenterId(self, value):
		self._set_attribute('matchExperimenterId', value)

	@property
	def MaxEntries(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxEntries')
	@MaxEntries.setter
	def MaxEntries(self, value):
		self._set_attribute('maxEntries', value)

	@property
	def MetadataMatch(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataMatch')
	@MetadataMatch.setter
	def MetadataMatch(self, value):
		self._set_attribute('metadataMatch', value)

	@property
	def MetadataWrite(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataWrite')
	@MetadataWrite.setter
	def MetadataWrite(self, value):
		self._set_attribute('metadataWrite', value)

	@property
	def NextTable(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextTable')
	@NextTable.setter
	def NextTable(self, value):
		self._set_attribute('nextTable', value)

	@property
	def NextTableMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextTableMiss')
	@NextTableMiss.setter
	def NextTableMiss(self, value):
		self._set_attribute('nextTableMiss', value)

	@property
	def TableId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tableId')
	@TableId.setter
	def TableId(self, value):
		self._set_attribute('tableId', value)

	@property
	def TableName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tableName')
	@TableName.setter
	def TableName(self, value):
		self._set_attribute('tableName', value)

	@property
	def WildcardExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('wildcardExperimenterData')
	@WildcardExperimenterData.setter
	def WildcardExperimenterData(self, value):
		self._set_attribute('wildcardExperimenterData', value)

	@property
	def WildcardExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('wildcardExperimenterDataLength')
	@WildcardExperimenterDataLength.setter
	def WildcardExperimenterDataLength(self, value):
		self._set_attribute('wildcardExperimenterDataLength', value)

	@property
	def WildcardExperimenterField(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('wildcardExperimenterField')
	@WildcardExperimenterField.setter
	def WildcardExperimenterField(self, value):
		self._set_attribute('wildcardExperimenterField', value)

	@property
	def WildcardExperimenterHasMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('wildcardExperimenterHasMask')
	@WildcardExperimenterHasMask.setter
	def WildcardExperimenterHasMask(self, value):
		self._set_attribute('wildcardExperimenterHasMask', value)

	@property
	def WildcardExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('wildcardExperimenterId')
	@WildcardExperimenterId.setter
	def WildcardExperimenterId(self, value):
		self._set_attribute('wildcardExperimenterId', value)

	@property
	def WriteActionExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('writeActionExperimenterData')
	@WriteActionExperimenterData.setter
	def WriteActionExperimenterData(self, value):
		self._set_attribute('writeActionExperimenterData', value)

	@property
	def WriteActionExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('writeActionExperimenterDataLength')
	@WriteActionExperimenterDataLength.setter
	def WriteActionExperimenterDataLength(self, value):
		self._set_attribute('writeActionExperimenterDataLength', value)

	@property
	def WriteActionExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('writeActionExperimenterId')
	@WriteActionExperimenterId.setter
	def WriteActionExperimenterId(self, value):
		self._set_attribute('writeActionExperimenterId', value)

	@property
	def WriteActionMissExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('writeActionMissExperimenterData')
	@WriteActionMissExperimenterData.setter
	def WriteActionMissExperimenterData(self, value):
		self._set_attribute('writeActionMissExperimenterData', value)

	@property
	def WriteActionMissExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('writeActionMissExperimenterDataLength')
	@WriteActionMissExperimenterDataLength.setter
	def WriteActionMissExperimenterDataLength(self, value):
		self._set_attribute('writeActionMissExperimenterDataLength', value)

	@property
	def WriteActionMissExperimenterId(self):
		"""

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
			ApplyActionExperimenterData (str): 
			ApplyActionExperimenterDataLength (number): 
			ApplyActionExperimenterId (number): 
			ApplyActionMissExperimenterData (str): 
			ApplyActionMissExperimenterDataLength (number): 
			ApplyActionMissExperimenterId (number): 
			Config (number): 
			Enabled (bool): 
			ExperimenterData (str): 
			ExperimenterDataLength (number): 
			ExperimenterId (number): 
			ExperimenterMissData (str): 
			ExperimenterMissDataLength (number): 
			ExperimenterMissId (number): 
			ExperimenterMissType (number): 
			ExperimenterType (number): 
			InstructionExperimenterData (str): 
			InstructionExperimenterDataLength (number): 
			InstructionExperimenterId (number): 
			InstructionMissExperimenterData (str): 
			InstructionMissExperimenterDataLength (number): 
			InstructionMissExperimenterId (number): 
			MatchExperimenterData (str): 
			MatchExperimenterDataLength (number): 
			MatchExperimenterField (number): 
			MatchExperimenterHasMask (bool): 
			MatchExperimenterId (number): 
			MaxEntries (number): 
			MetadataMatch (str): 
			MetadataWrite (str): 
			NextTable (str): 
			NextTableMiss (str): 
			TableId (number): 
			TableName (str): 
			WildcardExperimenterData (str): 
			WildcardExperimenterDataLength (number): 
			WildcardExperimenterField (number): 
			WildcardExperimenterHasMask (bool): 
			WildcardExperimenterId (number): 
			WriteActionExperimenterData (str): 
			WriteActionExperimenterDataLength (number): 
			WriteActionExperimenterId (number): 
			WriteActionMissExperimenterData (str): 
			WriteActionMissExperimenterDataLength (number): 
			WriteActionMissExperimenterId (number): 

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
			ApplyActionExperimenterData (str): 
			ApplyActionExperimenterDataLength (number): 
			ApplyActionExperimenterId (number): 
			ApplyActionMissExperimenterData (str): 
			ApplyActionMissExperimenterDataLength (number): 
			ApplyActionMissExperimenterId (number): 
			Config (number): 
			Enabled (bool): 
			ExperimenterData (str): 
			ExperimenterDataLength (number): 
			ExperimenterId (number): 
			ExperimenterMissData (str): 
			ExperimenterMissDataLength (number): 
			ExperimenterMissId (number): 
			ExperimenterMissType (number): 
			ExperimenterType (number): 
			InstructionExperimenterData (str): 
			InstructionExperimenterDataLength (number): 
			InstructionExperimenterId (number): 
			InstructionMissExperimenterData (str): 
			InstructionMissExperimenterDataLength (number): 
			InstructionMissExperimenterId (number): 
			MatchExperimenterData (str): 
			MatchExperimenterDataLength (number): 
			MatchExperimenterField (number): 
			MatchExperimenterHasMask (bool): 
			MatchExperimenterId (number): 
			MaxEntries (number): 
			MetadataMatch (str): 
			MetadataWrite (str): 
			NextTable (str): 
			NextTableMiss (str): 
			TableId (number): 
			TableName (str): 
			WildcardExperimenterData (str): 
			WildcardExperimenterDataLength (number): 
			WildcardExperimenterField (number): 
			WildcardExperimenterHasMask (bool): 
			WildcardExperimenterId (number): 
			WriteActionExperimenterData (str): 
			WriteActionExperimenterDataLength (number): 
			WriteActionExperimenterId (number): 
			WriteActionMissExperimenterData (str): 
			WriteActionMissExperimenterDataLength (number): 
			WriteActionMissExperimenterId (number): 

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

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=controllerTables)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('TableModificationTrigger', payload=locals(), response_object=None)
