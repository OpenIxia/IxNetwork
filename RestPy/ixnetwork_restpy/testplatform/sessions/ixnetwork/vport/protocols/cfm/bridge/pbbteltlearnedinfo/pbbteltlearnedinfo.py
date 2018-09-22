from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PbbTeLtLearnedInfo(Base):
	"""The PbbTeLtLearnedInfo class encapsulates a system managed pbbTeLtLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTeLtLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTeLtLearnedInfo'

	def __init__(self, parent):
		super(PbbTeLtLearnedInfo, self).__init__(parent)

	@property
	def LtLearnedHop(self):
		"""An instance of the LtLearnedHop class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteltlearnedinfo.ltlearnedhop.ltlearnedhop.LtLearnedHop)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteltlearnedinfo.ltlearnedhop.ltlearnedhop import LtLearnedHop
		return LtLearnedHop(self)

	@property
	def BVlan(self):
		"""(read only) The learned B-VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def DstMacAddress(self):
		"""(read only) The learned destination MAC address.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def HopCount(self):
		"""(read only) The learned number of hops in the link.

		Returns:
			number
		"""
		return self._get_attribute('hopCount')

	@property
	def Hops(self):
		"""(read only) The learned list of hops to reach the particular MEP (MAC address).

		Returns:
			str
		"""
		return self._get_attribute('hops')

	@property
	def MdLevel(self):
		"""(read only) The learned MD level for the periodic OAM.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def ReplyStatus(self):
		"""(read only) The learned current reply status.

		Returns:
			str
		"""
		return self._get_attribute('replyStatus')

	@property
	def SrcMacAddress(self):
		"""(read only) The learned source MAC address.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def TransactionId(self):
		"""(read only) The learned identifier sent with the LTM.

		Returns:
			number
		"""
		return self._get_attribute('transactionId')

	def find(self, BVlan=None, DstMacAddress=None, HopCount=None, Hops=None, MdLevel=None, ReplyStatus=None, SrcMacAddress=None, TransactionId=None):
		"""Finds and retrieves pbbTeLtLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTeLtLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTeLtLearnedInfo data from the server.

		Args:
			BVlan (str): (read only) The learned B-VLAN identifier.
			DstMacAddress (str): (read only) The learned destination MAC address.
			HopCount (number): (read only) The learned number of hops in the link.
			Hops (str): (read only) The learned list of hops to reach the particular MEP (MAC address).
			MdLevel (number): (read only) The learned MD level for the periodic OAM.
			ReplyStatus (str): (read only) The learned current reply status.
			SrcMacAddress (str): (read only) The learned source MAC address.
			TransactionId (number): (read only) The learned identifier sent with the LTM.

		Returns:
			self: This instance with matching pbbTeLtLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTeLtLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTeLtLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
