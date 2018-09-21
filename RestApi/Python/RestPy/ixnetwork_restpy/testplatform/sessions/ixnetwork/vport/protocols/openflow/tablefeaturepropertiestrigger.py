from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TableFeaturePropertiesTrigger(Base):
	"""The TableFeaturePropertiesTrigger class encapsulates a system managed tableFeaturePropertiesTrigger node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TableFeaturePropertiesTrigger property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tableFeaturePropertiesTrigger'

	def __init__(self, parent):
		super(TableFeaturePropertiesTrigger, self).__init__(parent)

	@property
	def ApplyAction(self):
		"""An instance of the ApplyAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyaction.ApplyAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyaction import ApplyAction
		return ApplyAction(self)._select()

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
	def Experimenter(self):
		"""An instance of the Experimenter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.experimenter.Experimenter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.experimenter import Experimenter
		return Experimenter(self)._select()

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
	def NextTable(self):
		"""An instance of the NextTable class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.nexttable.NextTable)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.nexttable import NextTable
		return NextTable(self)._select()

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
	def WriteAction(self):
		"""An instance of the WriteAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeaction.WriteAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeaction import WriteAction
		return WriteAction(self)._select()

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
	def EnableApplyAction(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableApplyAction')
	@EnableApplyAction.setter
	def EnableApplyAction(self, value):
		self._set_attribute('enableApplyAction', value)

	@property
	def EnableApplyActionMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableApplyActionMiss')
	@EnableApplyActionMiss.setter
	def EnableApplyActionMiss(self, value):
		self._set_attribute('enableApplyActionMiss', value)

	@property
	def EnableApplySetField(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableApplySetField')
	@EnableApplySetField.setter
	def EnableApplySetField(self, value):
		self._set_attribute('enableApplySetField', value)

	@property
	def EnableApplySetFieldMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableApplySetFieldMiss')
	@EnableApplySetFieldMiss.setter
	def EnableApplySetFieldMiss(self, value):
		self._set_attribute('enableApplySetFieldMiss', value)

	@property
	def EnableExperimenter(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableExperimenter')
	@EnableExperimenter.setter
	def EnableExperimenter(self, value):
		self._set_attribute('enableExperimenter', value)

	@property
	def EnableExperimenterMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableExperimenterMiss')
	@EnableExperimenterMiss.setter
	def EnableExperimenterMiss(self, value):
		self._set_attribute('enableExperimenterMiss', value)

	@property
	def EnableInstruction(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableInstruction')
	@EnableInstruction.setter
	def EnableInstruction(self, value):
		self._set_attribute('enableInstruction', value)

	@property
	def EnableInstructionMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableInstructionMiss')
	@EnableInstructionMiss.setter
	def EnableInstructionMiss(self, value):
		self._set_attribute('enableInstructionMiss', value)

	@property
	def EnableMatch(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableMatch')
	@EnableMatch.setter
	def EnableMatch(self, value):
		self._set_attribute('enableMatch', value)

	@property
	def EnableNextTable(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableNextTable')
	@EnableNextTable.setter
	def EnableNextTable(self, value):
		self._set_attribute('enableNextTable', value)

	@property
	def EnableNextTableMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableNextTableMiss')
	@EnableNextTableMiss.setter
	def EnableNextTableMiss(self, value):
		self._set_attribute('enableNextTableMiss', value)

	@property
	def EnableWildCard(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableWildCard')
	@EnableWildCard.setter
	def EnableWildCard(self, value):
		self._set_attribute('enableWildCard', value)

	@property
	def EnableWriteAction(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableWriteAction')
	@EnableWriteAction.setter
	def EnableWriteAction(self, value):
		self._set_attribute('enableWriteAction', value)

	@property
	def EnableWriteActionMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableWriteActionMiss')
	@EnableWriteActionMiss.setter
	def EnableWriteActionMiss(self, value):
		self._set_attribute('enableWriteActionMiss', value)

	@property
	def EnableWriteSetField(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableWriteSetField')
	@EnableWriteSetField.setter
	def EnableWriteSetField(self, value):
		self._set_attribute('enableWriteSetField', value)

	@property
	def EnableWriteSetFieldMiss(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableWriteSetFieldMiss')
	@EnableWriteSetFieldMiss.setter
	def EnableWriteSetFieldMiss(self, value):
		self._set_attribute('enableWriteSetFieldMiss', value)

	def find(self, EnableApplyAction=None, EnableApplyActionMiss=None, EnableApplySetField=None, EnableApplySetFieldMiss=None, EnableExperimenter=None, EnableExperimenterMiss=None, EnableInstruction=None, EnableInstructionMiss=None, EnableMatch=None, EnableNextTable=None, EnableNextTableMiss=None, EnableWildCard=None, EnableWriteAction=None, EnableWriteActionMiss=None, EnableWriteSetField=None, EnableWriteSetFieldMiss=None):
		"""Finds and retrieves tableFeaturePropertiesTrigger data from the server.

		All named parameters support regex and can be used to selectively retrieve tableFeaturePropertiesTrigger data from the server.
		By default the find method takes no parameters and will retrieve all tableFeaturePropertiesTrigger data from the server.

		Args:
			EnableApplyAction (bool): NOT DEFINED
			EnableApplyActionMiss (bool): NOT DEFINED
			EnableApplySetField (bool): NOT DEFINED
			EnableApplySetFieldMiss (bool): NOT DEFINED
			EnableExperimenter (bool): NOT DEFINED
			EnableExperimenterMiss (bool): NOT DEFINED
			EnableInstruction (bool): NOT DEFINED
			EnableInstructionMiss (bool): NOT DEFINED
			EnableMatch (bool): NOT DEFINED
			EnableNextTable (bool): NOT DEFINED
			EnableNextTableMiss (bool): NOT DEFINED
			EnableWildCard (bool): NOT DEFINED
			EnableWriteAction (bool): NOT DEFINED
			EnableWriteActionMiss (bool): NOT DEFINED
			EnableWriteSetField (bool): NOT DEFINED
			EnableWriteSetFieldMiss (bool): NOT DEFINED

		Returns:
			self: This instance with matching tableFeaturePropertiesTrigger data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tableFeaturePropertiesTrigger data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tableFeaturePropertiesTrigger data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
