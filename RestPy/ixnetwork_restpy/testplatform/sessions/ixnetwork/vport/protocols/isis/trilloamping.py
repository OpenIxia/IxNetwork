
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


class TrillOamPing(Base):
	"""The TrillOamPing class encapsulates a system managed trillOamPing node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrillOamPing property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'trillOamPing'

	def __init__(self, parent):
		super(TrillOamPing, self).__init__(parent)

	@property
	def DestinationNickname(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destinationNickname')

	@property
	def IncomingPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('incomingPort')

	@property
	def NextHop(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nextHop')

	@property
	def OutgoingPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outgoingPort')

	@property
	def OutgoingPortMtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outgoingPortMtu')

	@property
	def PreviousHop(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('previousHop')

	@property
	def ResponseTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('responseTime')

	@property
	def SequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def SourceNickname(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceNickname')

	@property
	def Status(self):
		"""

		Returns:
			str(Failure|Success)
		"""
		return self._get_attribute('status')

	def find(self, DestinationNickname=None, IncomingPort=None, NextHop=None, OutgoingPort=None, OutgoingPortMtu=None, PreviousHop=None, ResponseTime=None, SequenceNumber=None, SourceNickname=None, Status=None):
		"""Finds and retrieves trillOamPing data from the server.

		All named parameters support regex and can be used to selectively retrieve trillOamPing data from the server.
		By default the find method takes no parameters and will retrieve all trillOamPing data from the server.

		Args:
			DestinationNickname (number): 
			IncomingPort (number): 
			NextHop (number): 
			OutgoingPort (number): 
			OutgoingPortMtu (number): 
			PreviousHop (number): 
			ResponseTime (number): 
			SequenceNumber (number): 
			SourceNickname (number): 
			Status (str(Failure|Success)): 

		Returns:
			self: This instance with matching trillOamPing data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trillOamPing data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trillOamPing data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
