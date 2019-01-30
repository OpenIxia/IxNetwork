
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


class Dhcpv4client(Base):
	"""The Dhcpv4client class encapsulates a required dhcpv4client node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcpv4client property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpv4client'

	def __init__(self, parent):
		super(Dhcpv4client, self).__init__(parent)

	@property
	def SessionLifetime(self):
		"""An instance of the SessionLifetime class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.sessionlifetime.sessionlifetime.SessionLifetime)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.sessionlifetime.sessionlifetime import SessionLifetime
		return SessionLifetime(self)._select()

	@property
	def StartRate(self):
		"""An instance of the StartRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.startrate.startrate.StartRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.startrate.startrate import StartRate
		return StartRate(self)._select()

	@property
	def StopRate(self):
		"""An instance of the StopRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.stoprate.stoprate.StopRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.stoprate.stoprate import StopRate
		return StopRate(self)._select()

	@property
	def TlvEditor(self):
		"""An instance of the TlvEditor class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlveditor.TlvEditor)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlveditor import TlvEditor
		return TlvEditor(self)

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
	def Dhcp4ArpGw(self):
		"""If enabled, DHCP clients ARP to find their Gateway MAC Addresses.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4ArpGw')

	@property
	def Dhcp4ClientPort(self):
		"""UDP port that the client listens on for DHCP and BOOTP responses.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4ClientPort')

	@property
	def Dhcp4MaxDiscoverTimeout(self):
		"""The max value, in seconds, that the discover timeout can reach though Discover Timeout Factor.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4MaxDiscoverTimeout')

	@property
	def Dhcp4NumRetry(self):
		"""Number of times that the client will retransmit a request for which it has not received a response. When the maximum number of retransmitions is reached, the port will increment the failure counter (DHCPSetupFail).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4NumRetry')

	@property
	def Dhcp4ResponseTimeout(self):
		"""The initial time, in seconds, that the subnet waits to receive a response from a DHCP server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4ResponseTimeout')

	@property
	def Dhcp4ResponseTimeoutFactor(self):
		"""The factor by which the timeout will be multiplied each time the response timeout has been reached.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4ResponseTimeoutFactor')

	@property
	def Dhcp4ServerPort(self):
		"""UDP port that the client addresses server requests to.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp4ServerPort')

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
	def RenewOnLinkUp(self):
		"""Indicate to renew the active DHCP sessions after link status goes down and up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('renewOnLinkUp')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def SkipReleaseOnStop(self):
		"""If enabled, the client does not send a DHCPRELEASE packet when the Stop command is given.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('skipReleaseOnStop')

	def get_device_ids(self, PortNames=None, Dhcp4ArpGw=None, Dhcp4ClientPort=None, Dhcp4MaxDiscoverTimeout=None, Dhcp4NumRetry=None, Dhcp4ResponseTimeout=None, Dhcp4ResponseTimeoutFactor=None, Dhcp4ServerPort=None, RenewOnLinkUp=None, SkipReleaseOnStop=None):
		"""Base class infrastructure that gets a list of dhcpv4client device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Dhcp4ArpGw (str): optional regex of dhcp4ArpGw
			Dhcp4ClientPort (str): optional regex of dhcp4ClientPort
			Dhcp4MaxDiscoverTimeout (str): optional regex of dhcp4MaxDiscoverTimeout
			Dhcp4NumRetry (str): optional regex of dhcp4NumRetry
			Dhcp4ResponseTimeout (str): optional regex of dhcp4ResponseTimeout
			Dhcp4ResponseTimeoutFactor (str): optional regex of dhcp4ResponseTimeoutFactor
			Dhcp4ServerPort (str): optional regex of dhcp4ServerPort
			RenewOnLinkUp (str): optional regex of renewOnLinkUp
			SkipReleaseOnStop (str): optional regex of skipReleaseOnStop

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
