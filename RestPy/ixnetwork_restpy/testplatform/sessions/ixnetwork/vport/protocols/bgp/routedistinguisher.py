
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


class RouteDistinguisher(Base):
	"""The RouteDistinguisher class encapsulates a required routeDistinguisher node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RouteDistinguisher property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'routeDistinguisher'

	def __init__(self, parent):
		super(RouteDistinguisher, self).__init__(parent)

	@property
	def AsNumber(self):
		"""If the type was set to as or asNumber2, this is the AS number in the Administrator subfield of the Value field of the MVPN Route Distinguisher (RD). It is the Global part of the RD. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('asNumber')
	@AsNumber.setter
	def AsNumber(self, value):
		self._set_attribute('asNumber', value)

	@property
	def AsNumberStep(self):
		"""The increment step for for the AS.

		Returns:
			number
		"""
		return self._get_attribute('asNumberStep')
	@AsNumberStep.setter
	def AsNumberStep(self, value):
		self._set_attribute('asNumberStep', value)

	@property
	def AssignedNumber(self):
		"""The Assigned Number sub-field of the Value field of the MVPN Route Distinguisher. It is a number from a numbering space, which the enterprise administers, for a given IP address or ASN space. It is the Local part of the RD. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('assignedNumber')
	@AssignedNumber.setter
	def AssignedNumber(self, value):
		self._set_attribute('assignedNumber', value)

	@property
	def AssignedNumberStep(self):
		"""The increment step for for the assigned number.

		Returns:
			number
		"""
		return self._get_attribute('assignedNumberStep')
	@AssignedNumberStep.setter
	def AssignedNumberStep(self, value):
		self._set_attribute('assignedNumberStep', value)

	@property
	def IpAddress(self):
		"""If the type was set to ip, this is the 4-byte IP address in the Administrator subfield of the Value field of the MVPN Route Distinguisher (RD). It is the Global part of the RD. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpAddressStep(self):
		"""The increment step for for the IP address.

		Returns:
			str
		"""
		return self._get_attribute('ipAddressStep')
	@IpAddressStep.setter
	def IpAddressStep(self, value):
		self._set_attribute('ipAddressStep', value)

	@property
	def Type(self):
		"""Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.

		Returns:
			str(as|ip|asNumber2)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)
