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
		"""Enables license check on port connect

		Returns:
			bool
		"""
		return self._get_attribute('enableLicenseCheck')
	@EnableLicenseCheck.setter
	def EnableLicenseCheck(self, value):
		self._set_attribute('enableLicenseCheck', value)

	@property
	def Hostname(self):
		"""Virtual Chassis hostname or IP

		Returns:
			str
		"""
		return self._get_attribute('hostname')

	@property
	def LicenseServer(self):
		"""The address of the license server

		Returns:
			str
		"""
		return self._get_attribute('licenseServer')
	@LicenseServer.setter
	def LicenseServer(self, value):
		self._set_attribute('licenseServer', value)

	@property
	def NtpServer(self):
		"""The address of the NTP server

		Returns:
			str
		"""
		return self._get_attribute('ntpServer')
	@NtpServer.setter
	def NtpServer(self, value):
		self._set_attribute('ntpServer', value)

	@property
	def StartTxDelay(self):
		"""The delay amount for transmit

		Returns:
			str
		"""
		return self._get_attribute('startTxDelay')
	@StartTxDelay.setter
	def StartTxDelay(self, value):
		self._set_attribute('startTxDelay', value)
