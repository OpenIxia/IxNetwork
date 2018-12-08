
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
		"""

		Returns:
			str
		"""
		return self._get_attribute('applyActions')

	@property
	def ApplyActionsMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('applyActionsMiss')

	@property
	def ApplySetField(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('applySetField')

	@property
	def ApplySetFieldMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('applySetFieldMiss')

	@property
	def Config(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('config')

	@property
	def DataPathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def Instruction(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('instruction')

	@property
	def InstructionMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('instructionMiss')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def Match(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('match')

	@property
	def MaxEntries(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxEntries')

	@property
	def MetadataMatch(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataMatch')

	@property
	def MetadataWrite(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataWrite')

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def NextTable(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextTable')

	@property
	def NextTableMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextTableMiss')

	@property
	def TableId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tableId')

	@property
	def WildCards(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('wildCards')

	@property
	def WriteActions(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('writeActions')

	@property
	def WriteActionsMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('writeActionsMiss')

	@property
	def WriteSetField(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('writeSetField')

	@property
	def WriteSetFieldMiss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('writeSetFieldMiss')

	def find(self, ApplyActions=None, ApplyActionsMiss=None, ApplySetField=None, ApplySetFieldMiss=None, Config=None, DataPathId=None, DataPathIdAsHex=None, Instruction=None, InstructionMiss=None, LocalIp=None, Match=None, MaxEntries=None, MetadataMatch=None, MetadataWrite=None, Name=None, NextTable=None, NextTableMiss=None, TableId=None, WildCards=None, WriteActions=None, WriteActionsMiss=None, WriteSetField=None, WriteSetFieldMiss=None):
		"""Finds and retrieves switchTableFeaturesStatLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchTableFeaturesStatLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchTableFeaturesStatLearnedInfo data from the server.

		Args:
			ApplyActions (str): 
			ApplyActionsMiss (str): 
			ApplySetField (str): 
			ApplySetFieldMiss (str): 
			Config (number): 
			DataPathId (str): 
			DataPathIdAsHex (str): 
			Instruction (str): 
			InstructionMiss (str): 
			LocalIp (str): 
			Match (str): 
			MaxEntries (number): 
			MetadataMatch (str): 
			MetadataWrite (str): 
			Name (str): 
			NextTable (str): 
			NextTableMiss (str): 
			TableId (str): 
			WildCards (str): 
			WriteActions (str): 
			WriteActionsMiss (str): 
			WriteSetField (str): 
			WriteSetFieldMiss (str): 

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
