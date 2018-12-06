
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


class PeriodicOamLmLearnedInfo(Base):
	"""The PeriodicOamLmLearnedInfo class encapsulates a system managed periodicOamLmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PeriodicOamLmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'periodicOamLmLearnedInfo'

	def __init__(self, parent):
		super(PeriodicOamLmLearnedInfo, self).__init__(parent)

	@property
	def AvgFarEndLoss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('avgFarEndLoss')

	@property
	def AvgNearEndLoss(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('avgNearEndLoss')

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
	def CcmReceivedCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmReceivedCount')

	@property
	def CcmSentCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmSentCount')

	@property
	def CurrentFarEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentFarEndLoss')

	@property
	def CurrentFarEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('currentFarEndLossRatio')

	@property
	def CurrentNearEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentNearEndLoss')

	@property
	def CurrentNearEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('currentNearEndLossRatio')

	@property
	def DestinationMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationMacAddress')

	@property
	def LmmSentCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmmSentCount')

	@property
	def MaxFarEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxFarEndLoss')

	@property
	def MaxFarEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxFarEndLossRatio')

	@property
	def MaxNearEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxNearEndLoss')

	@property
	def MaxNearEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxNearEndLossRatio')

	@property
	def MdLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def MinFarEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minFarEndLoss')

	@property
	def MinFarEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minFarEndLossRatio')

	@property
	def MinNearEndLoss(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minNearEndLoss')

	@property
	def MinNearEndLossRatio(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minNearEndLossRatio')

	@property
	def NoReplyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noReplyCount')

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

	def find(self, AvgFarEndLoss=None, AvgNearEndLoss=None, BVlan=None, CVlan=None, CcmReceivedCount=None, CcmSentCount=None, CurrentFarEndLoss=None, CurrentFarEndLossRatio=None, CurrentNearEndLoss=None, CurrentNearEndLossRatio=None, DestinationMacAddress=None, LmmSentCount=None, MaxFarEndLoss=None, MaxFarEndLossRatio=None, MaxNearEndLoss=None, MaxNearEndLossRatio=None, MdLevel=None, MinFarEndLoss=None, MinFarEndLossRatio=None, MinNearEndLoss=None, MinNearEndLossRatio=None, NoReplyCount=None, SVlan=None, SourceMacAddress=None, SourceMepId=None):
		"""Finds and retrieves periodicOamLmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve periodicOamLmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all periodicOamLmLearnedInfo data from the server.

		Args:
			AvgFarEndLoss (str): 
			AvgNearEndLoss (str): 
			BVlan (str): 
			CVlan (str): 
			CcmReceivedCount (number): 
			CcmSentCount (number): 
			CurrentFarEndLoss (number): 
			CurrentFarEndLossRatio (str): 
			CurrentNearEndLoss (number): 
			CurrentNearEndLossRatio (str): 
			DestinationMacAddress (str): 
			LmmSentCount (number): 
			MaxFarEndLoss (number): 
			MaxFarEndLossRatio (str): 
			MaxNearEndLoss (number): 
			MaxNearEndLossRatio (str): 
			MdLevel (number): 
			MinFarEndLoss (number): 
			MinFarEndLossRatio (str): 
			MinNearEndLoss (number): 
			MinNearEndLossRatio (str): 
			NoReplyCount (number): 
			SVlan (str): 
			SourceMacAddress (str): 
			SourceMepId (number): 

		Returns:
			self: This instance with matching periodicOamLmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of periodicOamLmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the periodicOamLmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
