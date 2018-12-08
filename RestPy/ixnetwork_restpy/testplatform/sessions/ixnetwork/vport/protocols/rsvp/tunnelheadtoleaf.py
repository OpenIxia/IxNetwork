
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


class TunnelHeadToLeaf(Base):
	"""The TunnelHeadToLeaf class encapsulates a user managed tunnelHeadToLeaf node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TunnelHeadToLeaf property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'tunnelHeadToLeaf'

	def __init__(self, parent):
		super(TunnelHeadToLeaf, self).__init__(parent)

	@property
	def DutHopType(self):
		"""

		Returns:
			str(strict|loose)
		"""
		return self._get_attribute('dutHopType')
	@DutHopType.setter
	def DutHopType(self, value):
		self._set_attribute('dutHopType', value)

	@property
	def DutPrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dutPrefixLength')
	@DutPrefixLength.setter
	def DutPrefixLength(self, value):
		self._set_attribute('dutPrefixLength', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def HeadIpStart(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('headIpStart')

	@property
	def IsAppendTunnelLeaf(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isAppendTunnelLeaf')
	@IsAppendTunnelLeaf.setter
	def IsAppendTunnelLeaf(self, value):
		self._set_attribute('isAppendTunnelLeaf', value)

	@property
	def IsPrependDut(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPrependDut')
	@IsPrependDut.setter
	def IsPrependDut(self, value):
		self._set_attribute('isPrependDut', value)

	@property
	def IsSendingAsEro(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsEro')
	@IsSendingAsEro.setter
	def IsSendingAsEro(self, value):
		self._set_attribute('isSendingAsEro', value)

	@property
	def IsSendingAsSero(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsSero')
	@IsSendingAsSero.setter
	def IsSendingAsSero(self, value):
		self._set_attribute('isSendingAsSero', value)

	@property
	def SubObjectList(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('subObjectList')
	@SubObjectList.setter
	def SubObjectList(self, value):
		self._set_attribute('subObjectList', value)

	@property
	def TunnelLeafCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tunnelLeafCount')
	@TunnelLeafCount.setter
	def TunnelLeafCount(self, value):
		self._set_attribute('tunnelLeafCount', value)

	@property
	def TunnelLeafHopType(self):
		"""

		Returns:
			str(strict|loose)
		"""
		return self._get_attribute('tunnelLeafHopType')
	@TunnelLeafHopType.setter
	def TunnelLeafHopType(self, value):
		self._set_attribute('tunnelLeafHopType', value)

	@property
	def TunnelLeafIpStart(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelLeafIpStart')
	@TunnelLeafIpStart.setter
	def TunnelLeafIpStart(self, value):
		self._set_attribute('tunnelLeafIpStart', value)

	@property
	def TunnelLeafPrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tunnelLeafPrefixLength')
	@TunnelLeafPrefixLength.setter
	def TunnelLeafPrefixLength(self, value):
		self._set_attribute('tunnelLeafPrefixLength', value)

	def add(self, DutHopType=None, DutPrefixLength=None, Enabled=None, IsAppendTunnelLeaf=None, IsPrependDut=None, IsSendingAsEro=None, IsSendingAsSero=None, SubObjectList=None, TunnelLeafCount=None, TunnelLeafHopType=None, TunnelLeafIpStart=None, TunnelLeafPrefixLength=None):
		"""Adds a new tunnelHeadToLeaf node on the server and retrieves it in this instance.

		Args:
			DutHopType (str(strict|loose)): 
			DutPrefixLength (number): 
			Enabled (bool): 
			IsAppendTunnelLeaf (bool): 
			IsPrependDut (bool): 
			IsSendingAsEro (bool): 
			IsSendingAsSero (bool): 
			SubObjectList (str): 
			TunnelLeafCount (number): 
			TunnelLeafHopType (str(strict|loose)): 
			TunnelLeafIpStart (str): 
			TunnelLeafPrefixLength (number): 

		Returns:
			self: This instance with all currently retrieved tunnelHeadToLeaf data using find and the newly added tunnelHeadToLeaf data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the tunnelHeadToLeaf data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DutHopType=None, DutPrefixLength=None, Enabled=None, HeadIpStart=None, IsAppendTunnelLeaf=None, IsPrependDut=None, IsSendingAsEro=None, IsSendingAsSero=None, SubObjectList=None, TunnelLeafCount=None, TunnelLeafHopType=None, TunnelLeafIpStart=None, TunnelLeafPrefixLength=None):
		"""Finds and retrieves tunnelHeadToLeaf data from the server.

		All named parameters support regex and can be used to selectively retrieve tunnelHeadToLeaf data from the server.
		By default the find method takes no parameters and will retrieve all tunnelHeadToLeaf data from the server.

		Args:
			DutHopType (str(strict|loose)): 
			DutPrefixLength (number): 
			Enabled (bool): 
			HeadIpStart (str): 
			IsAppendTunnelLeaf (bool): 
			IsPrependDut (bool): 
			IsSendingAsEro (bool): 
			IsSendingAsSero (bool): 
			SubObjectList (str): 
			TunnelLeafCount (number): 
			TunnelLeafHopType (str(strict|loose)): 
			TunnelLeafIpStart (str): 
			TunnelLeafPrefixLength (number): 

		Returns:
			self: This instance with matching tunnelHeadToLeaf data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tunnelHeadToLeaf data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tunnelHeadToLeaf data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
