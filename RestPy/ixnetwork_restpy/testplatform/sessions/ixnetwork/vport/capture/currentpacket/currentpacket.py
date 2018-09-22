from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CurrentPacket(Base):
	"""The CurrentPacket class encapsulates a required currentPacket node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CurrentPacket property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'currentPacket'

	def __init__(self, parent):
		super(CurrentPacket, self).__init__(parent)

	@property
	def Stack(self):
		"""An instance of the Stack class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.stack.Stack)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.stack import Stack
		return Stack(self)

	@property
	def PacketHex(self):
		"""Gets the packet hex of the current packet

		Returns:
			str
		"""
		return self._get_attribute('packetHex')

	def GetPacketFromControlCapture(self, Arg2):
		"""Executes the getPacketFromControlCapture operation on the server.

		The command retrieves a packet from the control capture started on a port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=currentPacket)): The method internally set Arg1 to the current href for this instance
			Arg2 (number): The packet index.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetPacketFromControlCapture', payload=locals(), response_object=None)

	def GetPacketFromDataCapture(self, Arg2):
		"""Executes the getPacketFromDataCapture operation on the server.

		The command retrieves a packet from the data capture started on a port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=currentPacket)): The method internally set Arg1 to the current href for this instance
			Arg2 (number): The packet index.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetPacketFromDataCapture', payload=locals(), response_object=None)
