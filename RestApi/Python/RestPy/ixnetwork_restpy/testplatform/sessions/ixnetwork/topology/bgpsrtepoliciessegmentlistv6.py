from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpSRTEPoliciesSegmentListV6(Base):
	"""The BgpSRTEPoliciesSegmentListV6 class encapsulates a required bgpSRTEPoliciesSegmentListV6 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpSRTEPoliciesSegmentListV6 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpSRTEPoliciesSegmentListV6'

	def __init__(self, parent):
		super(BgpSRTEPoliciesSegmentListV6, self).__init__(parent)

	@property
	def BgpSRTEPoliciesSegmentsCollectionV6(self):
		"""An instance of the BgpSRTEPoliciesSegmentsCollectionV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepoliciessegmentscollectionv6.BgpSRTEPoliciesSegmentsCollectionV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepoliciessegmentscollectionv6 import BgpSRTEPoliciesSegmentsCollectionV6
		return BgpSRTEPoliciesSegmentsCollectionV6(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

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
	def EnWeight(self):
		"""Enable Weight Sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enWeight')

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
	def NumberOfActiveSegments(self):
		"""Count of Segment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfActiveSegments')

	@property
	def NumberOfSegmentsV6(self):
		"""Count of Segments Per Segment List

		Returns:
			number
		"""
		return self._get_attribute('numberOfSegmentsV6')
	@NumberOfSegmentsV6.setter
	def NumberOfSegmentsV6(self, value):
		self._set_attribute('numberOfSegmentsV6', value)

	@property
	def SegmentListNumber(self):
		"""Segment List Number For Reference

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('segmentListNumber')

	@property
	def SrtepolicyName(self):
		"""Policy Name For Reference

		Returns:
			list(str)
		"""
		return self._get_attribute('srtepolicyName')

	@property
	def Weight(self):
		"""Weight Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')
