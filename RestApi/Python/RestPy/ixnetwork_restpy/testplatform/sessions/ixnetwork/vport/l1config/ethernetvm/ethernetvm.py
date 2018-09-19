from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ethernetvm(Base):
	"""The Ethernetvm class encapsulates a required ethernetvm node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ethernetvm property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ethernetvm'

	def __init__(self, parent):
		super(Ethernetvm, self).__init__(parent)

	@property
	def AutoInstrumentation(self):
		"""NOT DEFINED

		Returns:
			str(endOfFrame|floating)
		"""
		return self._get_attribute('autoInstrumentation')
	@AutoInstrumentation.setter
	def AutoInstrumentation(self, value):
		self._set_attribute('autoInstrumentation', value)

	@property
	def EnablePPM(self):
		"""If true, enables the portsppm.

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')

	@property
	def Loopback(self):
		"""If true, enables the ports ppm

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def Mtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def Ppm(self):
		"""Indicates the value that needs to be adjusted for the line transmit frequency

		Returns:
			number
		"""
		return self._get_attribute('ppm')

	@property
	def PromiscuousMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('promiscuousMode')
	@PromiscuousMode.setter
	def PromiscuousMode(self, value):
		self._set_attribute('promiscuousMode', value)

	@property
	def Speed(self):
		"""Select one of the enums to set the speed of the ethernet vm

		Returns:
			str(speed100|speed1000|speed10g|speed2000|speed20g|speed25g|speed3000|speed30g|speed4000|speed40g|speed5000|speed50g|speed6000|speed7000|speed8000|speed9000)
		"""
		return self._get_attribute('speed')
	@Speed.setter
	def Speed(self, value):
		self._set_attribute('speed', value)
