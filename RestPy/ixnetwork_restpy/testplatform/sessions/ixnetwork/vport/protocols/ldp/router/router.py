
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
	def AdvFecRange(self):
		"""An instance of the AdvFecRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.advfecrange.advfecrange.AdvFecRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.advfecrange.advfecrange import AdvFecRange
		return AdvFecRange(self)

	@property
	def IncludeIpFecRange(self):
		"""An instance of the IncludeIpFecRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.includeipfecrange.includeipfecrange.IncludeIpFecRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.includeipfecrange.includeipfecrange import IncludeIpFecRange
		return IncludeIpFecRange(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.interface import Interface
		return Interface(self)

	@property
	def L2Interface(self):
		"""An instance of the L2Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.l2interface.l2interface.L2Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.l2interface.l2interface import L2Interface
		return L2Interface(self)

	@property
	def LearnedBgpAdVplsLabels(self):
		"""An instance of the LearnedBgpAdVplsLabels class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.learnedbgpadvplslabels.learnedbgpadvplslabels.LearnedBgpAdVplsLabels)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.learnedbgpadvplslabels.learnedbgpadvplslabels import LearnedBgpAdVplsLabels
		return LearnedBgpAdVplsLabels(self)

	@property
	def MulticastLeafRange(self):
		"""An instance of the MulticastLeafRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastleafrange.multicastleafrange.MulticastLeafRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastleafrange.multicastleafrange import MulticastLeafRange
		return MulticastLeafRange(self)

	@property
	def MulticastRootRange(self):
		"""An instance of the MulticastRootRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.multicastrootrange.MulticastRootRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.multicastrootrange import MulticastRootRange
		return MulticastRootRange(self)

	@property
	def ReqFecRange(self):
		"""An instance of the ReqFecRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.reqfecrange.reqfecrange.ReqFecRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.reqfecrange.reqfecrange import ReqFecRange
		return ReqFecRange(self)

	@property
	def EnableBfdMplsLearnedLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdMplsLearnedLsp')
	@EnableBfdMplsLearnedLsp.setter
	def EnableBfdMplsLearnedLsp(self, value):
		self._set_attribute('enableBfdMplsLearnedLsp', value)

	@property
	def EnableFilterFec(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFilterFec')
	@EnableFilterFec.setter
	def EnableFilterFec(self, value):
		self._set_attribute('enableFilterFec', value)

	@property
	def EnableGracefulRestart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestart')
	@EnableGracefulRestart.setter
	def EnableGracefulRestart(self, value):
		self._set_attribute('enableGracefulRestart', value)

	@property
	def EnableLspPingLearnedLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPingLearnedLsp')
	@EnableLspPingLearnedLsp.setter
	def EnableLspPingLearnedLsp(self, value):
		self._set_attribute('enableLspPingLearnedLsp', value)

	@property
	def EnableOverrideRbit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOverrideRbit')
	@EnableOverrideRbit.setter
	def EnableOverrideRbit(self, value):
		self._set_attribute('enableOverrideRbit', value)

	@property
	def EnableP2mpCapabilty(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableP2mpCapabilty')
	@EnableP2mpCapabilty.setter
	def EnableP2mpCapabilty(self, value):
		self._set_attribute('enableP2mpCapabilty', value)

	@property
	def EnablePduRateControl(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePduRateControl')
	@EnablePduRateControl.setter
	def EnablePduRateControl(self, value):
		self._set_attribute('enablePduRateControl', value)

	@property
	def EnableVcFecs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVcFecs')
	@EnableVcFecs.setter
	def EnableVcFecs(self, value):
		self._set_attribute('enableVcFecs', value)

	@property
	def EnableVcGroupMatch(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVcGroupMatch')
	@EnableVcGroupMatch.setter
	def EnableVcGroupMatch(self, value):
		self._set_attribute('enableVcGroupMatch', value)

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
	def InterPduGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interPduGap')
	@InterPduGap.setter
	def InterPduGap(self, value):
		self._set_attribute('interPduGap', value)

	@property
	def IsBgpAdVplsLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isBgpAdVplsLearnedInfoRefreshed')

	@property
	def ReconnectTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('reconnectTime')
	@ReconnectTime.setter
	def ReconnectTime(self, value):
		self._set_attribute('reconnectTime', value)

	@property
	def RecoveryTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recoveryTime')
	@RecoveryTime.setter
	def RecoveryTime(self, value):
		self._set_attribute('recoveryTime', value)

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
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def TransportAddress(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('transportAddress')
	@TransportAddress.setter
	def TransportAddress(self, value):
		self._set_attribute('transportAddress', value)

	@property
	def UseTransportAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useTransportAddress')
	@UseTransportAddress.setter
	def UseTransportAddress(self, value):
		self._set_attribute('useTransportAddress', value)

	def add(self, EnableBfdMplsLearnedLsp=None, EnableFilterFec=None, EnableGracefulRestart=None, EnableLspPingLearnedLsp=None, EnableOverrideRbit=None, EnableP2mpCapabilty=None, EnablePduRateControl=None, EnableVcFecs=None, EnableVcGroupMatch=None, Enabled=None, InterPduGap=None, ReconnectTime=None, RecoveryTime=None, RouterId=None, TrafficGroupId=None, TransportAddress=None, UseTransportAddress=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			EnableBfdMplsLearnedLsp (bool): 
			EnableFilterFec (bool): 
			EnableGracefulRestart (bool): 
			EnableLspPingLearnedLsp (bool): 
			EnableOverrideRbit (bool): 
			EnableP2mpCapabilty (bool): 
			EnablePduRateControl (bool): 
			EnableVcFecs (bool): 
			EnableVcGroupMatch (bool): 
			Enabled (bool): 
			InterPduGap (number): 
			ReconnectTime (number): 
			RecoveryTime (number): 
			RouterId (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TransportAddress (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			UseTransportAddress (bool): 

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

	def find(self, EnableBfdMplsLearnedLsp=None, EnableFilterFec=None, EnableGracefulRestart=None, EnableLspPingLearnedLsp=None, EnableOverrideRbit=None, EnableP2mpCapabilty=None, EnablePduRateControl=None, EnableVcFecs=None, EnableVcGroupMatch=None, Enabled=None, InterPduGap=None, IsBgpAdVplsLearnedInfoRefreshed=None, ReconnectTime=None, RecoveryTime=None, RouterId=None, TrafficGroupId=None, TransportAddress=None, UseTransportAddress=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			EnableBfdMplsLearnedLsp (bool): 
			EnableFilterFec (bool): 
			EnableGracefulRestart (bool): 
			EnableLspPingLearnedLsp (bool): 
			EnableOverrideRbit (bool): 
			EnableP2mpCapabilty (bool): 
			EnablePduRateControl (bool): 
			EnableVcFecs (bool): 
			EnableVcGroupMatch (bool): 
			Enabled (bool): 
			InterPduGap (number): 
			IsBgpAdVplsLearnedInfoRefreshed (bool): 
			ReconnectTime (number): 
			RecoveryTime (number): 
			RouterId (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TransportAddress (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			UseTransportAddress (bool): 

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

	def RefreshBgpAdVplsLearnedInfo(self):
		"""Executes the refreshBgpAdVplsLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshBgpAdVplsLearnedInfo', payload=locals(), response_object=None)
