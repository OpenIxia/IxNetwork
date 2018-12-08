
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


class PppoxServerSessions(Base):
	"""The PppoxServerSessions class encapsulates a required pppoxServerSessions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PppoxServerSessions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pppoxServerSessions'

	def __init__(self, parent):
		super(PppoxServerSessions, self).__init__(parent)

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
	def ChapName(self):
		"""User name when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapName')

	@property
	def ChapSecret(self):
		"""Secret when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapSecret')

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
	def DiscoveredClientsMacs(self):
		"""The discovered remote MAC address.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredClientsMacs')

	@property
	def DiscoveredRemoteSessionIds(self):
		"""The negotiated session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteSessionIds')

	@property
	def DiscoveredRemoteTunnelIds(self):
		"""The negotiated tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteTunnelIds')

	@property
	def DiscoveredSessionIds(self):
		"""The negotiated session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredSessionIds')

	@property
	def DiscoveredTunnelIPs(self):
		"""The discovered remote tunnel IP.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredTunnelIPs')

	@property
	def DiscoveredTunnelIds(self):
		"""The negotiated tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredTunnelIds')

	@property
	def DomainList(self):
		"""Configure domain group settings

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domainList')

	@property
	def EnableDomainGroups(self):
		"""Enable domain groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDomainGroups')

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
	def PapPassword(self):
		"""Password when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papPassword')

	@property
	def PapUser(self):
		"""User name when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papUser')

	@property
	def ServerIpv4Addresses(self):
		"""IPv4 Server Address. Each PPPoX Server Session will display the v4 address from the PPPoX Server it belongs to.

		Returns:
			list(str)
		"""
		return self._get_attribute('serverIpv4Addresses')

	@property
	def ServerIpv6Addresses(self):
		"""IPv6 Server Address. Each PPPoX Server Session will display the v6 address from the PPPoX Server it belongs to.

		Returns:
			list(str)
		"""
		return self._get_attribute('serverIpv6Addresses')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[cLS_CFG_REJ_AUTH|cLS_CHAP_PEER_DET_FAIL|cLS_CHAP_PEER_RESP_BAD|cLS_CODE_REJ_IPCP|cLS_CODE_REJ_IPV6CP|cLS_CODE_REJ_LCP|cLS_ERR_PPP_NO_BUF|cLS_ERR_PPP_SEND_PKT|cLS_LINK_DISABLE|cLS_LOC_IPADDR_BROADCAST|cLS_LOC_IPADDR_CLASS_E|cLS_LOC_IPADDR_INVAL_ACKS_0|cLS_LOC_IPADDR_INVAL_ACKS_DIFF|cLS_LOC_IPADDR_LOOPBACK|cLS_LOC_IPADDR_PEER_MATCH_LOC|cLS_LOC_IPADDR_PEER_NO_GIVE|cLS_LOC_IPADDR_PEER_NO_HELP|cLS_LOC_IPADDR_PEER_NO_TAKE|cLS_LOC_IPADDR_PEER_REJ|cLS_LOOPBACK_DETECT|cLS_NO_NCP|cLS_NONE|cLS_PAP_BAD_PASSWD|cLS_PEER_DISCONNECTED|cLS_PEER_IPADDR_MATCH_LOC|cLS_PEER_IPADDR_PEER_NO_SET|cLS_PPOE_AC_SYSTEM_ERROR|cLS_PPOE_GENERIC_ERROR|cLS_PPP_DISABLE|cLS_PPPOE_PADI_TIMEOUT|cLS_PPPOE_PADO_TIMEOUT|cLS_PPPOE_PADR_TIMEOUT|cLS_PROTO_REJ_IPCP|cLS_PROTO_REJ_IPv6CP|cLS_TIMEOUT_CHAP_CHAL|cLS_TIMEOUT_CHAP_RESP|cLS_TIMEOUT_IPCP_CFG_REQ|cLS_TIMEOUT_IPV6CP_CFG_REQ|cLS_TIMEOUT_IPV6CP_RA|cLS_TIMEOUT_LCP_CFG_REQ|cLS_TIMEOUT_LCP_ECHO_REQ|cLS_TIMEOUT_PAP_AUTH_REQ])
		"""
		return self._get_attribute('sessionInfo')

	def get_device_ids(self, PortNames=None, ChapName=None, ChapSecret=None, DomainList=None, EnableDomainGroups=None, PapPassword=None, PapUser=None):
		"""Base class infrastructure that gets a list of pppoxServerSessions device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ChapName (str): optional regex of chapName
			ChapSecret (str): optional regex of chapSecret
			DomainList (str): optional regex of domainList
			EnableDomainGroups (str): optional regex of enableDomainGroups
			PapPassword (str): optional regex of papPassword
			PapUser (str): optional regex of papUser

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def CloseIpcp(self):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX Server Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('CloseIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX Server Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('CloseIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX Server Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('CloseIpcp', payload=locals(), response_object=None)

	def CloseIpv6cp(self):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX Severs Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('CloseIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX Severs Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('CloseIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX Severs Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('CloseIpv6cp', payload=locals(), response_object=None)
