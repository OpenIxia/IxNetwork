from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ldp(Base):
	"""The Ldp class encapsulates a required ldp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ldp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ldp'

	def __init__(self, parent):
		super(Ldp, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.router import Router
		return Router(self)

	@property
	def EnableDiscardSelfAdvFecs(self):
		"""Discards learned labels from the DUT that match any of the enabled configured IPv4 FEC ranges.

		Returns:
			bool
		"""
		return self._get_attribute('enableDiscardSelfAdvFecs')
	@EnableDiscardSelfAdvFecs.setter
	def EnableDiscardSelfAdvFecs(self, value):
		self._set_attribute('enableDiscardSelfAdvFecs', value)

	@property
	def EnableHelloJitter(self):
		"""Allows staggered transmission of many HELLO messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableHelloJitter')
	@EnableHelloJitter.setter
	def EnableHelloJitter(self, value):
		self._set_attribute('enableHelloJitter', value)

	@property
	def EnableLabelExchangeOverLsp(self):
		"""Enables the ability to exchange labels over LSP for VPNs.

		Returns:
			bool
		"""
		return self._get_attribute('enableLabelExchangeOverLsp')
	@EnableLabelExchangeOverLsp.setter
	def EnableLabelExchangeOverLsp(self, value):
		self._set_attribute('enableLabelExchangeOverLsp', value)

	@property
	def EnableVpnLabelExchangeOverLsp(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableVpnLabelExchangeOverLsp')
	@EnableVpnLabelExchangeOverLsp.setter
	def EnableVpnLabelExchangeOverLsp(self, value):
		self._set_attribute('enableVpnLabelExchangeOverLsp', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of this emulated LDP router in the emulated LDP network. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def HelloHoldTime(self):
		"""One of the timers associated with maintaining adjacencies based on hello messages.

		Returns:
			number
		"""
		return self._get_attribute('helloHoldTime')
	@HelloHoldTime.setter
	def HelloHoldTime(self, value):
		self._set_attribute('helloHoldTime', value)

	@property
	def HelloInterval(self):
		"""One of the timers associated with maintaining adjacencies based on hello messages.

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def KeepAliveHoldTime(self):
		"""One of the timers associated with maintaining adjacencies based on PDU and keep-alive messages.

		Returns:
			number
		"""
		return self._get_attribute('keepAliveHoldTime')
	@KeepAliveHoldTime.setter
	def KeepAliveHoldTime(self, value):
		self._set_attribute('keepAliveHoldTime', value)

	@property
	def KeepAliveInterval(self):
		"""One of the timers associated with maintaining adjacencies based on PDU and keep-alive messages.

		Returns:
			number
		"""
		return self._get_attribute('keepAliveInterval')
	@KeepAliveInterval.setter
	def KeepAliveInterval(self, value):
		self._set_attribute('keepAliveInterval', value)

	@property
	def P2mpCapabilityParam(self):
		"""The P2MP capability parameter value in hexadecimal.

		Returns:
			number
		"""
		return self._get_attribute('p2mpCapabilityParam')
	@P2mpCapabilityParam.setter
	def P2mpCapabilityParam(self, value):
		self._set_attribute('p2mpCapabilityParam', value)

	@property
	def P2mpFecType(self):
		"""The MLDP P2MP FEC type value in hexadecimal.

		Returns:
			number
		"""
		return self._get_attribute('p2mpFecType')
	@P2mpFecType.setter
	def P2mpFecType(self, value):
		self._set_attribute('p2mpFecType', value)

	@property
	def RunningState(self):
		"""The current state of the LDP server.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def TargetedHelloInterval(self):
		"""One of the timers associated with maintaining targeted peer adjacencies based on hello messages.

		Returns:
			number
		"""
		return self._get_attribute('targetedHelloInterval')
	@TargetedHelloInterval.setter
	def TargetedHelloInterval(self, value):
		self._set_attribute('targetedHelloInterval', value)

	@property
	def TargetedHoldTime(self):
		"""One of the timers associated with maintaining targeted peer adjacencies based on hello messages.

		Returns:
			number
		"""
		return self._get_attribute('targetedHoldTime')
	@TargetedHoldTime.setter
	def TargetedHoldTime(self, value):
		self._set_attribute('targetedHoldTime', value)

	@property
	def UseTransportLabelsForMplsOam(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('useTransportLabelsForMplsOam')
	@UseTransportLabelsForMplsOam.setter
	def UseTransportLabelsForMplsOam(self, value):
		self._set_attribute('useTransportLabelsForMplsOam', value)

	def Start(self):
		"""Executes the start operation on the server.

		Starts the LDP protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ldp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the LDP protocol on a port of group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ldp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
