
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


class RemoteLocators(Base):
	"""The RemoteLocators class encapsulates a system managed remoteLocators node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RemoteLocators property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'remoteLocators'

	def __init__(self, parent):
		super(RemoteLocators, self).__init__(parent)

	@property
	def MPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mPriority')

	@property
	def MWeight(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mWeight')

	@property
	def Priority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priority')

	@property
	def RemoteLocator(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteLocator')

	@property
	def RemoteLocatorAfi(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteLocatorAfi')

	@property
	def RlocFlagL(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rlocFlagL')

	@property
	def RlocFlagP(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rlocFlagP')

	@property
	def RlocFlagR(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rlocFlagR')

	@property
	def Weight(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('weight')

	def find(self, MPriority=None, MWeight=None, Priority=None, RemoteLocator=None, RemoteLocatorAfi=None, RlocFlagL=None, RlocFlagP=None, RlocFlagR=None, Weight=None):
		"""Finds and retrieves remoteLocators data from the server.

		All named parameters support regex and can be used to selectively retrieve remoteLocators data from the server.
		By default the find method takes no parameters and will retrieve all remoteLocators data from the server.

		Args:
			MPriority (number): 
			MWeight (number): 
			Priority (number): 
			RemoteLocator (str): 
			RemoteLocatorAfi (str): 
			RlocFlagL (bool): 
			RlocFlagP (bool): 
			RlocFlagR (bool): 
			Weight (number): 

		Returns:
			self: This instance with matching remoteLocators data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of remoteLocators data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the remoteLocators data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
