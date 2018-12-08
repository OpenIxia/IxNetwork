
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


class AdVpls(Base):
	"""The AdVpls class encapsulates a system managed adVpls node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdVpls property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'adVpls'

	def __init__(self, parent):
		super(AdVpls, self).__init__(parent)

	@property
	def NeighborAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighborAddress')

	@property
	def NextHopAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextHopAddress')

	@property
	def RemotePeAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remotePeAddress')

	@property
	def RemoteVplsId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteVplsId')

	@property
	def RemoteVsiId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteVsiId')

	@property
	def RouteDistinguisher(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def RouteTarget(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeTarget')

	@property
	def SupportedLocally(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportedLocally')

	def find(self, NeighborAddress=None, NextHopAddress=None, RemotePeAddress=None, RemoteVplsId=None, RemoteVsiId=None, RouteDistinguisher=None, RouteTarget=None, SupportedLocally=None):
		"""Finds and retrieves adVpls data from the server.

		All named parameters support regex and can be used to selectively retrieve adVpls data from the server.
		By default the find method takes no parameters and will retrieve all adVpls data from the server.

		Args:
			NeighborAddress (str): 
			NextHopAddress (str): 
			RemotePeAddress (str): 
			RemoteVplsId (str): 
			RemoteVsiId (number): 
			RouteDistinguisher (str): 
			RouteTarget (str): 
			SupportedLocally (bool): 

		Returns:
			self: This instance with matching adVpls data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of adVpls data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the adVpls data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
