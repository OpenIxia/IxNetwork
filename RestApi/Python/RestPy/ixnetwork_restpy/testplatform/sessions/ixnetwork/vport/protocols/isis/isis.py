from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Isis(Base):
	"""The Isis class encapsulates a required isis node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Isis property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'isis'

	def __init__(self, parent):
		super(Isis, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.router import Router
		return Router(self)

	@property
	def AllL1RbridgesMac(self):
		"""ISIS All L1 RBridge MAC

		Returns:
			str
		"""
		return self._get_attribute('allL1RbridgesMac')
	@AllL1RbridgesMac.setter
	def AllL1RbridgesMac(self, value):
		self._set_attribute('allL1RbridgesMac', value)

	@property
	def EmulationType(self):
		"""Sets the router emulation type of ISIS component of the protocol server for a particular port.

		Returns:
			str(isisL3Routing|dceIsis|spbIsis|trillIsis)
		"""
		return self._get_attribute('emulationType')
	@EmulationType.setter
	def EmulationType(self, value):
		self._set_attribute('emulationType', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of this emulated IS-IS router in the emulated IS-IS network. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def HelloMulticastMac(self):
		"""ISIS Hello Multicast MAC

		Returns:
			str
		"""
		return self._get_attribute('helloMulticastMac')
	@HelloMulticastMac.setter
	def HelloMulticastMac(self, value):
		self._set_attribute('helloMulticastMac', value)

	@property
	def LspMgroupPdusPerInterval(self):
		"""Indicates the number of LSP MGROUP-PDUs to be sent for each interval.

		Returns:
			number
		"""
		return self._get_attribute('lspMgroupPdusPerInterval')
	@LspMgroupPdusPerInterval.setter
	def LspMgroupPdusPerInterval(self, value):
		self._set_attribute('lspMgroupPdusPerInterval', value)

	@property
	def NlpId(self):
		"""ISIS NLP ID

		Returns:
			number
		"""
		return self._get_attribute('nlpId')
	@NlpId.setter
	def NlpId(self, value):
		self._set_attribute('nlpId', value)

	@property
	def RateControlInterval(self):
		"""Indicates the wait time for transmission.

		Returns:
			number
		"""
		return self._get_attribute('rateControlInterval')
	@RateControlInterval.setter
	def RateControlInterval(self, value):
		self._set_attribute('rateControlInterval', value)

	@property
	def RunningState(self):
		"""The current running state of the ISIS server.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def SendP2PHellosToUnicastMac(self):
		"""If enabled, sends point to point hello messages to unicast mac addresses.

		Returns:
			bool
		"""
		return self._get_attribute('sendP2PHellosToUnicastMac')
	@SendP2PHellosToUnicastMac.setter
	def SendP2PHellosToUnicastMac(self, value):
		self._set_attribute('sendP2PHellosToUnicastMac', value)

	@property
	def SpbAllL1BridgesMac(self):
		"""Contains all SPB ISIS specific attributes.

		Returns:
			str
		"""
		return self._get_attribute('spbAllL1BridgesMac')
	@SpbAllL1BridgesMac.setter
	def SpbAllL1BridgesMac(self, value):
		self._set_attribute('spbAllL1BridgesMac', value)

	@property
	def SpbHelloMulticastMac(self):
		"""Contains all hello messages to multicast mac addresses.

		Returns:
			str
		"""
		return self._get_attribute('spbHelloMulticastMac')
	@SpbHelloMulticastMac.setter
	def SpbHelloMulticastMac(self, value):
		self._set_attribute('spbHelloMulticastMac', value)

	@property
	def SpbNlpId(self):
		"""SPB NLP ID

		Returns:
			number
		"""
		return self._get_attribute('spbNlpId')
	@SpbNlpId.setter
	def SpbNlpId(self, value):
		self._set_attribute('spbNlpId', value)

	def Start(self):
		"""Executes the start operation on the server.

		Starts the ISIS protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=isis)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the ISIS protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=isis)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
