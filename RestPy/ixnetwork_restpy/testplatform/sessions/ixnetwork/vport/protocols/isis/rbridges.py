
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


class RBridges(Base):
	"""The RBridges class encapsulates a system managed rBridges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RBridges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rBridges'

	def __init__(self, parent):
		super(RBridges, self).__init__(parent)

	@property
	def Age(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def EnableCommonMtId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCommonMtId')

	@property
	def ExtendedCircuitId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('extendedCircuitId')

	@property
	def GraphId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('graphId')

	@property
	def HostName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def LinkMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')

	@property
	def MtId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtId')

	@property
	def PrimaryFtag(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('primaryFtag')

	@property
	def Priority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priority')

	@property
	def Role(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def SecondaryFtag(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('secondaryFtag')

	@property
	def SequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def SwitchId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchId')

	@property
	def SystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('systemId')

	def find(self, Age=None, EnableCommonMtId=None, ExtendedCircuitId=None, GraphId=None, HostName=None, LinkMetric=None, MtId=None, PrimaryFtag=None, Priority=None, Role=None, SecondaryFtag=None, SequenceNumber=None, SwitchId=None, SystemId=None):
		"""Finds and retrieves rBridges data from the server.

		All named parameters support regex and can be used to selectively retrieve rBridges data from the server.
		By default the find method takes no parameters and will retrieve all rBridges data from the server.

		Args:
			Age (number): 
			EnableCommonMtId (bool): 
			ExtendedCircuitId (number): 
			GraphId (number): 
			HostName (str): 
			LinkMetric (number): 
			MtId (number): 
			PrimaryFtag (number): 
			Priority (number): 
			Role (str): 
			SecondaryFtag (number): 
			SequenceNumber (number): 
			SwitchId (number): 
			SystemId (str): 

		Returns:
			self: This instance with matching rBridges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rBridges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rBridges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
