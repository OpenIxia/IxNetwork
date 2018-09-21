from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LinkType(Base):
	"""The LinkType class encapsulates a required linkType node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkType property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'linkType'

	def __init__(self, parent):
		super(LinkType, self).__init__(parent)

	@property
	def OfppfCopper(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppfCopper')
	@OfppfCopper.setter
	def OfppfCopper(self, value):
		self._set_attribute('ofppfCopper', value)

	@property
	def OfppfFiber(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppfFiber')
	@OfppfFiber.setter
	def OfppfFiber(self, value):
		self._set_attribute('ofppfFiber', value)
