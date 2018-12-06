
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


class Hops(Base):
	"""The Hops class encapsulates a system managed hops node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Hops property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'hops'

	def __init__(self, parent):
		super(Hops, self).__init__(parent)

	@property
	def DownStreamAddressInfo(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downStreamAddressInfo')

	@property
	def DownStreamLabelsInfo(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downStreamLabelsInfo')

	@property
	def DownStreamMultiPathInfo(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downStreamMultiPathInfo')

	@property
	def DownStreamReturnCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downStreamReturnCode')

	@property
	def DownStreamReturnSubCode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('downStreamReturnSubCode')

	@property
	def ErrorTlvType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('errorTlvType')

	@property
	def InterfaceLabelStackTlvInterface(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceLabelStackTlvInterface')

	@property
	def InterfaceLabelStackTlvIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvIpAddress')

	@property
	def InterfaceLabelStackTlvLabels(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvLabels')

	@property
	def ReturnCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('returnCode')

	@property
	def ReturnSubcode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('returnSubcode')

	@property
	def SrcIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('srcIp')

	@property
	def Ttl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ttl')

	def find(self, DownStreamAddressInfo=None, DownStreamLabelsInfo=None, DownStreamMultiPathInfo=None, DownStreamReturnCode=None, DownStreamReturnSubCode=None, ErrorTlvType=None, InterfaceLabelStackTlvInterface=None, InterfaceLabelStackTlvIpAddress=None, InterfaceLabelStackTlvLabels=None, ReturnCode=None, ReturnSubcode=None, SrcIp=None, Ttl=None):
		"""Finds and retrieves hops data from the server.

		All named parameters support regex and can be used to selectively retrieve hops data from the server.
		By default the find method takes no parameters and will retrieve all hops data from the server.

		Args:
			DownStreamAddressInfo (str): 
			DownStreamLabelsInfo (str): 
			DownStreamMultiPathInfo (str): 
			DownStreamReturnCode (str): 
			DownStreamReturnSubCode (number): 
			ErrorTlvType (number): 
			InterfaceLabelStackTlvInterface (number): 
			InterfaceLabelStackTlvIpAddress (str): 
			InterfaceLabelStackTlvLabels (str): 
			ReturnCode (str): 
			ReturnSubcode (number): 
			SrcIp (str): 
			Ttl (number): 

		Returns:
			self: This instance with matching hops data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of hops data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the hops data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
