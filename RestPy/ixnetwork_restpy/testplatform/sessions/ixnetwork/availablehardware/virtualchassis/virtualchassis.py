
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


class VirtualChassis(Base):
	"""The VirtualChassis class encapsulates a required virtualChassis node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VirtualChassis property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'virtualChassis'

	def __init__(self, parent):
		super(VirtualChassis, self).__init__(parent)

	@property
	def DiscoveredAppliance(self):
		"""An instance of the DiscoveredAppliance class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.discoveredappliance.discoveredappliance.DiscoveredAppliance)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.discoveredappliance.discoveredappliance import DiscoveredAppliance
		return DiscoveredAppliance(self)

	@property
	def Hypervisor(self):
		"""An instance of the Hypervisor class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.hypervisor.hypervisor.Hypervisor)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.hypervisor.hypervisor import Hypervisor
		return Hypervisor(self)

	@property
	def IxVmCard(self):
		"""An instance of the IxVmCard class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.ixvmcard.ixvmcard.IxVmCard)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.ixvmcard.ixvmcard import IxVmCard
		return IxVmCard(self)

	@property
	def EnableLicenseCheck(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLicenseCheck')
	@EnableLicenseCheck.setter
	def EnableLicenseCheck(self, value):
		self._set_attribute('enableLicenseCheck', value)

	@property
	def Hostname(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostname')

	@property
	def LicenseServer(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('licenseServer')
	@LicenseServer.setter
	def LicenseServer(self, value):
		self._set_attribute('licenseServer', value)

	@property
	def NtpServer(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ntpServer')
	@NtpServer.setter
	def NtpServer(self, value):
		self._set_attribute('ntpServer', value)

	@property
	def StartTxDelay(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startTxDelay')
	@StartTxDelay.setter
	def StartTxDelay(self, value):
		self._set_attribute('startTxDelay', value)
