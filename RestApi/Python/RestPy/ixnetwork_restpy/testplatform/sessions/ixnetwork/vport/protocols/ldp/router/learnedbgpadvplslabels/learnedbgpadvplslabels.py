from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedBgpAdVplsLabels(Base):
	"""The LearnedBgpAdVplsLabels class encapsulates a system managed learnedBgpAdVplsLabels node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedBgpAdVplsLabels property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedBgpAdVplsLabels'

	def __init__(self, parent):
		super(LearnedBgpAdVplsLabels, self).__init__(parent)

	@property
	def CBit(self):
		"""(Read Only) The boolean value for c Bit.

		Returns:
			bool
		"""
		return self._get_attribute('cBit')

	@property
	def GroupId(self):
		"""(Read Only) The 4-byte unsigned number indicating the Group Id.

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def Label(self):
		"""(Read Only) The 4-byte unsigned number indicating the Label.

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LocalPwSubState(self):
		"""(Read Only) The 4-byte unsigned number indicating the Local PW Sub State.

		Returns:
			number
		"""
		return self._get_attribute('localPwSubState')

	@property
	def Mtu(self):
		"""(Read Only) The 2 byte value for the maximum Transmission Unit (MTU).

		Returns:
			number
		"""
		return self._get_attribute('mtu')

	@property
	def PeerAddress(self):
		"""(Read Only) The Peer Address.

		Returns:
			str
		"""
		return self._get_attribute('peerAddress')

	@property
	def PwState(self):
		"""(Read Only) The boolean value for PW State.

		Returns:
			bool
		"""
		return self._get_attribute('pwState')

	@property
	def RemotePwSubState(self):
		"""(Read Only)The 4-byte unsigned number indicating the PE Sub State.

		Returns:
			number
		"""
		return self._get_attribute('remotePwSubState')

	@property
	def SourceAii(self):
		"""(Read Only) The 4 byte unsigned number indicationg the Source AII.

		Returns:
			number
		"""
		return self._get_attribute('sourceAii')

	@property
	def TargetAii(self):
		"""(Read Only) The 4 byte unsigned number indicationg the Target AII.

		Returns:
			number
		"""
		return self._get_attribute('targetAii')

	@property
	def VplsId(self):
		"""(Read Only) The VPLS ID indicated by an IP or AS.

		Returns:
			str
		"""
		return self._get_attribute('vplsId')

	def find(self, CBit=None, GroupId=None, Label=None, LocalPwSubState=None, Mtu=None, PeerAddress=None, PwState=None, RemotePwSubState=None, SourceAii=None, TargetAii=None, VplsId=None):
		"""Finds and retrieves learnedBgpAdVplsLabels data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedBgpAdVplsLabels data from the server.
		By default the find method takes no parameters and will retrieve all learnedBgpAdVplsLabels data from the server.

		Args:
			CBit (bool): (Read Only) The boolean value for c Bit.
			GroupId (number): (Read Only) The 4-byte unsigned number indicating the Group Id.
			Label (number): (Read Only) The 4-byte unsigned number indicating the Label.
			LocalPwSubState (number): (Read Only) The 4-byte unsigned number indicating the Local PW Sub State.
			Mtu (number): (Read Only) The 2 byte value for the maximum Transmission Unit (MTU).
			PeerAddress (str): (Read Only) The Peer Address.
			PwState (bool): (Read Only) The boolean value for PW State.
			RemotePwSubState (number): (Read Only)The 4-byte unsigned number indicating the PE Sub State.
			SourceAii (number): (Read Only) The 4 byte unsigned number indicationg the Source AII.
			TargetAii (number): (Read Only) The 4 byte unsigned number indicationg the Target AII.
			VplsId (str): (Read Only) The VPLS ID indicated by an IP or AS.

		Returns:
			self: This instance with matching learnedBgpAdVplsLabels data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedBgpAdVplsLabels data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedBgpAdVplsLabels data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
