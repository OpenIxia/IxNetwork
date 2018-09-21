from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MplsTp(Base):
	"""The MplsTp class encapsulates a required mplsTp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MplsTp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'mplsTp'

	def __init__(self, parent):
		super(MplsTp, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.router import Router
		return Router(self)

	@property
	def ApsChannelType(self):
		"""This signifies the Automatic Protection Switching Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('apsChannelType')
	@ApsChannelType.setter
	def ApsChannelType(self, value):
		self._set_attribute('apsChannelType', value)

	@property
	def BfdCcChannelType(self):
		"""This signifies the BFD Continuity Check Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('bfdCcChannelType')
	@BfdCcChannelType.setter
	def BfdCcChannelType(self, value):
		self._set_attribute('bfdCcChannelType', value)

	@property
	def DelayManagementChannelType(self):
		"""This signifies the Delay Measurement Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('delayManagementChannelType')
	@DelayManagementChannelType.setter
	def DelayManagementChannelType(self, value):
		self._set_attribute('delayManagementChannelType', value)

	@property
	def EnableHighPerformanceMode(self):
		"""This signifies select the checkbox to enable high performance mode.

		Returns:
			bool
		"""
		return self._get_attribute('enableHighPerformanceMode')
	@EnableHighPerformanceMode.setter
	def EnableHighPerformanceMode(self, value):
		self._set_attribute('enableHighPerformanceMode', value)

	@property
	def Enabled(self):
		"""This signifies that the mplsTp protocol is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FaultManagementChannelType(self):
		"""This signifies the Fault Management Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('faultManagementChannelType')
	@FaultManagementChannelType.setter
	def FaultManagementChannelType(self, value):
		self._set_attribute('faultManagementChannelType', value)

	@property
	def LossMeasurementChannelType(self):
		"""This signifies the Loss Measurement Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('lossMeasurementChannelType')
	@LossMeasurementChannelType.setter
	def LossMeasurementChannelType(self, value):
		self._set_attribute('lossMeasurementChannelType', value)

	@property
	def OnDemandCvChannelType(self):
		"""This signifies the On Demand Connectivity Verification Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('onDemandCvChannelType')
	@OnDemandCvChannelType.setter
	def OnDemandCvChannelType(self, value):
		self._set_attribute('onDemandCvChannelType', value)

	@property
	def PwStatusChannelType(self):
		"""This signifies the Pseudowire Status Channel Type.

		Returns:
			str
		"""
		return self._get_attribute('pwStatusChannelType')
	@PwStatusChannelType.setter
	def PwStatusChannelType(self, value):
		self._set_attribute('pwStatusChannelType', value)

	@property
	def RunningState(self):
		"""This signifies the running state of the protocol. Possible values include Started, Starting, Unknown, Stopping and Stopped.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def Y1731ChannelType(self):
		"""This signifies the Y.1731 Channel Type in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('y1731ChannelType')
	@Y1731ChannelType.setter
	def Y1731ChannelType(self, value):
		self._set_attribute('y1731ChannelType', value)

	def Start(self):
		"""Executes the start operation on the server.

		This signifies the starting of the MPLSTP protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mplsTp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This signifies the stopping of the MPLSTP protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mplsTp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
