
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


class LinkTlv(Base):
	"""The LinkTlv class encapsulates a system managed linkTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'linkTlv'

	def __init__(self, parent):
		super(LinkTlv, self).__init__(parent)

	@property
	def EnableLinkId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkId')
	@EnableLinkId.setter
	def EnableLinkId(self, value):
		self._set_attribute('enableLinkId', value)

	@property
	def EnableLinkMetric(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkMetric')
	@EnableLinkMetric.setter
	def EnableLinkMetric(self, value):
		self._set_attribute('enableLinkMetric', value)

	@property
	def EnableLinkResourceClass(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkResourceClass')
	@EnableLinkResourceClass.setter
	def EnableLinkResourceClass(self, value):
		self._set_attribute('enableLinkResourceClass', value)

	@property
	def EnableLinkType(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkType')
	@EnableLinkType.setter
	def EnableLinkType(self, value):
		self._set_attribute('enableLinkType', value)

	@property
	def EnableLocalIpAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLocalIpAddress')
	@EnableLocalIpAddress.setter
	def EnableLocalIpAddress(self, value):
		self._set_attribute('enableLocalIpAddress', value)

	@property
	def EnableMaxBandwidth(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMaxBandwidth')
	@EnableMaxBandwidth.setter
	def EnableMaxBandwidth(self, value):
		self._set_attribute('enableMaxBandwidth', value)

	@property
	def EnableMaxResBandwidth(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMaxResBandwidth')
	@EnableMaxResBandwidth.setter
	def EnableMaxResBandwidth(self, value):
		self._set_attribute('enableMaxResBandwidth', value)

	@property
	def EnableRemoteIpAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRemoteIpAddress')
	@EnableRemoteIpAddress.setter
	def EnableRemoteIpAddress(self, value):
		self._set_attribute('enableRemoteIpAddress', value)

	@property
	def EnableUnreservedBandwidth(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableUnreservedBandwidth')
	@EnableUnreservedBandwidth.setter
	def EnableUnreservedBandwidth(self, value):
		self._set_attribute('enableUnreservedBandwidth', value)

	@property
	def LinkId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('linkId')
	@LinkId.setter
	def LinkId(self, value):
		self._set_attribute('linkId', value)

	@property
	def LinkLocalIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('linkLocalIpAddress')
	@LinkLocalIpAddress.setter
	def LinkLocalIpAddress(self, value):
		self._set_attribute('linkLocalIpAddress', value)

	@property
	def LinkMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')
	@LinkMetric.setter
	def LinkMetric(self, value):
		self._set_attribute('linkMetric', value)

	@property
	def LinkRemoteIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('linkRemoteIpAddress')
	@LinkRemoteIpAddress.setter
	def LinkRemoteIpAddress(self, value):
		self._set_attribute('linkRemoteIpAddress', value)

	@property
	def LinkResourceClass(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('linkResourceClass')
	@LinkResourceClass.setter
	def LinkResourceClass(self, value):
		self._set_attribute('linkResourceClass', value)

	@property
	def LinkType(self):
		"""

		Returns:
			str(pointToPoint|multiaccess)
		"""
		return self._get_attribute('linkType')
	@LinkType.setter
	def LinkType(self, value):
		self._set_attribute('linkType', value)

	@property
	def LinkUnreservedBandwidth(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('linkUnreservedBandwidth')
	@LinkUnreservedBandwidth.setter
	def LinkUnreservedBandwidth(self, value):
		self._set_attribute('linkUnreservedBandwidth', value)

	@property
	def MaxBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxBandwidth')
	@MaxBandwidth.setter
	def MaxBandwidth(self, value):
		self._set_attribute('maxBandwidth', value)

	@property
	def MaxResBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxResBandwidth')
	@MaxResBandwidth.setter
	def MaxResBandwidth(self, value):
		self._set_attribute('maxResBandwidth', value)

	@property
	def SubTlvs(self):
		"""

		Returns:
			list(dict(arg1:str,arg2:number,arg3:number))
		"""
		return self._get_attribute('subTlvs')
	@SubTlvs.setter
	def SubTlvs(self, value):
		self._set_attribute('subTlvs', value)

	def find(self, EnableLinkId=None, EnableLinkMetric=None, EnableLinkResourceClass=None, EnableLinkType=None, EnableLocalIpAddress=None, EnableMaxBandwidth=None, EnableMaxResBandwidth=None, EnableRemoteIpAddress=None, EnableUnreservedBandwidth=None, LinkId=None, LinkLocalIpAddress=None, LinkMetric=None, LinkRemoteIpAddress=None, LinkResourceClass=None, LinkType=None, LinkUnreservedBandwidth=None, MaxBandwidth=None, MaxResBandwidth=None, SubTlvs=None):
		"""Finds and retrieves linkTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve linkTlv data from the server.
		By default the find method takes no parameters and will retrieve all linkTlv data from the server.

		Args:
			EnableLinkId (bool): 
			EnableLinkMetric (bool): 
			EnableLinkResourceClass (bool): 
			EnableLinkType (bool): 
			EnableLocalIpAddress (bool): 
			EnableMaxBandwidth (bool): 
			EnableMaxResBandwidth (bool): 
			EnableRemoteIpAddress (bool): 
			EnableUnreservedBandwidth (bool): 
			LinkId (str): 
			LinkLocalIpAddress (str): 
			LinkMetric (number): 
			LinkRemoteIpAddress (str): 
			LinkResourceClass (str): 
			LinkType (str(pointToPoint|multiaccess)): 
			LinkUnreservedBandwidth (list(number)): 
			MaxBandwidth (number): 
			MaxResBandwidth (number): 
			SubTlvs (list(dict(arg1:str,arg2:number,arg3:number))): 

		Returns:
			self: This instance with matching linkTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of linkTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the linkTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
