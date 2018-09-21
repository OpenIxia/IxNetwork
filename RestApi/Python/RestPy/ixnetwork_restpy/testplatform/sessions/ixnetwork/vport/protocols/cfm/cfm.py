from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Cfm(Base):
	"""The Cfm class encapsulates a required cfm node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Cfm property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'cfm'

	def __init__(self, parent):
		super(Cfm, self).__init__(parent)

	@property
	def Bridge(self):
		"""An instance of the Bridge class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.bridge.Bridge)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.bridge import Bridge
		return Bridge(self)

	@property
	def EnableOptionalLmFunctionality(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableOptionalLmFunctionality')
	@EnableOptionalLmFunctionality.setter
	def EnableOptionalLmFunctionality(self, value):
		self._set_attribute('enableOptionalLmFunctionality', value)

	@property
	def EnableOptionalTlvValidation(self):
		"""If true, the CFM protocol will validate optional TLVs present in CFM packets.

		Returns:
			bool
		"""
		return self._get_attribute('enableOptionalTlvValidation')
	@EnableOptionalTlvValidation.setter
	def EnableOptionalTlvValidation(self, value):
		self._set_attribute('enableOptionalTlvValidation', value)

	@property
	def Enabled(self):
		"""If true, the CFM protcol is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ReceiveCcm(self):
		"""If true, the CFM protocol can receive CFM CCMs on this port.

		Returns:
			bool
		"""
		return self._get_attribute('receiveCcm')
	@ReceiveCcm.setter
	def ReceiveCcm(self, value):
		self._set_attribute('receiveCcm', value)

	@property
	def RunningState(self):
		"""The current running state of the CFM protocol.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def SendCcm(self):
		"""If true, the CFM protocol can send CFM CCMs from this port.

		Returns:
			bool
		"""
		return self._get_attribute('sendCcm')
	@SendCcm.setter
	def SendCcm(self, value):
		self._set_attribute('sendCcm', value)

	@property
	def SuppressErrorsOnAis(self):
		"""If true, the errors on AIS are suopressed.

		Returns:
			bool
		"""
		return self._get_attribute('suppressErrorsOnAis')
	@SuppressErrorsOnAis.setter
	def SuppressErrorsOnAis(self, value):
		self._set_attribute('suppressErrorsOnAis', value)

	def Start(self):
		"""Executes the start operation on the server.

		Starts the CFM protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=cfm)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the CFM protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=cfm)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
