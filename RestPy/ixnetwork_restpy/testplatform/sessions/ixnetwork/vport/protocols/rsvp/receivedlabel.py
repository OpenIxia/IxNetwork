
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


class ReceivedLabel(Base):
	"""The ReceivedLabel class encapsulates a system managed receivedLabel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ReceivedLabel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'receivedLabel'

	def __init__(self, parent):
		super(ReceivedLabel, self).__init__(parent)

	@property
	def CurrentLspOrSubLspUpTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentLspOrSubLspUpTime')

	@property
	def DestinationIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationIp')

	@property
	def Label(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LeafIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('leafIp')

	@property
	def LspId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspId')

	@property
	def LspOrSubLspSetupTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspOrSubLspSetupTime')

	@property
	def ReservationState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('reservationState')

	@property
	def SourceIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceIp')

	@property
	def TunnelId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tunnelId')

	@property
	def Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, CurrentLspOrSubLspUpTime=None, DestinationIp=None, Label=None, LeafIp=None, LspId=None, LspOrSubLspSetupTime=None, ReservationState=None, SourceIp=None, TunnelId=None, Type=None):
		"""Finds and retrieves receivedLabel data from the server.

		All named parameters support regex and can be used to selectively retrieve receivedLabel data from the server.
		By default the find method takes no parameters and will retrieve all receivedLabel data from the server.

		Args:
			CurrentLspOrSubLspUpTime (number): 
			DestinationIp (str): 
			Label (number): 
			LeafIp (str): 
			LspId (number): 
			LspOrSubLspSetupTime (number): 
			ReservationState (str): 
			SourceIp (str): 
			TunnelId (number): 
			Type (str): 

		Returns:
			self: This instance with matching receivedLabel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of receivedLabel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the receivedLabel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
