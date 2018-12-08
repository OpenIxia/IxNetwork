
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


class SwitchHostRangeLearnedInfo(Base):
	"""The SwitchHostRangeLearnedInfo class encapsulates a system managed switchHostRangeLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchHostRangeLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchHostRangeLearnedInfo'

	def __init__(self, parent):
		super(SwitchHostRangeLearnedInfo, self).__init__(parent)

	@property
	def SwitchHostRangeHopsLearnedInfo(self):
		"""An instance of the SwitchHostRangeHopsLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangehopslearnedinfo.SwitchHostRangeHopsLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangehopslearnedinfo import SwitchHostRangeHopsLearnedInfo
		return SwitchHostRangeHopsLearnedInfo(self)

	@property
	def DestinationHostIpv4Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationHostIpv4Address')

	@property
	def DestinationHostMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationHostMac')

	@property
	def PacketType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('packetType')

	@property
	def Path(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('path')

	@property
	def SourceHostIpv4Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceHostIpv4Address')

	@property
	def SourceHostMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceHostMac')

	@property
	def Status(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('status')

	def find(self, DestinationHostIpv4Address=None, DestinationHostMac=None, PacketType=None, Path=None, SourceHostIpv4Address=None, SourceHostMac=None, Status=None):
		"""Finds and retrieves switchHostRangeLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchHostRangeLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchHostRangeLearnedInfo data from the server.

		Args:
			DestinationHostIpv4Address (str): 
			DestinationHostMac (str): 
			PacketType (str): 
			Path (str): 
			SourceHostIpv4Address (str): 
			SourceHostMac (str): 
			Status (str): 

		Returns:
			self: This instance with matching switchHostRangeLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchHostRangeLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchHostRangeLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
