
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


class LearnedIpv4P2mpLables(Base):
	"""The LearnedIpv4P2mpLables class encapsulates a system managed learnedIpv4P2mpLables node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedIpv4P2mpLables property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedIpv4P2mpLables'

	def __init__(self, parent):
		super(LearnedIpv4P2mpLables, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4p2mplables.opaquevalueelement.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4p2mplables.opaquevalueelement.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def Label(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LabelSpaceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceId')

	@property
	def PeerIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	@property
	def RootAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')

	def find(self, Label=None, LabelSpaceId=None, PeerIpAddress=None, RootAddress=None):
		"""Finds and retrieves learnedIpv4P2mpLables data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedIpv4P2mpLables data from the server.
		By default the find method takes no parameters and will retrieve all learnedIpv4P2mpLables data from the server.

		Args:
			Label (number): 
			LabelSpaceId (number): 
			PeerIpAddress (str): 
			RootAddress (str): 

		Returns:
			self: This instance with matching learnedIpv4P2mpLables data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedIpv4P2mpLables data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedIpv4P2mpLables data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
