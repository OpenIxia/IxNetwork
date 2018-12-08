
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


class SwitchHostRangeHopsLearnedInfo(Base):
	"""The SwitchHostRangeHopsLearnedInfo class encapsulates a system managed switchHostRangeHopsLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchHostRangeHopsLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchHostRangeHopsLearnedInfo'

	def __init__(self, parent):
		super(SwitchHostRangeHopsLearnedInfo, self).__init__(parent)

	@property
	def Action(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('action')

	@property
	def DestinationHostMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationHostMac')

	@property
	def InputPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('inputPort')

	@property
	def InputTimeInMs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('inputTimeInMs')

	@property
	def OutputPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def OutputTimeInMs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outputTimeInMs')

	@property
	def SourceHostMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceHostMac')

	@property
	def SwitchDataPathId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchDataPathId')

	@property
	def SwitchIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('switchIp')

	def find(self, Action=None, DestinationHostMac=None, InputPort=None, InputTimeInMs=None, OutputPort=None, OutputTimeInMs=None, SourceHostMac=None, SwitchDataPathId=None, SwitchIp=None):
		"""Finds and retrieves switchHostRangeHopsLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchHostRangeHopsLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchHostRangeHopsLearnedInfo data from the server.

		Args:
			Action (str): 
			DestinationHostMac (str): 
			InputPort (number): 
			InputTimeInMs (number): 
			OutputPort (number): 
			OutputTimeInMs (number): 
			SourceHostMac (str): 
			SwitchDataPathId (number): 
			SwitchIp (str): 

		Returns:
			self: This instance with matching switchHostRangeHopsLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchHostRangeHopsLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchHostRangeHopsLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
