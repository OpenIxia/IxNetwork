from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SbfdInitiator(Base):
	"""The SbfdInitiator class encapsulates a required sbfdInitiator node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SbfdInitiator property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'sbfdInitiator'

	def __init__(self, parent):
		super(SbfdInitiator, self).__init__(parent)

	@property
	def MplsLabelList(self):
		"""An instance of the MplsLabelList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplslabellist.MplsLabelList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplslabellist import MplsLabelList
		return MplsLabelList(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DestIPAddr(self):
		"""Destination IP address in SBFD Packet sent to Responder. Should be in 127 subnet as defined in specification.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destIPAddr')

	@property
	def MplsLabelCount(self):
		"""Number of MPLS Labels

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelCount')
	@MplsLabelCount.setter
	def MplsLabelCount(self, value):
		self._set_attribute('mplsLabelCount', value)

	@property
	def MyDiscriminator(self):
		"""The value to be used for My Discriminator in S-BFD packets sent to the Responder by this Initiator. Should be unique in sessions from a single Initiator.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('myDiscriminator')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PeerDiscriminator(self):
		"""Configured Peer Discriminator which should match the configured Local or My Discriminator on the target Responder.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerDiscriminator')

	@property
	def SessionInfo(self):
		"""Current state of the S-BFD Initiator Session, normally Up or Down depending on whether Responder is responding correctly or not.

		Returns:
			list(str[adminDown|down|up])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def TimeoutMultiplier(self):
		"""Timeout Multiplier. If packets are not recieved within Interval * Timeout Interval , session is brought down and Flap Count is increased in statistics.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutMultiplier')

	@property
	def TxInterval(self):
		"""Tx Interval in Milli Seconds. Note: Initial transmission interval is set to maximum of 1s and configured Tx Interval. Once session comes up, the timer will auto-transition to the negotiated value i.e. maximum of local Tx Interval and recieved Rx Interval from Responder.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('txInterval')
