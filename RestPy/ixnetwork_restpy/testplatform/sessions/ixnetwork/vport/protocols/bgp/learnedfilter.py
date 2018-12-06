
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


class LearnedFilter(Base):
	"""The LearnedFilter class encapsulates a required learnedFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedFilter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedFilter'

	def __init__(self, parent):
		super(LearnedFilter, self).__init__(parent)

	@property
	def Capabilities(self):
		"""An instance of the Capabilities class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.capabilities.Capabilities)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.capabilities import Capabilities
		return Capabilities(self)._select()

	@property
	def Prefix(self):
		"""An instance of the Prefix class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.prefix.Prefix)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.prefix import Prefix
		return Prefix(self)._select()

	@property
	def Afi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('afi')
	@Afi.setter
	def Afi(self, value):
		self._set_attribute('afi', value)

	@property
	def EnableAfiSafi(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAfiSafi')
	@EnableAfiSafi.setter
	def EnableAfiSafi(self, value):
		self._set_attribute('enableAfiSafi', value)

	@property
	def EnablePrefix(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePrefix')
	@EnablePrefix.setter
	def EnablePrefix(self, value):
		self._set_attribute('enablePrefix', value)

	@property
	def Safi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('safi')
	@Safi.setter
	def Safi(self, value):
		self._set_attribute('safi', value)
