
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


class LmiStatusLearnedInfo(Base):
	"""The LmiStatusLearnedInfo class encapsulates a system managed lmiStatusLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LmiStatusLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'lmiStatusLearnedInfo'

	def __init__(self, parent):
		super(LmiStatusLearnedInfo, self).__init__(parent)

	@property
	def DataInstance(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataInstance')

	@property
	def DuplicatedIe(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('duplicatedIe')

	@property
	def InvalidEvcReferenceId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('invalidEvcReferenceId')

	@property
	def InvalidMandatoryIe(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('invalidMandatoryIe')

	@property
	def InvalidMsgType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('invalidMsgType')

	@property
	def InvalidNonMandatoryIe(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('invalidNonMandatoryIe')

	@property
	def InvalidProtocolVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('invalidProtocolVersion')

	@property
	def LmiStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lmiStatus')

	@property
	def MandatoryIeMissing(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mandatoryIeMissing')

	@property
	def OutOfSequenceIe(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outOfSequenceIe')

	@property
	def ProtocolVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('protocolVersion')

	@property
	def ReceiveSequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('receiveSequenceNumber')

	@property
	def SendSequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sendSequenceNumber')

	@property
	def ShortMsgCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('shortMsgCounter')

	@property
	def UnexpectedIe(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('unexpectedIe')

	@property
	def UnrecognizedIe(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('unrecognizedIe')

	def find(self, DataInstance=None, DuplicatedIe=None, InvalidEvcReferenceId=None, InvalidMandatoryIe=None, InvalidMsgType=None, InvalidNonMandatoryIe=None, InvalidProtocolVersion=None, LmiStatus=None, MandatoryIeMissing=None, OutOfSequenceIe=None, ProtocolVersion=None, ReceiveSequenceNumber=None, SendSequenceNumber=None, ShortMsgCounter=None, UnexpectedIe=None, UnrecognizedIe=None):
		"""Finds and retrieves lmiStatusLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve lmiStatusLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all lmiStatusLearnedInfo data from the server.

		Args:
			DataInstance (number): 
			DuplicatedIe (str): 
			InvalidEvcReferenceId (str): 
			InvalidMandatoryIe (str): 
			InvalidMsgType (str): 
			InvalidNonMandatoryIe (str): 
			InvalidProtocolVersion (str): 
			LmiStatus (str): 
			MandatoryIeMissing (str): 
			OutOfSequenceIe (str): 
			ProtocolVersion (number): 
			ReceiveSequenceNumber (number): 
			SendSequenceNumber (number): 
			ShortMsgCounter (number): 
			UnexpectedIe (str): 
			UnrecognizedIe (str): 

		Returns:
			self: This instance with matching lmiStatusLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lmiStatusLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lmiStatusLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
