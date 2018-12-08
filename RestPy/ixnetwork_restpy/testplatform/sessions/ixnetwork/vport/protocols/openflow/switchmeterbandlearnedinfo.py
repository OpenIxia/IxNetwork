
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


class SwitchMeterBandLearnedInfo(Base):
	"""The SwitchMeterBandLearnedInfo class encapsulates a system managed switchMeterBandLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchMeterBandLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchMeterBandLearnedInfo'

	def __init__(self, parent):
		super(SwitchMeterBandLearnedInfo, self).__init__(parent)

	@property
	def BandRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bandRate')

	@property
	def BandType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bandType')

	@property
	def BurstSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('burstSize')

	@property
	def ByteCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('byteCount')

	@property
	def DatapathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathId')

	@property
	def DatapathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathIdAsHex')

	@property
	def DropPrecedenceLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dropPrecedenceLevel')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MeterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def PacketCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetCount')

	def find(self, BandRate=None, BandType=None, BurstSize=None, ByteCount=None, DatapathId=None, DatapathIdAsHex=None, DropPrecedenceLevel=None, LocalIp=None, MeterId=None, PacketCount=None):
		"""Finds and retrieves switchMeterBandLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchMeterBandLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchMeterBandLearnedInfo data from the server.

		Args:
			BandRate (number): 
			BandType (str): 
			BurstSize (number): 
			ByteCount (number): 
			DatapathId (str): 
			DatapathIdAsHex (str): 
			DropPrecedenceLevel (number): 
			LocalIp (str): 
			MeterId (number): 
			PacketCount (number): 

		Returns:
			self: This instance with matching switchMeterBandLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchMeterBandLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchMeterBandLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
