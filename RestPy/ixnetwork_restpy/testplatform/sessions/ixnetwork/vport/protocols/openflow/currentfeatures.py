from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CurrentFeatures(Base):
	"""The CurrentFeatures class encapsulates a required currentFeatures node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CurrentFeatures property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'currentFeatures'

	def __init__(self, parent):
		super(CurrentFeatures, self).__init__(parent)

	@property
	def 100MbFd(self):
		"""Indicates that the current features include 100 Mb full-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('100MbFd')
	@100MbFd.setter
	def 100MbFd(self, value):
		self._set_attribute('100MbFd', value)

	@property
	def 100MbHd(self):
		"""Indicates that the current features include 100 Mb half-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('100MbHd')
	@100MbHd.setter
	def 100MbHd(self, value):
		self._set_attribute('100MbHd', value)

	@property
	def 10GbFd(self):
		"""Indicates that the current features include 10 Gb full-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('10GbFd')
	@10GbFd.setter
	def 10GbFd(self, value):
		self._set_attribute('10GbFd', value)

	@property
	def 10MbFd(self):
		"""Indicates that the current features include 10 Mb full-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('10MbFd')
	@10MbFd.setter
	def 10MbFd(self, value):
		self._set_attribute('10MbFd', value)

	@property
	def 10MbHd(self):
		"""Indicates that the current features include 10 Mb half-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('10MbHd')
	@10MbHd.setter
	def 10MbHd(self, value):
		self._set_attribute('10MbHd', value)

	@property
	def 1GbFd(self):
		"""Indicates that the current features include 1 Gb full-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('1GbFd')
	@1GbFd.setter
	def 1GbFd(self, value):
		self._set_attribute('1GbFd', value)

	@property
	def 1GbHd(self):
		"""Indicates that the current features include 1 Gb half-duplex rate support.

		Returns:
			bool
		"""
		return self._get_attribute('1GbHd')
	@1GbHd.setter
	def 1GbHd(self, value):
		self._set_attribute('1GbHd', value)

	@property
	def AsymmetricPause(self):
		"""Indicates that the current features include Asymmetric pause.

		Returns:
			bool
		"""
		return self._get_attribute('asymmetricPause')
	@AsymmetricPause.setter
	def AsymmetricPause(self, value):
		self._set_attribute('asymmetricPause', value)

	@property
	def AutoNegotiation(self):
		"""Indicates that the current features include Auto-negotiation.

		Returns:
			bool
		"""
		return self._get_attribute('autoNegotiation')
	@AutoNegotiation.setter
	def AutoNegotiation(self, value):
		self._set_attribute('autoNegotiation', value)

	@property
	def CopperMedium(self):
		"""Indicates that the current features include Copper medium.

		Returns:
			bool
		"""
		return self._get_attribute('copperMedium')
	@CopperMedium.setter
	def CopperMedium(self, value):
		self._set_attribute('copperMedium', value)

	@property
	def FiberMedium(self):
		"""Indicates that the current features include Fiber medium.

		Returns:
			bool
		"""
		return self._get_attribute('fiberMedium')
	@FiberMedium.setter
	def FiberMedium(self, value):
		self._set_attribute('fiberMedium', value)

	@property
	def Pause(self):
		"""Indicates that the current features include Pause.

		Returns:
			bool
		"""
		return self._get_attribute('pause')
	@Pause.setter
	def Pause(self, value):
		self._set_attribute('pause', value)
