from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Egress(Base):
	"""The Egress class encapsulates a required egress node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Egress property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'egress'

	def __init__(self, parent):
		super(Egress, self).__init__(parent)

	@property
	def Bandwidth(self):
		"""The requested bandwidth for the tunnel, expressed in kbits per second.

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def EgressBehavior(self):
		"""Dictates the RSVP reservation style when the value of behavior is rsvpEgress.

		Returns:
			str(alwaysUseConfiguredStyle|useSeWhenIndicatedInSessionAttribute)
		"""
		return self._get_attribute('egressBehavior')
	@EgressBehavior.setter
	def EgressBehavior(self, value):
		self._set_attribute('egressBehavior', value)

	@property
	def EnableFixedLabelForResv(self):
		"""Enables the use of a fixed label in RESV messages while in Egress mode.

		Returns:
			bool
		"""
		return self._get_attribute('enableFixedLabelForResv')
	@EnableFixedLabelForResv.setter
	def EnableFixedLabelForResv(self, value):
		self._set_attribute('enableFixedLabelForResv', value)

	@property
	def LabelValue(self):
		"""RSVP label for IPV4 and IPv6 RSVP related routes.

		Returns:
			str
		"""
		return self._get_attribute('labelValue')
	@LabelValue.setter
	def LabelValue(self, value):
		self._set_attribute('labelValue', value)

	@property
	def PathErrorTlv(self):
		"""When signaling fails in the head-end area, a path error message is sent to the head-end.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('pathErrorTlv')
	@PathErrorTlv.setter
	def PathErrorTlv(self, value):
		self._set_attribute('pathErrorTlv', value)

	@property
	def ReflectRro(self):
		"""Enables the reflection of a received RRO object for Egress mode destination ranges. When selected, any RRO items added with addRroItem are ignored. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('reflectRro')
	@ReflectRro.setter
	def ReflectRro(self, value):
		self._set_attribute('reflectRro', value)

	@property
	def RefreshInterval(self):
		"""When the destination range is used in Egress mode, this indicates the time, in seconds, between the simulated router's message to the DUT.

		Returns:
			number
		"""
		return self._get_attribute('refreshInterval')
	@RefreshInterval.setter
	def RefreshInterval(self, value):
		self._set_attribute('refreshInterval', value)

	@property
	def ReservationStyle(self):
		"""The reservation style desired. One of the following options: rsvpFF (fixed filtered mode) or rsvpSE (shared explicit mode).

		Returns:
			str(se|ff|wf)
		"""
		return self._get_attribute('reservationStyle')
	@ReservationStyle.setter
	def ReservationStyle(self, value):
		self._set_attribute('reservationStyle', value)

	@property
	def ReservationTearTlv(self):
		"""a set of custom TLVs to be included in RESV TEAR messages. These may only be used for egress routers.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('reservationTearTlv')
	@ReservationTearTlv.setter
	def ReservationTearTlv(self, value):
		self._set_attribute('reservationTearTlv', value)

	@property
	def ReservationTlv(self):
		"""a set of custom TLVs to be included in RESV messages. These may only be used for egress routers.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('reservationTlv')
	@ReservationTlv.setter
	def ReservationTlv(self, value):
		self._set_attribute('reservationTlv', value)

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
	def SendResvConfirmation(self):
		"""Enables the generation of RESV Confirmation messages for received RESV messages which contain a RESV Confirmation Class object. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('sendResvConfirmation')
	@SendResvConfirmation.setter
	def SendResvConfirmation(self, value):
		self._set_attribute('sendResvConfirmation', value)

	@property
	def TimeoutMultiplier(self):
		"""The number of Hellos before a router is declared dead.

		Returns:
			number
		"""
		return self._get_attribute('timeoutMultiplier')
	@TimeoutMultiplier.setter
	def TimeoutMultiplier(self, value):
		self._set_attribute('timeoutMultiplier', value)
