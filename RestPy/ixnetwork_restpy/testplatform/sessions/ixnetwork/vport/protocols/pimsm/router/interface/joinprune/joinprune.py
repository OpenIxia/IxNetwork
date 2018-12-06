
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


class JoinPrune(Base):
	"""The JoinPrune class encapsulates a user managed joinPrune node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the JoinPrune property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'joinPrune'

	def __init__(self, parent):
		super(JoinPrune, self).__init__(parent)

	@property
	def LearnedMgrState(self):
		"""An instance of the LearnedMgrState class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.learnedmgrstate.learnedmgrstate.LearnedMgrState)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.learnedmgrstate.learnedmgrstate import LearnedMgrState
		return LearnedMgrState(self)

	@property
	def DiscardRegisterStates(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardRegisterStates')
	@DiscardRegisterStates.setter
	def DiscardRegisterStates(self, value):
		self._set_attribute('discardRegisterStates', value)

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
	def EnabledDataMdt(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabledDataMdt')
	@EnabledDataMdt.setter
	def EnabledDataMdt(self, value):
		self._set_attribute('enabledDataMdt', value)

	@property
	def FlapEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('flapEnabled')
	@FlapEnabled.setter
	def FlapEnabled(self, value):
		self._set_attribute('flapEnabled', value)

	@property
	def FlapInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flapInterval')
	@FlapInterval.setter
	def FlapInterval(self, value):
		self._set_attribute('flapInterval', value)

	@property
	def GroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')
	@GroupAddress.setter
	def GroupAddress(self, value):
		self._set_attribute('groupAddress', value)

	@property
	def GroupCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupMappingMode(self):
		"""

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('groupMappingMode')
	@GroupMappingMode.setter
	def GroupMappingMode(self, value):
		self._set_attribute('groupMappingMode', value)

	@property
	def GroupMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupMaskWidth')
	@GroupMaskWidth.setter
	def GroupMaskWidth(self, value):
		self._set_attribute('groupMaskWidth', value)

	@property
	def GroupRange(self):
		"""

		Returns:
			str(rp|g|sg|sptSwitchOver|registerTriggeredSg)
		"""
		return self._get_attribute('groupRange')
	@GroupRange.setter
	def GroupRange(self, value):
		self._set_attribute('groupRange', value)

	@property
	def NumRegToReceivePerSg(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numRegToReceivePerSg')
	@NumRegToReceivePerSg.setter
	def NumRegToReceivePerSg(self, value):
		self._set_attribute('numRegToReceivePerSg', value)

	@property
	def PackGroupsEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('packGroupsEnabled')
	@PackGroupsEnabled.setter
	def PackGroupsEnabled(self, value):
		self._set_attribute('packGroupsEnabled', value)

	@property
	def PruneSourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pruneSourceAddress')
	@PruneSourceAddress.setter
	def PruneSourceAddress(self, value):
		self._set_attribute('pruneSourceAddress', value)

	@property
	def PruneSourceCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pruneSourceCount')
	@PruneSourceCount.setter
	def PruneSourceCount(self, value):
		self._set_attribute('pruneSourceCount', value)

	@property
	def PruneSourceMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pruneSourceMaskWidth')
	@PruneSourceMaskWidth.setter
	def PruneSourceMaskWidth(self, value):
		self._set_attribute('pruneSourceMaskWidth', value)

	@property
	def RpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rpAddress')
	@RpAddress.setter
	def RpAddress(self, value):
		self._set_attribute('rpAddress', value)

	@property
	def SourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')
	@SourceAddress.setter
	def SourceAddress(self, value):
		self._set_attribute('sourceAddress', value)

	@property
	def SourceCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceCount')
	@SourceCount.setter
	def SourceCount(self, value):
		self._set_attribute('sourceCount', value)

	@property
	def SourceMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceMaskWidth')
	@SourceMaskWidth.setter
	def SourceMaskWidth(self, value):
		self._set_attribute('sourceMaskWidth', value)

	@property
	def SptSwitchoverInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sptSwitchoverInterval')
	@SptSwitchoverInterval.setter
	def SptSwitchoverInterval(self, value):
		self._set_attribute('sptSwitchoverInterval', value)

	def add(self, DiscardRegisterStates=None, Enabled=None, EnabledDataMdt=None, FlapEnabled=None, FlapInterval=None, GroupAddress=None, GroupCount=None, GroupMappingMode=None, GroupMaskWidth=None, GroupRange=None, NumRegToReceivePerSg=None, PackGroupsEnabled=None, PruneSourceAddress=None, PruneSourceCount=None, PruneSourceMaskWidth=None, RpAddress=None, SourceAddress=None, SourceCount=None, SourceMaskWidth=None, SptSwitchoverInterval=None):
		"""Adds a new joinPrune node on the server and retrieves it in this instance.

		Args:
			DiscardRegisterStates (bool): 
			Enabled (bool): 
			EnabledDataMdt (bool): 
			FlapEnabled (bool): 
			FlapInterval (number): 
			GroupAddress (str): 
			GroupCount (number): 
			GroupMappingMode (str(fullyMeshed|oneToOne)): 
			GroupMaskWidth (number): 
			GroupRange (str(rp|g|sg|sptSwitchOver|registerTriggeredSg)): 
			NumRegToReceivePerSg (number): 
			PackGroupsEnabled (bool): 
			PruneSourceAddress (str): 
			PruneSourceCount (number): 
			PruneSourceMaskWidth (number): 
			RpAddress (str): 
			SourceAddress (str): 
			SourceCount (number): 
			SourceMaskWidth (number): 
			SptSwitchoverInterval (number): 

		Returns:
			self: This instance with all currently retrieved joinPrune data using find and the newly added joinPrune data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the joinPrune data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DiscardRegisterStates=None, Enabled=None, EnabledDataMdt=None, FlapEnabled=None, FlapInterval=None, GroupAddress=None, GroupCount=None, GroupMappingMode=None, GroupMaskWidth=None, GroupRange=None, NumRegToReceivePerSg=None, PackGroupsEnabled=None, PruneSourceAddress=None, PruneSourceCount=None, PruneSourceMaskWidth=None, RpAddress=None, SourceAddress=None, SourceCount=None, SourceMaskWidth=None, SptSwitchoverInterval=None):
		"""Finds and retrieves joinPrune data from the server.

		All named parameters support regex and can be used to selectively retrieve joinPrune data from the server.
		By default the find method takes no parameters and will retrieve all joinPrune data from the server.

		Args:
			DiscardRegisterStates (bool): 
			Enabled (bool): 
			EnabledDataMdt (bool): 
			FlapEnabled (bool): 
			FlapInterval (number): 
			GroupAddress (str): 
			GroupCount (number): 
			GroupMappingMode (str(fullyMeshed|oneToOne)): 
			GroupMaskWidth (number): 
			GroupRange (str(rp|g|sg|sptSwitchOver|registerTriggeredSg)): 
			NumRegToReceivePerSg (number): 
			PackGroupsEnabled (bool): 
			PruneSourceAddress (str): 
			PruneSourceCount (number): 
			PruneSourceMaskWidth (number): 
			RpAddress (str): 
			SourceAddress (str): 
			SourceCount (number): 
			SourceMaskWidth (number): 
			SptSwitchoverInterval (number): 

		Returns:
			self: This instance with matching joinPrune data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of joinPrune data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the joinPrune data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
