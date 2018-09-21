from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Cist(Base):
	"""The Cist class encapsulates a required cist node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Cist property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'cist'

	def __init__(self, parent):
		super(Cist, self).__init__(parent)

	@property
	def CistLearnedInfo(self):
		"""An instance of the CistLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.cistlearnedinfo.cistlearnedinfo.CistLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.cistlearnedinfo.cistlearnedinfo import CistLearnedInfo
		return CistLearnedInfo(self)._select()

	@property
	def LearnedInterface(self):
		"""An instance of the LearnedInterface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.learnedinterface.learnedinterface.LearnedInterface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.learnedinterface.learnedinterface import LearnedInterface
		return LearnedInterface(self)
