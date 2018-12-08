
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


class SpbBaseVidRange(Base):
	"""The SpbBaseVidRange class encapsulates a user managed spbBaseVidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbBaseVidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbBaseVidRange'

	def __init__(self, parent):
		super(SpbBaseVidRange, self).__init__(parent)

	@property
	def SpbIsIdRange(self):
		"""An instance of the SpbIsIdRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbisidrange.SpbIsIdRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbisidrange import SpbIsIdRange
		return SpbIsIdRange(self)

	@property
	def BMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bMacAddress')
	@BMacAddress.setter
	def BMacAddress(self, value):
		self._set_attribute('bMacAddress', value)

	@property
	def BVlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bVlanPriority')
	@BVlanPriority.setter
	def BVlanPriority(self, value):
		self._set_attribute('bVlanPriority', value)

	@property
	def BVlanTpId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bVlanTpId')
	@BVlanTpId.setter
	def BVlanTpId(self, value):
		self._set_attribute('bVlanTpId', value)

	@property
	def BaseVid(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('baseVid')
	@BaseVid.setter
	def BaseVid(self, value):
		self._set_attribute('baseVid', value)

	@property
	def EctAlgorithmType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ectAlgorithmType')
	@EctAlgorithmType.setter
	def EctAlgorithmType(self, value):
		self._set_attribute('ectAlgorithmType', value)

	@property
	def EnableAutoBmacEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoBmacEnabled')
	@EnableAutoBmacEnabled.setter
	def EnableAutoBmacEnabled(self, value):
		self._set_attribute('enableAutoBmacEnabled', value)

	@property
	def EnableUseFlagBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableUseFlagBit')
	@EnableUseFlagBit.setter
	def EnableUseFlagBit(self, value):
		self._set_attribute('enableUseFlagBit', value)

	def add(self, BMacAddress=None, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithmType=None, EnableAutoBmacEnabled=None, EnableUseFlagBit=None):
		"""Adds a new spbBaseVidRange node on the server and retrieves it in this instance.

		Args:
			BMacAddress (str): 
			BVlanPriority (number): 
			BVlanTpId (number): 
			BaseVid (number): 
			EctAlgorithmType (number): 
			EnableAutoBmacEnabled (bool): 
			EnableUseFlagBit (bool): 

		Returns:
			self: This instance with all currently retrieved spbBaseVidRange data using find and the newly added spbBaseVidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbBaseVidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BMacAddress=None, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithmType=None, EnableAutoBmacEnabled=None, EnableUseFlagBit=None):
		"""Finds and retrieves spbBaseVidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbBaseVidRange data from the server.
		By default the find method takes no parameters and will retrieve all spbBaseVidRange data from the server.

		Args:
			BMacAddress (str): 
			BVlanPriority (number): 
			BVlanTpId (number): 
			BaseVid (number): 
			EctAlgorithmType (number): 
			EnableAutoBmacEnabled (bool): 
			EnableUseFlagBit (bool): 

		Returns:
			self: This instance with matching spbBaseVidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbBaseVidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbBaseVidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
