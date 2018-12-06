
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


class TopologyLearnedInfo(Base):
	"""The TopologyLearnedInfo class encapsulates a system managed topologyLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TopologyLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'topologyLearnedInfo'

	def __init__(self, parent):
		super(TopologyLearnedInfo, self).__init__(parent)

	@property
	def InDataPathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inDataPathId')

	@property
	def InDataPathIdAshex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inDataPathIdAshex')

	@property
	def InIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inIp')

	@property
	def InPortEthernetAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inPortEthernetAddress')

	@property
	def InPortName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inPortName')

	@property
	def InPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('inPortNumber')

	@property
	def OutDataPathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outDataPathId')

	@property
	def OutDataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outDataPathIdAsHex')

	@property
	def OutIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outIp')

	@property
	def OutPortEthernetAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outPortEthernetAddress')

	@property
	def OutPortName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outPortName')

	@property
	def OutPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outPortNumber')

	def find(self, InDataPathId=None, InDataPathIdAshex=None, InIp=None, InPortEthernetAddress=None, InPortName=None, InPortNumber=None, OutDataPathId=None, OutDataPathIdAsHex=None, OutIp=None, OutPortEthernetAddress=None, OutPortName=None, OutPortNumber=None):
		"""Finds and retrieves topologyLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve topologyLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all topologyLearnedInfo data from the server.

		Args:
			InDataPathId (str): 
			InDataPathIdAshex (str): 
			InIp (str): 
			InPortEthernetAddress (str): 
			InPortName (str): 
			InPortNumber (number): 
			OutDataPathId (str): 
			OutDataPathIdAsHex (str): 
			OutIp (str): 
			OutPortEthernetAddress (str): 
			OutPortName (str): 
			OutPortNumber (number): 

		Returns:
			self: This instance with matching topologyLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of topologyLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the topologyLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
