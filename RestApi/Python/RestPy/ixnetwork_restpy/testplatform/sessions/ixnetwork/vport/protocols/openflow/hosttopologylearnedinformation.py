from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class HostTopologyLearnedInformation(Base):
	"""The HostTopologyLearnedInformation class encapsulates a required hostTopologyLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the HostTopologyLearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'hostTopologyLearnedInformation'

	def __init__(self, parent):
		super(HostTopologyLearnedInformation, self).__init__(parent)

	@property
	def SwitchHostRangeLearnedInfo(self):
		"""An instance of the SwitchHostRangeLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfo.SwitchHostRangeLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfo import SwitchHostRangeLearnedInfo
		return SwitchHostRangeLearnedInfo(self)

	@property
	def SwitchHostRangeLearnedInfoTriggerAttributes(self):
		"""An instance of the SwitchHostRangeLearnedInfoTriggerAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfotriggerattributes.SwitchHostRangeLearnedInfoTriggerAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfotriggerattributes import SwitchHostRangeLearnedInfoTriggerAttributes
		return SwitchHostRangeLearnedInfoTriggerAttributes(self)._select()

	def RefreshHostRangeLearnedInformation(self):
		"""Executes the refreshHostRangeLearnedInformation operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=hostTopologyLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshHostRangeLearnedInformation', payload=locals(), response_object=None)
