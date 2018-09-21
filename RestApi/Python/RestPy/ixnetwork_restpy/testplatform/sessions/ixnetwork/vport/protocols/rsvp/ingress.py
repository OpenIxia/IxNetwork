from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ingress(Base):
	"""The Ingress class encapsulates a required ingress node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ingress property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ingress'

	def __init__(self, parent):
		super(Ingress, self).__init__(parent)

	@property
	def SenderRange(self):
		"""An instance of the SenderRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.senderrange.SenderRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.senderrange import SenderRange
		return SenderRange(self)

	@property
	def EnableEro(self):
		"""Enables use of the ERO option in Ingress mode.

		Returns:
			bool
		"""
		return self._get_attribute('enableEro')
	@EnableEro.setter
	def EnableEro(self, value):
		self._set_attribute('enableEro', value)

	@property
	def Ero(self):
		"""Enables use of the ERO option in Ingress mode.

		Returns:
			list(dict(arg1:str[ip|as],arg2:str,arg3:number,arg4:bool))
		"""
		return self._get_attribute('ero')
	@Ero.setter
	def Ero(self, value):
		self._set_attribute('ero', value)

	@property
	def PrefixLength(self):
		"""If the DUT's address is to be prepended to the ERO list, this indicates what prefix length is to be used for the entry.

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')
	@PrefixLength.setter
	def PrefixLength(self, value):
		self._set_attribute('prefixLength', value)

	@property
	def PrependDutToEro(self):
		"""Enables the user to insert the DUT address at the beginning of the list of hops in the path.

		Returns:
			str(none|prependLoose|prependStrict)
		"""
		return self._get_attribute('prependDutToEro')
	@PrependDutToEro.setter
	def PrependDutToEro(self, value):
		self._set_attribute('prependDutToEro', value)

	@property
	def ReservationErrorTlv(self):
		"""a set of custom TLVs to be included in RESV ERR messages. These may only be used for ingress routers.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('reservationErrorTlv')
	@ReservationErrorTlv.setter
	def ReservationErrorTlv(self, value):
		self._set_attribute('reservationErrorTlv', value)

	@property
	def Rro(self):
		"""If enabled, an RRO is reflected back to the originating router.

		Returns:
			list(dict(arg1:str[ip|label],arg2:str,arg3:bool,arg4:bool,arg5:number,arg6:bool,arg7:bool,arg8:bool))
		"""
		return self._get_attribute('rro')
	@Rro.setter
	def Rro(self, value):
		self._set_attribute('rro', value)

	@property
	def SendRro(self):
		"""When the destination range is used in Ingress mode, this indicates that a SEND RRO option is to be included in RSVP messages sent downstream.

		Returns:
			bool
		"""
		return self._get_attribute('sendRro')
	@SendRro.setter
	def SendRro(self, value):
		self._set_attribute('sendRro', value)

	@property
	def TunnelIdsCount(self):
		"""The number of destination routers. Each router's address is one greater than the previous one's.

		Returns:
			number
		"""
		return self._get_attribute('tunnelIdsCount')
	@TunnelIdsCount.setter
	def TunnelIdsCount(self, value):
		self._set_attribute('tunnelIdsCount', value)

	@property
	def TunnelIdsStart(self):
		"""Sets the start of the range of Tunnel IDs to be used in simulations.

		Returns:
			number
		"""
		return self._get_attribute('tunnelIdsStart')
	@TunnelIdsStart.setter
	def TunnelIdsStart(self, value):
		self._set_attribute('tunnelIdsStart', value)
