
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


class EidToRlocMapCacheInfo(Base):
	"""The EidToRlocMapCacheInfo class encapsulates a system managed eidToRlocMapCacheInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EidToRlocMapCacheInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'eidToRlocMapCacheInfo'

	def __init__(self, parent):
		super(EidToRlocMapCacheInfo, self).__init__(parent)

	@property
	def RemoteLocators(self):
		"""An instance of the RemoteLocators class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.eidtorlocmapcacheinfo.remotelocators.remotelocators.RemoteLocators)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.eidtorlocmapcacheinfo.remotelocators.remotelocators import RemoteLocators
		return RemoteLocators(self)

	@property
	def Action(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('action')

	@property
	def ExpiresAfter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('expiresAfter')

	@property
	def InstanceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instanceId')

	@property
	def MapReplyRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mapReplyRx')

	@property
	def MapRequestTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mapRequestTx')

	@property
	def MapVersionNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mapVersionNumber')

	@property
	def NegativeMapReplyRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('negativeMapReplyRx')

	@property
	def RemoteEidMappingStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteEidMappingStatus')

	@property
	def RemoteEidPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteEidPrefix')

	@property
	def RemoteEidPrefixAfi(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteEidPrefixAfi')

	@property
	def RemoteEidPrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteEidPrefixLength')

	@property
	def ResponderIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('responderIp')

	@property
	def RlocProbeReplyRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rlocProbeReplyRx')

	@property
	def RlocProbeRequestTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rlocProbeRequestTx')

	def find(self, Action=None, ExpiresAfter=None, InstanceId=None, MapReplyRx=None, MapRequestTx=None, MapVersionNumber=None, NegativeMapReplyRx=None, RemoteEidMappingStatus=None, RemoteEidPrefix=None, RemoteEidPrefixAfi=None, RemoteEidPrefixLength=None, ResponderIp=None, RlocProbeReplyRx=None, RlocProbeRequestTx=None):
		"""Finds and retrieves eidToRlocMapCacheInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve eidToRlocMapCacheInfo data from the server.
		By default the find method takes no parameters and will retrieve all eidToRlocMapCacheInfo data from the server.

		Args:
			Action (str): 
			ExpiresAfter (str): 
			InstanceId (number): 
			MapReplyRx (number): 
			MapRequestTx (number): 
			MapVersionNumber (number): 
			NegativeMapReplyRx (number): 
			RemoteEidMappingStatus (str): 
			RemoteEidPrefix (str): 
			RemoteEidPrefixAfi (str): 
			RemoteEidPrefixLength (number): 
			ResponderIp (str): 
			RlocProbeReplyRx (number): 
			RlocProbeRequestTx (number): 

		Returns:
			self: This instance with matching eidToRlocMapCacheInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of eidToRlocMapCacheInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the eidToRlocMapCacheInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
