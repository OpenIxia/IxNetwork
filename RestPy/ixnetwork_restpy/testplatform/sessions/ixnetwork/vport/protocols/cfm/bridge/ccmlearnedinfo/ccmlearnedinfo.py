
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


class CcmLearnedInfo(Base):
	"""The CcmLearnedInfo class encapsulates a system managed ccmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CcmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ccmLearnedInfo'

	def __init__(self, parent):
		super(CcmLearnedInfo, self).__init__(parent)

	@property
	def AllRmepDead(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('allRmepDead')

	@property
	def CVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

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
	def MepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mepId')

	@property
	def MepMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mepMacAddress')

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
	def ReceivedAis(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('receivedAis')

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
	def RemoteMepDefectCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteMepDefectCount')

	@property
	def RmepCcmDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rmepCcmDefect')

	@property
	def SVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

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
	def SomeRmepDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('someRmepDefect')

	def find(self, AllRmepDead=None, CVlan=None, CciInterval=None, ErrCcmDefect=None, ErrCcmDefectCount=None, IfaceTlvDefectCount=None, MdLevel=None, MdName=None, MdNameFormat=None, MepId=None, MepMacAddress=None, OutOfSequenceCcmCount=None, PortTlvDefectCount=None, RdiRxCount=None, RdiRxState=None, ReceivedAis=None, ReceivedIfaceTlvDefect=None, ReceivedPortTlvDefect=None, ReceivedRdi=None, RemoteMepDefectCount=None, RmepCcmDefect=None, SVlan=None, ShortMaName=None, ShortMaNameFormat=None, SomeRmepDefect=None):
		"""Finds and retrieves ccmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ccmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all ccmLearnedInfo data from the server.

		Args:
			AllRmepDead (bool): 
			CVlan (str): 
			CciInterval (str): 
			ErrCcmDefect (bool): 
			ErrCcmDefectCount (number): 
			IfaceTlvDefectCount (number): 
			MdLevel (number): 
			MdName (str): 
			MdNameFormat (number): 
			MepId (number): 
			MepMacAddress (str): 
			OutOfSequenceCcmCount (number): 
			PortTlvDefectCount (number): 
			RdiRxCount (number): 
			RdiRxState (str): 
			ReceivedAis (bool): 
			ReceivedIfaceTlvDefect (bool): 
			ReceivedPortTlvDefect (bool): 
			ReceivedRdi (bool): 
			RemoteMepDefectCount (number): 
			RmepCcmDefect (bool): 
			SVlan (str): 
			ShortMaName (str): 
			ShortMaNameFormat (number): 
			SomeRmepDefect (bool): 

		Returns:
			self: This instance with matching ccmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ccmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ccmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
