
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


class Source(Base):
	"""The Source class encapsulates a user managed source node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Source property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'source'

	def __init__(self, parent):
		super(Source, self).__init__(parent)

	@property
	def LearnedSgState(self):
		"""An instance of the LearnedSgState class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.source.learnedsgstate.learnedsgstate.LearnedSgState)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.source.learnedsgstate.learnedsgstate import LearnedSgState
		return LearnedSgState(self)

	@property
	def DiscardSgJoinStates(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardSgJoinStates')
	@DiscardSgJoinStates.setter
	def DiscardSgJoinStates(self, value):
		self._set_attribute('discardSgJoinStates', value)

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
	def MulticastDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multicastDataLength')
	@MulticastDataLength.setter
	def MulticastDataLength(self, value):
		self._set_attribute('multicastDataLength', value)

	@property
	def RegisterProbeTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('registerProbeTime')
	@RegisterProbeTime.setter
	def RegisterProbeTime(self, value):
		self._set_attribute('registerProbeTime', value)

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
	def SendNullRegAtBegin(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendNullRegAtBegin')
	@SendNullRegAtBegin.setter
	def SendNullRegAtBegin(self, value):
		self._set_attribute('sendNullRegAtBegin', value)

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
	def SuppressionTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('suppressionTime')
	@SuppressionTime.setter
	def SuppressionTime(self, value):
		self._set_attribute('suppressionTime', value)

	@property
	def SwitchOverInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchOverInterval')
	@SwitchOverInterval.setter
	def SwitchOverInterval(self, value):
		self._set_attribute('switchOverInterval', value)

	@property
	def TxIterationGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('txIterationGap')
	@TxIterationGap.setter
	def TxIterationGap(self, value):
		self._set_attribute('txIterationGap', value)

	@property
	def UdpDstPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('udpDstPort')
	@UdpDstPort.setter
	def UdpDstPort(self, value):
		self._set_attribute('udpDstPort', value)

	@property
	def UdpSrcPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('udpSrcPort')
	@UdpSrcPort.setter
	def UdpSrcPort(self, value):
		self._set_attribute('udpSrcPort', value)

	def add(self, DiscardSgJoinStates=None, Enabled=None, GroupAddress=None, GroupCount=None, GroupMappingMode=None, GroupMaskWidth=None, MulticastDataLength=None, RegisterProbeTime=None, RpAddress=None, SendNullRegAtBegin=None, SourceAddress=None, SourceCount=None, SuppressionTime=None, SwitchOverInterval=None, TxIterationGap=None, UdpDstPort=None, UdpSrcPort=None):
		"""Adds a new source node on the server and retrieves it in this instance.

		Args:
			DiscardSgJoinStates (bool): 
			Enabled (bool): 
			GroupAddress (str): 
			GroupCount (number): 
			GroupMappingMode (str(fullyMeshed|oneToOne)): 
			GroupMaskWidth (number): 
			MulticastDataLength (number): 
			RegisterProbeTime (number): 
			RpAddress (str): 
			SendNullRegAtBegin (bool): 
			SourceAddress (str): 
			SourceCount (number): 
			SuppressionTime (number): 
			SwitchOverInterval (number): 
			TxIterationGap (number): 
			UdpDstPort (number): 
			UdpSrcPort (number): 

		Returns:
			self: This instance with all currently retrieved source data using find and the newly added source data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the source data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DiscardSgJoinStates=None, Enabled=None, GroupAddress=None, GroupCount=None, GroupMappingMode=None, GroupMaskWidth=None, MulticastDataLength=None, RegisterProbeTime=None, RpAddress=None, SendNullRegAtBegin=None, SourceAddress=None, SourceCount=None, SuppressionTime=None, SwitchOverInterval=None, TxIterationGap=None, UdpDstPort=None, UdpSrcPort=None):
		"""Finds and retrieves source data from the server.

		All named parameters support regex and can be used to selectively retrieve source data from the server.
		By default the find method takes no parameters and will retrieve all source data from the server.

		Args:
			DiscardSgJoinStates (bool): 
			Enabled (bool): 
			GroupAddress (str): 
			GroupCount (number): 
			GroupMappingMode (str(fullyMeshed|oneToOne)): 
			GroupMaskWidth (number): 
			MulticastDataLength (number): 
			RegisterProbeTime (number): 
			RpAddress (str): 
			SendNullRegAtBegin (bool): 
			SourceAddress (str): 
			SourceCount (number): 
			SuppressionTime (number): 
			SwitchOverInterval (number): 
			TxIterationGap (number): 
			UdpDstPort (number): 
			UdpSrcPort (number): 

		Returns:
			self: This instance with matching source data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of source data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the source data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
