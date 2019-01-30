
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


class Ipv6PrefixPools(Base):
	"""The Ipv6PrefixPools class encapsulates a user managed ipv6PrefixPools node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv6PrefixPools property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ipv6PrefixPools'

	def __init__(self, parent):
		super(Ipv6PrefixPools, self).__init__(parent)

	@property
	def BgpIPRouteProperty(self):
		"""An instance of the BgpIPRouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpiprouteproperty.BgpIPRouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpiprouteproperty import BgpIPRouteProperty
		return BgpIPRouteProperty(self)

	@property
	def BgpL3VpnRouteProperty(self):
		"""An instance of the BgpL3VpnRouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpl3vpnrouteproperty.BgpL3VpnRouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpl3vpnrouteproperty import BgpL3VpnRouteProperty
		return BgpL3VpnRouteProperty(self)

	@property
	def BgpMVpnReceiverSitesIpv4(self):
		"""An instance of the BgpMVpnReceiverSitesIpv4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv4.BgpMVpnReceiverSitesIpv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv4 import BgpMVpnReceiverSitesIpv4
		return BgpMVpnReceiverSitesIpv4(self)

	@property
	def BgpMVpnReceiverSitesIpv6(self):
		"""An instance of the BgpMVpnReceiverSitesIpv6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv6.BgpMVpnReceiverSitesIpv6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv6 import BgpMVpnReceiverSitesIpv6
		return BgpMVpnReceiverSitesIpv6(self)

	@property
	def BgpMVpnSenderSitesIpv4(self):
		"""An instance of the BgpMVpnSenderSitesIpv4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv4.BgpMVpnSenderSitesIpv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv4 import BgpMVpnSenderSitesIpv4
		return BgpMVpnSenderSitesIpv4(self)

	@property
	def BgpMVpnSenderSitesIpv6(self):
		"""An instance of the BgpMVpnSenderSitesIpv6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv6.BgpMVpnSenderSitesIpv6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv6 import BgpMVpnSenderSitesIpv6
		return BgpMVpnSenderSitesIpv6(self)

	@property
	def BgpV6IPRouteProperty(self):
		"""An instance of the BgpV6IPRouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6iprouteproperty.BgpV6IPRouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6iprouteproperty import BgpV6IPRouteProperty
		return BgpV6IPRouteProperty(self)

	@property
	def BgpV6L3VpnRouteProperty(self):
		"""An instance of the BgpV6L3VpnRouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6l3vpnrouteproperty.BgpV6L3VpnRouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6l3vpnrouteproperty import BgpV6L3VpnRouteProperty
		return BgpV6L3VpnRouteProperty(self)

	@property
	def CMacProperties(self):
		"""An instance of the CMacProperties class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return CMacProperties(self)

	@property
	def Connector(self):
		"""An instance of the Connector class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return Connector(self)

	@property
	def EvpnIPv4PrefixRange(self):
		"""An instance of the EvpnIPv4PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return EvpnIPv4PrefixRange(self)

	@property
	def EvpnIPv6PrefixRange(self):
		"""An instance of the EvpnIPv6PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return EvpnIPv6PrefixRange(self)

	@property
	def IsisL3RouteProperty(self):
		"""An instance of the IsisL3RouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3routeproperty.IsisL3RouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3routeproperty import IsisL3RouteProperty
		return IsisL3RouteProperty(self)

	@property
	def LdpIpv6FECProperty(self):
		"""An instance of the LdpIpv6FECProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpipv6fecproperty.LdpIpv6FECProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpipv6fecproperty import LdpIpv6FECProperty
		return LdpIpv6FECProperty(self)

	@property
	def OspfRouteProperty(self):
		"""An instance of the OspfRouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfrouteproperty.OspfRouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfrouteproperty import OspfRouteProperty
		return OspfRouteProperty(self)

	@property
	def Ospfv3RouteProperty(self):
		"""An instance of the Ospfv3RouteProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3routeproperty.Ospfv3RouteProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3routeproperty import Ospfv3RouteProperty
		return Ospfv3RouteProperty(self)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def AddrStepSupported(self):
		"""Indicates whether the Route Range provider allows address increment step of more than one

		Returns:
			bool
		"""
		return self._get_attribute('addrStepSupported')
	@AddrStepSupported.setter
	def AddrStepSupported(self, value):
		self._set_attribute('addrStepSupported', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def LastNetworkAddress(self):
		"""Last Address of host/network address pool in the simulated IPv6 host/network range

		Returns:
			list(str)
		"""
		return self._get_attribute('lastNetworkAddress')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NetworkAddress(self):
		"""First address of host/network address pool in the simulated IPv6 host/network range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkAddress')

	@property
	def NumberOfAddresses(self):
		"""Number of host/network addresses in the simulated IPv6 host/network range

		Returns:
			number
		"""
		return self._get_attribute('numberOfAddresses')
	@NumberOfAddresses.setter
	def NumberOfAddresses(self, value):
		self._set_attribute('numberOfAddresses', value)

	@property
	def PrefixAddrStep(self):
		"""The difference between each address, and its next, in the IPv6 host/network range.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixAddrStep')

	@property
	def PrefixLength(self):
		"""The length (in bits) of the mask to be used in conjunction with all the addresses created in the range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	def add(self, AddrStepSupported=None, Name=None, NumberOfAddresses=None):
		"""Adds a new ipv6PrefixPools node on the server and retrieves it in this instance.

		Args:
			AddrStepSupported (bool): Indicates whether the Route Range provider allows address increment step of more than one
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAddresses (number): Number of host/network addresses in the simulated IPv6 host/network range

		Returns:
			self: This instance with all currently retrieved ipv6PrefixPools data using find and the newly added ipv6PrefixPools data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ipv6PrefixPools data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddrStepSupported=None, Count=None, DescriptiveName=None, LastNetworkAddress=None, Name=None, NumberOfAddresses=None):
		"""Finds and retrieves ipv6PrefixPools data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv6PrefixPools data from the server.
		By default the find method takes no parameters and will retrieve all ipv6PrefixPools data from the server.

		Args:
			AddrStepSupported (bool): Indicates whether the Route Range provider allows address increment step of more than one
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			LastNetworkAddress (list(str)): Last Address of host/network address pool in the simulated IPv6 host/network range
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAddresses (number): Number of host/network addresses in the simulated IPv6 host/network range

		Returns:
			self: This instance with matching ipv6PrefixPools data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv6PrefixPools data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv6PrefixPools data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, NetworkAddress=None, PrefixAddrStep=None, PrefixLength=None):
		"""Base class infrastructure that gets a list of ipv6PrefixPools device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			NetworkAddress (str): optional regex of networkAddress
			PrefixAddrStep (str): optional regex of prefixAddrStep
			PrefixLength (str): optional regex of prefixLength

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
