from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LinkFeature(Base):
	"""The LinkFeature class encapsulates a required linkFeature node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkFeature property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'linkFeature'

	def __init__(self, parent):
		super(LinkFeature, self).__init__(parent)

	@property
	def OfppfAutoNegotiation(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppfAutoNegotiation')
	@OfppfAutoNegotiation.setter
	def OfppfAutoNegotiation(self, value):
		self._set_attribute('ofppfAutoNegotiation', value)

	@property
	def OfppfPause(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppfPause')
	@OfppfPause.setter
	def OfppfPause(self, value):
		self._set_attribute('ofppfPause', value)

	@property
	def OfppfPauseAsym(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ofppfPauseAsym')
	@OfppfPauseAsym.setter
	def OfppfPauseAsym(self, value):
		self._set_attribute('ofppfPauseAsym', value)
