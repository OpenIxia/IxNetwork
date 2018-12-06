
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


class GroupStatLearnedInformation(Base):
	"""The GroupStatLearnedInformation class encapsulates a system managed groupStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groupStatLearnedInformation'

	def __init__(self, parent):
		super(GroupStatLearnedInformation, self).__init__(parent)

	@property
	def GroupStatBucketLearnedInformation(self):
		"""An instance of the GroupStatBucketLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.groupstatbucketlearnedinformation.GroupStatBucketLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.groupstatbucketlearnedinformation import GroupStatBucketLearnedInformation
		return GroupStatBucketLearnedInformation(self)

	@property
	def ByteCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('byteCount')

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
	def DurationInNSec(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('durationInNSec')

	@property
	def DurationInSec(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('durationInSec')

	@property
	def ErrorCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def GroupId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupId')

	@property
	def Latency(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def NegotiatedVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfBucketStats(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('numberOfBucketStats')

	@property
	def PacketCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('packetCount')

	@property
	def ReferenceCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('referenceCount')

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	def find(self, ByteCount=None, DataPathId=None, DataPathIdAsHex=None, DurationInNSec=None, DurationInSec=None, ErrorCode=None, ErrorType=None, GroupId=None, Latency=None, LocalIp=None, NegotiatedVersion=None, NumberOfBucketStats=None, PacketCount=None, ReferenceCount=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves groupStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve groupStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all groupStatLearnedInformation data from the server.

		Args:
			ByteCount (str): 
			DataPathId (str): 
			DataPathIdAsHex (str): 
			DurationInNSec (str): 
			DurationInSec (str): 
			ErrorCode (str): 
			ErrorType (str): 
			GroupId (str): 
			Latency (number): 
			LocalIp (str): 
			NegotiatedVersion (str): 
			NumberOfBucketStats (str): 
			PacketCount (str): 
			ReferenceCount (str): 
			RemoteIp (str): 
			ReplyState (str): 

		Returns:
			self: This instance with matching groupStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
