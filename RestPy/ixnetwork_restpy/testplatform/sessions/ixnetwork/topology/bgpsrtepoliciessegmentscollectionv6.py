
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


class BgpSRTEPoliciesSegmentsCollectionV6(Base):
	"""The BgpSRTEPoliciesSegmentsCollectionV6 class encapsulates a required bgpSRTEPoliciesSegmentsCollectionV6 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpSRTEPoliciesSegmentsCollectionV6 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpSRTEPoliciesSegmentsCollectionV6'

	def __init__(self, parent):
		super(BgpSRTEPoliciesSegmentsCollectionV6, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BottomOfStack(self):
		"""Bottom Of Stack

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bottomOfStack')

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
	def InterfaceIndex(self):
		"""Interface Index

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interfaceIndex')

	@property
	def Ipv4LocalAddress(self):
		"""IPv4 Local Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4LocalAddress')

	@property
	def Ipv4NodeAddress(self):
		"""IPv4 Node Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4NodeAddress')

	@property
	def Ipv4RemoteAddress(self):
		"""IPv4 Remote Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4RemoteAddress')

	@property
	def Ipv6LocalAddress(self):
		"""IPv6 Local Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6LocalAddress')

	@property
	def Ipv6NodeAddress(self):
		"""IPv6 Node Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6NodeAddress')

	@property
	def Ipv6RemoteAddress(self):
		"""IPv6 Remote Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6RemoteAddress')

	@property
	def Ipv6SID(self):
		"""IPv6 SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6SID')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

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
	def OptionalBottomOfStack(self):
		"""Bottom Of Stack

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('optionalBottomOfStack')

	@property
	def OptionalIpv6SID(self):
		"""IPv6 SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('optionalIpv6SID')

	@property
	def OptionalLabel(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('optionalLabel')

	@property
	def OptionalTLVType(self):
		"""Optional TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('optionalTLVType')

	@property
	def OptionalTimeToLive(self):
		"""TTL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('optionalTimeToLive')

	@property
	def OptionalTrafficClass(self):
		"""Traffic Class

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('optionalTrafficClass')

	@property
	def SegmentListNumber(self):
		"""Segment List Number For Reference

		Returns:
			list(str)
		"""
		return self._get_attribute('segmentListNumber')

	@property
	def SegmentType(self):
		"""Segment Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('segmentType')

	@property
	def SrtepolicyName(self):
		"""Policy Name For Reference

		Returns:
			list(str)
		"""
		return self._get_attribute('srtepolicyName')

	@property
	def TimeToLive(self):
		"""TTL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeToLive')

	@property
	def TrafficClass(self):
		"""Traffic Class

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('trafficClass')

	def get_device_ids(self, PortNames=None, Active=None, BottomOfStack=None, InterfaceIndex=None, Ipv4LocalAddress=None, Ipv4NodeAddress=None, Ipv4RemoteAddress=None, Ipv6LocalAddress=None, Ipv6NodeAddress=None, Ipv6RemoteAddress=None, Ipv6SID=None, Label=None, OptionalBottomOfStack=None, OptionalIpv6SID=None, OptionalLabel=None, OptionalTLVType=None, OptionalTimeToLive=None, OptionalTrafficClass=None, SegmentType=None, TimeToLive=None, TrafficClass=None):
		"""Base class infrastructure that gets a list of bgpSRTEPoliciesSegmentsCollectionV6 device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			BottomOfStack (str): optional regex of bottomOfStack
			InterfaceIndex (str): optional regex of interfaceIndex
			Ipv4LocalAddress (str): optional regex of ipv4LocalAddress
			Ipv4NodeAddress (str): optional regex of ipv4NodeAddress
			Ipv4RemoteAddress (str): optional regex of ipv4RemoteAddress
			Ipv6LocalAddress (str): optional regex of ipv6LocalAddress
			Ipv6NodeAddress (str): optional regex of ipv6NodeAddress
			Ipv6RemoteAddress (str): optional regex of ipv6RemoteAddress
			Ipv6SID (str): optional regex of ipv6SID
			Label (str): optional regex of label
			OptionalBottomOfStack (str): optional regex of optionalBottomOfStack
			OptionalIpv6SID (str): optional regex of optionalIpv6SID
			OptionalLabel (str): optional regex of optionalLabel
			OptionalTLVType (str): optional regex of optionalTLVType
			OptionalTimeToLive (str): optional regex of optionalTimeToLive
			OptionalTrafficClass (str): optional regex of optionalTrafficClass
			SegmentType (str): optional regex of segmentType
			TimeToLive (str): optional regex of timeToLive
			TrafficClass (str): optional regex of trafficClass

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
