
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


class SwitchOfChannel(Base):
	"""The SwitchOfChannel class encapsulates a user managed switchOfChannel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchOfChannel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'switchOfChannel'

	def __init__(self, parent):
		super(SwitchOfChannel, self).__init__(parent)

	@property
	def AuxiliaryConnection(self):
		"""An instance of the AuxiliaryConnection class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.auxiliaryconnection.AuxiliaryConnection)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.auxiliaryconnection import AuxiliaryConnection
		return AuxiliaryConnection(self)

	@property
	def Description(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

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
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')
	@RemoteIp.setter
	def RemoteIp(self, value):
		self._set_attribute('remoteIp', value)

	def add(self, Description=None, Enabled=None, RemoteIp=None):
		"""Adds a new switchOfChannel node on the server and retrieves it in this instance.

		Args:
			Description (str): 
			Enabled (bool): 
			RemoteIp (str): 

		Returns:
			self: This instance with all currently retrieved switchOfChannel data using find and the newly added switchOfChannel data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the switchOfChannel data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Description=None, Enabled=None, RemoteIp=None):
		"""Finds and retrieves switchOfChannel data from the server.

		All named parameters support regex and can be used to selectively retrieve switchOfChannel data from the server.
		By default the find method takes no parameters and will retrieve all switchOfChannel data from the server.

		Args:
			Description (str): 
			Enabled (bool): 
			RemoteIp (str): 

		Returns:
			self: This instance with matching switchOfChannel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchOfChannel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchOfChannel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
