
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


class MacMulticast(Base):
	"""The MacMulticast class encapsulates a system managed macMulticast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MacMulticast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'macMulticast'

	def __init__(self, parent):
		super(MacMulticast, self).__init__(parent)

	@property
	def UnicastMacItem(self):
		"""An instance of the UnicastMacItem class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.unicastmacitem.UnicastMacItem)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.unicastmacitem import UnicastMacItem
		return UnicastMacItem(self)

	@property
	def Age(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def HostName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def LspId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lspId')

	@property
	def MulticastGroupMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('multicastGroupMacAddress')

	@property
	def SequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def VlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	def find(self, Age=None, HostName=None, LspId=None, MulticastGroupMacAddress=None, SequenceNumber=None, VlanId=None):
		"""Finds and retrieves macMulticast data from the server.

		All named parameters support regex and can be used to selectively retrieve macMulticast data from the server.
		By default the find method takes no parameters and will retrieve all macMulticast data from the server.

		Args:
			Age (number): 
			HostName (str): 
			LspId (str): 
			MulticastGroupMacAddress (str): 
			SequenceNumber (number): 
			VlanId (number): 

		Returns:
			self: This instance with matching macMulticast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of macMulticast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the macMulticast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
