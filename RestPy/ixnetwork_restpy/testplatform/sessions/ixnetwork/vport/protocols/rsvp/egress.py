
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


class Egress(Base):
	"""The Egress class encapsulates a required egress node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Egress property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'egress'

	def __init__(self, parent):
		super(Egress, self).__init__(parent)

	@property
	def Bandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def EgressBehavior(self):
		"""

		Returns:
			str(alwaysUseConfiguredStyle|useSeWhenIndicatedInSessionAttribute)
		"""
		return self._get_attribute('egressBehavior')
	@EgressBehavior.setter
	def EgressBehavior(self, value):
		self._set_attribute('egressBehavior', value)

	@property
	def EnableFixedLabelForResv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFixedLabelForResv')
	@EnableFixedLabelForResv.setter
	def EnableFixedLabelForResv(self, value):
		self._set_attribute('enableFixedLabelForResv', value)

	@property
	def LabelValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('labelValue')
	@LabelValue.setter
	def LabelValue(self, value):
		self._set_attribute('labelValue', value)

	@property
	def PathErrorTlv(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('pathErrorTlv')
	@PathErrorTlv.setter
	def PathErrorTlv(self, value):
		self._set_attribute('pathErrorTlv', value)

	@property
	def ReflectRro(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('reflectRro')
	@ReflectRro.setter
	def ReflectRro(self, value):
		self._set_attribute('reflectRro', value)

	@property
	def RefreshInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('refreshInterval')
	@RefreshInterval.setter
	def RefreshInterval(self, value):
		self._set_attribute('refreshInterval', value)

	@property
	def ReservationStyle(self):
		"""

		Returns:
			str(se|ff|wf)
		"""
		return self._get_attribute('reservationStyle')
	@ReservationStyle.setter
	def ReservationStyle(self, value):
		self._set_attribute('reservationStyle', value)

	@property
	def ReservationTearTlv(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('reservationTearTlv')
	@ReservationTearTlv.setter
	def ReservationTearTlv(self, value):
		self._set_attribute('reservationTearTlv', value)

	@property
	def ReservationTlv(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('reservationTlv')
	@ReservationTlv.setter
	def ReservationTlv(self, value):
		self._set_attribute('reservationTlv', value)

	@property
	def Rro(self):
		"""

		Returns:
			list(dict(arg1:str[ip|label],arg2:str,arg3:bool,arg4:bool,arg5:number,arg6:bool,arg7:bool,arg8:bool))
		"""
		return self._get_attribute('rro')
	@Rro.setter
	def Rro(self, value):
		self._set_attribute('rro', value)

	@property
	def SendResvConfirmation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendResvConfirmation')
	@SendResvConfirmation.setter
	def SendResvConfirmation(self, value):
		self._set_attribute('sendResvConfirmation', value)

	@property
	def TimeoutMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timeoutMultiplier')
	@TimeoutMultiplier.setter
	def TimeoutMultiplier(self, value):
		self._set_attribute('timeoutMultiplier', value)
