from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FramePayload(Base):
	"""The FramePayload class encapsulates a required framePayload node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FramePayload property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'framePayload'

	def __init__(self, parent):
		super(FramePayload, self).__init__(parent)

	@property
	def CustomPattern(self):
		"""If Frame Payload type is Custom, then this attribute specifies a string in hex format.

		Returns:
			str
		"""
		return self._get_attribute('customPattern')
	@CustomPattern.setter
	def CustomPattern(self, value):
		self._set_attribute('customPattern', value)

	@property
	def CustomRepeat(self):
		"""If true, Custom Pattern is repeated.

		Returns:
			bool
		"""
		return self._get_attribute('customRepeat')
	@CustomRepeat.setter
	def CustomRepeat(self, value):
		self._set_attribute('customRepeat', value)

	@property
	def Type(self):
		"""The types of Frame Payload.

		Returns:
			str(CJPAT|CRPAT|custom|decrementByte|decrementWord|incrementByte|incrementWord|random)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)
