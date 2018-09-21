from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DiscoveredLearnedInfo(Base):
	"""The DiscoveredLearnedInfo class encapsulates a system managed discoveredLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DiscoveredLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'discoveredLearnedInfo'

	def __init__(self, parent):
		super(DiscoveredLearnedInfo, self).__init__(parent)

	@property
	def LocalDiscoveryStatus(self):
		"""

		Returns:
			str(fault|activeSendLocal|passiveWait|sendLocalRemote|sendLocalRemoteOk|sendAny)
		"""
		return self._get_attribute('localDiscoveryStatus')

	@property
	def LocalEvaluating(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('localEvaluating')

	@property
	def LocalMuxAction(self):
		"""

		Returns:
			str(fwd|discard)
		"""
		return self._get_attribute('localMuxAction')

	@property
	def LocalParserAction(self):
		"""

		Returns:
			str(fwd|lb|discard)
		"""
		return self._get_attribute('localParserAction')

	@property
	def LocalRevision(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localRevision')

	@property
	def LocalStable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('localStable')

	@property
	def RemoteCriticalEvent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteCriticalEvent')

	@property
	def RemoteDyingGasp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteDyingGasp')

	@property
	def RemoteEvaluating(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteEvaluating')

	@property
	def RemoteHeaderRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteHeaderRefreshed')

	@property
	def RemoteLinkEvent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteLinkEvent')

	@property
	def RemoteLinkFault(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteLinkFault')

	@property
	def RemoteLoopbackSupport(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteLoopbackSupport')

	@property
	def RemoteMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteMacAddress')

	@property
	def RemoteMaxPduSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteMaxPduSize')

	@property
	def RemoteMode(self):
		"""

		Returns:
			str(active|passive)
		"""
		return self._get_attribute('remoteMode')

	@property
	def RemoteMuxAction(self):
		"""

		Returns:
			str(fwd|discard)
		"""
		return self._get_attribute('remoteMuxAction')

	@property
	def RemoteOamVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteOamVersion')

	@property
	def RemoteOui(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteOui')

	@property
	def RemoteParserAction(self):
		"""

		Returns:
			str(fwd|lb|discard)
		"""
		return self._get_attribute('remoteParserAction')

	@property
	def RemoteRevision(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteRevision')

	@property
	def RemoteStable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteStable')

	@property
	def RemoteTlvRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteTlvRefreshed')

	@property
	def RemoteUnidirectionalSupport(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteUnidirectionalSupport')

	@property
	def RemoteVariableRetrieval(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('remoteVariableRetrieval')

	@property
	def RemoteVendorSpecificInfo(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteVendorSpecificInfo')

	def find(self, LocalDiscoveryStatus=None, LocalEvaluating=None, LocalMuxAction=None, LocalParserAction=None, LocalRevision=None, LocalStable=None, RemoteCriticalEvent=None, RemoteDyingGasp=None, RemoteEvaluating=None, RemoteHeaderRefreshed=None, RemoteLinkEvent=None, RemoteLinkFault=None, RemoteLoopbackSupport=None, RemoteMacAddress=None, RemoteMaxPduSize=None, RemoteMode=None, RemoteMuxAction=None, RemoteOamVersion=None, RemoteOui=None, RemoteParserAction=None, RemoteRevision=None, RemoteStable=None, RemoteTlvRefreshed=None, RemoteUnidirectionalSupport=None, RemoteVariableRetrieval=None, RemoteVendorSpecificInfo=None):
		"""Finds and retrieves discoveredLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve discoveredLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all discoveredLearnedInfo data from the server.

		Args:
			LocalDiscoveryStatus (str(fault|activeSendLocal|passiveWait|sendLocalRemote|sendLocalRemoteOk|sendAny)): 
			LocalEvaluating (bool): 
			LocalMuxAction (str(fwd|discard)): 
			LocalParserAction (str(fwd|lb|discard)): 
			LocalRevision (number): 
			LocalStable (bool): 
			RemoteCriticalEvent (bool): 
			RemoteDyingGasp (bool): 
			RemoteEvaluating (bool): 
			RemoteHeaderRefreshed (bool): 
			RemoteLinkEvent (bool): 
			RemoteLinkFault (bool): 
			RemoteLoopbackSupport (bool): 
			RemoteMacAddress (str): 
			RemoteMaxPduSize (number): 
			RemoteMode (str(active|passive)): 
			RemoteMuxAction (str(fwd|discard)): 
			RemoteOamVersion (number): 
			RemoteOui (str): 
			RemoteParserAction (str(fwd|lb|discard)): 
			RemoteRevision (number): 
			RemoteStable (bool): 
			RemoteTlvRefreshed (bool): 
			RemoteUnidirectionalSupport (bool): 
			RemoteVariableRetrieval (bool): 
			RemoteVendorSpecificInfo (str): 

		Returns:
			self: This instance with matching discoveredLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of discoveredLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the discoveredLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
