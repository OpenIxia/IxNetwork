
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


class PortStatLearnedInformation(Base):
	"""The PortStatLearnedInformation class encapsulates a system managed portStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PortStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'portStatLearnedInformation'

	def __init__(self, parent):
		super(PortStatLearnedInformation, self).__init__(parent)

	@property
	def Collisions(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('collisions')

	@property
	def CrcErrors(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('crcErrors')

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
	def Duration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('duration')

	@property
	def DurationInNsec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('durationInNsec')

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
	def FrameAlignmentErrors(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('frameAlignmentErrors')

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
	def PacketsDroppedByRx(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('packetsDroppedByRx')

	@property
	def PacketsDroppedByTx(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('packetsDroppedByTx')

	@property
	def PacketsWithRxOverrun(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('packetsWithRxOverrun')

	@property
	def PortNo(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portNo')

	@property
	def ReceivedBytes(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('receivedBytes')

	@property
	def ReceivedErrors(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('receivedErrors')

	@property
	def ReceivedPackets(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('receivedPackets')

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

	@property
	def TransmitErrors(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transmitErrors')

	@property
	def TransmittedBytes(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transmittedBytes')

	@property
	def TransmittedPackets(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transmittedPackets')

	def find(self, Collisions=None, CrcErrors=None, DataPathId=None, DataPathIdAsHex=None, Duration=None, DurationInNsec=None, ErrorCode=None, ErrorType=None, FrameAlignmentErrors=None, Latency=None, LocalIp=None, NegotiatedVersion=None, PacketsDroppedByRx=None, PacketsDroppedByTx=None, PacketsWithRxOverrun=None, PortNo=None, ReceivedBytes=None, ReceivedErrors=None, ReceivedPackets=None, RemoteIp=None, ReplyState=None, TransmitErrors=None, TransmittedBytes=None, TransmittedPackets=None):
		"""Finds and retrieves portStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve portStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all portStatLearnedInformation data from the server.

		Args:
			Collisions (str): 
			CrcErrors (str): 
			DataPathId (str): 
			DataPathIdAsHex (str): 
			Duration (number): 
			DurationInNsec (number): 
			ErrorCode (str): 
			ErrorType (str): 
			FrameAlignmentErrors (str): 
			Latency (number): 
			LocalIp (str): 
			NegotiatedVersion (str): 
			PacketsDroppedByRx (str): 
			PacketsDroppedByTx (str): 
			PacketsWithRxOverrun (str): 
			PortNo (number): 
			ReceivedBytes (str): 
			ReceivedErrors (str): 
			ReceivedPackets (str): 
			RemoteIp (str): 
			ReplyState (str): 
			TransmitErrors (str): 
			TransmittedBytes (str): 
			TransmittedPackets (str): 

		Returns:
			self: This instance with matching portStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of portStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the portStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
