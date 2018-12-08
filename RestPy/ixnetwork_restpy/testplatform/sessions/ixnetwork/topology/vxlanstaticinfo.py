
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


class VxlanStaticInfo(Base):
	"""The VxlanStaticInfo class encapsulates a required vxlanStaticInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VxlanStaticInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'vxlanStaticInfo'

	def __init__(self, parent):
		super(VxlanStaticInfo, self).__init__(parent)

	@property
	def Active(self):
		"""Flag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def LocalVNI(self):
		"""VNI

		Returns:
			list(str)
		"""
		return self._get_attribute('localVNI')

	@property
	def MacStaticConfig(self):
		"""Statically configure the Remote Inner Mac address to Outer Vtep IP mapping, used for traffic.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('macStaticConfig')

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
	def RemoteVmStaticIpv4(self):
		"""VM IPv4 Address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteVmStaticIpv4')

	@property
	def RemoteVmStaticMac(self):
		"""Remote VM MAC address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteVmStaticMac')

	@property
	def RemoteVtepIpv4(self):
		"""Remote VTEP Unicast IPv4

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteVtepIpv4')

	@property
	def SuppressArp(self):
		"""Suppress Arp for VM IP, VM MAC pair.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('suppressArp')

	def get_device_ids(self, PortNames=None, Active=None, MacStaticConfig=None, RemoteVmStaticIpv4=None, RemoteVmStaticMac=None, RemoteVtepIpv4=None, SuppressArp=None):
		"""Base class infrastructure that gets a list of vxlanStaticInfo device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			MacStaticConfig (str): optional regex of macStaticConfig
			RemoteVmStaticIpv4 (str): optional regex of remoteVmStaticIpv4
			RemoteVmStaticMac (str): optional regex of remoteVmStaticMac
			RemoteVtepIpv4 (str): optional regex of remoteVtepIpv4
			SuppressArp (str): optional regex of suppressArp

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
