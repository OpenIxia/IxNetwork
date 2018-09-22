from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LtLearnedInfo(Base):
	"""The LtLearnedInfo class encapsulates a system managed ltLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LtLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ltLearnedInfo'

	def __init__(self, parent):
		super(LtLearnedInfo, self).__init__(parent)

	@property
	def LtLearnedHop(self):
		"""An instance of the LtLearnedHop class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.ltlearnedinfo.ltlearnedhop.ltlearnedhop.LtLearnedHop)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.ltlearnedinfo.ltlearnedhop.ltlearnedhop import LtLearnedHop
		return LtLearnedHop(self)

	@property
	def CVlan(self):
		"""(read only) The stacked VLAN identifier for the link trace message.

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def DstMacAddress(self):
		"""(read only) The destination MAC address associated with the link trace message.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def HopCount(self):
		"""(read only) The hop count for the link trace message.

		Returns:
			number
		"""
		return self._get_attribute('hopCount')

	@property
	def Hops(self):
		"""(read only) The number of hops for the link trace message.

		Returns:
			str
		"""
		return self._get_attribute('hops')

	@property
	def MdLevel(self):
		"""(read only) The MD level associated with the link trace message.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def ReplyStatus(self):
		"""(read only) Indicates the status of the reply for the link trace message.

		Returns:
			str
		"""
		return self._get_attribute('replyStatus')

	@property
	def SVlan(self):
		"""(read only) The single VLAN identifier associated with the link trace message.

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def SrcMacAddress(self):
		"""(read only) The source MAC address associated with the link trace message.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def TransactionId(self):
		"""(read only) The transaction identifier sent with the link trace message.

		Returns:
			number
		"""
		return self._get_attribute('transactionId')

	def find(self, CVlan=None, DstMacAddress=None, HopCount=None, Hops=None, MdLevel=None, ReplyStatus=None, SVlan=None, SrcMacAddress=None, TransactionId=None):
		"""Finds and retrieves ltLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ltLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all ltLearnedInfo data from the server.

		Args:
			CVlan (str): (read only) The stacked VLAN identifier for the link trace message.
			DstMacAddress (str): (read only) The destination MAC address associated with the link trace message.
			HopCount (number): (read only) The hop count for the link trace message.
			Hops (str): (read only) The number of hops for the link trace message.
			MdLevel (number): (read only) The MD level associated with the link trace message.
			ReplyStatus (str): (read only) Indicates the status of the reply for the link trace message.
			SVlan (str): (read only) The single VLAN identifier associated with the link trace message.
			SrcMacAddress (str): (read only) The source MAC address associated with the link trace message.
			TransactionId (number): (read only) The transaction identifier sent with the link trace message.

		Returns:
			self: This instance with matching ltLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ltLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ltLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
