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
		"""It gives details about the action (Read-only)

		Returns:
			str
		"""
		return self._get_attribute('action')

	@property
	def ExpiresAfter(self):
		"""It gives details about the expiration (Read-only)

		Returns:
			str
		"""
		return self._get_attribute('expiresAfter')

	@property
	def InstanceId(self):
		"""It gives details about the instance id (Read-only)

		Returns:
			number
		"""
		return self._get_attribute('instanceId')

	@property
	def MapReplyRx(self):
		"""It gives details about the Map reply at the receivers end (Read-only)

		Returns:
			number
		"""
		return self._get_attribute('mapReplyRx')

	@property
	def MapRequestTx(self):
		"""It gives details about the Map request at the transmitters end (Read-only)

		Returns:
			number
		"""
		return self._get_attribute('mapRequestTx')

	@property
	def MapVersionNumber(self):
		"""It gives details about map version number(Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('mapVersionNumber')

	@property
	def NegativeMapReplyRx(self):
		"""It gives details about the Map reply at the receivers end in negation (Read-only)

		Returns:
			number
		"""
		return self._get_attribute('negativeMapReplyRx')

	@property
	def RemoteEidMappingStatus(self):
		"""It gives details about the remote Eid mapping status (Read-only)

		Returns:
			str
		"""
		return self._get_attribute('remoteEidMappingStatus')

	@property
	def RemoteEidPrefix(self):
		"""It gives details about the remote Eid Prefix (Read-only)

		Returns:
			str
		"""
		return self._get_attribute('remoteEidPrefix')

	@property
	def RemoteEidPrefixAfi(self):
		"""It gives details about the remote Eid Prefix Afi(Read-only)

		Returns:
			str
		"""
		return self._get_attribute('remoteEidPrefixAfi')

	@property
	def RemoteEidPrefixLength(self):
		"""It gives details about the remote Eid Prefix Length(Read-only)

		Returns:
			number
		"""
		return self._get_attribute('remoteEidPrefixLength')

	@property
	def ResponderIp(self):
		"""It gives details about the responder Ip (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('responderIp')

	@property
	def RlocProbeReplyRx(self):
		"""It gives details about the rloc Probe Reply at receivers end(Read-only)

		Returns:
			number
		"""
		return self._get_attribute('rlocProbeReplyRx')

	@property
	def RlocProbeRequestTx(self):
		"""It gives details about the rloc Probe Reply at transmitters end(Read-only)

		Returns:
			number
		"""
		return self._get_attribute('rlocProbeRequestTx')

	def find(self, Action=None, ExpiresAfter=None, InstanceId=None, MapReplyRx=None, MapRequestTx=None, MapVersionNumber=None, NegativeMapReplyRx=None, RemoteEidMappingStatus=None, RemoteEidPrefix=None, RemoteEidPrefixAfi=None, RemoteEidPrefixLength=None, ResponderIp=None, RlocProbeReplyRx=None, RlocProbeRequestTx=None):
		"""Finds and retrieves eidToRlocMapCacheInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve eidToRlocMapCacheInfo data from the server.
		By default the find method takes no parameters and will retrieve all eidToRlocMapCacheInfo data from the server.

		Args:
			Action (str): It gives details about the action (Read-only)
			ExpiresAfter (str): It gives details about the expiration (Read-only)
			InstanceId (number): It gives details about the instance id (Read-only)
			MapReplyRx (number): It gives details about the Map reply at the receivers end (Read-only)
			MapRequestTx (number): It gives details about the Map request at the transmitters end (Read-only)
			MapVersionNumber (number): It gives details about map version number(Read-Only)
			NegativeMapReplyRx (number): It gives details about the Map reply at the receivers end in negation (Read-only)
			RemoteEidMappingStatus (str): It gives details about the remote Eid mapping status (Read-only)
			RemoteEidPrefix (str): It gives details about the remote Eid Prefix (Read-only)
			RemoteEidPrefixAfi (str): It gives details about the remote Eid Prefix Afi(Read-only)
			RemoteEidPrefixLength (number): It gives details about the remote Eid Prefix Length(Read-only)
			ResponderIp (str): It gives details about the responder Ip (Read-Only)
			RlocProbeReplyRx (number): It gives details about the rloc Probe Reply at receivers end(Read-only)
			RlocProbeRequestTx (number): It gives details about the rloc Probe Reply at transmitters end(Read-only)

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
