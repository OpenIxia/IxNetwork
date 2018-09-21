from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MulticastLeafRange(Base):
	"""The MulticastLeafRange class encapsulates a user managed multicastLeafRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastLeafRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastLeafRange'

	def __init__(self, parent):
		super(MulticastLeafRange, self).__init__(parent)

	@property
	def GroupTrafficRange(self):
		"""An instance of the GroupTrafficRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastleafrange.grouptrafficrange.grouptrafficrange.GroupTrafficRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastleafrange.grouptrafficrange.grouptrafficrange import GroupTrafficRange
		return GroupTrafficRange(self)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastleafrange.opaquevalueelement.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.multicastleafrange.opaquevalueelement.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def ContinuousIncrOpaqueValuesAcrossRoot(self):
		"""It signifies the continuous increment of opaque values across root.

		Returns:
			bool
		"""
		return self._get_attribute('continuousIncrOpaqueValuesAcrossRoot')
	@ContinuousIncrOpaqueValuesAcrossRoot.setter
	def ContinuousIncrOpaqueValuesAcrossRoot(self, value):
		self._set_attribute('continuousIncrOpaqueValuesAcrossRoot', value)

	@property
	def Enabled(self):
		"""If true, enables the protocol.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def LabelValueStart(self):
		"""The first label in the range of labels.

		Returns:
			number
		"""
		return self._get_attribute('labelValueStart')
	@LabelValueStart.setter
	def LabelValueStart(self, value):
		self._set_attribute('labelValueStart', value)

	@property
	def LabelValueStep(self):
		"""The label value increment step for more than 1 range.

		Returns:
			number
		"""
		return self._get_attribute('labelValueStep')
	@LabelValueStep.setter
	def LabelValueStep(self, value):
		self._set_attribute('labelValueStep', value)

	@property
	def LspCountPerRoot(self):
		"""This is to specify how many different LSPs are created per Root.

		Returns:
			number
		"""
		return self._get_attribute('lspCountPerRoot')
	@LspCountPerRoot.setter
	def LspCountPerRoot(self, value):
		self._set_attribute('lspCountPerRoot', value)

	@property
	def LspType(self):
		"""The type of multicast LSP.

		Returns:
			str(p2mp)
		"""
		return self._get_attribute('lspType')

	@property
	def RootAddrCount(self):
		"""The root address count for this Multicast FEC range.

		Returns:
			number
		"""
		return self._get_attribute('rootAddrCount')
	@RootAddrCount.setter
	def RootAddrCount(self, value):
		self._set_attribute('rootAddrCount', value)

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

	def add(self, ContinuousIncrOpaqueValuesAcrossRoot=None, Enabled=None, LabelValueStart=None, LabelValueStep=None, LspCountPerRoot=None, RootAddrCount=None, RootAddrStep=None, RootAddress=None):
		"""Adds a new multicastLeafRange node on the server and retrieves it in this instance.

		Args:
			ContinuousIncrOpaqueValuesAcrossRoot (bool): It signifies the continuous increment of opaque values across root.
			Enabled (bool): If true, enables the protocol.
			LabelValueStart (number): The first label in the range of labels.
			LabelValueStep (number): The label value increment step for more than 1 range.
			LspCountPerRoot (number): This is to specify how many different LSPs are created per Root.
			RootAddrCount (number): The root address count for this Multicast FEC range.
			RootAddrStep (str): The Root Address increment step. This is applicable only if Root Address Count is greater than 1.
			RootAddress (str): The root address of the multicast LSP.

		Returns:
			self: This instance with all currently retrieved multicastLeafRange data using find and the newly added multicastLeafRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastLeafRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ContinuousIncrOpaqueValuesAcrossRoot=None, Enabled=None, LabelValueStart=None, LabelValueStep=None, LspCountPerRoot=None, LspType=None, RootAddrCount=None, RootAddrStep=None, RootAddress=None):
		"""Finds and retrieves multicastLeafRange data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastLeafRange data from the server.
		By default the find method takes no parameters and will retrieve all multicastLeafRange data from the server.

		Args:
			ContinuousIncrOpaqueValuesAcrossRoot (bool): It signifies the continuous increment of opaque values across root.
			Enabled (bool): If true, enables the protocol.
			LabelValueStart (number): The first label in the range of labels.
			LabelValueStep (number): The label value increment step for more than 1 range.
			LspCountPerRoot (number): This is to specify how many different LSPs are created per Root.
			LspType (str(p2mp)): The type of multicast LSP.
			RootAddrCount (number): The root address count for this Multicast FEC range.
			RootAddrStep (str): The Root Address increment step. This is applicable only if Root Address Count is greater than 1.
			RootAddress (str): The root address of the multicast LSP.

		Returns:
			self: This instance with matching multicastLeafRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastLeafRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastLeafRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
