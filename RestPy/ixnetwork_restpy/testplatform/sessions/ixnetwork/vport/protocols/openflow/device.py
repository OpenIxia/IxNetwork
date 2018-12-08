
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


class Device(Base):
	"""The Device class encapsulates a user managed device node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Device property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'device'

	def __init__(self, parent):
		super(Device, self).__init__(parent)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.interface import Interface
		return Interface(self)

	@property
	def CaCertificateFile(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('caCertificateFile')

	@property
	def CertificateFile(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('certificateFile')

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
	def DeviceRole(self):
		"""

		Returns:
			str(controller|switch)
		"""
		return self._get_attribute('deviceRole')
	@DeviceRole.setter
	def DeviceRole(self, value):
		self._set_attribute('deviceRole', value)

	@property
	def EnableVersion100(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVersion100')
	@EnableVersion100.setter
	def EnableVersion100(self, value):
		self._set_attribute('enableVersion100', value)

	@property
	def EnableVersion131(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVersion131')
	@EnableVersion131.setter
	def EnableVersion131(self, value):
		self._set_attribute('enableVersion131', value)

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
	def PrivateFile(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('privateFile')

	@property
	def Version(self):
		"""

		Returns:
			str(1.0.0)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, Description=None, DeviceRole=None, EnableVersion100=None, EnableVersion131=None, Enabled=None, Version=None):
		"""Adds a new device node on the server and retrieves it in this instance.

		Args:
			Description (str): 
			DeviceRole (str(controller|switch)): 
			EnableVersion100 (bool): 
			EnableVersion131 (bool): 
			Enabled (bool): 
			Version (str(1.0.0)): 

		Returns:
			self: This instance with all currently retrieved device data using find and the newly added device data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the device data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CaCertificateFile=None, CertificateFile=None, Description=None, DeviceRole=None, EnableVersion100=None, EnableVersion131=None, Enabled=None, PrivateFile=None, Version=None):
		"""Finds and retrieves device data from the server.

		All named parameters support regex and can be used to selectively retrieve device data from the server.
		By default the find method takes no parameters and will retrieve all device data from the server.

		Args:
			CaCertificateFile (str): 
			CertificateFile (str): 
			Description (str): 
			DeviceRole (str(controller|switch)): 
			EnableVersion100 (bool): 
			EnableVersion131 (bool): 
			Enabled (bool): 
			PrivateFile (str): 
			Version (str(1.0.0)): 

		Returns:
			self: This instance with matching device data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of device data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the device data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddTlsCertificates(self, Arg2, Arg3, Arg4):
		"""Executes the addTlsCertificates operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=device)): The method internally sets Arg1 to the current href for this instance
			Arg2 (obj(ixnetwork_restpy.files.Files)): 
			Arg3 (obj(ixnetwork_restpy.files.Files)): 
			Arg4 (obj(ixnetwork_restpy.files.Files)): 

		Returns:
			number: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		self._check_arg_type(Arg3, Files)
		self._check_arg_type(Arg4, Files)
		return self._execute('AddTlsCertificates', payload=locals(), response_object=None)
