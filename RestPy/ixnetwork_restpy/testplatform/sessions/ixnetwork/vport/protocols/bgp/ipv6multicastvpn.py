
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


class Ipv6MulticastVpn(Base):
	"""The Ipv6MulticastVpn class encapsulates a system managed ipv6MulticastVpn node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv6MulticastVpn property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv6MulticastVpn'

	def __init__(self, parent):
		super(Ipv6MulticastVpn, self).__init__(parent)

	@property
	def CMcastRouteType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cMcastRouteType')

	@property
	def GroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')

	@property
	def Neighbor(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def OriginatingRouter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('originatingRouter')

	@property
	def RouteDistinguisher(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def RouteKeyGroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeKeyGroupAddress')

	@property
	def RouteKeyOriginatingRouter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeKeyOriginatingRouter')

	@property
	def RouteKeyRouteDistinguisher(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeKeyRouteDistinguisher')

	@property
	def RouteKeyRsvpP2mpExtendedTunnelId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeKeyRsvpP2mpExtendedTunnelId')

	@property
	def RouteKeyRsvpP2mpId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeKeyRsvpP2mpId')

	@property
	def RouteKeyRsvpP2mpTunnelId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeKeyRsvpP2mpTunnelId')

	@property
	def RouteKeySourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeKeySourceAddress')

	@property
	def RouteKeyTunnelType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeKeyTunnelType')

	@property
	def RouteKeyUpstreamLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeKeyUpstreamLabel')

	@property
	def RouteType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeType')

	@property
	def RsvpP2mpExtendedTunnelId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rsvpP2mpExtendedTunnelId')

	@property
	def RsvpP2mpId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rsvpP2mpId')

	@property
	def RsvpP2mpTunnelId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rsvpP2mpTunnelId')

	@property
	def SourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')

	@property
	def SourceAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceAs')

	@property
	def TunnelType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelType')

	@property
	def UpstreamLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('upstreamLabel')

	def find(self, CMcastRouteType=None, GroupAddress=None, Neighbor=None, OriginatingRouter=None, RouteDistinguisher=None, RouteKeyGroupAddress=None, RouteKeyOriginatingRouter=None, RouteKeyRouteDistinguisher=None, RouteKeyRsvpP2mpExtendedTunnelId=None, RouteKeyRsvpP2mpId=None, RouteKeyRsvpP2mpTunnelId=None, RouteKeySourceAddress=None, RouteKeyTunnelType=None, RouteKeyUpstreamLabel=None, RouteType=None, RsvpP2mpExtendedTunnelId=None, RsvpP2mpId=None, RsvpP2mpTunnelId=None, SourceAddress=None, SourceAs=None, TunnelType=None, UpstreamLabel=None):
		"""Finds and retrieves ipv6MulticastVpn data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv6MulticastVpn data from the server.
		By default the find method takes no parameters and will retrieve all ipv6MulticastVpn data from the server.

		Args:
			CMcastRouteType (str): 
			GroupAddress (str): 
			Neighbor (str): 
			OriginatingRouter (str): 
			RouteDistinguisher (str): 
			RouteKeyGroupAddress (str): 
			RouteKeyOriginatingRouter (str): 
			RouteKeyRouteDistinguisher (str): 
			RouteKeyRsvpP2mpExtendedTunnelId (str): 
			RouteKeyRsvpP2mpId (number): 
			RouteKeyRsvpP2mpTunnelId (number): 
			RouteKeySourceAddress (str): 
			RouteKeyTunnelType (str): 
			RouteKeyUpstreamLabel (number): 
			RouteType (str): 
			RsvpP2mpExtendedTunnelId (str): 
			RsvpP2mpId (number): 
			RsvpP2mpTunnelId (number): 
			SourceAddress (str): 
			SourceAs (number): 
			TunnelType (str): 
			UpstreamLabel (number): 

		Returns:
			self: This instance with matching ipv6MulticastVpn data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv6MulticastVpn data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv6MulticastVpn data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
