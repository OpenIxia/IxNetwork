from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchTableFeaturesStatLearnedInfo(Base):
	"""The SwitchTableFeaturesStatLearnedInfo class encapsulates a system managed switchTableFeaturesStatLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchTableFeaturesStatLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchTableFeaturesStatLearnedInfo'

	def __init__(self, parent):
		super(SwitchTableFeaturesStatLearnedInfo, self).__init__(parent)

	@property
	def ApplyActionsLearnedInfo(self):
		"""An instance of the ApplyActionsLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionslearnedinfo.ApplyActionsLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionslearnedinfo import ApplyActionsLearnedInfo
		return ApplyActionsLearnedInfo(self)

	@property
	def ApplyActionsMissLearnedInfo(self):
		"""An instance of the ApplyActionsMissLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionsmisslearnedinfo.ApplyActionsMissLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionsmisslearnedinfo import ApplyActionsMissLearnedInfo
		return ApplyActionsMissLearnedInfo(self)

	@property
	def ApplySetFieldLearnedInfo(self):
		"""An instance of the ApplySetFieldLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfieldlearnedinfo.ApplySetFieldLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfieldlearnedinfo import ApplySetFieldLearnedInfo
		return ApplySetFieldLearnedInfo(self)

	@property
	def ApplySetFieldMissLearnedInfo(self):
		"""An instance of the ApplySetFieldMissLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfieldmisslearnedinfo.ApplySetFieldMissLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applysetfieldmisslearnedinfo import ApplySetFieldMissLearnedInfo
		return ApplySetFieldMissLearnedInfo(self)

	@property
	def InstructionLearnedInfo(self):
		"""An instance of the InstructionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructionlearnedinfo.InstructionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructionlearnedinfo import InstructionLearnedInfo
		return InstructionLearnedInfo(self)

	@property
	def InstructionMissLearnedInfo(self):
		"""An instance of the InstructionMissLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructionmisslearnedinfo.InstructionMissLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructionmisslearnedinfo import InstructionMissLearnedInfo
		return InstructionMissLearnedInfo(self)

	@property
	def MatchLearnedInfo(self):
		"""An instance of the MatchLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.matchlearnedinfo.MatchLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.matchlearnedinfo import MatchLearnedInfo
		return MatchLearnedInfo(self)

	@property
	def NextTableLearnedInfo(self):
		"""An instance of the NextTableLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.nexttablelearnedinfo.NextTableLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.nexttablelearnedinfo import NextTableLearnedInfo
		return NextTableLearnedInfo(self)

	@property
	def NextTableMissLearnedInfo(self):
		"""An instance of the NextTableMissLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.nexttablemisslearnedinfo.NextTableMissLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.nexttablemisslearnedinfo import NextTableMissLearnedInfo
		return NextTableMissLearnedInfo(self)

	@property
	def WildcardsLearnedInfo(self):
		"""An instance of the WildcardsLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.wildcardslearnedinfo.WildcardsLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.wildcardslearnedinfo import WildcardsLearnedInfo
		return WildcardsLearnedInfo(self)

	@property
	def WriteActionsLearnedInfo(self):
		"""An instance of the WriteActionsLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactionslearnedinfo.WriteActionsLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactionslearnedinfo import WriteActionsLearnedInfo
		return WriteActionsLearnedInfo(self)

	@property
	def WriteActionsMissLearnedInfo(self):
		"""An instance of the WriteActionsMissLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactionsmisslearnedinfo.WriteActionsMissLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writeactionsmisslearnedinfo import WriteActionsMissLearnedInfo
		return WriteActionsMissLearnedInfo(self)

	@property
	def WriteSetFieldLearnedInfo(self):
		"""An instance of the WriteSetFieldLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfieldlearnedinfo.WriteSetFieldLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfieldlearnedinfo import WriteSetFieldLearnedInfo
		return WriteSetFieldLearnedInfo(self)

	@property
	def WriteSetFieldMissLearnedInfo(self):
		"""An instance of the WriteSetFieldMissLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfieldmisslearnedinfo.WriteSetFieldMissLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.writesetfieldmisslearnedinfo import WriteSetFieldMissLearnedInfo
		return WriteSetFieldMissLearnedInfo(self)

	@property
	def ApplyActions(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('applyActions')

	@property
	def ApplyActionsMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('applyActionsMiss')

	@property
	def ApplySetField(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('applySetField')

	@property
	def ApplySetFieldMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('applySetFieldMiss')

	@property
	def Config(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('config')

	@property
	def DataPathId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def Instruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('instruction')

	@property
	def InstructionMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('instructionMiss')

	@property
	def LocalIp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def Match(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('match')

	@property
	def MaxEntries(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxEntries')

	@property
	def MetadataMatch(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('metadataMatch')

	@property
	def MetadataWrite(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('metadataWrite')

	@property
	def Name(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def NextTable(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('nextTable')

	@property
	def NextTableMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('nextTableMiss')

	@property
	def TableId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('tableId')

	@property
	def WildCards(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('wildCards')

	@property
	def WriteActions(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('writeActions')

	@property
	def WriteActionsMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('writeActionsMiss')

	@property
	def WriteSetField(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('writeSetField')

	@property
	def WriteSetFieldMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('writeSetFieldMiss')

	def find(self, ApplyActions=None, ApplyActionsMiss=None, ApplySetField=None, ApplySetFieldMiss=None, Config=None, DataPathId=None, DataPathIdAsHex=None, Instruction=None, InstructionMiss=None, LocalIp=None, Match=None, MaxEntries=None, MetadataMatch=None, MetadataWrite=None, Name=None, NextTable=None, NextTableMiss=None, TableId=None, WildCards=None, WriteActions=None, WriteActionsMiss=None, WriteSetField=None, WriteSetFieldMiss=None):
		"""Finds and retrieves switchTableFeaturesStatLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchTableFeaturesStatLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchTableFeaturesStatLearnedInfo data from the server.

		Args:
			ApplyActions (str): NOT DEFINED
			ApplyActionsMiss (str): NOT DEFINED
			ApplySetField (str): NOT DEFINED
			ApplySetFieldMiss (str): NOT DEFINED
			Config (number): NOT DEFINED
			DataPathId (str): NOT DEFINED
			DataPathIdAsHex (str): NOT DEFINED
			Instruction (str): NOT DEFINED
			InstructionMiss (str): NOT DEFINED
			LocalIp (str): NOT DEFINED
			Match (str): NOT DEFINED
			MaxEntries (number): NOT DEFINED
			MetadataMatch (str): NOT DEFINED
			MetadataWrite (str): NOT DEFINED
			Name (str): NOT DEFINED
			NextTable (str): NOT DEFINED
			NextTableMiss (str): NOT DEFINED
			TableId (str): NOT DEFINED
			WildCards (str): NOT DEFINED
			WriteActions (str): NOT DEFINED
			WriteActionsMiss (str): NOT DEFINED
			WriteSetField (str): NOT DEFINED
			WriteSetFieldMiss (str): NOT DEFINED

		Returns:
			self: This instance with matching switchTableFeaturesStatLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchTableFeaturesStatLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchTableFeaturesStatLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
