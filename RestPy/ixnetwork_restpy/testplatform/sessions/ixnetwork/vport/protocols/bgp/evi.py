
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


class Evi(Base):
	"""The Evi class encapsulates a user managed evi node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Evi property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'evi'

	def __init__(self, parent):
		super(Evi, self).__init__(parent)

	@property
	def AdInclusiveMulticastRouteAttributes(self):
		"""An instance of the AdInclusiveMulticastRouteAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.adinclusivemulticastrouteattributes.AdInclusiveMulticastRouteAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.adinclusivemulticastrouteattributes import AdInclusiveMulticastRouteAttributes
		return AdInclusiveMulticastRouteAttributes(self)._select()

	@property
	def BroadcastDomains(self):
		"""An instance of the BroadcastDomains class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.broadcastdomains.BroadcastDomains)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.broadcastdomains import BroadcastDomains
		return BroadcastDomains(self)

	@property
	def EviOpaqueTlv(self):
		"""An instance of the EviOpaqueTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.eviopaquetlv.EviOpaqueTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.eviopaquetlv import EviOpaqueTlv
		return EviOpaqueTlv(self)

	@property
	def AdRouteLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('adRouteLabel')
	@AdRouteLabel.setter
	def AdRouteLabel(self, value):
		self._set_attribute('adRouteLabel', value)

	@property
	def AutoConfigureRdEvi(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoConfigureRdEvi')
	@AutoConfigureRdEvi.setter
	def AutoConfigureRdEvi(self, value):
		self._set_attribute('autoConfigureRdEvi', value)

	@property
	def AutoConfigureRdIpAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoConfigureRdIpAddress')
	@AutoConfigureRdIpAddress.setter
	def AutoConfigureRdIpAddress(self, value):
		self._set_attribute('autoConfigureRdIpAddress', value)

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
	def ExportTargetList(self):
		"""

		Returns:
			list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))
		"""
		return self._get_attribute('exportTargetList')
	@ExportTargetList.setter
	def ExportTargetList(self, value):
		self._set_attribute('exportTargetList', value)

	@property
	def ImportTargetList(self):
		"""

		Returns:
			list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))
		"""
		return self._get_attribute('importTargetList')
	@ImportTargetList.setter
	def ImportTargetList(self, value):
		self._set_attribute('importTargetList', value)

	@property
	def IncludePmsiTunnelAttribute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includePmsiTunnelAttribute')
	@IncludePmsiTunnelAttribute.setter
	def IncludePmsiTunnelAttribute(self, value):
		self._set_attribute('includePmsiTunnelAttribute', value)

	@property
	def MplsAssignedUpstreamOrDownStreamLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsAssignedUpstreamOrDownStreamLabel')
	@MplsAssignedUpstreamOrDownStreamLabel.setter
	def MplsAssignedUpstreamOrDownStreamLabel(self, value):
		self._set_attribute('mplsAssignedUpstreamOrDownStreamLabel', value)

	@property
	def MulticastTunnelType(self):
		"""

		Returns:
			str(rsvpTeP2mp|mldpP2mp|ingressReplication)
		"""
		return self._get_attribute('multicastTunnelType')
	@MulticastTunnelType.setter
	def MulticastTunnelType(self, value):
		self._set_attribute('multicastTunnelType', value)

	@property
	def RdEvi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rdEvi')
	@RdEvi.setter
	def RdEvi(self, value):
		self._set_attribute('rdEvi', value)

	@property
	def RdIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rdIpAddress')
	@RdIpAddress.setter
	def RdIpAddress(self, value):
		self._set_attribute('rdIpAddress', value)

	@property
	def RsvpP2mpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rsvpP2mpId')
	@RsvpP2mpId.setter
	def RsvpP2mpId(self, value):
		self._set_attribute('rsvpP2mpId', value)

	@property
	def RsvpP2mpIdAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rsvpP2mpIdAsNumber')
	@RsvpP2mpIdAsNumber.setter
	def RsvpP2mpIdAsNumber(self, value):
		self._set_attribute('rsvpP2mpIdAsNumber', value)

	@property
	def RsvpTunnelId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rsvpTunnelId')
	@RsvpTunnelId.setter
	def RsvpTunnelId(self, value):
		self._set_attribute('rsvpTunnelId', value)

	@property
	def UseUpstreamOrDownStreamAssignedLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useUpstreamOrDownStreamAssignedLabel')
	@UseUpstreamOrDownStreamAssignedLabel.setter
	def UseUpstreamOrDownStreamAssignedLabel(self, value):
		self._set_attribute('useUpstreamOrDownStreamAssignedLabel', value)

	@property
	def UseV4MappedV6Address(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useV4MappedV6Address')
	@UseV4MappedV6Address.setter
	def UseV4MappedV6Address(self, value):
		self._set_attribute('useV4MappedV6Address', value)

	def add(self, AdRouteLabel=None, AutoConfigureRdEvi=None, AutoConfigureRdIpAddress=None, Enabled=None, ExportTargetList=None, ImportTargetList=None, IncludePmsiTunnelAttribute=None, MplsAssignedUpstreamOrDownStreamLabel=None, MulticastTunnelType=None, RdEvi=None, RdIpAddress=None, RsvpP2mpId=None, RsvpP2mpIdAsNumber=None, RsvpTunnelId=None, UseUpstreamOrDownStreamAssignedLabel=None, UseV4MappedV6Address=None):
		"""Adds a new evi node on the server and retrieves it in this instance.

		Args:
			AdRouteLabel (number): 
			AutoConfigureRdEvi (bool): 
			AutoConfigureRdIpAddress (bool): 
			Enabled (bool): 
			ExportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): 
			ImportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): 
			IncludePmsiTunnelAttribute (bool): 
			MplsAssignedUpstreamOrDownStreamLabel (number): 
			MulticastTunnelType (str(rsvpTeP2mp|mldpP2mp|ingressReplication)): 
			RdEvi (number): 
			RdIpAddress (str): 
			RsvpP2mpId (str): 
			RsvpP2mpIdAsNumber (number): 
			RsvpTunnelId (number): 
			UseUpstreamOrDownStreamAssignedLabel (bool): 
			UseV4MappedV6Address (bool): 

		Returns:
			self: This instance with all currently retrieved evi data using find and the newly added evi data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the evi data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdRouteLabel=None, AutoConfigureRdEvi=None, AutoConfigureRdIpAddress=None, Enabled=None, ExportTargetList=None, ImportTargetList=None, IncludePmsiTunnelAttribute=None, MplsAssignedUpstreamOrDownStreamLabel=None, MulticastTunnelType=None, RdEvi=None, RdIpAddress=None, RsvpP2mpId=None, RsvpP2mpIdAsNumber=None, RsvpTunnelId=None, UseUpstreamOrDownStreamAssignedLabel=None, UseV4MappedV6Address=None):
		"""Finds and retrieves evi data from the server.

		All named parameters support regex and can be used to selectively retrieve evi data from the server.
		By default the find method takes no parameters and will retrieve all evi data from the server.

		Args:
			AdRouteLabel (number): 
			AutoConfigureRdEvi (bool): 
			AutoConfigureRdIpAddress (bool): 
			Enabled (bool): 
			ExportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): 
			ImportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): 
			IncludePmsiTunnelAttribute (bool): 
			MplsAssignedUpstreamOrDownStreamLabel (number): 
			MulticastTunnelType (str(rsvpTeP2mp|mldpP2mp|ingressReplication)): 
			RdEvi (number): 
			RdIpAddress (str): 
			RsvpP2mpId (str): 
			RsvpP2mpIdAsNumber (number): 
			RsvpTunnelId (number): 
			UseUpstreamOrDownStreamAssignedLabel (bool): 
			UseV4MappedV6Address (bool): 

		Returns:
			self: This instance with matching evi data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evi data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evi data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AdvertiseAliasing(self):
		"""Executes the advertiseAliasing operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=evi)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AdvertiseAliasing', payload=locals(), response_object=None)

	def WithdrawAliasing(self):
		"""Executes the withdrawAliasing operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=evi)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('WithdrawAliasing', payload=locals(), response_object=None)
