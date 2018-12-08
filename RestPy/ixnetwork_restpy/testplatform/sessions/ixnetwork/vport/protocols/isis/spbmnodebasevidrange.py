
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


class SpbmNodeBaseVidRange(Base):
	"""The SpbmNodeBaseVidRange class encapsulates a user managed spbmNodeBaseVidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbmNodeBaseVidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbmNodeBaseVidRange'

	def __init__(self, parent):
		super(SpbmNodeBaseVidRange, self).__init__(parent)

	@property
	def SpbmNodeIsIdRange(self):
		"""An instance of the SpbmNodeIsIdRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodeisidrange.SpbmNodeIsIdRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodeisidrange import SpbmNodeIsIdRange
		return SpbmNodeIsIdRange(self)

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
	def EctAlgorithm(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ectAlgorithm')
	@EctAlgorithm.setter
	def EctAlgorithm(self, value):
		self._set_attribute('ectAlgorithm', value)

	@property
	def UseFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useFlag')
	@UseFlag.setter
	def UseFlag(self, value):
		self._set_attribute('useFlag', value)

	def add(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
		"""Adds a new spbmNodeBaseVidRange node on the server and retrieves it in this instance.

		Args:
			BVlanPriority (number): 
			BVlanTpId (number): 
			BaseVid (number): 
			EctAlgorithm (number): 
			UseFlag (bool): 

		Returns:
			self: This instance with all currently retrieved spbmNodeBaseVidRange data using find and the newly added spbmNodeBaseVidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbmNodeBaseVidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
		"""Finds and retrieves spbmNodeBaseVidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbmNodeBaseVidRange data from the server.
		By default the find method takes no parameters and will retrieve all spbmNodeBaseVidRange data from the server.

		Args:
			BVlanPriority (number): 
			BVlanTpId (number): 
			BaseVid (number): 
			EctAlgorithm (number): 
			UseFlag (bool): 

		Returns:
			self: This instance with matching spbmNodeBaseVidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbmNodeBaseVidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbmNodeBaseVidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
