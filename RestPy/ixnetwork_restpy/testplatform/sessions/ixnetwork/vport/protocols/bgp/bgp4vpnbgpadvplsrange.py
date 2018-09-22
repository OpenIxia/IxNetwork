from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Bgp4VpnBgpAdVplsRange(Base):
	"""The Bgp4VpnBgpAdVplsRange class encapsulates a user managed bgp4VpnBgpAdVplsRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bgp4VpnBgpAdVplsRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bgp4VpnBgpAdVplsRange'

	def __init__(self, parent):
		super(Bgp4VpnBgpAdVplsRange, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables one BGP AD VPLS.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def RouteDistinguisherAsNumber(self):
		"""This option is available for use if Distinguish Type is set to AS. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAsNumber')
	@RouteDistinguisherAsNumber.setter
	def RouteDistinguisherAsNumber(self, value):
		self._set_attribute('routeDistinguisherAsNumber', value)

	@property
	def RouteDistinguisherAsNumberStep(self):
		"""This option is available for use if Distinguish Type is set to AS. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAsNumberStep')
	@RouteDistinguisherAsNumberStep.setter
	def RouteDistinguisherAsNumberStep(self, value):
		self._set_attribute('routeDistinguisherAsNumberStep', value)

	@property
	def RouteDistinguisherAssignedNumber(self):
		"""The distinguisher assigned number. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAssignedNumber')
	@RouteDistinguisherAssignedNumber.setter
	def RouteDistinguisherAssignedNumber(self, value):
		self._set_attribute('routeDistinguisherAssignedNumber', value)

	@property
	def RouteDistinguisherAssignedNumberStep(self):
		"""The distinguisher assigned number. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAssignedNumberStep')
	@RouteDistinguisherAssignedNumberStep.setter
	def RouteDistinguisherAssignedNumberStep(self, value):
		self._set_attribute('routeDistinguisherAssignedNumberStep', value)

	@property
	def RouteDistinguisherIpAddress(self):
		"""Available for use only if the IPv4 Input is set to IP

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisherIpAddress')
	@RouteDistinguisherIpAddress.setter
	def RouteDistinguisherIpAddress(self, value):
		self._set_attribute('routeDistinguisherIpAddress', value)

	@property
	def RouteDistinguisherIpAddressStep(self):
		"""Available for use only if the IPv4 Input is set to IP.

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisherIpAddressStep')
	@RouteDistinguisherIpAddressStep.setter
	def RouteDistinguisherIpAddressStep(self, value):
		self._set_attribute('routeDistinguisherIpAddressStep', value)

	@property
	def RouteDistinguisherType(self):
		"""The RD type, one of AS and IP.

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('routeDistinguisherType')
	@RouteDistinguisherType.setter
	def RouteDistinguisherType(self, value):
		self._set_attribute('routeDistinguisherType', value)

	@property
	def RouteTargetAsNumber(self):
		"""Available for use only if Distinguish Type is set to AS.

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAsNumber')
	@RouteTargetAsNumber.setter
	def RouteTargetAsNumber(self, value):
		self._set_attribute('routeTargetAsNumber', value)

	@property
	def RouteTargetAsNumberStep(self):
		"""Available for use only if Target AS Number is set to AS. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAsNumberStep')
	@RouteTargetAsNumberStep.setter
	def RouteTargetAsNumberStep(self, value):
		self._set_attribute('routeTargetAsNumberStep', value)

	@property
	def RouteTargetAssignedNumber(self):
		"""The target assigned number. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAssignedNumber')
	@RouteTargetAssignedNumber.setter
	def RouteTargetAssignedNumber(self, value):
		self._set_attribute('routeTargetAssignedNumber', value)

	@property
	def RouteTargetAssignedNumberStep(self):
		"""The target assigned number. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAssignedNumberStep')
	@RouteTargetAssignedNumberStep.setter
	def RouteTargetAssignedNumberStep(self, value):
		self._set_attribute('routeTargetAssignedNumberStep', value)

	@property
	def RouteTargetIpAddress(self):
		"""Available for use only if the IPv4 Input is set to IP.

		Returns:
			str
		"""
		return self._get_attribute('routeTargetIpAddress')
	@RouteTargetIpAddress.setter
	def RouteTargetIpAddress(self, value):
		self._set_attribute('routeTargetIpAddress', value)

	@property
	def RouteTargetIpAddressStep(self):
		"""Available for use only if it is set to IP. The default is 0.0.0.0.

		Returns:
			str
		"""
		return self._get_attribute('routeTargetIpAddressStep')
	@RouteTargetIpAddressStep.setter
	def RouteTargetIpAddressStep(self, value):
		self._set_attribute('routeTargetIpAddressStep', value)

	@property
	def RouteTargetType(self):
		"""The RT format, one of AS and IP. The default is AS.

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('routeTargetType')
	@RouteTargetType.setter
	def RouteTargetType(self, value):
		self._set_attribute('routeTargetType', value)

	@property
	def UseRouteDistinguisherAsRouteTarget(self):
		"""If true, the route distinginguisher is used as the route target.

		Returns:
			bool
		"""
		return self._get_attribute('useRouteDistinguisherAsRouteTarget')
	@UseRouteDistinguisherAsRouteTarget.setter
	def UseRouteDistinguisherAsRouteTarget(self, value):
		self._set_attribute('useRouteDistinguisherAsRouteTarget', value)

	@property
	def UseVplsIdAsRouteDistinguisher(self):
		"""If true, the VPLS Id is used as the route distinguisher.

		Returns:
			bool
		"""
		return self._get_attribute('useVplsIdAsRouteDistinguisher')
	@UseVplsIdAsRouteDistinguisher.setter
	def UseVplsIdAsRouteDistinguisher(self, value):
		self._set_attribute('useVplsIdAsRouteDistinguisher', value)

	@property
	def VplsCount(self):
		"""The Integer value that indicates the number of VPLS instance emulated using this VPLS range.

		Returns:
			number
		"""
		return self._get_attribute('vplsCount')
	@VplsCount.setter
	def VplsCount(self, value):
		self._set_attribute('vplsCount', value)

	@property
	def VplsIdAsNumber(self):
		"""Available for use if VPLS Id Type is set to AS. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumber')
	@VplsIdAsNumber.setter
	def VplsIdAsNumber(self, value):
		self._set_attribute('vplsIdAsNumber', value)

	@property
	def VplsIdAsNumberStep(self):
		"""Available for use only if VPLS Id Type is set to AS. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumberStep')
	@VplsIdAsNumberStep.setter
	def VplsIdAsNumberStep(self, value):
		self._set_attribute('vplsIdAsNumberStep', value)

	@property
	def VplsIdAssignedNumber(self):
		"""The indicated value for the VPLS Id Assigned Number attribute. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumber')
	@VplsIdAssignedNumber.setter
	def VplsIdAssignedNumber(self, value):
		self._set_attribute('vplsIdAssignedNumber', value)

	@property
	def VplsIdAssignedNumberStep(self):
		"""The indicated number for the VPLS Id Assigned Number attribute. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumberStep')
	@VplsIdAssignedNumberStep.setter
	def VplsIdAssignedNumberStep(self, value):
		self._set_attribute('vplsIdAssignedNumberStep', value)

	@property
	def VplsIdIpAddress(self):
		"""Available for use only if the route VPLS Id Type is set to IP. The default is 0.0.0.0

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddress')
	@VplsIdIpAddress.setter
	def VplsIdIpAddress(self, value):
		self._set_attribute('vplsIdIpAddress', value)

	@property
	def VplsIdIpAddressStep(self):
		"""Available for use only if the route VPLS Id Type is set to IP. The default is 0.0.0.0

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddressStep')
	@VplsIdIpAddressStep.setter
	def VplsIdIpAddressStep(self, value):
		self._set_attribute('vplsIdIpAddressStep', value)

	@property
	def VplsIdType(self):
		"""The VPLS ID type, one of AS and IP. Default is AS.

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('vplsIdType')
	@VplsIdType.setter
	def VplsIdType(self, value):
		self._set_attribute('vplsIdType', value)

	@property
	def VsiId(self):
		"""The VSI ID, one of concatenatePeAddress and concatenateAssignedNumber.

		Returns:
			str(concatenatePeAddress|concatenateAssignedNumber)
		"""
		return self._get_attribute('vsiId')
	@VsiId.setter
	def VsiId(self, value):
		self._set_attribute('vsiId', value)

	@property
	def VsiIdAssignedNumber(self):
		"""The indicated value for the VSI ID Assigned Number attribute.

		Returns:
			number
		"""
		return self._get_attribute('vsiIdAssignedNumber')
	@VsiIdAssignedNumber.setter
	def VsiIdAssignedNumber(self, value):
		self._set_attribute('vsiIdAssignedNumber', value)

	def add(self, Enabled=None, RouteDistinguisherAsNumber=None, RouteDistinguisherAsNumberStep=None, RouteDistinguisherAssignedNumber=None, RouteDistinguisherAssignedNumberStep=None, RouteDistinguisherIpAddress=None, RouteDistinguisherIpAddressStep=None, RouteDistinguisherType=None, RouteTargetAsNumber=None, RouteTargetAsNumberStep=None, RouteTargetAssignedNumber=None, RouteTargetAssignedNumberStep=None, RouteTargetIpAddress=None, RouteTargetIpAddressStep=None, RouteTargetType=None, UseRouteDistinguisherAsRouteTarget=None, UseVplsIdAsRouteDistinguisher=None, VplsCount=None, VplsIdAsNumber=None, VplsIdAsNumberStep=None, VplsIdAssignedNumber=None, VplsIdAssignedNumberStep=None, VplsIdIpAddress=None, VplsIdIpAddressStep=None, VplsIdType=None, VsiId=None, VsiIdAssignedNumber=None):
		"""Adds a new bgp4VpnBgpAdVplsRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true, enables one BGP AD VPLS.
			RouteDistinguisherAsNumber (number): This option is available for use if Distinguish Type is set to AS. The default is 0.
			RouteDistinguisherAsNumberStep (number): This option is available for use if Distinguish Type is set to AS. The default is 0.
			RouteDistinguisherAssignedNumber (number): The distinguisher assigned number. The default is 0.
			RouteDistinguisherAssignedNumberStep (number): The distinguisher assigned number. The default is 0.
			RouteDistinguisherIpAddress (str): Available for use only if the IPv4 Input is set to IP
			RouteDistinguisherIpAddressStep (str): Available for use only if the IPv4 Input is set to IP.
			RouteDistinguisherType (str(asNumber|ipAddress)): The RD type, one of AS and IP.
			RouteTargetAsNumber (number): Available for use only if Distinguish Type is set to AS.
			RouteTargetAsNumberStep (number): Available for use only if Target AS Number is set to AS. The default is 0.
			RouteTargetAssignedNumber (number): The target assigned number. The default is 0.
			RouteTargetAssignedNumberStep (number): The target assigned number. The default is 0.
			RouteTargetIpAddress (str): Available for use only if the IPv4 Input is set to IP.
			RouteTargetIpAddressStep (str): Available for use only if it is set to IP. The default is 0.0.0.0.
			RouteTargetType (str(asNumber|ipAddress)): The RT format, one of AS and IP. The default is AS.
			UseRouteDistinguisherAsRouteTarget (bool): If true, the route distinginguisher is used as the route target.
			UseVplsIdAsRouteDistinguisher (bool): If true, the VPLS Id is used as the route distinguisher.
			VplsCount (number): The Integer value that indicates the number of VPLS instance emulated using this VPLS range.
			VplsIdAsNumber (number): Available for use if VPLS Id Type is set to AS. The default is 0.
			VplsIdAsNumberStep (number): Available for use only if VPLS Id Type is set to AS. The default is 0.
			VplsIdAssignedNumber (number): The indicated value for the VPLS Id Assigned Number attribute. The default is 0.
			VplsIdAssignedNumberStep (number): The indicated number for the VPLS Id Assigned Number attribute. The default is 0.
			VplsIdIpAddress (str): Available for use only if the route VPLS Id Type is set to IP. The default is 0.0.0.0
			VplsIdIpAddressStep (str): Available for use only if the route VPLS Id Type is set to IP. The default is 0.0.0.0
			VplsIdType (str(asNumber|ipAddress)): The VPLS ID type, one of AS and IP. Default is AS.
			VsiId (str(concatenatePeAddress|concatenateAssignedNumber)): The VSI ID, one of concatenatePeAddress and concatenateAssignedNumber.
			VsiIdAssignedNumber (number): The indicated value for the VSI ID Assigned Number attribute.

		Returns:
			self: This instance with all currently retrieved bgp4VpnBgpAdVplsRange data using find and the newly added bgp4VpnBgpAdVplsRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bgp4VpnBgpAdVplsRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, RouteDistinguisherAsNumber=None, RouteDistinguisherAsNumberStep=None, RouteDistinguisherAssignedNumber=None, RouteDistinguisherAssignedNumberStep=None, RouteDistinguisherIpAddress=None, RouteDistinguisherIpAddressStep=None, RouteDistinguisherType=None, RouteTargetAsNumber=None, RouteTargetAsNumberStep=None, RouteTargetAssignedNumber=None, RouteTargetAssignedNumberStep=None, RouteTargetIpAddress=None, RouteTargetIpAddressStep=None, RouteTargetType=None, UseRouteDistinguisherAsRouteTarget=None, UseVplsIdAsRouteDistinguisher=None, VplsCount=None, VplsIdAsNumber=None, VplsIdAsNumberStep=None, VplsIdAssignedNumber=None, VplsIdAssignedNumberStep=None, VplsIdIpAddress=None, VplsIdIpAddressStep=None, VplsIdType=None, VsiId=None, VsiIdAssignedNumber=None):
		"""Finds and retrieves bgp4VpnBgpAdVplsRange data from the server.

		All named parameters support regex and can be used to selectively retrieve bgp4VpnBgpAdVplsRange data from the server.
		By default the find method takes no parameters and will retrieve all bgp4VpnBgpAdVplsRange data from the server.

		Args:
			Enabled (bool): If true, enables one BGP AD VPLS.
			RouteDistinguisherAsNumber (number): This option is available for use if Distinguish Type is set to AS. The default is 0.
			RouteDistinguisherAsNumberStep (number): This option is available for use if Distinguish Type is set to AS. The default is 0.
			RouteDistinguisherAssignedNumber (number): The distinguisher assigned number. The default is 0.
			RouteDistinguisherAssignedNumberStep (number): The distinguisher assigned number. The default is 0.
			RouteDistinguisherIpAddress (str): Available for use only if the IPv4 Input is set to IP
			RouteDistinguisherIpAddressStep (str): Available for use only if the IPv4 Input is set to IP.
			RouteDistinguisherType (str(asNumber|ipAddress)): The RD type, one of AS and IP.
			RouteTargetAsNumber (number): Available for use only if Distinguish Type is set to AS.
			RouteTargetAsNumberStep (number): Available for use only if Target AS Number is set to AS. The default is 0.
			RouteTargetAssignedNumber (number): The target assigned number. The default is 0.
			RouteTargetAssignedNumberStep (number): The target assigned number. The default is 0.
			RouteTargetIpAddress (str): Available for use only if the IPv4 Input is set to IP.
			RouteTargetIpAddressStep (str): Available for use only if it is set to IP. The default is 0.0.0.0.
			RouteTargetType (str(asNumber|ipAddress)): The RT format, one of AS and IP. The default is AS.
			UseRouteDistinguisherAsRouteTarget (bool): If true, the route distinginguisher is used as the route target.
			UseVplsIdAsRouteDistinguisher (bool): If true, the VPLS Id is used as the route distinguisher.
			VplsCount (number): The Integer value that indicates the number of VPLS instance emulated using this VPLS range.
			VplsIdAsNumber (number): Available for use if VPLS Id Type is set to AS. The default is 0.
			VplsIdAsNumberStep (number): Available for use only if VPLS Id Type is set to AS. The default is 0.
			VplsIdAssignedNumber (number): The indicated value for the VPLS Id Assigned Number attribute. The default is 0.
			VplsIdAssignedNumberStep (number): The indicated number for the VPLS Id Assigned Number attribute. The default is 0.
			VplsIdIpAddress (str): Available for use only if the route VPLS Id Type is set to IP. The default is 0.0.0.0
			VplsIdIpAddressStep (str): Available for use only if the route VPLS Id Type is set to IP. The default is 0.0.0.0
			VplsIdType (str(asNumber|ipAddress)): The VPLS ID type, one of AS and IP. Default is AS.
			VsiId (str(concatenatePeAddress|concatenateAssignedNumber)): The VSI ID, one of concatenatePeAddress and concatenateAssignedNumber.
			VsiIdAssignedNumber (number): The indicated value for the VSI ID Assigned Number attribute.

		Returns:
			self: This instance with matching bgp4VpnBgpAdVplsRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgp4VpnBgpAdVplsRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgp4VpnBgpAdVplsRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
