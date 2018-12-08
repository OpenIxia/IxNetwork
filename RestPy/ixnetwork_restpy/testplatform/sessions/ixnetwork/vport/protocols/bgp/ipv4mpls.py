
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


class Ipv4mpls(Base):
	"""The Ipv4mpls class encapsulates a system managed ipv4mpls node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4mpls property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4mpls'

	def __init__(self, parent):
		super(Ipv4mpls, self).__init__(parent)

	@property
	def AsPath(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('asPath')

	@property
	def BlockOffset(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('blockOffset')

	@property
	def BlockSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('blockSize')

	@property
	def ControlWordEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('controlWordEnabled')

	@property
	def IpPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipPrefix')

	@property
	def LabelBase(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelBase')

	@property
	def LocalPreference(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localPreference')

	@property
	def MaxLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxLabel')

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

	@property
	def RouteDistinguisher(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def SeqDeliveryEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('seqDeliveryEnabled')

	@property
	def SiteId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('siteId')

	def find(self, AsPath=None, BlockOffset=None, BlockSize=None, ControlWordEnabled=None, IpPrefix=None, LabelBase=None, LocalPreference=None, MaxLabel=None, MultiExitDiscriminator=None, Neighbor=None, NextHop=None, OriginType=None, PrefixLength=None, RouteDistinguisher=None, SeqDeliveryEnabled=None, SiteId=None):
		"""Finds and retrieves ipv4mpls data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4mpls data from the server.
		By default the find method takes no parameters and will retrieve all ipv4mpls data from the server.

		Args:
			AsPath (str): 
			BlockOffset (number): 
			BlockSize (number): 
			ControlWordEnabled (bool): 
			IpPrefix (str): 
			LabelBase (number): 
			LocalPreference (number): 
			MaxLabel (number): 
			MultiExitDiscriminator (number): 
			Neighbor (str): 
			NextHop (str): 
			OriginType (str): 
			PrefixLength (number): 
			RouteDistinguisher (str): 
			SeqDeliveryEnabled (bool): 
			SiteId (number): 

		Returns:
			self: This instance with matching ipv4mpls data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4mpls data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4mpls data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
