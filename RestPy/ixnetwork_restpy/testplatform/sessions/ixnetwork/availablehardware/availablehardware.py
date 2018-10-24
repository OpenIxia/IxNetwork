
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
