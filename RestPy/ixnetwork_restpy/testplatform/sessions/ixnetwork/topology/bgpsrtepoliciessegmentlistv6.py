
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

	def get_device_ids(self, PortNames=None, Active=None, EnWeight=None, NumberOfActiveSegments=None, SegmentListNumber=None, Weight=None):
		"""Base class infrastructure that gets a list of bgpSRTEPoliciesSegmentListV6 device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			EnWeight (str): optional regex of enWeight
			NumberOfActiveSegments (str): optional regex of numberOfActiveSegments
			SegmentListNumber (str): optional regex of segmentListNumber
			Weight (str): optional regex of weight

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
