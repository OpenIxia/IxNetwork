
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


class Session(Base):
	"""The Session class encapsulates a user managed session node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Session property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'session'

	def __init__(self, parent):
		super(Session, self).__init__(parent)

	@property
	def BfdSessionType(self):
		"""

		Returns:
			str(singleHop|multipleHops)
		"""
		return self._get_attribute('bfdSessionType')
	@BfdSessionType.setter
	def BfdSessionType(self, value):
		self._set_attribute('bfdSessionType', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EnabledAutoChooseSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabledAutoChooseSource')
	@EnabledAutoChooseSource.setter
	def EnabledAutoChooseSource(self, value):
		self._set_attribute('enabledAutoChooseSource', value)

	@property
	def IpType(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def LocalBfdAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localBfdAddress')
	@LocalBfdAddress.setter
	def LocalBfdAddress(self, value):
		self._set_attribute('localBfdAddress', value)

	@property
	def MyDisc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('myDisc')
	@MyDisc.setter
	def MyDisc(self, value):
		self._set_attribute('myDisc', value)

	@property
	def RemoteBfdAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteBfdAddress')
	@RemoteBfdAddress.setter
	def RemoteBfdAddress(self, value):
		self._set_attribute('remoteBfdAddress', value)

	@property
	def RemoteDisc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteDisc')
	@RemoteDisc.setter
	def RemoteDisc(self, value):
		self._set_attribute('remoteDisc', value)

	@property
	def RemoteDiscLearned(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteDiscLearned')
	@RemoteDiscLearned.setter
	def RemoteDiscLearned(self, value):
		self._set_attribute('remoteDiscLearned', value)

	def add(self, BfdSessionType=None, Enabled=None, EnabledAutoChooseSource=None, IpType=None, LocalBfdAddress=None, MyDisc=None, RemoteBfdAddress=None, RemoteDisc=None, RemoteDiscLearned=None):
		"""Adds a new session node on the server and retrieves it in this instance.

		Args:
			BfdSessionType (str(singleHop|multipleHops)): 
			Enabled (bool): 
			EnabledAutoChooseSource (bool): 
			IpType (str(ipv4|ipv6)): 
			LocalBfdAddress (str): 
			MyDisc (number): 
			RemoteBfdAddress (str): 
			RemoteDisc (number): 
			RemoteDiscLearned (bool): 

		Returns:
			self: This instance with all currently retrieved session data using find and the newly added session data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the session data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BfdSessionType=None, Enabled=None, EnabledAutoChooseSource=None, IpType=None, LocalBfdAddress=None, MyDisc=None, RemoteBfdAddress=None, RemoteDisc=None, RemoteDiscLearned=None):
		"""Finds and retrieves session data from the server.

		All named parameters support regex and can be used to selectively retrieve session data from the server.
		By default the find method takes no parameters and will retrieve all session data from the server.

		Args:
			BfdSessionType (str(singleHop|multipleHops)): 
			Enabled (bool): 
			EnabledAutoChooseSource (bool): 
			IpType (str(ipv4|ipv6)): 
			LocalBfdAddress (str): 
			MyDisc (number): 
			RemoteBfdAddress (str): 
			RemoteDisc (number): 
			RemoteDiscLearned (bool): 

		Returns:
			self: This instance with matching session data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of session data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the session data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
