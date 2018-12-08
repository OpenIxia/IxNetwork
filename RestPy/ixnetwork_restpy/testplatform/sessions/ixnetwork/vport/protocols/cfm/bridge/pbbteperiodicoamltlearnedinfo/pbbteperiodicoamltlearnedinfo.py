
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


class PbbTePeriodicOamLtLearnedInfo(Base):
	"""The PbbTePeriodicOamLtLearnedInfo class encapsulates a system managed pbbTePeriodicOamLtLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTePeriodicOamLtLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTePeriodicOamLtLearnedInfo'

	def __init__(self, parent):
		super(PbbTePeriodicOamLtLearnedInfo, self).__init__(parent)

	@property
	def LtLearnedHop(self):
		"""An instance of the LtLearnedHop class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamltlearnedinfo.ltlearnedhop.ltlearnedhop.LtLearnedHop)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamltlearnedinfo.ltlearnedhop.ltlearnedhop import LtLearnedHop
		return LtLearnedHop(self)

	@property
	def AverageHopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('averageHopCount')

	@property
	def BVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def CompleteReplyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('completeReplyCount')

	@property
	def DstMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def LtmSentCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ltmSentCount')

	@property
	def MdLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def NoReplyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noReplyCount')

	@property
	def PartialReplyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('partialReplyCount')

	@property
	def RecentHopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recentHopCount')

	@property
	def RecentHops(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('recentHops')

	@property
	def RecentReplyStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('recentReplyStatus')

	@property
	def SrcMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	def find(self, AverageHopCount=None, BVlan=None, CompleteReplyCount=None, DstMacAddress=None, LtmSentCount=None, MdLevel=None, NoReplyCount=None, PartialReplyCount=None, RecentHopCount=None, RecentHops=None, RecentReplyStatus=None, SrcMacAddress=None):
		"""Finds and retrieves pbbTePeriodicOamLtLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTePeriodicOamLtLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTePeriodicOamLtLearnedInfo data from the server.

		Args:
			AverageHopCount (number): 
			BVlan (str): 
			CompleteReplyCount (number): 
			DstMacAddress (str): 
			LtmSentCount (number): 
			MdLevel (number): 
			NoReplyCount (number): 
			PartialReplyCount (number): 
			RecentHopCount (number): 
			RecentHops (str): 
			RecentReplyStatus (str): 
			SrcMacAddress (str): 

		Returns:
			self: This instance with matching pbbTePeriodicOamLtLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTePeriodicOamLtLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTePeriodicOamLtLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
