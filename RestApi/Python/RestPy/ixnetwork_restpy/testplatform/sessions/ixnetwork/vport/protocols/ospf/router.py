from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Router(Base):
	"""The Router class encapsulates a user managed router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'router'

	def __init__(self, parent):
		super(Router, self).__init__(parent)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.interface import Interface
		return Interface(self)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.routerange import RouteRange
		return RouteRange(self)

	@property
	def UserLsaGroup(self):
		"""An instance of the UserLsaGroup class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.userlsagroup.UserLsaGroup)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.userlsagroup import UserLsaGroup
		return UserLsaGroup(self)

	@property
	def DiscardLearnedLsa(self):
		"""When this option is true, this simulated OSPF router (RID) will not learn any LSAs from the neighbor. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedLsa')
	@DiscardLearnedLsa.setter
	def DiscardLearnedLsa(self, value):
		self._set_attribute('discardLearnedLsa', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of this emulated OSPF router in the emulated OSPF network. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GenerateRouterLsa(self):
		"""If enabled, the router will automatically generate a router LSA including all of the interfaces added with the ospfRouter addInterface command. This should be turned off if you are building OSPF topologies with ospfUserLsa commands. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('generateRouterLsa')
	@GenerateRouterLsa.setter
	def GenerateRouterLsa(self, value):
		self._set_attribute('generateRouterLsa', value)

	@property
	def GracefulRestart(self):
		"""Enables the graceful restart Helper Mode function, per the IETF drafts, for the emulated OSPF router. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('gracefulRestart')
	@GracefulRestart.setter
	def GracefulRestart(self, value):
		self._set_attribute('gracefulRestart', value)

	@property
	def InterFloodLsUpdateBurstGap(self):
		"""The number of FloodlsUpdates sent between each Burst gap.

		Returns:
			number
		"""
		return self._get_attribute('interFloodLsUpdateBurstGap')
	@InterFloodLsUpdateBurstGap.setter
	def InterFloodLsUpdateBurstGap(self, value):
		self._set_attribute('interFloodLsUpdateBurstGap', value)

	@property
	def LsaRefreshTime(self):
		"""The time taken for LSA refresh.

		Returns:
			number
		"""
		return self._get_attribute('lsaRefreshTime')
	@LsaRefreshTime.setter
	def LsaRefreshTime(self, value):
		self._set_attribute('lsaRefreshTime', value)

	@property
	def LsaRetransmitTime(self):
		"""The time taken to retransmit LSA.

		Returns:
			number
		"""
		return self._get_attribute('lsaRetransmitTime')
	@LsaRetransmitTime.setter
	def LsaRetransmitTime(self, value):
		self._set_attribute('lsaRetransmitTime', value)

	@property
	def MaxFloodLsUpdatesPerBurst(self):
		"""The maximum number of FloodLsUpdates sent for each Burst.

		Returns:
			number
		"""
		return self._get_attribute('maxFloodLsUpdatesPerBurst')
	@MaxFloodLsUpdatesPerBurst.setter
	def MaxFloodLsUpdatesPerBurst(self, value):
		self._set_attribute('maxFloodLsUpdatesPerBurst', value)

	@property
	def RebuildAdjForLsdbChange(self):
		"""The enableGracefulRestart option must be true. If this option is true, Database Description (DBD) packets will have the R bit set - and the DBD packets will also have the LR (LSDB Resynchronization) bit set in the LLS Extended Options TLV. Out-of-Band Link State Database (OOB LSDB) resynchronization will be used instead of normal LSDB resynchronization, in order to preserve the OSPF adjacency with the neighbor router across OSPF Graceful Restart. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('rebuildAdjForLsdbChange')
	@RebuildAdjForLsdbChange.setter
	def RebuildAdjForLsdbChange(self, value):
		self._set_attribute('rebuildAdjForLsdbChange', value)

	@property
	def RouterId(self):
		"""The router ID for this emulated OSPF router, in IPv4 format.

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def StrictLsaChecking(self):
		"""If enabled, the OSPFv2 Restart Helper will terminate Graceful Restart when there are changes to an LSA that would be flooded to, or retransmitted by, the restarting router.

		Returns:
			bool
		"""
		return self._get_attribute('strictLsaChecking')
	@StrictLsaChecking.setter
	def StrictLsaChecking(self, value):
		self._set_attribute('strictLsaChecking', value)

	@property
	def SupportForRfc3623(self):
		"""Enables Graceful Restart Helper Mode per RFC 3623 on the emulated OSPF router. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('supportForRfc3623')
	@SupportForRfc3623.setter
	def SupportForRfc3623(self, value):
		self._set_attribute('supportForRfc3623', value)

	@property
	def SupportReasonSoftReloadUpgrade(self):
		"""If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is a Software Reload or Upgrade on the restarting router. (Planned outage) The default is checked/enabled.

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonSoftReloadUpgrade')
	@SupportReasonSoftReloadUpgrade.setter
	def SupportReasonSoftReloadUpgrade(self, value):
		self._set_attribute('supportReasonSoftReloadUpgrade', value)

	@property
	def SupportReasonSoftRestart(self):
		"""If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is an OSPFv2 software restart (on the restarting router). (Planned or unplanned outage) The default is checked/enabled.

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonSoftRestart')
	@SupportReasonSoftRestart.setter
	def SupportReasonSoftRestart(self, value):
		self._set_attribute('supportReasonSoftRestart', value)

	@property
	def SupportReasonSwotchRedundantCntrlProcessor(self):
		"""If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is a unplanned switchover to a redundant control processor on the restarting router. (Unplanned outage)

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonSwotchRedundantCntrlProcessor')
	@SupportReasonSwotchRedundantCntrlProcessor.setter
	def SupportReasonSwotchRedundantCntrlProcessor(self, value):
		self._set_attribute('supportReasonSwotchRedundantCntrlProcessor', value)

	@property
	def SupportReasonUnknown(self):
		"""If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is unknown and unplanned. (Unplanned outage) The default is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonUnknown')
	@SupportReasonUnknown.setter
	def SupportReasonUnknown(self, value):
		self._set_attribute('supportReasonUnknown', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this emulated OSPF router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, DiscardLearnedLsa=None, Enabled=None, GenerateRouterLsa=None, GracefulRestart=None, InterFloodLsUpdateBurstGap=None, LsaRefreshTime=None, LsaRetransmitTime=None, MaxFloodLsUpdatesPerBurst=None, RebuildAdjForLsdbChange=None, RouterId=None, StrictLsaChecking=None, SupportForRfc3623=None, SupportReasonSoftReloadUpgrade=None, SupportReasonSoftRestart=None, SupportReasonSwotchRedundantCntrlProcessor=None, SupportReasonUnknown=None, TrafficGroupId=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			DiscardLearnedLsa (bool): When this option is true, this simulated OSPF router (RID) will not learn any LSAs from the neighbor. (default = false)
			Enabled (bool): Enables or disables the use of this emulated OSPF router in the emulated OSPF network. (default = disabled)
			GenerateRouterLsa (bool): If enabled, the router will automatically generate a router LSA including all of the interfaces added with the ospfRouter addInterface command. This should be turned off if you are building OSPF topologies with ospfUserLsa commands. (default = true)
			GracefulRestart (bool): Enables the graceful restart Helper Mode function, per the IETF drafts, for the emulated OSPF router. (default = false)
			InterFloodLsUpdateBurstGap (number): The number of FloodlsUpdates sent between each Burst gap.
			LsaRefreshTime (number): The time taken for LSA refresh.
			LsaRetransmitTime (number): The time taken to retransmit LSA.
			MaxFloodLsUpdatesPerBurst (number): The maximum number of FloodLsUpdates sent for each Burst.
			RebuildAdjForLsdbChange (bool): The enableGracefulRestart option must be true. If this option is true, Database Description (DBD) packets will have the R bit set - and the DBD packets will also have the LR (LSDB Resynchronization) bit set in the LLS Extended Options TLV. Out-of-Band Link State Database (OOB LSDB) resynchronization will be used instead of normal LSDB resynchronization, in order to preserve the OSPF adjacency with the neighbor router across OSPF Graceful Restart. (default = false)
			RouterId (str): The router ID for this emulated OSPF router, in IPv4 format.
			StrictLsaChecking (bool): If enabled, the OSPFv2 Restart Helper will terminate Graceful Restart when there are changes to an LSA that would be flooded to, or retransmitted by, the restarting router.
			SupportForRfc3623 (bool): Enables Graceful Restart Helper Mode per RFC 3623 on the emulated OSPF router. (default = false)
			SupportReasonSoftReloadUpgrade (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is a Software Reload or Upgrade on the restarting router. (Planned outage) The default is checked/enabled.
			SupportReasonSoftRestart (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is an OSPFv2 software restart (on the restarting router). (Planned or unplanned outage) The default is checked/enabled.
			SupportReasonSwotchRedundantCntrlProcessor (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is a unplanned switchover to a redundant control processor on the restarting router. (Unplanned outage)
			SupportReasonUnknown (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is unknown and unplanned. (Unplanned outage) The default is enabled.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this emulated OSPF router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the router data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DiscardLearnedLsa=None, Enabled=None, GenerateRouterLsa=None, GracefulRestart=None, InterFloodLsUpdateBurstGap=None, LsaRefreshTime=None, LsaRetransmitTime=None, MaxFloodLsUpdatesPerBurst=None, RebuildAdjForLsdbChange=None, RouterId=None, StrictLsaChecking=None, SupportForRfc3623=None, SupportReasonSoftReloadUpgrade=None, SupportReasonSoftRestart=None, SupportReasonSwotchRedundantCntrlProcessor=None, SupportReasonUnknown=None, TrafficGroupId=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			DiscardLearnedLsa (bool): When this option is true, this simulated OSPF router (RID) will not learn any LSAs from the neighbor. (default = false)
			Enabled (bool): Enables or disables the use of this emulated OSPF router in the emulated OSPF network. (default = disabled)
			GenerateRouterLsa (bool): If enabled, the router will automatically generate a router LSA including all of the interfaces added with the ospfRouter addInterface command. This should be turned off if you are building OSPF topologies with ospfUserLsa commands. (default = true)
			GracefulRestart (bool): Enables the graceful restart Helper Mode function, per the IETF drafts, for the emulated OSPF router. (default = false)
			InterFloodLsUpdateBurstGap (number): The number of FloodlsUpdates sent between each Burst gap.
			LsaRefreshTime (number): The time taken for LSA refresh.
			LsaRetransmitTime (number): The time taken to retransmit LSA.
			MaxFloodLsUpdatesPerBurst (number): The maximum number of FloodLsUpdates sent for each Burst.
			RebuildAdjForLsdbChange (bool): The enableGracefulRestart option must be true. If this option is true, Database Description (DBD) packets will have the R bit set - and the DBD packets will also have the LR (LSDB Resynchronization) bit set in the LLS Extended Options TLV. Out-of-Band Link State Database (OOB LSDB) resynchronization will be used instead of normal LSDB resynchronization, in order to preserve the OSPF adjacency with the neighbor router across OSPF Graceful Restart. (default = false)
			RouterId (str): The router ID for this emulated OSPF router, in IPv4 format.
			StrictLsaChecking (bool): If enabled, the OSPFv2 Restart Helper will terminate Graceful Restart when there are changes to an LSA that would be flooded to, or retransmitted by, the restarting router.
			SupportForRfc3623 (bool): Enables Graceful Restart Helper Mode per RFC 3623 on the emulated OSPF router. (default = false)
			SupportReasonSoftReloadUpgrade (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is a Software Reload or Upgrade on the restarting router. (Planned outage) The default is checked/enabled.
			SupportReasonSoftRestart (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is an OSPFv2 software restart (on the restarting router). (Planned or unplanned outage) The default is checked/enabled.
			SupportReasonSwotchRedundantCntrlProcessor (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is a unplanned switchover to a redundant control processor on the restarting router. (Unplanned outage)
			SupportReasonUnknown (bool): If enabled, Graceful Restart Helper Mode will be supported on this emulated OSPFv2 Router when the restart reason is unknown and unplanned. (Unplanned outage) The default is enabled.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this emulated OSPF router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with matching router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
