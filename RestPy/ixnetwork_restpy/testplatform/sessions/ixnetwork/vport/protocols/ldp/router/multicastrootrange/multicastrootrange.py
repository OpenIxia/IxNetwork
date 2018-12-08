
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


class MulticastRootRange(Base):
	"""The MulticastRootRange class encapsulates a user managed multicastRootRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastRootRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastRootRange'

	def __init__(self, parent):
		super(MulticastRootRange, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.opaquevalueelement.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.opaquevalueelement.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def SourceTrafficRange(self):
		"""An instance of the SourceTrafficRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.sourcetrafficrange.sourcetrafficrange.SourceTrafficRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.sourcetrafficrange.sourcetrafficrange import SourceTrafficRange
		return SourceTrafficRange(self)

	@property
	def ContinuousIncrOpaqueValuesAcrossRoot(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('continuousIncrOpaqueValuesAcrossRoot')
	@ContinuousIncrOpaqueValuesAcrossRoot.setter
	def ContinuousIncrOpaqueValuesAcrossRoot(self, value):
		self._set_attribute('continuousIncrOpaqueValuesAcrossRoot', value)

	@property
	def LspCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspCount')
	@LspCount.setter
	def LspCount(self, value):
		self._set_attribute('lspCount', value)

	@property
	def LspType(self):
		"""

		Returns:
			str()
		"""
		return self._get_attribute('lspType')

	@property
	def RootAddrStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rootAddrStep')
	@RootAddrStep.setter
	def RootAddrStep(self, value):
		self._set_attribute('rootAddrStep', value)

	@property
	def RootAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')
	@RootAddress.setter
	def RootAddress(self, value):
		self._set_attribute('rootAddress', value)

	@property
	def RootAddressCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rootAddressCount')
	@RootAddressCount.setter
	def RootAddressCount(self, value):
		self._set_attribute('rootAddressCount', value)

	def add(self, ContinuousIncrOpaqueValuesAcrossRoot=None, LspCount=None, RootAddrStep=None, RootAddress=None, RootAddressCount=None):
		"""Adds a new multicastRootRange node on the server and retrieves it in this instance.

		Args:
			ContinuousIncrOpaqueValuesAcrossRoot (bool): 
			LspCount (number): 
			RootAddrStep (str): 
			RootAddress (str): 
			RootAddressCount (number): 

		Returns:
			self: This instance with all currently retrieved multicastRootRange data using find and the newly added multicastRootRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastRootRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ContinuousIncrOpaqueValuesAcrossRoot=None, LspCount=None, LspType=None, RootAddrStep=None, RootAddress=None, RootAddressCount=None):
		"""Finds and retrieves multicastRootRange data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastRootRange data from the server.
		By default the find method takes no parameters and will retrieve all multicastRootRange data from the server.

		Args:
			ContinuousIncrOpaqueValuesAcrossRoot (bool): 
			LspCount (number): 
			LspType (str()): 
			RootAddrStep (str): 
			RootAddress (str): 
			RootAddressCount (number): 

		Returns:
			self: This instance with matching multicastRootRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastRootRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastRootRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
