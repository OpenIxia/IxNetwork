from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Lacp(Base):
	"""The Lacp class encapsulates a required lacp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Lacp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'lacp'

	def __init__(self, parent):
		super(Lacp, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lacp.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lacp.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)

	@property
	def Link(self):
		"""An instance of the Link class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lacp.link.link.Link)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lacp.link.link import Link
		return Link(self)

	@property
	def EnablePreservePartnerInfo(self):
		"""If true, the fields of previous link are updatedw

		Returns:
			bool
		"""
		return self._get_attribute('enablePreservePartnerInfo')
	@EnablePreservePartnerInfo.setter
	def EnablePreservePartnerInfo(self, value):
		self._set_attribute('enablePreservePartnerInfo', value)

	@property
	def Enabled(self):
		"""If true, the Link Aggregation Control Protocol (LACP) is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IsLacpPortLearnedInfoRefreshed(self):
		"""(read only) If true, the learned port information is up to date.

		Returns:
			bool
		"""
		return self._get_attribute('isLacpPortLearnedInfoRefreshed')

	@property
	def RunningState(self):
		"""The current running state of LACP.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def RefreshLacpPortLearnedInfo(self):
		"""Executes the refreshLacpPortLearnedInfo operation on the server.

		This exec refreshes the LACP port learned information.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLacpPortLearnedInfo', payload=locals(), response_object=None)

	def SendMarkerRequest(self):
		"""Executes the sendMarkerRequest operation on the server.

		This sends a marker request. The contents of the marker PDU contain the current view of partner (which can be defaulted if no partner is present). The marker will be sent regardless of which state the link is in.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendMarkerRequest', payload=locals(), response_object=None)

	def SendUpdate(self):
		"""Executes the sendUpdate operation on the server.

		This exec sends an update to the actor's partners after a change has been made to the link's parameters.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendUpdate', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		This exec starts the LACP protocol.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def StartPdu(self):
		"""Executes the startPdu operation on the server.

		This exec starts PDUs related to LACP (for example, LACPDU, Marker Request PDU, Marker Response PDU) while the protocol is running on the port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartPdu', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This exec stops the LACP protocol.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)

	def StopPdu(self):
		"""Executes the stopPdu operation on the server.

		This exec stops PDUs related to LACP (for example, LACPDU, Marker Request PDU, Marker Response PDU) while the protocol is running on the port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lacp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StopPdu', payload=locals(), response_object=None)
