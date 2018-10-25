
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


class EgressOnlyTracking(Base):
	"""The EgressOnlyTracking class encapsulates a user managed egressOnlyTracking node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EgressOnlyTracking property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'egressOnlyTracking'

	def __init__(self, parent):
		super(EgressOnlyTracking, self).__init__(parent)

	@property
	def Egress(self):
		"""Struct contains: egress offset and egress mask

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('egress')
	@Egress.setter
	def Egress(self, value):
		self._set_attribute('egress', value)

	@property
	def Enabled(self):
		"""Enables the egress only tracking for the given port.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Port(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)
		"""
		return self._get_attribute('port')
	@Port.setter
	def Port(self, value):
		self._set_attribute('port', value)

	@property
	def SignatureOffset(self):
		"""Offset where the signature value will be placed in the packet.

		Returns:
			number
		"""
		return self._get_attribute('signatureOffset')
	@SignatureOffset.setter
	def SignatureOffset(self, value):
		self._set_attribute('signatureOffset', value)

	@property
	def SignatureValue(self):
		"""Signature value to be placed inside the packet.

		Returns:
			str
		"""
		return self._get_attribute('signatureValue')
	@SignatureValue.setter
	def SignatureValue(self, value):
		self._set_attribute('signatureValue', value)

	def add(self, Egress=None, Enabled=None, Port=None, SignatureOffset=None, SignatureValue=None):
		"""Adds a new egressOnlyTracking node on the server and retrieves it in this instance.

		Args:
			Egress (list(dict(arg1:number,arg2:str))): Struct contains: egress offset and egress mask
			Enabled (bool): Enables the egress only tracking for the given port.
			Port (str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)): 
			SignatureOffset (number): Offset where the signature value will be placed in the packet.
			SignatureValue (str): Signature value to be placed inside the packet.

		Returns:
			self: This instance with all currently retrieved egressOnlyTracking data using find and the newly added egressOnlyTracking data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the egressOnlyTracking data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Egress=None, Enabled=None, Port=None, SignatureOffset=None, SignatureValue=None):
		"""Finds and retrieves egressOnlyTracking data from the server.

		All named parameters support regex and can be used to selectively retrieve egressOnlyTracking data from the server.
		By default the find method takes no parameters and will retrieve all egressOnlyTracking data from the server.

		Args:
			Egress (list(dict(arg1:number,arg2:str))): Struct contains: egress offset and egress mask
			Enabled (bool): Enables the egress only tracking for the given port.
			Port (str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)): 
			SignatureOffset (number): Offset where the signature value will be placed in the packet.
			SignatureValue (str): Signature value to be placed inside the packet.

		Returns:
			self: This instance with matching egressOnlyTracking data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of egressOnlyTracking data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the egressOnlyTracking data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
