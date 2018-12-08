
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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def RouteDistinguisherAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAsNumber')
	@RouteDistinguisherAsNumber.setter
	def RouteDistinguisherAsNumber(self, value):
		self._set_attribute('routeDistinguisherAsNumber', value)

	@property
	def RouteDistinguisherAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAsNumberStep')
	@RouteDistinguisherAsNumberStep.setter
	def RouteDistinguisherAsNumberStep(self, value):
		self._set_attribute('routeDistinguisherAsNumberStep', value)

	@property
	def RouteDistinguisherAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAssignedNumber')
	@RouteDistinguisherAssignedNumber.setter
	def RouteDistinguisherAssignedNumber(self, value):
		self._set_attribute('routeDistinguisherAssignedNumber', value)

	@property
	def RouteDistinguisherAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAssignedNumberStep')
	@RouteDistinguisherAssignedNumberStep.setter
	def RouteDistinguisherAssignedNumberStep(self, value):
		self._set_attribute('routeDistinguisherAssignedNumberStep', value)

	@property
	def RouteDistinguisherIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisherIpAddress')
	@RouteDistinguisherIpAddress.setter
	def RouteDistinguisherIpAddress(self, value):
		self._set_attribute('routeDistinguisherIpAddress', value)

	@property
	def RouteDistinguisherIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisherIpAddressStep')
	@RouteDistinguisherIpAddressStep.setter
	def RouteDistinguisherIpAddressStep(self, value):
		self._set_attribute('routeDistinguisherIpAddressStep', value)

	@property
	def RouteDistinguisherType(self):
		"""

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('routeDistinguisherType')
	@RouteDistinguisherType.setter
	def RouteDistinguisherType(self, value):
		self._set_attribute('routeDistinguisherType', value)

	@property
	def RouteTargetAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAsNumber')
	@RouteTargetAsNumber.setter
	def RouteTargetAsNumber(self, value):
		self._set_attribute('routeTargetAsNumber', value)

	@property
	def RouteTargetAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAsNumberStep')
	@RouteTargetAsNumberStep.setter
	def RouteTargetAsNumberStep(self, value):
		self._set_attribute('routeTargetAsNumberStep', value)

	@property
	def RouteTargetAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAssignedNumber')
	@RouteTargetAssignedNumber.setter
	def RouteTargetAssignedNumber(self, value):
		self._set_attribute('routeTargetAssignedNumber', value)

	@property
	def RouteTargetAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAssignedNumberStep')
	@RouteTargetAssignedNumberStep.setter
	def RouteTargetAssignedNumberStep(self, value):
		self._set_attribute('routeTargetAssignedNumberStep', value)

	@property
	def RouteTargetIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeTargetIpAddress')
	@RouteTargetIpAddress.setter
	def RouteTargetIpAddress(self, value):
		self._set_attribute('routeTargetIpAddress', value)

	@property
	def RouteTargetIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeTargetIpAddressStep')
	@RouteTargetIpAddressStep.setter
	def RouteTargetIpAddressStep(self, value):
		self._set_attribute('routeTargetIpAddressStep', value)

	@property
	def RouteTargetType(self):
		"""

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('routeTargetType')
	@RouteTargetType.setter
	def RouteTargetType(self, value):
		self._set_attribute('routeTargetType', value)

	@property
	def UseRouteDistinguisherAsRouteTarget(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useRouteDistinguisherAsRouteTarget')
	@UseRouteDistinguisherAsRouteTarget.setter
	def UseRouteDistinguisherAsRouteTarget(self, value):
		self._set_attribute('useRouteDistinguisherAsRouteTarget', value)

	@property
	def UseVplsIdAsRouteDistinguisher(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useVplsIdAsRouteDistinguisher')
	@UseVplsIdAsRouteDistinguisher.setter
	def UseVplsIdAsRouteDistinguisher(self, value):
		self._set_attribute('useVplsIdAsRouteDistinguisher', value)

	@property
	def VplsCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsCount')
	@VplsCount.setter
	def VplsCount(self, value):
		self._set_attribute('vplsCount', value)

	@property
	def VplsIdAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumber')
	@VplsIdAsNumber.setter
	def VplsIdAsNumber(self, value):
		self._set_attribute('vplsIdAsNumber', value)

	@property
	def VplsIdAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumberStep')
	@VplsIdAsNumberStep.setter
	def VplsIdAsNumberStep(self, value):
		self._set_attribute('vplsIdAsNumberStep', value)

	@property
	def VplsIdAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumber')
	@VplsIdAssignedNumber.setter
	def VplsIdAssignedNumber(self, value):
		self._set_attribute('vplsIdAssignedNumber', value)

	@property
	def VplsIdAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumberStep')
	@VplsIdAssignedNumberStep.setter
	def VplsIdAssignedNumberStep(self, value):
		self._set_attribute('vplsIdAssignedNumberStep', value)

	@property
	def VplsIdIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddress')
	@VplsIdIpAddress.setter
	def VplsIdIpAddress(self, value):
		self._set_attribute('vplsIdIpAddress', value)

	@property
	def VplsIdIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddressStep')
	@VplsIdIpAddressStep.setter
	def VplsIdIpAddressStep(self, value):
		self._set_attribute('vplsIdIpAddressStep', value)

	@property
	def VplsIdType(self):
		"""

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('vplsIdType')
	@VplsIdType.setter
	def VplsIdType(self, value):
		self._set_attribute('vplsIdType', value)

	@property
	def VsiId(self):
		"""

		Returns:
			str(concatenatePeAddress|concatenateAssignedNumber)
		"""
		return self._get_attribute('vsiId')
	@VsiId.setter
	def VsiId(self, value):
		self._set_attribute('vsiId', value)

	@property
	def VsiIdAssignedNumber(self):
		"""

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
			Enabled (bool): 
			RouteDistinguisherAsNumber (number): 
			RouteDistinguisherAsNumberStep (number): 
			RouteDistinguisherAssignedNumber (number): 
			RouteDistinguisherAssignedNumberStep (number): 
			RouteDistinguisherIpAddress (str): 
			RouteDistinguisherIpAddressStep (str): 
			RouteDistinguisherType (str(asNumber|ipAddress)): 
			RouteTargetAsNumber (number): 
			RouteTargetAsNumberStep (number): 
			RouteTargetAssignedNumber (number): 
			RouteTargetAssignedNumberStep (number): 
			RouteTargetIpAddress (str): 
			RouteTargetIpAddressStep (str): 
			RouteTargetType (str(asNumber|ipAddress)): 
			UseRouteDistinguisherAsRouteTarget (bool): 
			UseVplsIdAsRouteDistinguisher (bool): 
			VplsCount (number): 
			VplsIdAsNumber (number): 
			VplsIdAsNumberStep (number): 
			VplsIdAssignedNumber (number): 
			VplsIdAssignedNumberStep (number): 
			VplsIdIpAddress (str): 
			VplsIdIpAddressStep (str): 
			VplsIdType (str(asNumber|ipAddress)): 
			VsiId (str(concatenatePeAddress|concatenateAssignedNumber)): 
			VsiIdAssignedNumber (number): 

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
			Enabled (bool): 
			RouteDistinguisherAsNumber (number): 
			RouteDistinguisherAsNumberStep (number): 
			RouteDistinguisherAssignedNumber (number): 
			RouteDistinguisherAssignedNumberStep (number): 
			RouteDistinguisherIpAddress (str): 
			RouteDistinguisherIpAddressStep (str): 
			RouteDistinguisherType (str(asNumber|ipAddress)): 
			RouteTargetAsNumber (number): 
			RouteTargetAsNumberStep (number): 
			RouteTargetAssignedNumber (number): 
			RouteTargetAssignedNumberStep (number): 
			RouteTargetIpAddress (str): 
			RouteTargetIpAddressStep (str): 
			RouteTargetType (str(asNumber|ipAddress)): 
			UseRouteDistinguisherAsRouteTarget (bool): 
			UseVplsIdAsRouteDistinguisher (bool): 
			VplsCount (number): 
			VplsIdAsNumber (number): 
			VplsIdAsNumberStep (number): 
			VplsIdAssignedNumber (number): 
			VplsIdAssignedNumberStep (number): 
			VplsIdIpAddress (str): 
			VplsIdIpAddressStep (str): 
			VplsIdType (str(asNumber|ipAddress)): 
			VsiId (str(concatenatePeAddress|concatenateAssignedNumber)): 
			VsiIdAssignedNumber (number): 

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
