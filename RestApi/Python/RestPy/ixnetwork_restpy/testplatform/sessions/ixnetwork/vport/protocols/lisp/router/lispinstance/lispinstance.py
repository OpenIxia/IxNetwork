from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LispInstance(Base):
	"""The LispInstance class encapsulates a user managed lispInstance node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LispInstance property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'lispInstance'

	def __init__(self, parent):
		super(LispInstance, self).__init__(parent)

	@property
	def ItrRemoteEidRange(self):
		"""An instance of the ItrRemoteEidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.itrremoteeidrange.itrremoteeidrange.ItrRemoteEidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.itrremoteeidrange.itrremoteeidrange import ItrRemoteEidRange
		return ItrRemoteEidRange(self)

	@property
	def LocalEidRange(self):
		"""An instance of the LocalEidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.localeidrange.localeidrange.LocalEidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.localeidrange.localeidrange import LocalEidRange
		return LocalEidRange(self)

	@property
	def MapServerResolver(self):
		"""An instance of the MapServerResolver class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.mapserverresolver.mapserverresolver.MapServerResolver)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.mapserverresolver.mapserverresolver import MapServerResolver
		return MapServerResolver(self)

	@property
	def MsAllowedEidRange(self):
		"""An instance of the MsAllowedEidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.msallowedeidrange.msallowedeidrange.MsAllowedEidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.msallowedeidrange.msallowedeidrange import MsAllowedEidRange
		return MsAllowedEidRange(self)

	@property
	def Act(self):
		"""It gives details about the action

		Returns:
			str(noAction|nativelyForward|sendMapRequest|drop)
		"""
		return self._get_attribute('act')
	@Act.setter
	def Act(self, value):
		self._set_attribute('act', value)

	@property
	def AllowAllEids(self):
		"""It allows all the eids

		Returns:
			bool
		"""
		return self._get_attribute('allowAllEids')
	@AllowAllEids.setter
	def AllowAllEids(self, value):
		self._set_attribute('allowAllEids', value)

	@property
	def AuthenticationAlgorithm(self):
		"""It gives details about the authentication algorithm

		Returns:
			str(sha-1-96|sha-128-256)
		"""
		return self._get_attribute('authenticationAlgorithm')
	@AuthenticationAlgorithm.setter
	def AuthenticationAlgorithm(self, value):
		self._set_attribute('authenticationAlgorithm', value)

	@property
	def AuthoritativeBit(self):
		"""If true, it enables the authoritative bit

		Returns:
			bool
		"""
		return self._get_attribute('authoritativeBit')
	@AuthoritativeBit.setter
	def AuthoritativeBit(self, value):
		self._set_attribute('authoritativeBit', value)

	@property
	def AutoComposeNegativeMapReply(self):
		"""If true, it enables the auto compose negative map reply

		Returns:
			bool
		"""
		return self._get_attribute('autoComposeNegativeMapReply')
	@AutoComposeNegativeMapReply.setter
	def AutoComposeNegativeMapReply(self, value):
		self._set_attribute('autoComposeNegativeMapReply', value)

	@property
	def Enabled(self):
		"""If true, it enables the protocol

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EtrRegistrationTimeout(self):
		"""It gives the etr registration timeout

		Returns:
			number
		"""
		return self._get_attribute('etrRegistrationTimeout')
	@EtrRegistrationTimeout.setter
	def EtrRegistrationTimeout(self, value):
		self._set_attribute('etrRegistrationTimeout', value)

	@property
	def InstanceId(self):
		"""It gives the instance id

		Returns:
			str
		"""
		return self._get_attribute('instanceId')
	@InstanceId.setter
	def InstanceId(self, value):
		self._set_attribute('instanceId', value)

	@property
	def InternalMsmrSelectionMode(self):
		"""it gives the details about the internal Msmr selection mode

		Returns:
			str(allMsmrInSameIxiaPort|custom|none)
		"""
		return self._get_attribute('internalMsmrSelectionMode')
	@InternalMsmrSelectionMode.setter
	def InternalMsmrSelectionMode(self, value):
		self._set_attribute('internalMsmrSelectionMode', value)

	@property
	def Key(self):
		"""It gives details about the key

		Returns:
			str
		"""
		return self._get_attribute('key')
	@Key.setter
	def Key(self, value):
		self._set_attribute('key', value)

	@property
	def MapVersionNumber(self):
		"""It gives details about the map version number

		Returns:
			number
		"""
		return self._get_attribute('mapVersionNumber')
	@MapVersionNumber.setter
	def MapVersionNumber(self, value):
		self._set_attribute('mapVersionNumber', value)

	@property
	def Reserved(self):
		"""It gives details about the reserved protocols

		Returns:
			number
		"""
		return self._get_attribute('reserved')
	@Reserved.setter
	def Reserved(self, value):
		self._set_attribute('reserved', value)

	@property
	def Rsvd(self):
		"""It gives details about the rsvd

		Returns:
			number
		"""
		return self._get_attribute('rsvd')
	@Rsvd.setter
	def Rsvd(self, value):
		self._set_attribute('rsvd', value)

	@property
	def Ttl(self):
		"""It gives details about the ttl

		Returns:
			number
		"""
		return self._get_attribute('ttl')
	@Ttl.setter
	def Ttl(self, value):
		self._set_attribute('ttl', value)

	def add(self, Act=None, AllowAllEids=None, AuthenticationAlgorithm=None, AuthoritativeBit=None, AutoComposeNegativeMapReply=None, Enabled=None, EtrRegistrationTimeout=None, InstanceId=None, InternalMsmrSelectionMode=None, Key=None, MapVersionNumber=None, Reserved=None, Rsvd=None, Ttl=None):
		"""Adds a new lispInstance node on the server and retrieves it in this instance.

		Args:
			Act (str(noAction|nativelyForward|sendMapRequest|drop)): It gives details about the action
			AllowAllEids (bool): It allows all the eids
			AuthenticationAlgorithm (str(sha-1-96|sha-128-256)): It gives details about the authentication algorithm
			AuthoritativeBit (bool): If true, it enables the authoritative bit
			AutoComposeNegativeMapReply (bool): If true, it enables the auto compose negative map reply
			Enabled (bool): If true, it enables the protocol
			EtrRegistrationTimeout (number): It gives the etr registration timeout
			InstanceId (str): It gives the instance id
			InternalMsmrSelectionMode (str(allMsmrInSameIxiaPort|custom|none)): it gives the details about the internal Msmr selection mode
			Key (str): It gives details about the key
			MapVersionNumber (number): It gives details about the map version number
			Reserved (number): It gives details about the reserved protocols
			Rsvd (number): It gives details about the rsvd
			Ttl (number): It gives details about the ttl

		Returns:
			self: This instance with all currently retrieved lispInstance data using find and the newly added lispInstance data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the lispInstance data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Act=None, AllowAllEids=None, AuthenticationAlgorithm=None, AuthoritativeBit=None, AutoComposeNegativeMapReply=None, Enabled=None, EtrRegistrationTimeout=None, InstanceId=None, InternalMsmrSelectionMode=None, Key=None, MapVersionNumber=None, Reserved=None, Rsvd=None, Ttl=None):
		"""Finds and retrieves lispInstance data from the server.

		All named parameters support regex and can be used to selectively retrieve lispInstance data from the server.
		By default the find method takes no parameters and will retrieve all lispInstance data from the server.

		Args:
			Act (str(noAction|nativelyForward|sendMapRequest|drop)): It gives details about the action
			AllowAllEids (bool): It allows all the eids
			AuthenticationAlgorithm (str(sha-1-96|sha-128-256)): It gives details about the authentication algorithm
			AuthoritativeBit (bool): If true, it enables the authoritative bit
			AutoComposeNegativeMapReply (bool): If true, it enables the auto compose negative map reply
			Enabled (bool): If true, it enables the protocol
			EtrRegistrationTimeout (number): It gives the etr registration timeout
			InstanceId (str): It gives the instance id
			InternalMsmrSelectionMode (str(allMsmrInSameIxiaPort|custom|none)): it gives the details about the internal Msmr selection mode
			Key (str): It gives details about the key
			MapVersionNumber (number): It gives details about the map version number
			Reserved (number): It gives details about the reserved protocols
			Rsvd (number): It gives details about the rsvd
			Ttl (number): It gives details about the ttl

		Returns:
			self: This instance with matching lispInstance data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lispInstance data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lispInstance data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
