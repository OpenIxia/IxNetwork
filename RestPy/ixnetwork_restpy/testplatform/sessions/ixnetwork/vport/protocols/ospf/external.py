
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


class External(Base):
	"""The External class encapsulates a system managed external node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the External property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'external'

	def __init__(self, parent):
		super(External, self).__init__(parent)

	@property
	def EBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('eBit')
	@EBit.setter
	def EBit(self, value):
		self._set_attribute('eBit', value)

	@property
	def ForwardingAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('forwardingAddress')
	@ForwardingAddress.setter
	def ForwardingAddress(self, value):
		self._set_attribute('forwardingAddress', value)

	@property
	def IncrementLinkStateIdBy(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incrementLinkStateIdBy')
	@IncrementLinkStateIdBy.setter
	def IncrementLinkStateIdBy(self, value):
		self._set_attribute('incrementLinkStateIdBy', value)

	@property
	def Metric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def NetworkMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkMask')
	@NetworkMask.setter
	def NetworkMask(self, value):
		self._set_attribute('networkMask', value)

	@property
	def NumberOfLsa(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfLsa')
	@NumberOfLsa.setter
	def NumberOfLsa(self, value):
		self._set_attribute('numberOfLsa', value)

	@property
	def RouteTag(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeTag')
	@RouteTag.setter
	def RouteTag(self, value):
		self._set_attribute('routeTag', value)

	def find(self, EBit=None, ForwardingAddress=None, IncrementLinkStateIdBy=None, Metric=None, NetworkMask=None, NumberOfLsa=None, RouteTag=None):
		"""Finds and retrieves external data from the server.

		All named parameters support regex and can be used to selectively retrieve external data from the server.
		By default the find method takes no parameters and will retrieve all external data from the server.

		Args:
			EBit (bool): 
			ForwardingAddress (str): 
			IncrementLinkStateIdBy (str): 
			Metric (number): 
			NetworkMask (str): 
			NumberOfLsa (number): 
			RouteTag (str): 

		Returns:
			self: This instance with matching external data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of external data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the external data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
