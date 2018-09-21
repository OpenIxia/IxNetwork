from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EthernetSegments(Base):
	"""The EthernetSegments class encapsulates a user managed ethernetSegments node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EthernetSegments property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ethernetSegments'

	def __init__(self, parent):
		super(EthernetSegments, self).__init__(parent)

	@property
	def AdBmacEsRouteAttributes(self):
		"""An instance of the AdBmacEsRouteAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.adbmacesrouteattributes.AdBmacEsRouteAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.adbmacesrouteattributes import AdBmacEsRouteAttributes
		return AdBmacEsRouteAttributes(self)._select()

	@property
	def BMacMappedIp(self):
		"""An instance of the BMacMappedIp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.bmacmappedip.BMacMappedIp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.bmacmappedip import BMacMappedIp
		return BMacMappedIp(self)

	@property
	def Evi(self):
		"""An instance of the Evi class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evi.Evi)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evi import Evi
		return Evi(self)

	@property
	def AutoConfigureEsImport(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('autoConfigureEsImport')
	@AutoConfigureEsImport.setter
	def AutoConfigureEsImport(self, value):
		self._set_attribute('autoConfigureEsImport', value)

	@property
	def BMacPrefix(self):
		"""B-MAC address as a prefix where the MAC address length field is set to the length of the prefix. This provides the ability to aggregate MAC addresses if the deployment environment supports that. By default a unique B-MAC is constructed per ethernet segment. it can be changed to any value but multicast and broadcast addresses are not used.

		Returns:
			str
		"""
		return self._get_attribute('bMacPrefix')
	@BMacPrefix.setter
	def BMacPrefix(self, value):
		self._set_attribute('bMacPrefix', value)

	@property
	def BMacPrefixLength(self):
		"""The MAC address length field is typically set to 48. However this length value can be changed to specify the MAC address as a prefix; in which case, the MAC address length field is set to the length of the prefix. This provides the ability to aggregate MAC addresses if the deployment environment supports that. Default value is 48. Minimum value is 0 and maximum value is 48.

		Returns:
			number
		"""
		return self._get_attribute('bMacPrefixLength')
	@BMacPrefixLength.setter
	def BMacPrefixLength(self, value):
		self._set_attribute('bMacPrefixLength', value)

	@property
	def DfElectionMethod(self):
		"""This is a read only field. user can not change the value of this field. This is just to show that IxNetwork is using Service Carving method for DF election.

		Returns:
			str(serviceCarving)
		"""
		return self._get_attribute('dfElectionMethod')
	@DfElectionMethod.setter
	def DfElectionMethod(self, value):
		self._set_attribute('dfElectionMethod', value)

	@property
	def DfElectionTimer(self):
		"""Time interval in second to wait for DF election process to complete. Default value is 3 seconds. Minimum value is 1 second and maximum value is 300 seconds.

		Returns:
			number
		"""
		return self._get_attribute('dfElectionTimer')
	@DfElectionTimer.setter
	def DfElectionTimer(self, value):
		self._set_attribute('dfElectionTimer', value)

	@property
	def EnableActiveStandby(self):
		"""If true then this ethernet segment operates in active-standby mode. If false then this ethernet segment operates in all-active mode. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('enableActiveStandby')
	@EnableActiveStandby.setter
	def EnableActiveStandby(self, value):
		self._set_attribute('enableActiveStandby', value)

	@property
	def EnableRootLeaf(self):
		"""If true then ESI label is associated with a leaf side. If false then ESI label is associated with a root side. Default value is true.

		Returns:
			bool
		"""
		return self._get_attribute('enableRootLeaf')
	@EnableRootLeaf.setter
	def EnableRootLeaf(self, value):
		self._set_attribute('enableRootLeaf', value)

	@property
	def EnableSecondLabel(self):
		"""If true then second EVPN label is inserted in label stack for ES route, AD per segment route.

		Returns:
			bool
		"""
		return self._get_attribute('enableSecondLabel')
	@EnableSecondLabel.setter
	def EnableSecondLabel(self, value):
		self._set_attribute('enableSecondLabel', value)

	@property
	def Enabled(self):
		"""If true, ethernet segment is enabled and is used in evpn. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EsImport(self):
		"""When Auto Configure ES-Import is false then user has to put ES-Import here. Default value is 0x00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('esImport')
	@EsImport.setter
	def EsImport(self, value):
		self._set_attribute('esImport', value)

	@property
	def Esi(self):
		"""Ethernet Segment Identifier (ESI) which is encoded as a ten octets integer. Default value is 0x00 00 00 00 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('esi')
	@Esi.setter
	def Esi(self, value):
		self._set_attribute('esi', value)

	@property
	def EsiLabel(self):
		"""Label value carried in ESI Label Extended Community in AD route per segment. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('esiLabel')
	@EsiLabel.setter
	def EsiLabel(self, value):
		self._set_attribute('esiLabel', value)

	@property
	def FirstLabel(self):
		"""First EVPN label in label stack for ES route, AD per segment route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('firstLabel')
	@FirstLabel.setter
	def FirstLabel(self, value):
		self._set_attribute('firstLabel', value)

	@property
	def IncludeMacMobilityExtendedCommunity(self):
		"""If true then MAC mobility is performed in EVPN mode. If false then MAC mobility is not performed even if duplicate MAC address is found from remote PE.

		Returns:
			bool
		"""
		return self._get_attribute('includeMacMobilityExtendedCommunity')
	@IncludeMacMobilityExtendedCommunity.setter
	def IncludeMacMobilityExtendedCommunity(self, value):
		self._set_attribute('includeMacMobilityExtendedCommunity', value)

	@property
	def SecondLabel(self):
		"""Second EVPN label in label stack for ES route, AD per segment route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('secondLabel')
	@SecondLabel.setter
	def SecondLabel(self, value):
		self._set_attribute('secondLabel', value)

	@property
	def SupportFastConvergence(self):
		"""If true then fast convergence is performed. Default value is true.

		Returns:
			bool
		"""
		return self._get_attribute('supportFastConvergence')
	@SupportFastConvergence.setter
	def SupportFastConvergence(self, value):
		self._set_attribute('supportFastConvergence', value)

	@property
	def SupportMultiHomedEsAutoDiscovery(self):
		"""If true then auto discovery between multihomed PEs is performed.

		Returns:
			bool
		"""
		return self._get_attribute('supportMultiHomedEsAutoDiscovery')
	@SupportMultiHomedEsAutoDiscovery.setter
	def SupportMultiHomedEsAutoDiscovery(self, value):
		self._set_attribute('supportMultiHomedEsAutoDiscovery', value)

	@property
	def TypeOfEthernetVpn(self):
		"""Type of ethernet vpn. It can be either EVPN or PBB-EVPN. Default mode is PBB-EVPN.

		Returns:
			str(evpn|pbbEvpn)
		"""
		return self._get_attribute('typeOfEthernetVpn')
	@TypeOfEthernetVpn.setter
	def TypeOfEthernetVpn(self, value):
		self._set_attribute('typeOfEthernetVpn', value)

	@property
	def UseSameSequenceNumber(self):
		"""If true then same sequence number is used in MAC Mobility Extended Community for all MAC route to flush the remote C-MAC forwarding table. If false then subsequent C-MAC route uses unique sequence number in MAC Mobility Extended Community.

		Returns:
			bool
		"""
		return self._get_attribute('useSameSequenceNumber')
	@UseSameSequenceNumber.setter
	def UseSameSequenceNumber(self, value):
		self._set_attribute('useSameSequenceNumber', value)

	def add(self, AutoConfigureEsImport=None, BMacPrefix=None, BMacPrefixLength=None, DfElectionMethod=None, DfElectionTimer=None, EnableActiveStandby=None, EnableRootLeaf=None, EnableSecondLabel=None, Enabled=None, EsImport=None, Esi=None, EsiLabel=None, FirstLabel=None, IncludeMacMobilityExtendedCommunity=None, SecondLabel=None, SupportFastConvergence=None, SupportMultiHomedEsAutoDiscovery=None, TypeOfEthernetVpn=None, UseSameSequenceNumber=None):
		"""Adds a new ethernetSegments node on the server and retrieves it in this instance.

		Args:
			AutoConfigureEsImport (bool): NOT DEFINED
			BMacPrefix (str): B-MAC address as a prefix where the MAC address length field is set to the length of the prefix. This provides the ability to aggregate MAC addresses if the deployment environment supports that. By default a unique B-MAC is constructed per ethernet segment. it can be changed to any value but multicast and broadcast addresses are not used.
			BMacPrefixLength (number): The MAC address length field is typically set to 48. However this length value can be changed to specify the MAC address as a prefix; in which case, the MAC address length field is set to the length of the prefix. This provides the ability to aggregate MAC addresses if the deployment environment supports that. Default value is 48. Minimum value is 0 and maximum value is 48.
			DfElectionMethod (str(serviceCarving)): This is a read only field. user can not change the value of this field. This is just to show that IxNetwork is using Service Carving method for DF election.
			DfElectionTimer (number): Time interval in second to wait for DF election process to complete. Default value is 3 seconds. Minimum value is 1 second and maximum value is 300 seconds.
			EnableActiveStandby (bool): If true then this ethernet segment operates in active-standby mode. If false then this ethernet segment operates in all-active mode. Default value is false.
			EnableRootLeaf (bool): If true then ESI label is associated with a leaf side. If false then ESI label is associated with a root side. Default value is true.
			EnableSecondLabel (bool): If true then second EVPN label is inserted in label stack for ES route, AD per segment route.
			Enabled (bool): If true, ethernet segment is enabled and is used in evpn. Default value is false.
			EsImport (str): When Auto Configure ES-Import is false then user has to put ES-Import here. Default value is 0x00 00 00 00 00 00.
			Esi (str): Ethernet Segment Identifier (ESI) which is encoded as a ten octets integer. Default value is 0x00 00 00 00 00 00 00 00 00 00.
			EsiLabel (number): Label value carried in ESI Label Extended Community in AD route per segment. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			FirstLabel (number): First EVPN label in label stack for ES route, AD per segment route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			IncludeMacMobilityExtendedCommunity (bool): If true then MAC mobility is performed in EVPN mode. If false then MAC mobility is not performed even if duplicate MAC address is found from remote PE.
			SecondLabel (number): Second EVPN label in label stack for ES route, AD per segment route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			SupportFastConvergence (bool): If true then fast convergence is performed. Default value is true.
			SupportMultiHomedEsAutoDiscovery (bool): If true then auto discovery between multihomed PEs is performed.
			TypeOfEthernetVpn (str(evpn|pbbEvpn)): Type of ethernet vpn. It can be either EVPN or PBB-EVPN. Default mode is PBB-EVPN.
			UseSameSequenceNumber (bool): If true then same sequence number is used in MAC Mobility Extended Community for all MAC route to flush the remote C-MAC forwarding table. If false then subsequent C-MAC route uses unique sequence number in MAC Mobility Extended Community.

		Returns:
			self: This instance with all currently retrieved ethernetSegments data using find and the newly added ethernetSegments data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ethernetSegments data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoConfigureEsImport=None, BMacPrefix=None, BMacPrefixLength=None, DfElectionMethod=None, DfElectionTimer=None, EnableActiveStandby=None, EnableRootLeaf=None, EnableSecondLabel=None, Enabled=None, EsImport=None, Esi=None, EsiLabel=None, FirstLabel=None, IncludeMacMobilityExtendedCommunity=None, SecondLabel=None, SupportFastConvergence=None, SupportMultiHomedEsAutoDiscovery=None, TypeOfEthernetVpn=None, UseSameSequenceNumber=None):
		"""Finds and retrieves ethernetSegments data from the server.

		All named parameters support regex and can be used to selectively retrieve ethernetSegments data from the server.
		By default the find method takes no parameters and will retrieve all ethernetSegments data from the server.

		Args:
			AutoConfigureEsImport (bool): NOT DEFINED
			BMacPrefix (str): B-MAC address as a prefix where the MAC address length field is set to the length of the prefix. This provides the ability to aggregate MAC addresses if the deployment environment supports that. By default a unique B-MAC is constructed per ethernet segment. it can be changed to any value but multicast and broadcast addresses are not used.
			BMacPrefixLength (number): The MAC address length field is typically set to 48. However this length value can be changed to specify the MAC address as a prefix; in which case, the MAC address length field is set to the length of the prefix. This provides the ability to aggregate MAC addresses if the deployment environment supports that. Default value is 48. Minimum value is 0 and maximum value is 48.
			DfElectionMethod (str(serviceCarving)): This is a read only field. user can not change the value of this field. This is just to show that IxNetwork is using Service Carving method for DF election.
			DfElectionTimer (number): Time interval in second to wait for DF election process to complete. Default value is 3 seconds. Minimum value is 1 second and maximum value is 300 seconds.
			EnableActiveStandby (bool): If true then this ethernet segment operates in active-standby mode. If false then this ethernet segment operates in all-active mode. Default value is false.
			EnableRootLeaf (bool): If true then ESI label is associated with a leaf side. If false then ESI label is associated with a root side. Default value is true.
			EnableSecondLabel (bool): If true then second EVPN label is inserted in label stack for ES route, AD per segment route.
			Enabled (bool): If true, ethernet segment is enabled and is used in evpn. Default value is false.
			EsImport (str): When Auto Configure ES-Import is false then user has to put ES-Import here. Default value is 0x00 00 00 00 00 00.
			Esi (str): Ethernet Segment Identifier (ESI) which is encoded as a ten octets integer. Default value is 0x00 00 00 00 00 00 00 00 00 00.
			EsiLabel (number): Label value carried in ESI Label Extended Community in AD route per segment. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			FirstLabel (number): First EVPN label in label stack for ES route, AD per segment route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			IncludeMacMobilityExtendedCommunity (bool): If true then MAC mobility is performed in EVPN mode. If false then MAC mobility is not performed even if duplicate MAC address is found from remote PE.
			SecondLabel (number): Second EVPN label in label stack for ES route, AD per segment route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF.
			SupportFastConvergence (bool): If true then fast convergence is performed. Default value is true.
			SupportMultiHomedEsAutoDiscovery (bool): If true then auto discovery between multihomed PEs is performed.
			TypeOfEthernetVpn (str(evpn|pbbEvpn)): Type of ethernet vpn. It can be either EVPN or PBB-EVPN. Default mode is PBB-EVPN.
			UseSameSequenceNumber (bool): If true then same sequence number is used in MAC Mobility Extended Community for all MAC route to flush the remote C-MAC forwarding table. If false then subsequent C-MAC route uses unique sequence number in MAC Mobility Extended Community.

		Returns:
			self: This instance with matching ethernetSegments data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ethernetSegments data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ethernetSegments data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def FlushRemoteCmacForwardingTable(self):
		"""Executes the flushRemoteCmacForwardingTable operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ethernetSegments)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FlushRemoteCmacForwardingTable', payload=locals(), response_object=None)
