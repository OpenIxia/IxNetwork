
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


class MeterStatsBandLearnedInformation(Base):
	"""The MeterStatsBandLearnedInformation class encapsulates a system managed meterStatsBandLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterStatsBandLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meterStatsBandLearnedInformation'

	def __init__(self, parent):
		super(MeterStatsBandLearnedInformation, self).__init__(parent)

	@property
	def DataPathId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def InBandByteCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('inBandByteCount')

	@property
	def InBandPacketCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('inBandPacketCount')

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
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	def find(self, DataPathId=None, DataPathIdAsHex=None, InBandByteCount=None, InBandPacketCount=None, LocalIp=None, MeterId=None, RemoteIp=None):
		"""Finds and retrieves meterStatsBandLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve meterStatsBandLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all meterStatsBandLearnedInformation data from the server.

		Args:
			DataPathId (number): 
			DataPathIdAsHex (str): 
			InBandByteCount (number): 
			InBandPacketCount (number): 
			LocalIp (str): 
			MeterId (number): 
			RemoteIp (str): 

		Returns:
			self: This instance with matching meterStatsBandLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meterStatsBandLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meterStatsBandLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
