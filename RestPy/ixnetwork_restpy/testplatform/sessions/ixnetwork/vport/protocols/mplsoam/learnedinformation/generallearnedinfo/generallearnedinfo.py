
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


class GeneralLearnedInfo(Base):
	"""The GeneralLearnedInfo class encapsulates a system managed generalLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GeneralLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'generalLearnedInfo'

	def __init__(self, parent):
		super(GeneralLearnedInfo, self).__init__(parent)

	@property
	def AverageRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('averageRtt')

	@property
	def BfdSessionMyState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bfdSessionMyState')

	@property
	def BfdSessionPeerState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bfdSessionPeerState')

	@property
	def CcInUse(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ccInUse')

	@property
	def CvInUse(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cvInUse')

	@property
	def Fec(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fec')

	@property
	def IncomingLabelStack(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelStack')

	@property
	def IncomingLspLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incomingLspLabel')

	@property
	def IncomingPwLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incomingPwLabel')

	@property
	def LspPingReachability(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lspPingReachability')

	@property
	def MaxRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxRtt')

	@property
	def MinRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minRtt')

	@property
	def MyDiscriminator(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('myDiscriminator')

	@property
	def MyIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('myIpAddress')

	@property
	def OutgoingLabelStack(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelStack')

	@property
	def OutgoingLspLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingLspLabel')

	@property
	def OutgoingPwLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingPwLabel')

	@property
	def PeerDiscriminator(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('peerDiscriminator')

	@property
	def PeerIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	@property
	def PingAttempts(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pingAttempts')

	@property
	def PingFailures(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pingFailures')

	@property
	def PingReplyTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pingReplyTx')

	@property
	def PingRequestRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pingRequestRx')

	@property
	def PingSuccess(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pingSuccess')

	@property
	def ReceivedMinRxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('receivedMinRxInterval')

	@property
	def ReceivedMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('receivedMultiplier')

	@property
	def ReceivedPeerFlags(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('receivedPeerFlags')

	@property
	def ReceivedTxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('receivedTxInterval')

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
	def SignalingProtocol(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('signalingProtocol')

	@property
	def TunnelEndpointType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelEndpointType')

	@property
	def TunnelType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelType')

	def find(self, AverageRtt=None, BfdSessionMyState=None, BfdSessionPeerState=None, CcInUse=None, CvInUse=None, Fec=None, IncomingLabelStack=None, IncomingLspLabel=None, IncomingPwLabel=None, LspPingReachability=None, MaxRtt=None, MinRtt=None, MyDiscriminator=None, MyIpAddress=None, OutgoingLabelStack=None, OutgoingLspLabel=None, OutgoingPwLabel=None, PeerDiscriminator=None, PeerIpAddress=None, PingAttempts=None, PingFailures=None, PingReplyTx=None, PingRequestRx=None, PingSuccess=None, ReceivedMinRxInterval=None, ReceivedMultiplier=None, ReceivedPeerFlags=None, ReceivedTxInterval=None, ReturnCode=None, ReturnSubcode=None, SignalingProtocol=None, TunnelEndpointType=None, TunnelType=None):
		"""Finds and retrieves generalLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve generalLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all generalLearnedInfo data from the server.

		Args:
			AverageRtt (str): 
			BfdSessionMyState (str): 
			BfdSessionPeerState (str): 
			CcInUse (str): 
			CvInUse (str): 
			Fec (str): 
			IncomingLabelStack (str): 
			IncomingLspLabel (str): 
			IncomingPwLabel (str): 
			LspPingReachability (str): 
			MaxRtt (str): 
			MinRtt (str): 
			MyDiscriminator (number): 
			MyIpAddress (str): 
			OutgoingLabelStack (str): 
			OutgoingLspLabel (str): 
			OutgoingPwLabel (str): 
			PeerDiscriminator (number): 
			PeerIpAddress (str): 
			PingAttempts (number): 
			PingFailures (number): 
			PingReplyTx (number): 
			PingRequestRx (number): 
			PingSuccess (number): 
			ReceivedMinRxInterval (number): 
			ReceivedMultiplier (number): 
			ReceivedPeerFlags (str): 
			ReceivedTxInterval (number): 
			ReturnCode (str): 
			ReturnSubcode (number): 
			SignalingProtocol (str): 
			TunnelEndpointType (str): 
			TunnelType (str): 

		Returns:
			self: This instance with matching generalLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of generalLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the generalLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=generalLearnedInfo)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
