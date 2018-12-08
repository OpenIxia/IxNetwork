
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


class SpbRbridges(Base):
	"""The SpbRbridges class encapsulates a system managed spbRbridges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbRbridges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'spbRbridges'

	def __init__(self, parent):
		super(SpbRbridges, self).__init__(parent)

	@property
	def Age(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def AuxillaryMcidConfigName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('auxillaryMcidConfigName')

	@property
	def BaseVid(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('baseVid')

	@property
	def BridgeMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bridgeMacAddress')

	@property
	def BridgePriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bridgePriority')

	@property
	def EctAlgorithm(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ectAlgorithm')

	@property
	def HostName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def IsId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('isId')

	@property
	def LinkMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')

	@property
	def MBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('mBit')

	@property
	def McidConfigName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mcidConfigName')

	@property
	def RBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rBit')

	@property
	def SequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def SystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('systemId')

	@property
	def TBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tBit')

	@property
	def UseFlagBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useFlagBit')

	def find(self, Age=None, AuxillaryMcidConfigName=None, BaseVid=None, BridgeMacAddress=None, BridgePriority=None, EctAlgorithm=None, HostName=None, IsId=None, LinkMetric=None, MBit=None, McidConfigName=None, RBit=None, SequenceNumber=None, SystemId=None, TBit=None, UseFlagBit=None):
		"""Finds and retrieves spbRbridges data from the server.

		All named parameters support regex and can be used to selectively retrieve spbRbridges data from the server.
		By default the find method takes no parameters and will retrieve all spbRbridges data from the server.

		Args:
			Age (number): 
			AuxillaryMcidConfigName (str): 
			BaseVid (number): 
			BridgeMacAddress (str): 
			BridgePriority (number): 
			EctAlgorithm (number): 
			HostName (str): 
			IsId (number): 
			LinkMetric (number): 
			MBit (bool): 
			McidConfigName (str): 
			RBit (bool): 
			SequenceNumber (number): 
			SystemId (str): 
			TBit (bool): 
			UseFlagBit (bool): 

		Returns:
			self: This instance with matching spbRbridges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbRbridges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbRbridges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
