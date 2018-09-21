from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CMacRange(Base):
	"""The CMacRange class encapsulates a user managed cMacRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CMacRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'cMacRange'

	def __init__(self, parent):
		super(CMacRange, self).__init__(parent)

	@property
	def CMacMappedIp(self):
		"""An instance of the CMacMappedIp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacmappedip.CMacMappedIp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacmappedip import CMacMappedIp
		return CMacMappedIp(self)

	@property
	def CmacRouteAttributes(self):
		"""An instance of the CmacRouteAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacrouteattributes.CmacRouteAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacrouteattributes import CmacRouteAttributes
		return CmacRouteAttributes(self)._select()

	@property
	def CmacPrefixLength(self):
		"""Prefix length of C-MAC address. Default value is 48. Minimum value is 0 and maximum value is 48.

		Returns:
			number
		"""
		return self._get_attribute('cmacPrefixLength')
	@CmacPrefixLength.setter
	def CmacPrefixLength(self, value):
		self._set_attribute('cmacPrefixLength', value)

	@property
	def CvlanId(self):
		"""C-VLAN Identifier used in EVPN traffic. Default value is 1. Minimum value is 0 and maximum value is 4095.

		Returns:
			number
		"""
		return self._get_attribute('cvlanId')
	@CvlanId.setter
	def CvlanId(self, value):
		self._set_attribute('cvlanId', value)

	@property
	def CvlanPriority(self):
		"""C-VLAN Priority used in EVPN traffic. Default value is 0. Minimum value is 0 and maximum value is 7.

		Returns:
			number
		"""
		return self._get_attribute('cvlanPriority')
	@CvlanPriority.setter
	def CvlanPriority(self, value):
		self._set_attribute('cvlanPriority', value)

	@property
	def CvlanTpId(self):
		"""C-VLAN TPID used in EVPN traffic. Default value is 0x8100. User can select any one of {0x8100, 0x9100, 0x9200, 0x88A8}.

		Returns:
			str(0x8100|0x9100|0x9200|0x88A8)
		"""
		return self._get_attribute('cvlanTpId')
	@CvlanTpId.setter
	def CvlanTpId(self, value):
		self._set_attribute('cvlanTpId', value)

	@property
	def EnableCvlan(self):
		"""If true then C-VLAN is used in EVPN traffic. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('enableCvlan')
	@EnableCvlan.setter
	def EnableCvlan(self, value):
		self._set_attribute('enableCvlan', value)

	@property
	def EnableSecondLabel(self):
		"""If true then second label is inserted in the EVPN label stack. Default value is false. Label value is obtained for all macs in the same way of first label.

		Returns:
			bool
		"""
		return self._get_attribute('enableSecondLabel')
	@EnableSecondLabel.setter
	def EnableSecondLabel(self, value):
		self._set_attribute('enableSecondLabel', value)

	@property
	def EnableSvlan(self):
		"""If true then S-VLAN is used in EVPN traffic. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('enableSvlan')
	@EnableSvlan.setter
	def EnableSvlan(self, value):
		self._set_attribute('enableSvlan', value)

	@property
	def Enabled(self):
		"""If true then this C-MAC range is used in EVPN.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstLabelStart(self):
		"""First EVPN label in label stack for MAC route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF. This label value is used in first mac of this mac range. If Label mode is fixed then same label value is used for all mac in this mac range. If label mode is Increment then label value for subsequent mac is obtained by adding the label step value to the first label value.

		Returns:
			number
		"""
		return self._get_attribute('firstLabelStart')
	@FirstLabelStart.setter
	def FirstLabelStart(self, value):
		self._set_attribute('firstLabelStart', value)

	@property
	def LabelMode(self):
		"""It is used to get the label value of subsequent macs in the range by adding this value to the first label value. Default value is Increment. It can be either Fixed or Increment.

		Returns:
			str(fixed|increment)
		"""
		return self._get_attribute('labelMode')
	@LabelMode.setter
	def LabelMode(self, value):
		self._set_attribute('labelMode', value)

	@property
	def LabelStep(self):
		"""Label step to get the label value of subsequent macs in the mac range. Default value is 1. Minimum value is 0 and maximum value is 0xFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('labelStep')
	@LabelStep.setter
	def LabelStep(self, value):
		self._set_attribute('labelStep', value)

	@property
	def NoOfCmacs(self):
		"""Number of C-MACs in this mac range. Default value is 1. Minimum value is 1 and maximum value is 0xFFFFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('noOfCmacs')
	@NoOfCmacs.setter
	def NoOfCmacs(self, value):
		self._set_attribute('noOfCmacs', value)

	@property
	def SecondLabelStart(self):
		"""Second EVPN label in label stack for MAC route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF. This label value is used in first mac of this mac range. If Label mode is fixed then same label value is used for all mac in this mac range. If label mode is Increment then label value for subsequent mac is obtained by adding the label step value to the second label value.

		Returns:
			number
		"""
		return self._get_attribute('secondLabelStart')
	@SecondLabelStart.setter
	def SecondLabelStart(self, value):
		self._set_attribute('secondLabelStart', value)

	@property
	def StartCmacPrefix(self):
		"""Start mac address of this range. Default value is 0x00 00 00 00 00 01.

		Returns:
			str
		"""
		return self._get_attribute('startCmacPrefix')
	@StartCmacPrefix.setter
	def StartCmacPrefix(self, value):
		self._set_attribute('startCmacPrefix', value)

	@property
	def SvlanId(self):
		"""S-VLAN Identifier used in EVPN traffic. Default value is 1. Minimum value is 0 and maximum value is 4095.

		Returns:
			number
		"""
		return self._get_attribute('svlanId')
	@SvlanId.setter
	def SvlanId(self, value):
		self._set_attribute('svlanId', value)

	@property
	def SvlanPriority(self):
		"""S-VLAN Priority used in EVPN traffic. Default value is 0. Minimum value is 0 and maximum value is 7.

		Returns:
			number
		"""
		return self._get_attribute('svlanPriority')
	@SvlanPriority.setter
	def SvlanPriority(self, value):
		self._set_attribute('svlanPriority', value)

	@property
	def SvlanTpId(self):
		"""S-VLAN TPID used in EVPN traffic. Default value is 0x8100. User can select any one of {0x8100, 0x9100, 0x9200, 0x88A8}.

		Returns:
			str(0x8100|0x9100|0x9200|0x88A8)
		"""
		return self._get_attribute('svlanTpId')
	@SvlanTpId.setter
	def SvlanTpId(self, value):
		self._set_attribute('svlanTpId', value)

	@property
	def UseSameSequenceNumber(self):
		"""If true then same sequence number is used in MAC Mobility Extended Community for all MAC routes for mac mobility. If false then subsequent C-MAC route uses unique sequence number in MAC Mobility Extended Community.

		Returns:
			bool
		"""
		return self._get_attribute('useSameSequenceNumber')
	@UseSameSequenceNumber.setter
	def UseSameSequenceNumber(self, value):
		self._set_attribute('useSameSequenceNumber', value)

	def add(self, CmacPrefixLength=None, CvlanId=None, CvlanPriority=None, CvlanTpId=None, EnableCvlan=None, EnableSecondLabel=None, EnableSvlan=None, Enabled=None, FirstLabelStart=None, LabelMode=None, LabelStep=None, NoOfCmacs=None, SecondLabelStart=None, StartCmacPrefix=None, SvlanId=None, SvlanPriority=None, SvlanTpId=None, UseSameSequenceNumber=None):
		"""Adds a new cMacRange node on the server and retrieves it in this instance.

		Args:
			CmacPrefixLength (number): Prefix length of C-MAC address. Default value is 48. Minimum value is 0 and maximum value is 48.
			CvlanId (number): C-VLAN Identifier used in EVPN traffic. Default value is 1. Minimum value is 0 and maximum value is 4095.
			CvlanPriority (number): C-VLAN Priority used in EVPN traffic. Default value is 0. Minimum value is 0 and maximum value is 7.
			CvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): C-VLAN TPID used in EVPN traffic. Default value is 0x8100. User can select any one of {0x8100, 0x9100, 0x9200, 0x88A8}.
			EnableCvlan (bool): If true then C-VLAN is used in EVPN traffic. Default value is false.
			EnableSecondLabel (bool): If true then second label is inserted in the EVPN label stack. Default value is false. Label value is obtained for all macs in the same way of first label.
			EnableSvlan (bool): If true then S-VLAN is used in EVPN traffic. Default value is false.
			Enabled (bool): If true then this C-MAC range is used in EVPN.
			FirstLabelStart (number): First EVPN label in label stack for MAC route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF. This label value is used in first mac of this mac range. If Label mode is fixed then same label value is used for all mac in this mac range. If label mode is Increment then label value for subsequent mac is obtained by adding the label step value to the first label value.
			LabelMode (str(fixed|increment)): It is used to get the label value of subsequent macs in the range by adding this value to the first label value. Default value is Increment. It can be either Fixed or Increment.
			LabelStep (number): Label step to get the label value of subsequent macs in the mac range. Default value is 1. Minimum value is 0 and maximum value is 0xFFFFF.
			NoOfCmacs (number): Number of C-MACs in this mac range. Default value is 1. Minimum value is 1 and maximum value is 0xFFFFFFFF.
			SecondLabelStart (number): Second EVPN label in label stack for MAC route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF. This label value is used in first mac of this mac range. If Label mode is fixed then same label value is used for all mac in this mac range. If label mode is Increment then label value for subsequent mac is obtained by adding the label step value to the second label value.
			StartCmacPrefix (str): Start mac address of this range. Default value is 0x00 00 00 00 00 01.
			SvlanId (number): S-VLAN Identifier used in EVPN traffic. Default value is 1. Minimum value is 0 and maximum value is 4095.
			SvlanPriority (number): S-VLAN Priority used in EVPN traffic. Default value is 0. Minimum value is 0 and maximum value is 7.
			SvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): S-VLAN TPID used in EVPN traffic. Default value is 0x8100. User can select any one of {0x8100, 0x9100, 0x9200, 0x88A8}.
			UseSameSequenceNumber (bool): If true then same sequence number is used in MAC Mobility Extended Community for all MAC routes for mac mobility. If false then subsequent C-MAC route uses unique sequence number in MAC Mobility Extended Community.

		Returns:
			self: This instance with all currently retrieved cMacRange data using find and the newly added cMacRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the cMacRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CmacPrefixLength=None, CvlanId=None, CvlanPriority=None, CvlanTpId=None, EnableCvlan=None, EnableSecondLabel=None, EnableSvlan=None, Enabled=None, FirstLabelStart=None, LabelMode=None, LabelStep=None, NoOfCmacs=None, SecondLabelStart=None, StartCmacPrefix=None, SvlanId=None, SvlanPriority=None, SvlanTpId=None, UseSameSequenceNumber=None):
		"""Finds and retrieves cMacRange data from the server.

		All named parameters support regex and can be used to selectively retrieve cMacRange data from the server.
		By default the find method takes no parameters and will retrieve all cMacRange data from the server.

		Args:
			CmacPrefixLength (number): Prefix length of C-MAC address. Default value is 48. Minimum value is 0 and maximum value is 48.
			CvlanId (number): C-VLAN Identifier used in EVPN traffic. Default value is 1. Minimum value is 0 and maximum value is 4095.
			CvlanPriority (number): C-VLAN Priority used in EVPN traffic. Default value is 0. Minimum value is 0 and maximum value is 7.
			CvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): C-VLAN TPID used in EVPN traffic. Default value is 0x8100. User can select any one of {0x8100, 0x9100, 0x9200, 0x88A8}.
			EnableCvlan (bool): If true then C-VLAN is used in EVPN traffic. Default value is false.
			EnableSecondLabel (bool): If true then second label is inserted in the EVPN label stack. Default value is false. Label value is obtained for all macs in the same way of first label.
			EnableSvlan (bool): If true then S-VLAN is used in EVPN traffic. Default value is false.
			Enabled (bool): If true then this C-MAC range is used in EVPN.
			FirstLabelStart (number): First EVPN label in label stack for MAC route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF. This label value is used in first mac of this mac range. If Label mode is fixed then same label value is used for all mac in this mac range. If label mode is Increment then label value for subsequent mac is obtained by adding the label step value to the first label value.
			LabelMode (str(fixed|increment)): It is used to get the label value of subsequent macs in the range by adding this value to the first label value. Default value is Increment. It can be either Fixed or Increment.
			LabelStep (number): Label step to get the label value of subsequent macs in the mac range. Default value is 1. Minimum value is 0 and maximum value is 0xFFFFF.
			NoOfCmacs (number): Number of C-MACs in this mac range. Default value is 1. Minimum value is 1 and maximum value is 0xFFFFFFFF.
			SecondLabelStart (number): Second EVPN label in label stack for MAC route. Default value is 16. Minimum value is 16 and maximum value is 0xFFFFF. This label value is used in first mac of this mac range. If Label mode is fixed then same label value is used for all mac in this mac range. If label mode is Increment then label value for subsequent mac is obtained by adding the label step value to the second label value.
			StartCmacPrefix (str): Start mac address of this range. Default value is 0x00 00 00 00 00 01.
			SvlanId (number): S-VLAN Identifier used in EVPN traffic. Default value is 1. Minimum value is 0 and maximum value is 4095.
			SvlanPriority (number): S-VLAN Priority used in EVPN traffic. Default value is 0. Minimum value is 0 and maximum value is 7.
			SvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): S-VLAN TPID used in EVPN traffic. Default value is 0x8100. User can select any one of {0x8100, 0x9100, 0x9200, 0x88A8}.
			UseSameSequenceNumber (bool): If true then same sequence number is used in MAC Mobility Extended Community for all MAC routes for mac mobility. If false then subsequent C-MAC route uses unique sequence number in MAC Mobility Extended Community.

		Returns:
			self: This instance with matching cMacRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of cMacRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the cMacRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ReadvertiseCmac(self):
		"""Executes the readvertiseCmac operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=cMacRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ReadvertiseCmac', payload=locals(), response_object=None)
