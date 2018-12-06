
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


class TargetPeer(Base):
	"""The TargetPeer class encapsulates a user managed targetPeer node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TargetPeer property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'targetPeer'

	def __init__(self, parent):
		super(TargetPeer, self).__init__(parent)

	@property
	def Authentication(self):
		"""

		Returns:
			str(null|md5)
		"""
		return self._get_attribute('authentication')
	@Authentication.setter
	def Authentication(self, value):
		self._set_attribute('authentication', value)

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
	def InitiateTargetedHello(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('initiateTargetedHello')
	@InitiateTargetedHello.setter
	def InitiateTargetedHello(self, value):
		self._set_attribute('initiateTargetedHello', value)

	@property
	def IpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def Md5Key(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('md5Key')
	@Md5Key.setter
	def Md5Key(self, value):
		self._set_attribute('md5Key', value)

	def add(self, Authentication=None, Enabled=None, InitiateTargetedHello=None, IpAddress=None, Md5Key=None):
		"""Adds a new targetPeer node on the server and retrieves it in this instance.

		Args:
			Authentication (str(null|md5)): 
			Enabled (bool): 
			InitiateTargetedHello (bool): 
			IpAddress (str): 
			Md5Key (str): 

		Returns:
			self: This instance with all currently retrieved targetPeer data using find and the newly added targetPeer data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the targetPeer data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Authentication=None, Enabled=None, InitiateTargetedHello=None, IpAddress=None, Md5Key=None):
		"""Finds and retrieves targetPeer data from the server.

		All named parameters support regex and can be used to selectively retrieve targetPeer data from the server.
		By default the find method takes no parameters and will retrieve all targetPeer data from the server.

		Args:
			Authentication (str(null|md5)): 
			Enabled (bool): 
			InitiateTargetedHello (bool): 
			IpAddress (str): 
			Md5Key (str): 

		Returns:
			self: This instance with matching targetPeer data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of targetPeer data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the targetPeer data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
