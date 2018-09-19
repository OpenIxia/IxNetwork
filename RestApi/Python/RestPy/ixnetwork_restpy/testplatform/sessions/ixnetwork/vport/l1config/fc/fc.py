from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Fc(Base):
	"""The Fc class encapsulates a required fc node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Fc property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'fc'

	def __init__(self, parent):
		super(Fc, self).__init__(parent)

	@property
	def CreditStarvationValue(self):
		"""If selected, programs encounter a delay value specified in the Hold R_RDY field. The counter starts counting down after it receives the first frame. The port holds R_RDY for all frames received until counter reaches to 0. After counter reaches 0, the port sends out all accumulated R_RDY.

		Returns:
			number
		"""
		return self._get_attribute('creditStarvationValue')
	@CreditStarvationValue.setter
	def CreditStarvationValue(self, value):
		self._set_attribute('creditStarvationValue', value)

	@property
	def EnableEmissionLoweringProtocol(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableEmissionLoweringProtocol')
	@EnableEmissionLoweringProtocol.setter
	def EnableEmissionLoweringProtocol(self, value):
		self._set_attribute('enableEmissionLoweringProtocol', value)

	@property
	def EnablePPM(self):
		"""If true, enables the portsppm.

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def FixedDelayValue(self):
		"""Internally delays the R_RDY primitive signals with X ms. X is between 0 and 20000 milliseconds.

		Returns:
			number
		"""
		return self._get_attribute('fixedDelayValue')
	@FixedDelayValue.setter
	def FixedDelayValue(self, value):
		self._set_attribute('fixedDelayValue', value)

	@property
	def ForceErrors(self):
		"""Helps to configure the port to introduce errors in the transmission of R_RDYPrimitive Signals

		Returns:
			str(noErrors|noRRDY|noRRDYEvery)
		"""
		return self._get_attribute('forceErrors')
	@ForceErrors.setter
	def ForceErrors(self, value):
		self._set_attribute('forceErrors', value)

	@property
	def Loopback(self):
		"""If true, the port is set to internally loopback from transmit to receive.

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def MaxDelayForRandomValue(self):
		"""The maximum random delay value for the R_RDY primitives. The maximum value is 1,000,000 microseconds.

		Returns:
			number
		"""
		return self._get_attribute('maxDelayForRandomValue')
	@MaxDelayForRandomValue.setter
	def MaxDelayForRandomValue(self, value):
		self._set_attribute('maxDelayForRandomValue', value)

	@property
	def MinDelayForRandomValue(self):
		"""The minimum random delay value for the R_RDY primitives. The minimum value is 0 microseconds.

		Returns:
			number
		"""
		return self._get_attribute('minDelayForRandomValue')
	@MinDelayForRandomValue.setter
	def MinDelayForRandomValue(self, value):
		self._set_attribute('minDelayForRandomValue', value)

	@property
	def NoRRDYAfter(self):
		"""Sends R_RDY primitive signals without any delay.

		Returns:
			number
		"""
		return self._get_attribute('noRRDYAfter')
	@NoRRDYAfter.setter
	def NoRRDYAfter(self, value):
		self._set_attribute('noRRDYAfter', value)

	@property
	def Ppm(self):
		"""Indicates the value that needs to be adjusted for the line transmit frequency.

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def RrdyResponseDelays(self):
		"""Helps to set internal delays for the transmission of R_RDY Primitive Signals.

		Returns:
			str(creditStarvation|fixedDelay|noDelay|randomDelay)
		"""
		return self._get_attribute('rrdyResponseDelays')
	@RrdyResponseDelays.setter
	def RrdyResponseDelays(self, value):
		self._set_attribute('rrdyResponseDelays', value)

	@property
	def Speed(self):
		"""Indicates the line speed.

		Returns:
			str(speed2000|speed4000|speed8000)
		"""
		return self._get_attribute('speed')
	@Speed.setter
	def Speed(self, value):
		self._set_attribute('speed', value)

	@property
	def TxIgnoreAvailableCredits(self):
		"""The transmitting port does not listen to flow control. It keeps transmittingpackets irrespective of available credits. For example, if two Fibre Channel portsare connected back-to-back andTransmitignoreavailablecredits'optionistrueonthetransmittingportand'Don'tsendR_RDY'optionistrueonthereceivingport,andthentransmitisstarted,theporttransmitsatfullrateeventhoughitdoesnothavecredits.

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreAvailableCredits')
	@TxIgnoreAvailableCredits.setter
	def TxIgnoreAvailableCredits(self, value):
		self._set_attribute('txIgnoreAvailableCredits', value)

	@property
	def TxIgnoreRxLinkFaults(self):
		"""If true, allows transmission of packets even if the receive link is down.

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreRxLinkFaults')
	@TxIgnoreRxLinkFaults.setter
	def TxIgnoreRxLinkFaults(self, value):
		self._set_attribute('txIgnoreRxLinkFaults', value)
