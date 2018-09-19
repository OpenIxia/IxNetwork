from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpSRTEPoliciesTunnelEncapsulationListV4(Base):
	"""The BgpSRTEPoliciesTunnelEncapsulationListV4 class encapsulates a required bgpSRTEPoliciesTunnelEncapsulationListV4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpSRTEPoliciesTunnelEncapsulationListV4 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpSRTEPoliciesTunnelEncapsulationListV4'

	def __init__(self, parent):
		super(BgpSRTEPoliciesTunnelEncapsulationListV4, self).__init__(parent)

	@property
	def BgpSRTEPoliciesSegmentListV4(self):
		"""An instance of the BgpSRTEPoliciesSegmentListV4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepoliciessegmentlistv4.BgpSRTEPoliciesSegmentListV4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepoliciessegmentlistv4 import BgpSRTEPoliciesSegmentListV4
		return BgpSRTEPoliciesSegmentListV4(self)._select()

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
	def NumberOfSegmentListV4(self):
		"""Count of Segment Lists Per Tunnel

		Returns:
			number
		"""
		return self._get_attribute('numberOfSegmentListV4')
	@NumberOfSegmentListV4.setter
	def NumberOfSegmentListV4(self, value):
		self._set_attribute('numberOfSegmentListV4', value)

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
