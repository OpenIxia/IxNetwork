
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


class EvcStatusLearnedInfo(Base):
	"""The EvcStatusLearnedInfo class encapsulates a system managed evcStatusLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EvcStatusLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'evcStatusLearnedInfo'

	def __init__(self, parent):
		super(EvcStatusLearnedInfo, self).__init__(parent)

	@property
	def CbsMagnitude(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cbsMagnitude')

	@property
	def CbsMultiplier(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cbsMultiplier')

	@property
	def Cf(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cf')

	@property
	def CirMagnitude(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cirMagnitude')

	@property
	def CirMultiplier(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cirMultiplier')

	@property
	def Cm(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cm')

	@property
	def DefaultEvc(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('defaultEvc')

	@property
	def EbsMagnitude(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ebsMagnitude')

	@property
	def EbsMultiplier(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ebsMultiplier')

	@property
	def EirMagnitude(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eirMagnitude')

	@property
	def EirMultiplier(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eirMultiplier')

	@property
	def EvcId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('evcId')

	@property
	def EvcIdLength(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('evcIdLength')

	@property
	def EvcType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('evcType')

	@property
	def PerCos(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('perCos')

	@property
	def ReferenceId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('referenceId')

	@property
	def StatusType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('statusType')

	@property
	def UntaggedPriorityTag(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('untaggedPriorityTag')

	@property
	def UserPriorityBits000(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits000')

	@property
	def UserPriorityBits001(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits001')

	@property
	def UserPriorityBits010(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits010')

	@property
	def UserPriorityBits011(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits011')

	@property
	def UserPriorityBits100(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits100')

	@property
	def UserPriorityBits101(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits101')

	@property
	def UserPriorityBits110(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits110')

	@property
	def UserPriorityBits111(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits111')

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	def find(self, CbsMagnitude=None, CbsMultiplier=None, Cf=None, CirMagnitude=None, CirMultiplier=None, Cm=None, DefaultEvc=None, EbsMagnitude=None, EbsMultiplier=None, EirMagnitude=None, EirMultiplier=None, EvcId=None, EvcIdLength=None, EvcType=None, PerCos=None, ReferenceId=None, StatusType=None, UntaggedPriorityTag=None, UserPriorityBits000=None, UserPriorityBits001=None, UserPriorityBits010=None, UserPriorityBits011=None, UserPriorityBits100=None, UserPriorityBits101=None, UserPriorityBits110=None, UserPriorityBits111=None, VlanId=None):
		"""Finds and retrieves evcStatusLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve evcStatusLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all evcStatusLearnedInfo data from the server.

		Args:
			CbsMagnitude (str): 
			CbsMultiplier (str): 
			Cf (str): 
			CirMagnitude (str): 
			CirMultiplier (str): 
			Cm (str): 
			DefaultEvc (str): 
			EbsMagnitude (str): 
			EbsMultiplier (str): 
			EirMagnitude (str): 
			EirMultiplier (str): 
			EvcId (str): 
			EvcIdLength (str): 
			EvcType (str): 
			PerCos (str): 
			ReferenceId (str): 
			StatusType (str): 
			UntaggedPriorityTag (str): 
			UserPriorityBits000 (str): 
			UserPriorityBits001 (str): 
			UserPriorityBits010 (str): 
			UserPriorityBits011 (str): 
			UserPriorityBits100 (str): 
			UserPriorityBits101 (str): 
			UserPriorityBits110 (str): 
			UserPriorityBits111 (str): 
			VlanId (str): 

		Returns:
			self: This instance with matching evcStatusLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evcStatusLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evcStatusLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
