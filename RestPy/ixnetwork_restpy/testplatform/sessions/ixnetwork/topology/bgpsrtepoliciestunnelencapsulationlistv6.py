
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


class BgpSRTEPoliciesTunnelEncapsulationListV6(Base):
	"""The BgpSRTEPoliciesTunnelEncapsulationListV6 class encapsulates a required bgpSRTEPoliciesTunnelEncapsulationListV6 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpSRTEPoliciesTunnelEncapsulationListV6 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpSRTEPoliciesTunnelEncapsulationListV6'

	def __init__(self, parent):
		super(BgpSRTEPoliciesTunnelEncapsulationListV6, self).__init__(parent)

	@property
	def BgpSRTEPoliciesSegmentListV6(self):
		"""An instance of the BgpSRTEPoliciesSegmentListV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepoliciessegmentlistv6.BgpSRTEPoliciesSegmentListV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepoliciessegmentlistv6 import BgpSRTEPoliciesSegmentListV6
		return BgpSRTEPoliciesSegmentListV6(self)._select()

	@property
	def IPv6SID(self):
		"""IPv6 SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('IPv6SID')

	@property
	def SID4Octet(self):
		"""4 Octet SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('SID4Octet')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AddressFamily(self):
		"""Address Family

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('addressFamily')

	@property
	def As4Number(self):
		"""AS Number (4 Octects)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('as4Number')

	@property
	def BindingSIDType(self):
		"""Binding SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bindingSIDType')

	@property
	def ColorCOBits(self):
		"""Color CO Bits

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorCOBits')

	@property
	def ColorReservedBits(self):
		"""Color Reserved Bits

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorReservedBits')

	@property
	def ColorValue(self):
		"""Color Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorValue')

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
	def EnBindingTLV(self):
		"""Enable Binding Sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enBindingTLV')

	@property
	def EnColorTLV(self):
		"""Enable Color Sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enColorTLV')

	@property
	def EnPrefTLV(self):
		"""Enable Preference Sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enPrefTLV')

	@property
	def EnRemoteEndPointTLV(self):
		"""Enable Remote Endpoint Sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enRemoteEndPointTLV')

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
	def NumberOfActiveSegmentList(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfActiveSegmentList')

	@property
	def NumberOfSegmentListV6(self):
		"""Count of Segment Lists Per Tunnel

		Returns:
			number
		"""
		return self._get_attribute('numberOfSegmentListV6')
	@NumberOfSegmentListV6.setter
	def NumberOfSegmentListV6(self, value):
		self._set_attribute('numberOfSegmentListV6', value)

	@property
	def PrefValue(self):
		"""Preference

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefValue')

	@property
	def RemoteEndpointIPv4(self):
		"""IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteEndpointIPv4')

	@property
	def RemoteEndpointIPv6(self):
		"""IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteEndpointIPv6')

	@property
	def SrtepolicyName(self):
		"""Policy Name For Reference

		Returns:
			list(str)
		"""
		return self._get_attribute('srtepolicyName')

	@property
	def TunnelType(self):
		"""Tunnel Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tunnelType')

	@property
	def UseAsMPLSLabel(self):
		"""Use BSID (SID 4 Octet) As MPLS Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useAsMPLSLabel')

	def get_device_ids(self, PortNames=None, IPv6SID=None, SID4Octet=None, Active=None, AddressFamily=None, As4Number=None, BindingSIDType=None, ColorCOBits=None, ColorReservedBits=None, ColorValue=None, EnBindingTLV=None, EnColorTLV=None, EnPrefTLV=None, EnRemoteEndPointTLV=None, NumberOfActiveSegmentList=None, PrefValue=None, RemoteEndpointIPv4=None, RemoteEndpointIPv6=None, TunnelType=None, UseAsMPLSLabel=None):
		"""Base class infrastructure that gets a list of bgpSRTEPoliciesTunnelEncapsulationListV6 device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			IPv6SID (str): optional regex of IPv6SID
			SID4Octet (str): optional regex of SID4Octet
			Active (str): optional regex of active
			AddressFamily (str): optional regex of addressFamily
			As4Number (str): optional regex of as4Number
			BindingSIDType (str): optional regex of bindingSIDType
			ColorCOBits (str): optional regex of colorCOBits
			ColorReservedBits (str): optional regex of colorReservedBits
			ColorValue (str): optional regex of colorValue
			EnBindingTLV (str): optional regex of enBindingTLV
			EnColorTLV (str): optional regex of enColorTLV
			EnPrefTLV (str): optional regex of enPrefTLV
			EnRemoteEndPointTLV (str): optional regex of enRemoteEndPointTLV
			NumberOfActiveSegmentList (str): optional regex of numberOfActiveSegmentList
			PrefValue (str): optional regex of prefValue
			RemoteEndpointIPv4 (str): optional regex of remoteEndpointIPv4
			RemoteEndpointIPv6 (str): optional regex of remoteEndpointIPv6
			TunnelType (str): optional regex of tunnelType
			UseAsMPLSLabel (str): optional regex of useAsMPLSLabel

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
