
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


class PbbTeCcmLearnedInfo(Base):
	"""The PbbTeCcmLearnedInfo class encapsulates a system managed pbbTeCcmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTeCcmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTeCcmLearnedInfo'

	def __init__(self, parent):
		super(PbbTeCcmLearnedInfo, self).__init__(parent)

	@property
	def BVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def CciInterval(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cciInterval')

	@property
	def ErrCcmDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('errCcmDefect')

	@property
	def ErrCcmDefectCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('errCcmDefectCount')

	@property
	def IfaceTlvDefectCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ifaceTlvDefectCount')

	@property
	def MdLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def MdName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mdName')

	@property
	def MdNameFormat(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mdNameFormat')

	@property
	def OutOfSequenceCcmCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outOfSequenceCcmCount')

	@property
	def PortTlvDefectCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portTlvDefectCount')

	@property
	def RdiRxCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rdiRxCount')

	@property
	def RdiRxState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rdiRxState')

	@property
	def RdiTxCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rdiTxCount')

	@property
	def RdiTxState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rdiTxState')

	@property
	def ReceivedIfaceTlvDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('receivedIfaceTlvDefect')

	@property
	def ReceivedPortTlvDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('receivedPortTlvDefect')

	@property
	def ReceivedRdi(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('receivedRdi')

	@property
	def RemoteMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteMacAddress')

	@property
	def RemoteMepDefectCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteMepDefectCount')

	@property
	def RemoteMepId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteMepId')

	@property
	def RmepCcmDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rmepCcmDefect')

	@property
	def ShortMaName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('shortMaName')

	@property
	def ShortMaNameFormat(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('shortMaNameFormat')

	@property
	def SrcMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def SrcMepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcMepId')

	def find(self, BVlan=None, CciInterval=None, ErrCcmDefect=None, ErrCcmDefectCount=None, IfaceTlvDefectCount=None, MdLevel=None, MdName=None, MdNameFormat=None, OutOfSequenceCcmCount=None, PortTlvDefectCount=None, RdiRxCount=None, RdiRxState=None, RdiTxCount=None, RdiTxState=None, ReceivedIfaceTlvDefect=None, ReceivedPortTlvDefect=None, ReceivedRdi=None, RemoteMacAddress=None, RemoteMepDefectCount=None, RemoteMepId=None, RmepCcmDefect=None, ShortMaName=None, ShortMaNameFormat=None, SrcMacAddress=None, SrcMepId=None):
		"""Finds and retrieves pbbTeCcmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTeCcmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTeCcmLearnedInfo data from the server.

		Args:
			BVlan (str): 
			CciInterval (str): 
			ErrCcmDefect (bool): 
			ErrCcmDefectCount (number): 
			IfaceTlvDefectCount (number): 
			MdLevel (number): 
			MdName (str): 
			MdNameFormat (number): 
			OutOfSequenceCcmCount (number): 
			PortTlvDefectCount (number): 
			RdiRxCount (number): 
			RdiRxState (str): 
			RdiTxCount (number): 
			RdiTxState (str): 
			ReceivedIfaceTlvDefect (bool): 
			ReceivedPortTlvDefect (bool): 
			ReceivedRdi (bool): 
			RemoteMacAddress (str): 
			RemoteMepDefectCount (number): 
			RemoteMepId (str): 
			RmepCcmDefect (bool): 
			ShortMaName (str): 
			ShortMaNameFormat (number): 
			SrcMacAddress (str): 
			SrcMepId (number): 

		Returns:
			self: This instance with matching pbbTeCcmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTeCcmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTeCcmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
