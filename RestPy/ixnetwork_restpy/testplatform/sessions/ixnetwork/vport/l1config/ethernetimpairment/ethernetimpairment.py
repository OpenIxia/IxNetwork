from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EthernetImpairment(Base):
	"""The EthernetImpairment class encapsulates a required ethernetImpairment node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EthernetImpairment property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ethernetImpairment'

	def __init__(self, parent):
		super(EthernetImpairment, self).__init__(parent)

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
	def Ppm(self):
		"""Indicates the value that needs to be adjusted for the line transmit frequency.

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)
