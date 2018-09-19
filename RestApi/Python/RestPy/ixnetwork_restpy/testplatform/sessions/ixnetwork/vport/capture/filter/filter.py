from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Filter(Base):
	"""The Filter class encapsulates a required filter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Filter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'filter'

	def __init__(self, parent):
		super(Filter, self).__init__(parent)

	@property
	def CaptureFilterDA(self):
		"""One of two available destination MAC addresses to filter on. Applicable only when capturefilternable is set to true.

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('captureFilterDA')
	@CaptureFilterDA.setter
	def CaptureFilterDA(self, value):
		self._set_attribute('captureFilterDA', value)

	@property
	def CaptureFilterEnable(self):
		"""Enables or disables the capture filter.

		Returns:
			bool
		"""
		return self._get_attribute('captureFilterEnable')
	@CaptureFilterEnable.setter
	def CaptureFilterEnable(self, value):
		self._set_attribute('captureFilterEnable', value)

	@property
	def CaptureFilterError(self):
		"""Applicable only when captureFilterEnable is set to true.

		Returns:
			str(errAnyFrame|errAnyIpTcpUdpChecksumError|errAnySequencekError|errBadCRC|errBadFrame|errBigSequenceError|errDataIntegrityError|errGoodFrame|errInvalidFcoeFrame|errReverseSequenceError|errSmallSequenceError)
		"""
		return self._get_attribute('captureFilterError')
	@CaptureFilterError.setter
	def CaptureFilterError(self, value):
		self._set_attribute('captureFilterError', value)

	@property
	def CaptureFilterExpressionString(self):
		"""String composed of SA1, DA1, P1, P2, optionally negated with '!', and connected with operators 'and', 'or', 'xor', 'nand' or 'nor'. (Eg: {DA1 and SA1 or !P1 and P2} ). NOTE: The 'or', 'xor', 'nand' and 'nor' operators are available only on the following load modules: XMVDC, NGY, XMSP12, LAVA(MK), Xcellon AP, Xcellon NP.

		Returns:
			str
		"""
		return self._get_attribute('captureFilterExpressionString')
	@CaptureFilterExpressionString.setter
	def CaptureFilterExpressionString(self, value):
		self._set_attribute('captureFilterExpressionString', value)

	@property
	def CaptureFilterFrameSizeEnable(self):
		"""Enables or disables the frame size constraint which specifies a range of frame.

		Returns:
			bool
		"""
		return self._get_attribute('captureFilterFrameSizeEnable')
	@CaptureFilterFrameSizeEnable.setter
	def CaptureFilterFrameSizeEnable(self, value):
		self._set_attribute('captureFilterFrameSizeEnable', value)

	@property
	def CaptureFilterFrameSizeFrom(self):
		"""Applicable only when captureFilterFrameSizeEnable is enabled. The minimum range of the size of frame to be filtered.

		Returns:
			number
		"""
		return self._get_attribute('captureFilterFrameSizeFrom')
	@CaptureFilterFrameSizeFrom.setter
	def CaptureFilterFrameSizeFrom(self, value):
		self._set_attribute('captureFilterFrameSizeFrom', value)

	@property
	def CaptureFilterFrameSizeTo(self):
		"""Applicable only when captureFilterFrameSizeEnable is enabled. The maximum range of the size of frame to be filtered.

		Returns:
			number
		"""
		return self._get_attribute('captureFilterFrameSizeTo')
	@CaptureFilterFrameSizeTo.setter
	def CaptureFilterFrameSizeTo(self, value):
		self._set_attribute('captureFilterFrameSizeTo', value)

	@property
	def CaptureFilterPattern(self):
		"""Applicable only when captureFilterEnable is set to true.

		Returns:
			str(anyPattern|notPattern1|notPattern2|pattern1|pattern1AndPattern2|pattern2)
		"""
		return self._get_attribute('captureFilterPattern')
	@CaptureFilterPattern.setter
	def CaptureFilterPattern(self, value):
		self._set_attribute('captureFilterPattern', value)

	@property
	def CaptureFilterSA(self):
		"""One of two available destination MAC addresses to filter on. Applicable only when capturefilternable is set to true.

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('captureFilterSA')
	@CaptureFilterSA.setter
	def CaptureFilterSA(self, value):
		self._set_attribute('captureFilterSA', value)
