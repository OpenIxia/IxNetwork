from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class JoinPrune(Base):
	"""The JoinPrune class encapsulates a user managed joinPrune node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the JoinPrune property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'joinPrune'

	def __init__(self, parent):
		super(JoinPrune, self).__init__(parent)

	@property
	def LearnedMgrState(self):
		"""An instance of the LearnedMgrState class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.learnedmgrstate.learnedmgrstate.LearnedMgrState)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.learnedmgrstate.learnedmgrstate import LearnedMgrState
		return LearnedMgrState(self)

	@property
	def DiscardRegisterStates(self):
		"""If checked, the Learned Join States sent by the RP (DUT) in response to this specific Register Message will be discarded - and will not be displayed in the table of the Register Range window.

		Returns:
			bool
		"""
		return self._get_attribute('discardRegisterStates')
	@DiscardRegisterStates.setter
	def DiscardRegisterStates(self, value):
		self._set_attribute('discardRegisterStates', value)

	@property
	def Enabled(self):
		"""Enables the use of this join/prune.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EnabledDataMdt(self):
		"""If enabled, pimsmLearnedDataMdt will be available. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabledDataMdt')
	@EnabledDataMdt.setter
	def EnabledDataMdt(self, value):
		self._set_attribute('enabledDataMdt', value)

	@property
	def FlapEnabled(self):
		"""Enables emulated flapping of this multicast group range. NOTE: Flapping is not supported for the Switchover (*, G) -> (S, G) range type.

		Returns:
			bool
		"""
		return self._get_attribute('flapEnabled')
	@FlapEnabled.setter
	def FlapEnabled(self, value):
		self._set_attribute('flapEnabled', value)

	@property
	def FlapInterval(self):
		"""Defines the join/prune flapping interval.

		Returns:
			number
		"""
		return self._get_attribute('flapInterval')
	@FlapInterval.setter
	def FlapInterval(self, value):
		self._set_attribute('flapInterval', value)

	@property
	def GroupAddress(self):
		"""An IPv4 or IPv6 address used with the group mask to create a range of multicast addresses.

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')
	@GroupAddress.setter
	def GroupAddress(self, value):
		self._set_attribute('groupAddress', value)

	@property
	def GroupCount(self):
		"""The number of multicast group addresses to be included in the multicast group range. The maximum number of valid possible addresses depends on the values for the group address and the group mask width.

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupMappingMode(self):
		"""Sets the type of mapping that occurs when routes are advertised. This only applies for (S, G) and switchover types for MGR and is meaningful for RR.

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('groupMappingMode')
	@GroupMappingMode.setter
	def GroupMappingMode(self, value):
		self._set_attribute('groupMappingMode', value)

	@property
	def GroupMaskWidth(self):
		"""The number of bits in the mask applied to the group address. (The masked bits in the group address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type.

		Returns:
			number
		"""
		return self._get_attribute('groupMaskWidth')
	@GroupMaskWidth.setter
	def GroupMaskWidth(self, value):
		self._set_attribute('groupMaskWidth', value)

	@property
	def GroupRange(self):
		"""The multicast group range type.

		Returns:
			str(rp|g|sg|sptSwitchOver|registerTriggeredSg)
		"""
		return self._get_attribute('groupRange')
	@GroupRange.setter
	def GroupRange(self, value):
		self._set_attribute('groupRange', value)

	@property
	def NumRegToReceivePerSg(self):
		"""If rangeType is set to pimsmJoinsPrunesTypeRegisterTriggeredSG, then this is the count of register messages received that will trigger transmission of a (S,G) message. (default = 10)

		Returns:
			number
		"""
		return self._get_attribute('numRegToReceivePerSg')
	@NumRegToReceivePerSg.setter
	def NumRegToReceivePerSg(self, value):
		self._set_attribute('numRegToReceivePerSg', value)

	@property
	def PackGroupsEnabled(self):
		"""If enabled, multiple groups can be included within a single packet.

		Returns:
			bool
		"""
		return self._get_attribute('packGroupsEnabled')
	@PackGroupsEnabled.setter
	def PackGroupsEnabled(self, value):
		self._set_attribute('packGroupsEnabled', value)

	@property
	def PruneSourceAddress(self):
		"""ONLY used for (*,G) Type to send (S,G,rpt) Prune Messages. (Multicast addresses are invalid.)

		Returns:
			str
		"""
		return self._get_attribute('pruneSourceAddress')
	@PruneSourceAddress.setter
	def PruneSourceAddress(self, value):
		self._set_attribute('pruneSourceAddress', value)

	@property
	def PruneSourceCount(self):
		"""The number of prune source addresses to be included. The maximum number of valid possible addresses depends on the values for the source address and the source mask width. The default value is 0. ONLY used for (*,G) type to send (S,G,rpt) prune messages.

		Returns:
			number
		"""
		return self._get_attribute('pruneSourceCount')
	@PruneSourceCount.setter
	def PruneSourceCount(self, value):
		self._set_attribute('pruneSourceCount', value)

	@property
	def PruneSourceMaskWidth(self):
		"""The number of bits in the mask applied to the prune source address. (The masked bits in the prune source address form the address prefix.)

		Returns:
			number
		"""
		return self._get_attribute('pruneSourceMaskWidth')
	@PruneSourceMaskWidth.setter
	def PruneSourceMaskWidth(self, value):
		self._set_attribute('pruneSourceMaskWidth', value)

	@property
	def RpAddress(self):
		"""The IP address of the Rendezvous Point (RP) router.

		Returns:
			str
		"""
		return self._get_attribute('rpAddress')
	@RpAddress.setter
	def RpAddress(self, value):
		self._set_attribute('rpAddress', value)

	@property
	def SourceAddress(self):
		"""The Multicast Source Address. Used for (S,G) Type and (S,G, rpt) only. (Multicast addresses are invalid.)

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')
	@SourceAddress.setter
	def SourceAddress(self, value):
		self._set_attribute('sourceAddress', value)

	@property
	def SourceCount(self):
		"""The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the source address and the source mask width.

		Returns:
			number
		"""
		return self._get_attribute('sourceCount')
	@SourceCount.setter
	def SourceCount(self, value):
		self._set_attribute('sourceCount', value)

	@property
	def SourceMaskWidth(self):
		"""The number of bits in the mask applied to the source address. (The masked bits in the source address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type. Used for (S,G) Type and (S,G, rpt) only.

		Returns:
			number
		"""
		return self._get_attribute('sourceMaskWidth')
	@SourceMaskWidth.setter
	def SourceMaskWidth(self, value):
		self._set_attribute('sourceMaskWidth', value)

	@property
	def SptSwitchoverInterval(self):
		"""The time interval (in seconds) allowed for the switch from using the RP tree to using a Source-specific tree - from (*,G) to (S,G). The default value is 0.

		Returns:
			number
		"""
		return self._get_attribute('sptSwitchoverInterval')
	@SptSwitchoverInterval.setter
	def SptSwitchoverInterval(self, value):
		self._set_attribute('sptSwitchoverInterval', value)

	def add(self, DiscardRegisterStates=None, Enabled=None, EnabledDataMdt=None, FlapEnabled=None, FlapInterval=None, GroupAddress=None, GroupCount=None, GroupMappingMode=None, GroupMaskWidth=None, GroupRange=None, NumRegToReceivePerSg=None, PackGroupsEnabled=None, PruneSourceAddress=None, PruneSourceCount=None, PruneSourceMaskWidth=None, RpAddress=None, SourceAddress=None, SourceCount=None, SourceMaskWidth=None, SptSwitchoverInterval=None):
		"""Adds a new joinPrune node on the server and retrieves it in this instance.

		Args:
			DiscardRegisterStates (bool): If checked, the Learned Join States sent by the RP (DUT) in response to this specific Register Message will be discarded - and will not be displayed in the table of the Register Range window.
			Enabled (bool): Enables the use of this join/prune.
			EnabledDataMdt (bool): If enabled, pimsmLearnedDataMdt will be available. (default = disabled)
			FlapEnabled (bool): Enables emulated flapping of this multicast group range. NOTE: Flapping is not supported for the Switchover (*, G) -> (S, G) range type.
			FlapInterval (number): Defines the join/prune flapping interval.
			GroupAddress (str): An IPv4 or IPv6 address used with the group mask to create a range of multicast addresses.
			GroupCount (number): The number of multicast group addresses to be included in the multicast group range. The maximum number of valid possible addresses depends on the values for the group address and the group mask width.
			GroupMappingMode (str(fullyMeshed|oneToOne)): Sets the type of mapping that occurs when routes are advertised. This only applies for (S, G) and switchover types for MGR and is meaningful for RR.
			GroupMaskWidth (number): The number of bits in the mask applied to the group address. (The masked bits in the group address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type.
			GroupRange (str(rp|g|sg|sptSwitchOver|registerTriggeredSg)): The multicast group range type.
			NumRegToReceivePerSg (number): If rangeType is set to pimsmJoinsPrunesTypeRegisterTriggeredSG, then this is the count of register messages received that will trigger transmission of a (S,G) message. (default = 10)
			PackGroupsEnabled (bool): If enabled, multiple groups can be included within a single packet.
			PruneSourceAddress (str): ONLY used for (*,G) Type to send (S,G,rpt) Prune Messages. (Multicast addresses are invalid.)
			PruneSourceCount (number): The number of prune source addresses to be included. The maximum number of valid possible addresses depends on the values for the source address and the source mask width. The default value is 0. ONLY used for (*,G) type to send (S,G,rpt) prune messages.
			PruneSourceMaskWidth (number): The number of bits in the mask applied to the prune source address. (The masked bits in the prune source address form the address prefix.)
			RpAddress (str): The IP address of the Rendezvous Point (RP) router.
			SourceAddress (str): The Multicast Source Address. Used for (S,G) Type and (S,G, rpt) only. (Multicast addresses are invalid.)
			SourceCount (number): The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the source address and the source mask width.
			SourceMaskWidth (number): The number of bits in the mask applied to the source address. (The masked bits in the source address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type. Used for (S,G) Type and (S,G, rpt) only.
			SptSwitchoverInterval (number): The time interval (in seconds) allowed for the switch from using the RP tree to using a Source-specific tree - from (*,G) to (S,G). The default value is 0.

		Returns:
			self: This instance with all currently retrieved joinPrune data using find and the newly added joinPrune data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the joinPrune data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DiscardRegisterStates=None, Enabled=None, EnabledDataMdt=None, FlapEnabled=None, FlapInterval=None, GroupAddress=None, GroupCount=None, GroupMappingMode=None, GroupMaskWidth=None, GroupRange=None, NumRegToReceivePerSg=None, PackGroupsEnabled=None, PruneSourceAddress=None, PruneSourceCount=None, PruneSourceMaskWidth=None, RpAddress=None, SourceAddress=None, SourceCount=None, SourceMaskWidth=None, SptSwitchoverInterval=None):
		"""Finds and retrieves joinPrune data from the server.

		All named parameters support regex and can be used to selectively retrieve joinPrune data from the server.
		By default the find method takes no parameters and will retrieve all joinPrune data from the server.

		Args:
			DiscardRegisterStates (bool): If checked, the Learned Join States sent by the RP (DUT) in response to this specific Register Message will be discarded - and will not be displayed in the table of the Register Range window.
			Enabled (bool): Enables the use of this join/prune.
			EnabledDataMdt (bool): If enabled, pimsmLearnedDataMdt will be available. (default = disabled)
			FlapEnabled (bool): Enables emulated flapping of this multicast group range. NOTE: Flapping is not supported for the Switchover (*, G) -> (S, G) range type.
			FlapInterval (number): Defines the join/prune flapping interval.
			GroupAddress (str): An IPv4 or IPv6 address used with the group mask to create a range of multicast addresses.
			GroupCount (number): The number of multicast group addresses to be included in the multicast group range. The maximum number of valid possible addresses depends on the values for the group address and the group mask width.
			GroupMappingMode (str(fullyMeshed|oneToOne)): Sets the type of mapping that occurs when routes are advertised. This only applies for (S, G) and switchover types for MGR and is meaningful for RR.
			GroupMaskWidth (number): The number of bits in the mask applied to the group address. (The masked bits in the group address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type.
			GroupRange (str(rp|g|sg|sptSwitchOver|registerTriggeredSg)): The multicast group range type.
			NumRegToReceivePerSg (number): If rangeType is set to pimsmJoinsPrunesTypeRegisterTriggeredSG, then this is the count of register messages received that will trigger transmission of a (S,G) message. (default = 10)
			PackGroupsEnabled (bool): If enabled, multiple groups can be included within a single packet.
			PruneSourceAddress (str): ONLY used for (*,G) Type to send (S,G,rpt) Prune Messages. (Multicast addresses are invalid.)
			PruneSourceCount (number): The number of prune source addresses to be included. The maximum number of valid possible addresses depends on the values for the source address and the source mask width. The default value is 0. ONLY used for (*,G) type to send (S,G,rpt) prune messages.
			PruneSourceMaskWidth (number): The number of bits in the mask applied to the prune source address. (The masked bits in the prune source address form the address prefix.)
			RpAddress (str): The IP address of the Rendezvous Point (RP) router.
			SourceAddress (str): The Multicast Source Address. Used for (S,G) Type and (S,G, rpt) only. (Multicast addresses are invalid.)
			SourceCount (number): The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the source address and the source mask width.
			SourceMaskWidth (number): The number of bits in the mask applied to the source address. (The masked bits in the source address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type. Used for (S,G) Type and (S,G, rpt) only.
			SptSwitchoverInterval (number): The time interval (in seconds) allowed for the switch from using the RP tree to using a Source-specific tree - from (*,G) to (S,G). The default value is 0.

		Returns:
			self: This instance with matching joinPrune data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of joinPrune data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the joinPrune data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
