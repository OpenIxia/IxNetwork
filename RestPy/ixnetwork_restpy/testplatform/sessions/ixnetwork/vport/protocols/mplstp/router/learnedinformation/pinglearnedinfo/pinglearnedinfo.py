
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


class PingLearnedInfo(Base):
	"""The PingLearnedInfo class encapsulates a system managed pingLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PingLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pingLearnedInfo'

	def __init__(self, parent):
		super(PingLearnedInfo, self).__init__(parent)

	@property
	def ErrorTlvType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('errorTlvType')

	@property
	def IncomingLabelOuterInner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def InterfaceLabelStackTlvInterface(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceLabelStackTlvInterface')

	@property
	def InterfaceLabelStackTlvIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvIpAddress')

	@property
	def InterfaceLabelStackTlvLabels(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvLabels')

	@property
	def OutgoingLabelOuterInner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def Reachability(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('reachability')

	@property
	def ReturnCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('returnCode')

	@property
	def ReturnSubcode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('returnSubcode')

	@property
	def ReversePathVerificationCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('reversePathVerificationCode')

	@property
	def Rtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rtt')

	@property
	def SenderHandle(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('senderHandle')

	@property
	def SequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, ErrorTlvType=None, IncomingLabelOuterInner=None, InterfaceLabelStackTlvInterface=None, InterfaceLabelStackTlvIpAddress=None, InterfaceLabelStackTlvLabels=None, OutgoingLabelOuterInner=None, Reachability=None, ReturnCode=None, ReturnSubcode=None, ReversePathVerificationCode=None, Rtt=None, SenderHandle=None, SequenceNumber=None, Type=None):
		"""Finds and retrieves pingLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pingLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pingLearnedInfo data from the server.

		Args:
			ErrorTlvType (number): 
			IncomingLabelOuterInner (str): 
			InterfaceLabelStackTlvInterface (number): 
			InterfaceLabelStackTlvIpAddress (str): 
			InterfaceLabelStackTlvLabels (str): 
			OutgoingLabelOuterInner (str): 
			Reachability (bool): 
			ReturnCode (str): 
			ReturnSubcode (number): 
			ReversePathVerificationCode (str): 
			Rtt (str): 
			SenderHandle (number): 
			SequenceNumber (number): 
			Type (str): 

		Returns:
			self: This instance with matching pingLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pingLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pingLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
