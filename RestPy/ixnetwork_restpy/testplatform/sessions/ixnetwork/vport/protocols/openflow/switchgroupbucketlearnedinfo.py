
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


class SwitchGroupBucketLearnedInfo(Base):
	"""The SwitchGroupBucketLearnedInfo class encapsulates a system managed switchGroupBucketLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchGroupBucketLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchGroupBucketLearnedInfo'

	def __init__(self, parent):
		super(SwitchGroupBucketLearnedInfo, self).__init__(parent)

	@property
	def SwitchGroupActionLearnedInfo(self):
		"""An instance of the SwitchGroupActionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchgroupactionlearnedinfo.SwitchGroupActionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchgroupactionlearnedinfo import SwitchGroupActionLearnedInfo
		return SwitchGroupActionLearnedInfo(self)

	@property
	def ByteCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('byteCount')

	@property
	def PacketCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('packetCount')

	@property
	def WatchGroup(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('watchGroup')

	@property
	def WatchPort(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('watchPort')

	@property
	def Weight(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('weight')

	def find(self, ByteCount=None, PacketCount=None, WatchGroup=None, WatchPort=None, Weight=None):
		"""Finds and retrieves switchGroupBucketLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchGroupBucketLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchGroupBucketLearnedInfo data from the server.

		Args:
			ByteCount (number): NOT DEFINED
			PacketCount (number): NOT DEFINED
			WatchGroup (number): NOT DEFINED
			WatchPort (number): NOT DEFINED
			Weight (number): NOT DEFINED

		Returns:
			self: This instance with matching switchGroupBucketLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchGroupBucketLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchGroupBucketLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
