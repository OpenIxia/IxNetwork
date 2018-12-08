
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


class DhcpV6Properties(Base):
	"""The DhcpV6Properties class encapsulates a required dhcpV6Properties node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DhcpV6Properties property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpV6Properties'

	def __init__(self, parent):
		super(DhcpV6Properties, self).__init__(parent)

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
	def IaId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iaId')
	@IaId.setter
	def IaId(self, value):
		self._set_attribute('iaId', value)

	@property
	def IaType(self):
		"""

		Returns:
			str(permanent|temporary|prefixDelegation)
		"""
		return self._get_attribute('iaType')
	@IaType.setter
	def IaType(self, value):
		self._set_attribute('iaType', value)

	@property
	def RenewTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('renewTimer')
	@RenewTimer.setter
	def RenewTimer(self, value):
		self._set_attribute('renewTimer', value)

	@property
	def RequestRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('requestRate')
	@RequestRate.setter
	def RequestRate(self, value):
		self._set_attribute('requestRate', value)

	@property
	def Tlvs(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('tlvs')
	@Tlvs.setter
	def Tlvs(self, value):
		self._set_attribute('tlvs', value)
