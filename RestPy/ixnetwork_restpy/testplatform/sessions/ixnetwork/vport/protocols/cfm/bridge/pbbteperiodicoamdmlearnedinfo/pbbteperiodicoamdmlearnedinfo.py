
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


class PbbTePeriodicOamDmLearnedInfo(Base):
	"""The PbbTePeriodicOamDmLearnedInfo class encapsulates a system managed pbbTePeriodicOamDmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTePeriodicOamDmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTePeriodicOamDmLearnedInfo'

	def __init__(self, parent):
		super(PbbTePeriodicOamDmLearnedInfo, self).__init__(parent)

	@property
	def AverageDelayNanoSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('averageDelayNanoSec')

	@property
	def AverageDelaySec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('averageDelaySec')

	@property
	def AverageDelayVariationNanoSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('averageDelayVariationNanoSec')

	@property
	def AverageDelayVariationSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('averageDelayVariationSec')

	@property
	def BVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def DmmCountSent(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmmCountSent')

	@property
	def DstMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

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
	def OneDmReceivedCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('oneDmReceivedCount')

	@property
	def RecentDelayNanoSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recentDelayNanoSec')

	@property
	def RecentDelaySec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recentDelaySec')

	@property
	def RecentDelayVariationNanoSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recentDelayVariationNanoSec')

	@property
	def RecentDelayVariationSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recentDelayVariationSec')

	@property
	def SrcMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	def find(self, AverageDelayNanoSec=None, AverageDelaySec=None, AverageDelayVariationNanoSec=None, AverageDelayVariationSec=None, BVlan=None, DmmCountSent=None, DstMacAddress=None, MdLevel=None, NoReplyCount=None, OneDmReceivedCount=None, RecentDelayNanoSec=None, RecentDelaySec=None, RecentDelayVariationNanoSec=None, RecentDelayVariationSec=None, SrcMacAddress=None):
		"""Finds and retrieves pbbTePeriodicOamDmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTePeriodicOamDmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTePeriodicOamDmLearnedInfo data from the server.

		Args:
			AverageDelayNanoSec (number): 
			AverageDelaySec (number): 
			AverageDelayVariationNanoSec (number): 
			AverageDelayVariationSec (number): 
			BVlan (str): 
			DmmCountSent (number): 
			DstMacAddress (str): 
			MdLevel (number): 
			NoReplyCount (number): 
			OneDmReceivedCount (number): 
			RecentDelayNanoSec (number): 
			RecentDelaySec (number): 
			RecentDelayVariationNanoSec (number): 
			RecentDelayVariationSec (number): 
			SrcMacAddress (str): 

		Returns:
			self: This instance with matching pbbTePeriodicOamDmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTePeriodicOamDmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTePeriodicOamDmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
