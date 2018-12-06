
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


class LossLearnedInfo(Base):
	"""The LossLearnedInfo class encapsulates a system managed lossLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LossLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'lossLearnedInfo'

	def __init__(self, parent):
		super(LossLearnedInfo, self).__init__(parent)

	@property
	def BVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def CVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def DestinationMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationMacAddress')

	@property
	def FarEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('farEndLoss')

	@property
	def FarEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('farEndLossRatio')

	@property
	def LmrReceived(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('lmrReceived')

	@property
	def MdLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def NearEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nearEndLoss')

	@property
	def NearEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nearEndLossRatio')

	@property
	def SVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def SourceMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceMacAddress')

	@property
	def SourceMepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceMepId')

	def find(self, BVlan=None, CVlan=None, DestinationMacAddress=None, FarEndLoss=None, FarEndLossRatio=None, LmrReceived=None, MdLevel=None, NearEndLoss=None, NearEndLossRatio=None, SVlan=None, SourceMacAddress=None, SourceMepId=None):
		"""Finds and retrieves lossLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve lossLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all lossLearnedInfo data from the server.

		Args:
			BVlan (str): 
			CVlan (str): 
			DestinationMacAddress (str): 
			FarEndLoss (number): 
			FarEndLossRatio (str): 
			LmrReceived (bool): 
			MdLevel (number): 
			NearEndLoss (number): 
			NearEndLossRatio (str): 
			SVlan (str): 
			SourceMacAddress (str): 
			SourceMepId (number): 

		Returns:
			self: This instance with matching lossLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lossLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lossLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
