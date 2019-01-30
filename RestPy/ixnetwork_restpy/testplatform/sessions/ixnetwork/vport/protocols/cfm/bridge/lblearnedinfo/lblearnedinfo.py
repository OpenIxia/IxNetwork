
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


class LbLearnedInfo(Base):
	"""The LbLearnedInfo class encapsulates a system managed lbLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LbLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'lbLearnedInfo'

	def __init__(self, parent):
		super(LbLearnedInfo, self).__init__(parent)

	@property
	def CVlan(self):
		"""(read only) The stacked VLAN identifier for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def DstMacAddress(self):
		"""(read only) The destination MAC address for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def MdLevel(self):
		"""(read only) The MD level for the loopback message.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def Reachability(self):
		"""(read only) Indiates the status of the Ping. If true, the ping was responded to.

		Returns:
			bool
		"""
		return self._get_attribute('reachability')

	@property
	def Rtt(self):
		"""(read only) The round trip time for the loopback message.

		Returns:
			number
		"""
		return self._get_attribute('rtt')

	@property
	def SVlan(self):
		"""(read only) The single VLAN identifier for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def SrcMacAddress(self):
		"""(read only) The source MAC address for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def TransactionId(self):
		"""(read only) The transaction identifier attached to the loopback message.

		Returns:
			number
		"""
		return self._get_attribute('transactionId')

	def find(self, CVlan=None, DstMacAddress=None, MdLevel=None, Reachability=None, Rtt=None, SVlan=None, SrcMacAddress=None, TransactionId=None):
		"""Finds and retrieves lbLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve lbLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all lbLearnedInfo data from the server.

		Args:
			CVlan (str): (read only) The stacked VLAN identifier for the loopback message.
			DstMacAddress (str): (read only) The destination MAC address for the loopback message.
			MdLevel (number): (read only) The MD level for the loopback message.
			Reachability (bool): (read only) Indiates the status of the Ping. If true, the ping was responded to.
			Rtt (number): (read only) The round trip time for the loopback message.
			SVlan (str): (read only) The single VLAN identifier for the loopback message.
			SrcMacAddress (str): (read only) The source MAC address for the loopback message.
			TransactionId (number): (read only) The transaction identifier attached to the loopback message.

		Returns:
			self: This instance with matching lbLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lbLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lbLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
