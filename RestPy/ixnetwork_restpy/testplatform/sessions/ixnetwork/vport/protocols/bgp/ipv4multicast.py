
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


class Ipv4Multicast(Base):
	"""The Ipv4Multicast class encapsulates a system managed ipv4Multicast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4Multicast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4Multicast'

	def __init__(self, parent):
		super(Ipv4Multicast, self).__init__(parent)

	@property
	def AsPath(self):
		"""Indicates the local IP address of the BGP router.

		Returns:
			str
		"""
		return self._get_attribute('asPath')

	@property
	def BlockOffset(self):
		"""The label block offset (VBO) is the value used to help define this specific label block uniquely as a subset of all of the possible labels.

		Returns:
			number
		"""
		return self._get_attribute('blockOffset')

	@property
	def BlockSize(self):
		"""The size of the label block, in bytes.

		Returns:
			number
		"""
		return self._get_attribute('blockSize')

	@property
	def ControlWordEnabled(self):
		"""If true, the route label uses a control word, as part of the extended community information. (One of the control flags.)

		Returns:
			bool
		"""
		return self._get_attribute('controlWordEnabled')

	@property
	def IpPrefix(self):
		"""The route IP prefix.

		Returns:
			str
		"""
		return self._get_attribute('ipPrefix')

	@property
	def LabelBase(self):
		"""The first label to be assigned to the FEC.

		Returns:
			number
		"""
		return self._get_attribute('labelBase')

	@property
	def LocalPreference(self):
		"""Indicates the value of the local preference attribute.

		Returns:
			number
		"""
		return self._get_attribute('localPreference')

	@property
	def MaxLabel(self):
		"""The last label to use.

		Returns:
			number
		"""
		return self._get_attribute('maxLabel')

	@property
	def MultiExitDiscriminator(self):
		"""A metric field of the route file.

		Returns:
			number
		"""
		return self._get_attribute('multiExitDiscriminator')

	@property
	def Neighbor(self):
		"""The descriptive identifier for the BGP neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def NextHop(self):
		"""A 4-octet IP address which indicates the next hop.

		Returns:
			str
		"""
		return self._get_attribute('nextHop')

	@property
	def OriginType(self):
		"""An indication of where the route entry originated.

		Returns:
			str
		"""
		return self._get_attribute('originType')

	@property
	def PrefixLength(self):
		"""The length of the route IP prefix, in bytes.

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')

	@property
	def RouteDistinguisher(self):
		"""The route distinguisher for the route, for use with IPv4 and IPv6 MPLS VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def SeqDeliveryEnabled(self):
		"""Indicates if sequential delivery is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('seqDeliveryEnabled')

	@property
	def SiteId(self):
		"""The site ID.

		Returns:
			number
		"""
		return self._get_attribute('siteId')

	def find(self, AsPath=None, BlockOffset=None, BlockSize=None, ControlWordEnabled=None, IpPrefix=None, LabelBase=None, LocalPreference=None, MaxLabel=None, MultiExitDiscriminator=None, Neighbor=None, NextHop=None, OriginType=None, PrefixLength=None, RouteDistinguisher=None, SeqDeliveryEnabled=None, SiteId=None):
		"""Finds and retrieves ipv4Multicast data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4Multicast data from the server.
		By default the find method takes no parameters and will retrieve all ipv4Multicast data from the server.

		Args:
			AsPath (str): Indicates the local IP address of the BGP router.
			BlockOffset (number): The label block offset (VBO) is the value used to help define this specific label block uniquely as a subset of all of the possible labels.
			BlockSize (number): The size of the label block, in bytes.
			ControlWordEnabled (bool): If true, the route label uses a control word, as part of the extended community information. (One of the control flags.)
			IpPrefix (str): The route IP prefix.
			LabelBase (number): The first label to be assigned to the FEC.
			LocalPreference (number): Indicates the value of the local preference attribute.
			MaxLabel (number): The last label to use.
			MultiExitDiscriminator (number): A metric field of the route file.
			Neighbor (str): The descriptive identifier for the BGP neighbor.
			NextHop (str): A 4-octet IP address which indicates the next hop.
			OriginType (str): An indication of where the route entry originated.
			PrefixLength (number): The length of the route IP prefix, in bytes.
			RouteDistinguisher (str): The route distinguisher for the route, for use with IPv4 and IPv6 MPLS VPN address types.
			SeqDeliveryEnabled (bool): Indicates if sequential delivery is enabled.
			SiteId (number): The site ID.

		Returns:
			self: This instance with matching ipv4Multicast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4Multicast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4Multicast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
