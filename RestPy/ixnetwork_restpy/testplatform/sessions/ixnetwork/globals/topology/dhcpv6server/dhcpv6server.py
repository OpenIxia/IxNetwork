
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


class Dhcpv6server(Base):
	"""The Dhcpv6server class encapsulates a required dhcpv6server node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcpv6server property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpv6server'

	def __init__(self, parent):
		super(Dhcpv6server, self).__init__(parent)

	@property
	def ReconfigureRate(self):
		"""An instance of the ReconfigureRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6server.reconfigurerate.reconfigurerate.ReconfigureRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6server.reconfigurerate.reconfigurerate import ReconfigureRate
		return ReconfigureRate(self)._select()

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
	def AdvertiseTimeout(self):
		"""Advertise timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseTimeout')

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
	def PingCheck(self):
		"""When enabled, the DHCP Server will not assign IP addresses that areresponding to ICMP echo requests (PING) within a certain time period.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pingCheck')

	@property
	def PingTimeout(self):
		"""The number of seconds the DHCP Server will wait for anICMP Echo response before assigning the address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pingTimeout')

	@property
	def ReconfigureMaxRc(self):
		"""RFC 3315 Reconfigure retry attempts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reconfigureMaxRc')

	@property
	def ReconfigureTimeout(self):
		"""RFC 3315 Reconfigure timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reconfigureTimeout')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	def get_device_ids(self, PortNames=None, AdvertiseTimeout=None, PingCheck=None, PingTimeout=None, ReconfigureMaxRc=None, ReconfigureTimeout=None):
		"""Base class infrastructure that gets a list of dhcpv6server device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AdvertiseTimeout (str): optional regex of advertiseTimeout
			PingCheck (str): optional regex of pingCheck
			PingTimeout (str): optional regex of pingTimeout
			ReconfigureMaxRc (str): optional regex of reconfigureMaxRc
			ReconfigureTimeout (str): optional regex of reconfigureTimeout

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
