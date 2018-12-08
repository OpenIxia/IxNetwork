
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


class MeterStatsLearnedInformation(Base):
	"""The MeterStatsLearnedInformation class encapsulates a system managed meterStatsLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterStatsLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meterStatsLearnedInformation'

	def __init__(self, parent):
		super(MeterStatsLearnedInformation, self).__init__(parent)

	@property
	def MeterStatsBandLearnedInformation(self):
		"""An instance of the MeterStatsBandLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meterstatsbandlearnedinformation.MeterStatsBandLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meterstatsbandlearnedinformation import MeterStatsBandLearnedInformation
		return MeterStatsBandLearnedInformation(self)

	@property
	def ByteInCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('byteInCount')

	@property
	def DataPathId(self):
		"""

		Returns:
			number
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
	def DurationNSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('durationNSec')

	@property
	def DurationSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('durationSec')

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
	def FlowCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowCount')

	@property
	def LastErrorCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastErrorCode')

	@property
	def LastErrorType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastErrorType')

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
	def MeterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def NegotiatedVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfBandStats(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfBandStats')

	@property
	def PacketInCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetInCount')

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

	def find(self, ByteInCount=None, DataPathId=None, DataPathIdAsHex=None, DurationNSec=None, DurationSec=None, ErrorCode=None, ErrorType=None, FlowCount=None, LastErrorCode=None, LastErrorType=None, Latency=None, LocalIp=None, MeterId=None, NegotiatedVersion=None, NumberOfBandStats=None, PacketInCount=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves meterStatsLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve meterStatsLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all meterStatsLearnedInformation data from the server.

		Args:
			ByteInCount (number): 
			DataPathId (number): 
			DataPathIdAsHex (str): 
			DurationNSec (number): 
			DurationSec (number): 
			ErrorCode (str): 
			ErrorType (str): 
			FlowCount (number): 
			LastErrorCode (str): 
			LastErrorType (str): 
			Latency (number): 
			LocalIp (str): 
			MeterId (number): 
			NegotiatedVersion (str): 
			NumberOfBandStats (number): 
			PacketInCount (number): 
			RemoteIp (str): 
			ReplyState (str): 

		Returns:
			self: This instance with matching meterStatsLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meterStatsLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meterStatsLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
