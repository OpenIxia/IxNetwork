from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NeighborPair(Base):
	"""The NeighborPair class encapsulates a user managed neighborPair node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NeighborPair property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'neighborPair'

	def __init__(self, parent):
		super(NeighborPair, self).__init__(parent)

	@property
	def AssignedLabel(self):
		"""An instance of the AssignedLabel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.assignedlabel.AssignedLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.assignedlabel import AssignedLabel
		return AssignedLabel(self)

	@property
	def DestinationRange(self):
		"""An instance of the DestinationRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.destinationrange.DestinationRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.destinationrange import DestinationRange
		return DestinationRange(self)

	@property
	def ReceivedLabel(self):
		"""An instance of the ReceivedLabel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.receivedlabel.ReceivedLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.receivedlabel import ReceivedLabel
		return ReceivedLabel(self)

	@property
	def ActualRestartTime(self):
		"""The time interval after which a hello packet is sent with a new Src Instance Id.

		Returns:
			number
		"""
		return self._get_attribute('actualRestartTime')
	@ActualRestartTime.setter
	def ActualRestartTime(self, value):
		self._set_attribute('actualRestartTime', value)

	@property
	def DutIp(self):
		"""The IP address for the device under test. This is the RSVP router that the simulated router is directly connected to.

		Returns:
			str
		"""
		return self._get_attribute('dutIp')
	@DutIp.setter
	def DutIp(self, value):
		self._set_attribute('dutIp', value)

	@property
	def EnableBfdRegistration(self):
		"""If true, enables BFD registration with RSVP-TE.

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableBundleMessageSending(self):
		"""If true, enables the sending of RSVP Bundle Message.

		Returns:
			bool
		"""
		return self._get_attribute('enableBundleMessageSending')
	@EnableBundleMessageSending.setter
	def EnableBundleMessageSending(self, value):
		self._set_attribute('enableBundleMessageSending', value)

	@property
	def EnableGracefulRestartHelperMode(self):
		"""When checked, enables the graceful restart helper mode.

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestartHelperMode')
	@EnableGracefulRestartHelperMode.setter
	def EnableGracefulRestartHelperMode(self, value):
		self._set_attribute('enableGracefulRestartHelperMode', value)

	@property
	def EnableGracefulRestartingMode(self):
		"""When checked, enables the graceful restart restarting mode.

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestartingMode')
	@EnableGracefulRestartingMode.setter
	def EnableGracefulRestartingMode(self, value):
		self._set_attribute('enableGracefulRestartingMode', value)

	@property
	def EnableHello(self):
		"""Enables the transmission of HELLO messages between the simulated router and the DUT.

		Returns:
			bool
		"""
		return self._get_attribute('enableHello')
	@EnableHello.setter
	def EnableHello(self, value):
		self._set_attribute('enableHello', value)

	@property
	def Enabled(self):
		"""Enables or disables the simulated neighbor pair.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GracefulRestartStartTime(self):
		"""The time interval after this restart timer is fired, and the neighboring nodes are restarted. During this interval the hello messages are not being sent.

		Returns:
			number
		"""
		return self._get_attribute('gracefulRestartStartTime')
	@GracefulRestartStartTime.setter
	def GracefulRestartStartTime(self, value):
		self._set_attribute('gracefulRestartStartTime', value)

	@property
	def GracefulRestartUpTime(self):
		"""The configured interval for which Ixia waits before repeating the Restart cycle, after the Restarting time is over.

		Returns:
			number
		"""
		return self._get_attribute('gracefulRestartUpTime')
	@GracefulRestartUpTime.setter
	def GracefulRestartUpTime(self, value):
		self._set_attribute('gracefulRestartUpTime', value)

	@property
	def HelloInterval(self):
		"""The interval, in seconds, between HELLO messages.

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def HelloTimeoutMultiplier(self):
		"""The number of Hellos sent without confirmation before the DUT is considered dead.

		Returns:
			number
		"""
		return self._get_attribute('helloTimeoutMultiplier')
	@HelloTimeoutMultiplier.setter
	def HelloTimeoutMultiplier(self, value):
		self._set_attribute('helloTimeoutMultiplier', value)

	@property
	def HelloTlvs(self):
		"""Generalized TLV messages that are included with all HELLO messages and built with the rsvpCustomTlv command.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('helloTlvs')
	@HelloTlvs.setter
	def HelloTlvs(self, value):
		self._set_attribute('helloTlvs', value)

	@property
	def IsAssignedInfoRefreshed(self):
		"""When enabled, refreshes the assigned label info automatically.

		Returns:
			bool
		"""
		return self._get_attribute('isAssignedInfoRefreshed')

	@property
	def IsLearnedInfoRefreshed(self):
		"""When enabled, refreshes the learned label info automatically.

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def LabelSpaceEnd(self):
		"""The last label to be used for RSVP tunnels.

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceEnd')
	@LabelSpaceEnd.setter
	def LabelSpaceEnd(self, value):
		self._set_attribute('labelSpaceEnd', value)

	@property
	def LabelSpaceStart(self):
		"""The first label to be used for RSVP tunnels.

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceStart')
	@LabelSpaceStart.setter
	def LabelSpaceStart(self, value):
		self._set_attribute('labelSpaceStart', value)

	@property
	def NumberOfGracefulRestarts(self):
		"""The number of times the Ixia emulated RSVP neighbor moves to Restarting/Recovering and Up states before stopping the cycle.

		Returns:
			number
		"""
		return self._get_attribute('numberOfGracefulRestarts')
	@NumberOfGracefulRestarts.setter
	def NumberOfGracefulRestarts(self, value):
		self._set_attribute('numberOfGracefulRestarts', value)

	@property
	def OurIp(self):
		"""The IP address of the simulated router.

		Returns:
			str
		"""
		return self._get_attribute('ourIp')
	@OurIp.setter
	def OurIp(self, value):
		self._set_attribute('ourIp', value)

	@property
	def RecoveryTimeInterval(self):
		"""The configured time interval for which Ixia waits for the DUT to recover the egress LSPs.

		Returns:
			number
		"""
		return self._get_attribute('recoveryTimeInterval')
	@RecoveryTimeInterval.setter
	def RecoveryTimeInterval(self, value):
		self._set_attribute('recoveryTimeInterval', value)

	@property
	def RefreshReduction(self):
		"""Enables or disables the feature.

		Returns:
			bool
		"""
		return self._get_attribute('refreshReduction')
	@RefreshReduction.setter
	def RefreshReduction(self, value):
		self._set_attribute('refreshReduction', value)

	@property
	def RestartTimeInterval(self):
		"""This value along with the Recovery Time is advertised in the Hello-packets as part of a Restart-capability object.

		Returns:
			number
		"""
		return self._get_attribute('restartTimeInterval')
	@RestartTimeInterval.setter
	def RestartTimeInterval(self, value):
		self._set_attribute('restartTimeInterval', value)

	@property
	def SummaryRefreshInterval(self):
		"""The interval between summary refresh messages.

		Returns:
			number
		"""
		return self._get_attribute('summaryRefreshInterval')
	@SummaryRefreshInterval.setter
	def SummaryRefreshInterval(self, value):
		self._set_attribute('summaryRefreshInterval', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, ActualRestartTime=None, DutIp=None, EnableBfdRegistration=None, EnableBundleMessageSending=None, EnableGracefulRestartHelperMode=None, EnableGracefulRestartingMode=None, EnableHello=None, Enabled=None, GracefulRestartStartTime=None, GracefulRestartUpTime=None, HelloInterval=None, HelloTimeoutMultiplier=None, HelloTlvs=None, LabelSpaceEnd=None, LabelSpaceStart=None, NumberOfGracefulRestarts=None, OurIp=None, RecoveryTimeInterval=None, RefreshReduction=None, RestartTimeInterval=None, SummaryRefreshInterval=None, TrafficGroupId=None):
		"""Adds a new neighborPair node on the server and retrieves it in this instance.

		Args:
			ActualRestartTime (number): The time interval after which a hello packet is sent with a new Src Instance Id.
			DutIp (str): The IP address for the device under test. This is the RSVP router that the simulated router is directly connected to.
			EnableBfdRegistration (bool): If true, enables BFD registration with RSVP-TE.
			EnableBundleMessageSending (bool): If true, enables the sending of RSVP Bundle Message.
			EnableGracefulRestartHelperMode (bool): When checked, enables the graceful restart helper mode.
			EnableGracefulRestartingMode (bool): When checked, enables the graceful restart restarting mode.
			EnableHello (bool): Enables the transmission of HELLO messages between the simulated router and the DUT.
			Enabled (bool): Enables or disables the simulated neighbor pair.
			GracefulRestartStartTime (number): The time interval after this restart timer is fired, and the neighboring nodes are restarted. During this interval the hello messages are not being sent.
			GracefulRestartUpTime (number): The configured interval for which Ixia waits before repeating the Restart cycle, after the Restarting time is over.
			HelloInterval (number): The interval, in seconds, between HELLO messages.
			HelloTimeoutMultiplier (number): The number of Hellos sent without confirmation before the DUT is considered dead.
			HelloTlvs (list(dict(arg1:number,arg2:number,arg3:str))): Generalized TLV messages that are included with all HELLO messages and built with the rsvpCustomTlv command.
			LabelSpaceEnd (number): The last label to be used for RSVP tunnels.
			LabelSpaceStart (number): The first label to be used for RSVP tunnels.
			NumberOfGracefulRestarts (number): The number of times the Ixia emulated RSVP neighbor moves to Restarting/Recovering and Up states before stopping the cycle.
			OurIp (str): The IP address of the simulated router.
			RecoveryTimeInterval (number): The configured time interval for which Ixia waits for the DUT to recover the egress LSPs.
			RefreshReduction (bool): Enables or disables the feature.
			RestartTimeInterval (number): This value along with the Recovery Time is advertised in the Hello-packets as part of a Restart-capability object.
			SummaryRefreshInterval (number): The interval between summary refresh messages.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with all currently retrieved neighborPair data using find and the newly added neighborPair data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the neighborPair data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActualRestartTime=None, DutIp=None, EnableBfdRegistration=None, EnableBundleMessageSending=None, EnableGracefulRestartHelperMode=None, EnableGracefulRestartingMode=None, EnableHello=None, Enabled=None, GracefulRestartStartTime=None, GracefulRestartUpTime=None, HelloInterval=None, HelloTimeoutMultiplier=None, HelloTlvs=None, IsAssignedInfoRefreshed=None, IsLearnedInfoRefreshed=None, LabelSpaceEnd=None, LabelSpaceStart=None, NumberOfGracefulRestarts=None, OurIp=None, RecoveryTimeInterval=None, RefreshReduction=None, RestartTimeInterval=None, SummaryRefreshInterval=None, TrafficGroupId=None):
		"""Finds and retrieves neighborPair data from the server.

		All named parameters support regex and can be used to selectively retrieve neighborPair data from the server.
		By default the find method takes no parameters and will retrieve all neighborPair data from the server.

		Args:
			ActualRestartTime (number): The time interval after which a hello packet is sent with a new Src Instance Id.
			DutIp (str): The IP address for the device under test. This is the RSVP router that the simulated router is directly connected to.
			EnableBfdRegistration (bool): If true, enables BFD registration with RSVP-TE.
			EnableBundleMessageSending (bool): If true, enables the sending of RSVP Bundle Message.
			EnableGracefulRestartHelperMode (bool): When checked, enables the graceful restart helper mode.
			EnableGracefulRestartingMode (bool): When checked, enables the graceful restart restarting mode.
			EnableHello (bool): Enables the transmission of HELLO messages between the simulated router and the DUT.
			Enabled (bool): Enables or disables the simulated neighbor pair.
			GracefulRestartStartTime (number): The time interval after this restart timer is fired, and the neighboring nodes are restarted. During this interval the hello messages are not being sent.
			GracefulRestartUpTime (number): The configured interval for which Ixia waits before repeating the Restart cycle, after the Restarting time is over.
			HelloInterval (number): The interval, in seconds, between HELLO messages.
			HelloTimeoutMultiplier (number): The number of Hellos sent without confirmation before the DUT is considered dead.
			HelloTlvs (list(dict(arg1:number,arg2:number,arg3:str))): Generalized TLV messages that are included with all HELLO messages and built with the rsvpCustomTlv command.
			IsAssignedInfoRefreshed (bool): When enabled, refreshes the assigned label info automatically.
			IsLearnedInfoRefreshed (bool): When enabled, refreshes the learned label info automatically.
			LabelSpaceEnd (number): The last label to be used for RSVP tunnels.
			LabelSpaceStart (number): The first label to be used for RSVP tunnels.
			NumberOfGracefulRestarts (number): The number of times the Ixia emulated RSVP neighbor moves to Restarting/Recovering and Up states before stopping the cycle.
			OurIp (str): The IP address of the simulated router.
			RecoveryTimeInterval (number): The configured time interval for which Ixia waits for the DUT to recover the egress LSPs.
			RefreshReduction (bool): Enables or disables the feature.
			RestartTimeInterval (number): This value along with the Recovery Time is advertised in the Hello-packets as part of a Restart-capability object.
			SummaryRefreshInterval (number): The interval between summary refresh messages.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with matching neighborPair data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of neighborPair data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the neighborPair data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshAssignedLabelInfo(self):
		"""Executes the refreshAssignedLabelInfo operation on the server.

		This exec refreshes the RSVP assigned label information from the DUT.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborPair)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshAssignedLabelInfo', payload=locals(), response_object=None)

	def RefreshReceivedLabelInfo(self):
		"""Executes the refreshReceivedLabelInfo operation on the server.

		This exec refreshes the RSVP received label information from the DUT.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborPair)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshReceivedLabelInfo', payload=locals(), response_object=None)

	def RestartNeighbor(self):
		"""Executes the restartNeighbor operation on the server.

		This command restarts the specifed RSVP neighbor.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborPair)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RestartNeighbor', payload=locals(), response_object=None)
