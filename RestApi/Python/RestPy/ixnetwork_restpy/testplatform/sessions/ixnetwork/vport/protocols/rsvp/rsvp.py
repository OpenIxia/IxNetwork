from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Rsvp(Base):
	"""The Rsvp class encapsulates a required rsvp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Rsvp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rsvp'

	def __init__(self, parent):
		super(Rsvp, self).__init__(parent)

	@property
	def NeighborPair(self):
		"""An instance of the NeighborPair class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.neighborpair.NeighborPair)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.neighborpair import NeighborPair
		return NeighborPair(self)

	@property
	def EnableBgpOverLsp(self):
		"""Enables the ability to exchange labels over LSP for VPNs.

		Returns:
			bool
		"""
		return self._get_attribute('enableBgpOverLsp')
	@EnableBgpOverLsp.setter
	def EnableBgpOverLsp(self, value):
		self._set_attribute('enableBgpOverLsp', value)

	@property
	def EnableControlLspInitiationRate(self):
		"""Controls the LSP initiation rate.

		Returns:
			bool
		"""
		return self._get_attribute('enableControlLspInitiationRate')
	@EnableControlLspInitiationRate.setter
	def EnableControlLspInitiationRate(self, value):
		self._set_attribute('enableControlLspInitiationRate', value)

	@property
	def EnableShowTimeValue(self):
		"""If true, allows to calculate LSP/sub LSP setup time. When a first path message is sent for an LSP or sub LSP, the state machine takes the time stamp and stores it in the internal structure. It repeats this, when a reserve message is received for that LSP or sub LSP.

		Returns:
			bool
		"""
		return self._get_attribute('enableShowTimeValue')
	@EnableShowTimeValue.setter
	def EnableShowTimeValue(self, value):
		self._set_attribute('enableShowTimeValue', value)

	@property
	def EnableVpnLabelExchangeOverLsp(self):
		"""If true, enables VPN label exchange over LSP

		Returns:
			bool
		"""
		return self._get_attribute('enableVpnLabelExchangeOverLsp')
	@EnableVpnLabelExchangeOverLsp.setter
	def EnableVpnLabelExchangeOverLsp(self, value):
		self._set_attribute('enableVpnLabelExchangeOverLsp', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of this emulated RSVP router in the emulated RSVP network. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def MaxLspInitiationsPerSec(self):
		"""The maximum number of LSP Initiations sent per second.

		Returns:
			number
		"""
		return self._get_attribute('maxLspInitiationsPerSec')
	@MaxLspInitiationsPerSec.setter
	def MaxLspInitiationsPerSec(self, value):
		self._set_attribute('maxLspInitiationsPerSec', value)

	@property
	def RunningState(self):
		"""The current running state of the RSVP server.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

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

		Starts RSVP on a port or a group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=rsvp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops RSVP on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=rsvp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
