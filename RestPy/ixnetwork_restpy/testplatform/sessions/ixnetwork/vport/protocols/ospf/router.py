
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedLsa')
	@DiscardLearnedLsa.setter
	def DiscardLearnedLsa(self, value):
		self._set_attribute('discardLearnedLsa', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GenerateRouterLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('generateRouterLsa')
	@GenerateRouterLsa.setter
	def GenerateRouterLsa(self, value):
		self._set_attribute('generateRouterLsa', value)

	@property
	def GracefulRestart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('gracefulRestart')
	@GracefulRestart.setter
	def GracefulRestart(self, value):
		self._set_attribute('gracefulRestart', value)

	@property
	def InterFloodLsUpdateBurstGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interFloodLsUpdateBurstGap')
	@InterFloodLsUpdateBurstGap.setter
	def InterFloodLsUpdateBurstGap(self, value):
		self._set_attribute('interFloodLsUpdateBurstGap', value)

	@property
	def LsaRefreshTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lsaRefreshTime')
	@LsaRefreshTime.setter
	def LsaRefreshTime(self, value):
		self._set_attribute('lsaRefreshTime', value)

	@property
	def LsaRetransmitTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lsaRetransmitTime')
	@LsaRetransmitTime.setter
	def LsaRetransmitTime(self, value):
		self._set_attribute('lsaRetransmitTime', value)

	@property
	def MaxFloodLsUpdatesPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxFloodLsUpdatesPerBurst')
	@MaxFloodLsUpdatesPerBurst.setter
	def MaxFloodLsUpdatesPerBurst(self, value):
		self._set_attribute('maxFloodLsUpdatesPerBurst', value)

	@property
	def RebuildAdjForLsdbChange(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rebuildAdjForLsdbChange')
	@RebuildAdjForLsdbChange.setter
	def RebuildAdjForLsdbChange(self, value):
		self._set_attribute('rebuildAdjForLsdbChange', value)

	@property
	def RouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def StrictLsaChecking(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('strictLsaChecking')
	@StrictLsaChecking.setter
	def StrictLsaChecking(self, value):
		self._set_attribute('strictLsaChecking', value)

	@property
	def SupportForRfc3623(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportForRfc3623')
	@SupportForRfc3623.setter
	def SupportForRfc3623(self, value):
		self._set_attribute('supportForRfc3623', value)

	@property
	def SupportReasonSoftReloadUpgrade(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonSoftReloadUpgrade')
	@SupportReasonSoftReloadUpgrade.setter
	def SupportReasonSoftReloadUpgrade(self, value):
		self._set_attribute('supportReasonSoftReloadUpgrade', value)

	@property
	def SupportReasonSoftRestart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonSoftRestart')
	@SupportReasonSoftRestart.setter
	def SupportReasonSoftRestart(self, value):
		self._set_attribute('supportReasonSoftRestart', value)

	@property
	def SupportReasonSwotchRedundantCntrlProcessor(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonSwotchRedundantCntrlProcessor')
	@SupportReasonSwotchRedundantCntrlProcessor.setter
	def SupportReasonSwotchRedundantCntrlProcessor(self, value):
		self._set_attribute('supportReasonSwotchRedundantCntrlProcessor', value)

	@property
	def SupportReasonUnknown(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportReasonUnknown')
	@SupportReasonUnknown.setter
	def SupportReasonUnknown(self, value):
		self._set_attribute('supportReasonUnknown', value)

	@property
	def TrafficGroupId(self):
		"""

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
			DiscardLearnedLsa (bool): 
			Enabled (bool): 
			GenerateRouterLsa (bool): 
			GracefulRestart (bool): 
			InterFloodLsUpdateBurstGap (number): 
			LsaRefreshTime (number): 
			LsaRetransmitTime (number): 
			MaxFloodLsUpdatesPerBurst (number): 
			RebuildAdjForLsdbChange (bool): 
			RouterId (str): 
			StrictLsaChecking (bool): 
			SupportForRfc3623 (bool): 
			SupportReasonSoftReloadUpgrade (bool): 
			SupportReasonSoftRestart (bool): 
			SupportReasonSwotchRedundantCntrlProcessor (bool): 
			SupportReasonUnknown (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

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
			DiscardLearnedLsa (bool): 
			Enabled (bool): 
			GenerateRouterLsa (bool): 
			GracefulRestart (bool): 
			InterFloodLsUpdateBurstGap (number): 
			LsaRefreshTime (number): 
			LsaRetransmitTime (number): 
			MaxFloodLsUpdatesPerBurst (number): 
			RebuildAdjForLsdbChange (bool): 
			RouterId (str): 
			StrictLsaChecking (bool): 
			SupportForRfc3623 (bool): 
			SupportReasonSoftReloadUpgrade (bool): 
			SupportReasonSoftRestart (bool): 
			SupportReasonSwotchRedundantCntrlProcessor (bool): 
			SupportReasonUnknown (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

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
