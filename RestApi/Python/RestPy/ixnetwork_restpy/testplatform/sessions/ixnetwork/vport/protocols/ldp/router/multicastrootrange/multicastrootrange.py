from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MulticastRootRange(Base):
	"""The MulticastRootRange class encapsulates a user managed multicastRootRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastRootRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastRootRange'

	def __init__(self, parent):
		super(MulticastRootRange, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.opaquevalueelement.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.opaquevalueelement.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def SourceTrafficRange(self):
		"""An instance of the SourceTrafficRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.sourcetrafficrange.sourcetrafficrange.SourceTrafficRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastrootrange.sourcetrafficrange.sourcetrafficrange import SourceTrafficRange
		return SourceTrafficRange(self)

	@property
	def ContinuousIncrOpaqueValuesAcrossRoot(self):
		"""Signifies the continuous incremented opaque values across root.

		Returns:
			bool
		"""
		return self._get_attribute('continuousIncrOpaqueValuesAcrossRoot')
	@ContinuousIncrOpaqueValuesAcrossRoot.setter
	def ContinuousIncrOpaqueValuesAcrossRoot(self, value):
		self._set_attribute('continuousIncrOpaqueValuesAcrossRoot', value)

	@property
	def LspCount(self):
		"""Signifies the count of LSP.

		Returns:
			number
		"""
		return self._get_attribute('lspCount')
	@LspCount.setter
	def LspCount(self, value):
		self._set_attribute('lspCount', value)

	@property
	def LspType(self):
		"""The type of multicast LSP.

		Returns:
			str()
		"""
		return self._get_attribute('lspType')

	@property
	def RootAddrStep(self):
		"""The Root Address increment step. This is applicable only if Root Address Count is greater than 1.

		Returns:
			str
		"""
		return self._get_attribute('rootAddrStep')
	@RootAddrStep.setter
	def RootAddrStep(self, value):
		self._set_attribute('rootAddrStep', value)

	@property
	def RootAddress(self):
		"""The root address of the multicast LSP.

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')
	@RootAddress.setter
	def RootAddress(self, value):
		self._set_attribute('rootAddress', value)

	@property
	def RootAddressCount(self):
		"""The root address count for this Multicast FEC range.

		Returns:
			number
		"""
		return self._get_attribute('rootAddressCount')
	@RootAddressCount.setter
	def RootAddressCount(self, value):
		self._set_attribute('rootAddressCount', value)

	def add(self, ContinuousIncrOpaqueValuesAcrossRoot=None, LspCount=None, RootAddrStep=None, RootAddress=None, RootAddressCount=None):
		"""Adds a new multicastRootRange node on the server and retrieves it in this instance.

		Args:
			ContinuousIncrOpaqueValuesAcrossRoot (bool): Signifies the continuous incremented opaque values across root.
			LspCount (number): Signifies the count of LSP.
			RootAddrStep (str): The Root Address increment step. This is applicable only if Root Address Count is greater than 1.
			RootAddress (str): The root address of the multicast LSP.
			RootAddressCount (number): The root address count for this Multicast FEC range.

		Returns:
			self: This instance with all currently retrieved multicastRootRange data using find and the newly added multicastRootRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastRootRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ContinuousIncrOpaqueValuesAcrossRoot=None, LspCount=None, LspType=None, RootAddrStep=None, RootAddress=None, RootAddressCount=None):
		"""Finds and retrieves multicastRootRange data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastRootRange data from the server.
		By default the find method takes no parameters and will retrieve all multicastRootRange data from the server.

		Args:
			ContinuousIncrOpaqueValuesAcrossRoot (bool): Signifies the continuous incremented opaque values across root.
			LspCount (number): Signifies the count of LSP.
			LspType (str()): The type of multicast LSP.
			RootAddrStep (str): The Root Address increment step. This is applicable only if Root Address Count is greater than 1.
			RootAddress (str): The root address of the multicast LSP.
			RootAddressCount (number): The root address count for this Multicast FEC range.

		Returns:
			self: This instance with matching multicastRootRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastRootRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastRootRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
