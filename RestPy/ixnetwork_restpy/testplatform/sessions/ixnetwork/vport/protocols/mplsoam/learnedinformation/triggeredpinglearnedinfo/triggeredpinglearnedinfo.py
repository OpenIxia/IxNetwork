
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


class TriggeredPingLearnedInfo(Base):
	"""The TriggeredPingLearnedInfo class encapsulates a system managed triggeredPingLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TriggeredPingLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'triggeredPingLearnedInfo'

	def __init__(self, parent):
		super(TriggeredPingLearnedInfo, self).__init__(parent)

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
	def OutgoingLabelStack(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelStack')

	@property
	def PeerIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	@property
	def Reachability(self):
		"""

		Returns:
			str
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
	def ReturnSubCode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('returnSubCode')

	@property
	def Rtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rtt')

	def find(self, Fec=None, IncomingLabelStack=None, OutgoingLabelStack=None, PeerIpAddress=None, Reachability=None, ReturnCode=None, ReturnSubCode=None, Rtt=None):
		"""Finds and retrieves triggeredPingLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve triggeredPingLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all triggeredPingLearnedInfo data from the server.

		Args:
			Fec (str): 
			IncomingLabelStack (str): 
			OutgoingLabelStack (str): 
			PeerIpAddress (str): 
			Reachability (str): 
			ReturnCode (str): 
			ReturnSubCode (number): 
			Rtt (str): 

		Returns:
			self: This instance with matching triggeredPingLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of triggeredPingLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the triggeredPingLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
