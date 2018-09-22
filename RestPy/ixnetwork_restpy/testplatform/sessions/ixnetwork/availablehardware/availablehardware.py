from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableHardware(Base):
	"""The AvailableHardware class encapsulates a required availableHardware node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableHardware property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'availableHardware'

	def __init__(self, parent):
		super(AvailableHardware, self).__init__(parent)

	@property
	def Chassis(self):
		"""An instance of the Chassis class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.chassis.Chassis)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.chassis import Chassis
		return Chassis(self)

	@property
	def VirtualChassis(self):
		"""An instance of the VirtualChassis class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.virtualchassis.VirtualChassis)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.virtualchassis import VirtualChassis
		return VirtualChassis(self)._select()

	@property
	def IsLocked(self):
		"""If true, locks the Hardware Manager.

		Returns:
			bool
		"""
		return self._get_attribute('isLocked')

	@property
	def IsOffChassis(self):
		"""If true, the Hardware Manager is Off Chassis.

		Returns:
			bool
		"""
		return self._get_attribute('isOffChassis')
	@IsOffChassis.setter
	def IsOffChassis(self, value):
		self._set_attribute('isOffChassis', value)

	@property
	def OffChassisHwM(self):
		"""Enables the Off Chassis Hardware Manager. The Hardware Manager is an IxOS component that manages the resources on an Ixia chassis. IxNetwork communicates with a chassis through Hardware Manager. Normally, Hardware Manager runs on the chassis itself; however, it can also be installed and run on a separate PC. This configuration is known as an Off-Chassis Hardware Manager.

		Returns:
			str
		"""
		return self._get_attribute('offChassisHwM')
	@OffChassisHwM.setter
	def OffChassisHwM(self, value):
		self._set_attribute('offChassisHwM', value)
