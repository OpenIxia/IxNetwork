from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LinkMode(Base):
	"""The LinkMode class encapsulates a required linkMode node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkMode property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'linkMode'

	def __init__(self, parent):
		super(LinkMode, self).__init__(parent)

	@property
	def Ofppf100GbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf100GbFd')
	@Ofppf100GbFd.setter
	def Ofppf100GbFd(self, value):
		self._set_attribute('ofppf100GbFd', value)

	@property
	def Ofppf100MbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf100MbFd')
	@Ofppf100MbFd.setter
	def Ofppf100MbFd(self, value):
		self._set_attribute('ofppf100MbFd', value)

	@property
	def Ofppf100MbHd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf100MbHd')
	@Ofppf100MbHd.setter
	def Ofppf100MbHd(self, value):
		self._set_attribute('ofppf100MbHd', value)

	@property
	def Ofppf10GbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf10GbFd')
	@Ofppf10GbFd.setter
	def Ofppf10GbFd(self, value):
		self._set_attribute('ofppf10GbFd', value)

	@property
	def Ofppf10MbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf10MbFd')
	@Ofppf10MbFd.setter
	def Ofppf10MbFd(self, value):
		self._set_attribute('ofppf10MbFd', value)

	@property
	def Ofppf10MbHd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf10MbHd')
	@Ofppf10MbHd.setter
	def Ofppf10MbHd(self, value):
		self._set_attribute('ofppf10MbHd', value)

	@property
	def Ofppf1GbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf1GbFd')
	@Ofppf1GbFd.setter
	def Ofppf1GbFd(self, value):
		self._set_attribute('ofppf1GbFd', value)

	@property
	def Ofppf1GbHd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf1GbHd')
	@Ofppf1GbHd.setter
	def Ofppf1GbHd(self, value):
		self._set_attribute('ofppf1GbHd', value)

	@property
	def Ofppf1TbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf1TbFd')
	@Ofppf1TbFd.setter
	def Ofppf1TbFd(self, value):
		self._set_attribute('ofppf1TbFd', value)

	@property
	def Ofppf40GbFd(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppf40GbFd')
	@Ofppf40GbFd.setter
	def Ofppf40GbFd(self, value):
		self._set_attribute('ofppf40GbFd', value)

	@property
	def OfppfOther(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppfOther')
	@OfppfOther.setter
	def OfppfOther(self, value):
		self._set_attribute('ofppfOther', value)
