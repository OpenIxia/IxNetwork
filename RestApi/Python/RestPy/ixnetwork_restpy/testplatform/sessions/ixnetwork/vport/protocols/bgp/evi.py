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
		"""Label value carried in AD route per EVI. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('adRouteLabel')
	@AdRouteLabel.setter
	def AdRouteLabel(self, value):
		self._set_attribute('adRouteLabel', value)

	@property
	def AutoConfigureRdEvi(self):
		"""If true then RD EVI part of RD is constructed automatically. If false then RD EVI is taken from user in GUI in RD EVI field. Default value is true.

		Returns:
			bool
		"""
		return self._get_attribute('autoConfigureRdEvi')
	@AutoConfigureRdEvi.setter
	def AutoConfigureRdEvi(self, value):
		self._set_attribute('autoConfigureRdEvi', value)

	@property
	def AutoConfigureRdIpAddress(self):
		"""If true then IP address part of RD is constructed automatically and this IP address is taken from loopback address of local BGP peer. If false then IP address is taken from user in GUI in RD IP Address field. Default value is true.

		Returns:
			bool
		"""
		return self._get_attribute('autoConfigureRdIpAddress')
	@AutoConfigureRdIpAddress.setter
	def AutoConfigureRdIpAddress(self, value):
		self._set_attribute('autoConfigureRdIpAddress', value)

	@property
	def Enabled(self):
		"""If true then this EVI is used in EVPN. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExportTargetList(self):
		"""NOT DEFINED

		Returns:
			list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))
		"""
		return self._get_attribute('exportTargetList')
	@ExportTargetList.setter
	def ExportTargetList(self, value):
		self._set_attribute('exportTargetList', value)

	@property
	def ImportTargetList(self):
		"""Used to import the routes received from remote peer. Ixia port needs to have at least one export RT of remote peer as import RT.

		Returns:
			list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))
		"""
		return self._get_attribute('importTargetList')
	@ImportTargetList.setter
	def ImportTargetList(self, value):
		self._set_attribute('importTargetList', value)

	@property
	def IncludePmsiTunnelAttribute(self):
		"""If true then PMSI tunnel attribute is included in Inclusive Multicast Ethernet Tag Route. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('includePmsiTunnelAttribute')
	@IncludePmsiTunnelAttribute.setter
	def IncludePmsiTunnelAttribute(self, value):
		self._set_attribute('includePmsiTunnelAttribute', value)

	@property
	def MplsAssignedUpstreamOrDownStreamLabel(self):
		"""If Use Upstream/Downstream Assigned Label is true then label value mentioned in this field is carried in PMSI tunnel attribute. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('mplsAssignedUpstreamOrDownStreamLabel')
	@MplsAssignedUpstreamOrDownStreamLabel.setter
	def MplsAssignedUpstreamOrDownStreamLabel(self, value):
		self._set_attribute('mplsAssignedUpstreamOrDownStreamLabel', value)

	@property
	def MulticastTunnelType(self):
		"""Drop down of {Ingress Replication, RSVP-TE P2MP, mLDP P2MP}. Default value is Ingress Replication.

		Returns:
			str(rsvpTeP2mp|mldpP2mp|ingressReplication)
		"""
		return self._get_attribute('multicastTunnelType')
	@MulticastTunnelType.setter
	def MulticastTunnelType(self, value):
		self._set_attribute('multicastTunnelType', value)

	@property
	def RdEvi(self):
		"""when Auto Configure RD EVI is false then RD EVI part of RD is taken from here. Default value is zero.

		Returns:
			number
		"""
		return self._get_attribute('rdEvi')
	@RdEvi.setter
	def RdEvi(self, value):
		self._set_attribute('rdEvi', value)

	@property
	def RdIpAddress(self):
		"""when Auto Configure RD IP Address is false then IP address part of RD is taken from here. Default value is all zero.

		Returns:
			str
		"""
		return self._get_attribute('rdIpAddress')
	@RdIpAddress.setter
	def RdIpAddress(self, value):
		self._set_attribute('rdIpAddress', value)

	@property
	def RsvpP2mpId(self):
		"""The P2MP Id represented in IP address format. Default value is all zero.

		Returns:
			str
		"""
		return self._get_attribute('rsvpP2mpId')
	@RsvpP2mpId.setter
	def RsvpP2mpId(self, value):
		self._set_attribute('rsvpP2mpId', value)

	@property
	def RsvpP2mpIdAsNumber(self):
		"""The P2MP Id represented in integer format. Default value is 0.

		Returns:
			number
		"""
		return self._get_attribute('rsvpP2mpIdAsNumber')
	@RsvpP2mpIdAsNumber.setter
	def RsvpP2mpIdAsNumber(self, value):
		self._set_attribute('rsvpP2mpIdAsNumber', value)

	@property
	def RsvpTunnelId(self):
		"""The Tunnel ID value. Default value is 0. Minimum value is 0 and maximum value is 0xFFFF.

		Returns:
			number
		"""
		return self._get_attribute('rsvpTunnelId')
	@RsvpTunnelId.setter
	def RsvpTunnelId(self, value):
		self._set_attribute('rsvpTunnelId', value)

	@property
	def UseUpstreamOrDownStreamAssignedLabel(self):
		"""If true then MPLS assigned Upstream/Downstream label is carried in PMSI tunnel attribute else 0 is carried in PMSI tunnel attribute. Default value is true.

		Returns:
			bool
		"""
		return self._get_attribute('useUpstreamOrDownStreamAssignedLabel')
	@UseUpstreamOrDownStreamAssignedLabel.setter
	def UseUpstreamOrDownStreamAssignedLabel(self, value):
		self._set_attribute('useUpstreamOrDownStreamAssignedLabel', value)

	@property
	def UseV4MappedV6Address(self):
		"""If true then V4 mapped V6 address is used for tunnel identifier in case of Ingress Replication only.

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
			AdRouteLabel (number): Label value carried in AD route per EVI. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			AutoConfigureRdEvi (bool): If true then RD EVI part of RD is constructed automatically. If false then RD EVI is taken from user in GUI in RD EVI field. Default value is true.
			AutoConfigureRdIpAddress (bool): If true then IP address part of RD is constructed automatically and this IP address is taken from loopback address of local BGP peer. If false then IP address is taken from user in GUI in RD IP Address field. Default value is true.
			Enabled (bool): If true then this EVI is used in EVPN. Default value is false.
			ExportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): NOT DEFINED
			ImportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): Used to import the routes received from remote peer. Ixia port needs to have at least one export RT of remote peer as import RT.
			IncludePmsiTunnelAttribute (bool): If true then PMSI tunnel attribute is included in Inclusive Multicast Ethernet Tag Route. Default value is false.
			MplsAssignedUpstreamOrDownStreamLabel (number): If Use Upstream/Downstream Assigned Label is true then label value mentioned in this field is carried in PMSI tunnel attribute. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			MulticastTunnelType (str(rsvpTeP2mp|mldpP2mp|ingressReplication)): Drop down of {Ingress Replication, RSVP-TE P2MP, mLDP P2MP}. Default value is Ingress Replication.
			RdEvi (number): when Auto Configure RD EVI is false then RD EVI part of RD is taken from here. Default value is zero.
			RdIpAddress (str): when Auto Configure RD IP Address is false then IP address part of RD is taken from here. Default value is all zero.
			RsvpP2mpId (str): The P2MP Id represented in IP address format. Default value is all zero.
			RsvpP2mpIdAsNumber (number): The P2MP Id represented in integer format. Default value is 0.
			RsvpTunnelId (number): The Tunnel ID value. Default value is 0. Minimum value is 0 and maximum value is 0xFFFF.
			UseUpstreamOrDownStreamAssignedLabel (bool): If true then MPLS assigned Upstream/Downstream label is carried in PMSI tunnel attribute else 0 is carried in PMSI tunnel attribute. Default value is true.
			UseV4MappedV6Address (bool): If true then V4 mapped V6 address is used for tunnel identifier in case of Ingress Replication only.

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
			AdRouteLabel (number): Label value carried in AD route per EVI. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			AutoConfigureRdEvi (bool): If true then RD EVI part of RD is constructed automatically. If false then RD EVI is taken from user in GUI in RD EVI field. Default value is true.
			AutoConfigureRdIpAddress (bool): If true then IP address part of RD is constructed automatically and this IP address is taken from loopback address of local BGP peer. If false then IP address is taken from user in GUI in RD IP Address field. Default value is true.
			Enabled (bool): If true then this EVI is used in EVPN. Default value is false.
			ExportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): NOT DEFINED
			ImportTargetList (list(dict(arg1:str[as|ip],arg2:number,arg3:str,arg4:number))): Used to import the routes received from remote peer. Ixia port needs to have at least one export RT of remote peer as import RT.
			IncludePmsiTunnelAttribute (bool): If true then PMSI tunnel attribute is included in Inclusive Multicast Ethernet Tag Route. Default value is false.
			MplsAssignedUpstreamOrDownStreamLabel (number): If Use Upstream/Downstream Assigned Label is true then label value mentioned in this field is carried in PMSI tunnel attribute. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			MulticastTunnelType (str(rsvpTeP2mp|mldpP2mp|ingressReplication)): Drop down of {Ingress Replication, RSVP-TE P2MP, mLDP P2MP}. Default value is Ingress Replication.
			RdEvi (number): when Auto Configure RD EVI is false then RD EVI part of RD is taken from here. Default value is zero.
			RdIpAddress (str): when Auto Configure RD IP Address is false then IP address part of RD is taken from here. Default value is all zero.
			RsvpP2mpId (str): The P2MP Id represented in IP address format. Default value is all zero.
			RsvpP2mpIdAsNumber (number): The P2MP Id represented in integer format. Default value is 0.
			RsvpTunnelId (number): The Tunnel ID value. Default value is 0. Minimum value is 0 and maximum value is 0xFFFF.
			UseUpstreamOrDownStreamAssignedLabel (bool): If true then MPLS assigned Upstream/Downstream label is carried in PMSI tunnel attribute else 0 is carried in PMSI tunnel attribute. Default value is true.
			UseV4MappedV6Address (bool): If true then V4 mapped V6 address is used for tunnel identifier in case of Ingress Replication only.

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

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=evi)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AdvertiseAliasing', payload=locals(), response_object=None)

	def WithdrawAliasing(self):
		"""Executes the withdrawAliasing operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=evi)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('WithdrawAliasing', payload=locals(), response_object=None)
