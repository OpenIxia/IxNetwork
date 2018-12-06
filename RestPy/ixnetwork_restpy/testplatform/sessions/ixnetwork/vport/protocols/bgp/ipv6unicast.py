
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


class Ipv6Unicast(Base):
	"""The Ipv6Unicast class encapsulates a system managed ipv6Unicast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv6Unicast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv6Unicast'

	def __init__(self, parent):
		super(Ipv6Unicast, self).__init__(parent)

	@property
	def AsPath(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('asPath')

	@property
	def Community(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('community')

	@property
	def IpPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipPrefix')

	@property
	def LocalPreference(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localPreference')

	@property
	def MultiExitDiscriminator(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multiExitDiscriminator')

	@property
	def Neighbor(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def NextHop(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextHop')

	@property
	def OriginType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('originType')

	@property
	def PrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')

	def find(self, AsPath=None, Community=None, IpPrefix=None, LocalPreference=None, MultiExitDiscriminator=None, Neighbor=None, NextHop=None, OriginType=None, PrefixLength=None):
		"""Finds and retrieves ipv6Unicast data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv6Unicast data from the server.
		By default the find method takes no parameters and will retrieve all ipv6Unicast data from the server.

		Args:
			AsPath (str): 
			Community (str): 
			IpPrefix (str): 
			LocalPreference (number): 
			MultiExitDiscriminator (number): 
			Neighbor (str): 
			NextHop (str): 
			OriginType (str): 
			PrefixLength (number): 

		Returns:
			self: This instance with matching ipv6Unicast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv6Unicast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv6Unicast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
