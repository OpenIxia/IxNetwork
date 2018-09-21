from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchFlowInstructionLearnedInfo(Base):
	"""The SwitchFlowInstructionLearnedInfo class encapsulates a system managed switchFlowInstructionLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchFlowInstructionLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchFlowInstructionLearnedInfo'

	def __init__(self, parent):
		super(SwitchFlowInstructionLearnedInfo, self).__init__(parent)

	@property
	def SwitchActionV131LearnedInfo(self):
		"""An instance of the SwitchActionV131LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchactionv131learnedinfo.SwitchActionV131LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchactionv131learnedinfo import SwitchActionV131LearnedInfo
		return SwitchActionV131LearnedInfo(self)

	@property
	def Experimenter(self):
		"""This describes the unique Experimenter identifier. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('experimenter')

	@property
	def ExperimenterData(self):
		"""This describes the data of the Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""This describes the data length of the Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def InstructionType(self):
		"""This describes the action type associated with this instruction.

		Returns:
			str
		"""
		return self._get_attribute('instructionType')

	@property
	def Metadata(self):
		"""This describes the table metadata value used to pass information between tables.

		Returns:
			str
		"""
		return self._get_attribute('metadata')

	@property
	def MetadataMask(self):
		"""This describes the metadata bitmask value.

		Returns:
			str
		"""
		return self._get_attribute('metadataMask')

	@property
	def MeterId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def TableId(self):
		"""This describes the table identifier. It indicates the next table in the packet processing pipeline.

		Returns:
			number
		"""
		return self._get_attribute('tableId')

	def find(self, Experimenter=None, ExperimenterData=None, ExperimenterDataLength=None, InstructionType=None, Metadata=None, MetadataMask=None, MeterId=None, TableId=None):
		"""Finds and retrieves switchFlowInstructionLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchFlowInstructionLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchFlowInstructionLearnedInfo data from the server.

		Args:
			Experimenter (number): This describes the unique Experimenter identifier. The default value is 1.
			ExperimenterData (str): This describes the data of the Experimenter.
			ExperimenterDataLength (number): This describes the data length of the Experimenter.
			InstructionType (str): This describes the action type associated with this instruction.
			Metadata (str): This describes the table metadata value used to pass information between tables.
			MetadataMask (str): This describes the metadata bitmask value.
			MeterId (number): NOT DEFINED
			TableId (number): This describes the table identifier. It indicates the next table in the packet processing pipeline.

		Returns:
			self: This instance with matching switchFlowInstructionLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchFlowInstructionLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchFlowInstructionLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
