
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


class IxVmPort(Base):
	"""The IxVmPort class encapsulates a user managed ixVmPort node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IxVmPort property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ixVmPort'

	def __init__(self, parent):
		super(IxVmPort, self).__init__(parent)

	@property
	def Interface(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interface')
	@Interface.setter
	def Interface(self, value):
		self._set_attribute('interface', value)

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
	def MacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def Mtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def Owner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('owner')

	@property
	def PortId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('portId')
	@PortId.setter
	def PortId(self, value):
		self._set_attribute('portId', value)

	@property
	def PortName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('portName')
	@PortName.setter
	def PortName(self, value):
		self._set_attribute('portName', value)

	@property
	def PortState(self):
		"""

		Returns:
			str(invalidNIC|ixVmPortUnitialized|portLicenseNotFound|portNotAdded|portOK|portRemoved|portUnconnectedCard|portUnknownError)
		"""
		return self._get_attribute('portState')

	@property
	def PromiscMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('promiscMode')
	@PromiscMode.setter
	def PromiscMode(self, value):
		self._set_attribute('promiscMode', value)

	def add(self, Interface=None, IpAddress=None, MacAddress=None, Mtu=None, PortId=None, PortName=None, PromiscMode=None):
		"""Adds a new ixVmPort node on the server and retrieves it in this instance.

		Args:
			Interface (str): 
			IpAddress (str): 
			MacAddress (str): 
			Mtu (number): 
			PortId (str): 
			PortName (str): 
			PromiscMode (bool): 

		Returns:
			self: This instance with all currently retrieved ixVmPort data using find and the newly added ixVmPort data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ixVmPort data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Interface=None, IpAddress=None, MacAddress=None, Mtu=None, Owner=None, PortId=None, PortName=None, PortState=None, PromiscMode=None):
		"""Finds and retrieves ixVmPort data from the server.

		All named parameters support regex and can be used to selectively retrieve ixVmPort data from the server.
		By default the find method takes no parameters and will retrieve all ixVmPort data from the server.

		Args:
			Interface (str): 
			IpAddress (str): 
			MacAddress (str): 
			Mtu (number): 
			Owner (str): 
			PortId (str): 
			PortName (str): 
			PortState (str(invalidNIC|ixVmPortUnitialized|portLicenseNotFound|portNotAdded|portOK|portRemoved|portUnconnectedCard|portUnknownError)): 
			PromiscMode (bool): 

		Returns:
			self: This instance with matching ixVmPort data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ixVmPort data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ixVmPort data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
