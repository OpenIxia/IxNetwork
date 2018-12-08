
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


class LearnedInfo(Base):
	"""The LearnedInfo class encapsulates a system managed learnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedInfo'

	def __init__(self, parent):
		super(LearnedInfo, self).__init__(parent)

	@property
	def DesMinTxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('desMinTxInterval')

	@property
	def MyDisc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('myDisc')

	@property
	def MyIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('myIpAddress')

	@property
	def PeerDisc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('peerDisc')

	@property
	def PeerFlags(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerFlags')

	@property
	def PeerIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	@property
	def PeerState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerState')

	@property
	def PeerUpTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('peerUpTime')

	@property
	def ProtocolUsingSession(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('protocolUsingSession')

	@property
	def ReqMinEchoInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('reqMinEchoInterval')

	@property
	def ReqMinRxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('reqMinRxInterval')

	@property
	def SessionState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sessionState')

	@property
	def SessionType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sessionType')

	def find(self, DesMinTxInterval=None, MyDisc=None, MyIpAddress=None, PeerDisc=None, PeerFlags=None, PeerIpAddress=None, PeerState=None, PeerUpTime=None, ProtocolUsingSession=None, ReqMinEchoInterval=None, ReqMinRxInterval=None, SessionState=None, SessionType=None):
		"""Finds and retrieves learnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedInfo data from the server.

		Args:
			DesMinTxInterval (number): 
			MyDisc (number): 
			MyIpAddress (str): 
			PeerDisc (number): 
			PeerFlags (str): 
			PeerIpAddress (str): 
			PeerState (str): 
			PeerUpTime (number): 
			ProtocolUsingSession (str): 
			ReqMinEchoInterval (number): 
			ReqMinRxInterval (number): 
			SessionState (str): 
			SessionType (str): 

		Returns:
			self: This instance with matching learnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
