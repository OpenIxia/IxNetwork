
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


class BgpLsAsPathSegmentList(Base):
	"""The BgpLsAsPathSegmentList class encapsulates a system managed bgpLsAsPathSegmentList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpLsAsPathSegmentList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'bgpLsAsPathSegmentList'

	def __init__(self, parent):
		super(BgpLsAsPathSegmentList, self).__init__(parent)

	@property
	def BgpAsNumberList(self):
		"""An instance of the BgpAsNumberList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpasnumberlist.BgpAsNumberList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpasnumberlist import BgpAsNumberList
		return BgpAsNumberList(self)

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
	def EnableASPathSegment(self):
		"""Enable AS Path Segment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableASPathSegment')

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
	def NumberOfAsNumberInSegment(self):
		"""Number of AS Number In Segment

		Returns:
			number
		"""
		return self._get_attribute('numberOfAsNumberInSegment')
	@NumberOfAsNumberInSegment.setter
	def NumberOfAsNumberInSegment(self, value):
		self._set_attribute('numberOfAsNumberInSegment', value)

	@property
	def SegmentType(self):
		"""SegmentType

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('segmentType')

	def find(self, Count=None, DescriptiveName=None, Name=None, NumberOfAsNumberInSegment=None):
		"""Finds and retrieves bgpLsAsPathSegmentList data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpLsAsPathSegmentList data from the server.
		By default the find method takes no parameters and will retrieve all bgpLsAsPathSegmentList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAsNumberInSegment (number): Number of AS Number In Segment

		Returns:
			self: This instance with matching bgpLsAsPathSegmentList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgpLsAsPathSegmentList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgpLsAsPathSegmentList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, EnableASPathSegment=None, SegmentType=None):
		"""Base class infrastructure that gets a list of bgpLsAsPathSegmentList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			EnableASPathSegment (str): optional regex of enableASPathSegment
			SegmentType (str): optional regex of segmentType

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
