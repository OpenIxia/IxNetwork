
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


class TstLearnedInfo(Base):
	"""The TstLearnedInfo class encapsulates a system managed tstLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TstLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tstLearnedInfo'

	def __init__(self, parent):
		super(TstLearnedInfo, self).__init__(parent)

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
	def MepMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mepMacAddress')

	@property
	def OutOfSequenceTstCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outOfSequenceTstCount')

	@property
	def PrbsBitErrorCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('prbsBitErrorCount')

	@property
	def RemoteMepMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteMepMacAddress')

	@property
	def RxCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rxCount')

	@property
	def SVlan(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def TxCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('txCount')

	@property
	def TxState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('txState')

	def find(self, BVlan=None, CVlan=None, MepMacAddress=None, OutOfSequenceTstCount=None, PrbsBitErrorCount=None, RemoteMepMacAddress=None, RxCount=None, SVlan=None, TxCount=None, TxState=None):
		"""Finds and retrieves tstLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve tstLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all tstLearnedInfo data from the server.

		Args:
			BVlan (str): 
			CVlan (str): 
			MepMacAddress (str): 
			OutOfSequenceTstCount (number): 
			PrbsBitErrorCount (number): 
			RemoteMepMacAddress (str): 
			RxCount (number): 
			SVlan (str): 
			TxCount (number): 
			TxState (str): 

		Returns:
			self: This instance with matching tstLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tstLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tstLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
