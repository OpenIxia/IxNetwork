from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PbbTeCcmLearnedInfo(Base):
	"""The PbbTeCcmLearnedInfo class encapsulates a system managed pbbTeCcmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTeCcmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTeCcmLearnedInfo'

	def __init__(self, parent):
		super(PbbTeCcmLearnedInfo, self).__init__(parent)

	@property
	def BVlan(self):
		"""(read only) The VLAN identifier for the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def CciInterval(self):
		"""(read only) The continuity check message interval, in seconds.

		Returns:
			str
		"""
		return self._get_attribute('cciInterval')

	@property
	def ErrCcmDefect(self):
		"""(read only) If true, CCM defect errors have been detected.

		Returns:
			bool
		"""
		return self._get_attribute('errCcmDefect')

	@property
	def ErrCcmDefectCount(self):
		"""(read only) The number of CCM defect errors received.

		Returns:
			number
		"""
		return self._get_attribute('errCcmDefectCount')

	@property
	def IfaceTlvDefectCount(self):
		"""(read only) The number of interface TLV defects received.

		Returns:
			number
		"""
		return self._get_attribute('ifaceTlvDefectCount')

	@property
	def MdLevel(self):
		"""(read only) The MD level for the CCM message.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def MdName(self):
		"""(read only) The MD name for the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('mdName')

	@property
	def MdNameFormat(self):
		"""(read only) The MD name format for the CCM message.

		Returns:
			number
		"""
		return self._get_attribute('mdNameFormat')

	@property
	def OutOfSequenceCcmCount(self):
		"""(read only) The number of out of sequence CCM messages received.

		Returns:
			number
		"""
		return self._get_attribute('outOfSequenceCcmCount')

	@property
	def PortTlvDefectCount(self):
		"""(read only) The number of port TLV defect errors received.

		Returns:
			number
		"""
		return self._get_attribute('portTlvDefectCount')

	@property
	def RdiRxCount(self):
		"""(read only) The rdi rx count.

		Returns:
			number
		"""
		return self._get_attribute('rdiRxCount')

	@property
	def RdiRxState(self):
		"""(read only) The rdi rx state.

		Returns:
			str
		"""
		return self._get_attribute('rdiRxState')

	@property
	def RdiTxCount(self):
		"""(read only) The rdi tx count.

		Returns:
			number
		"""
		return self._get_attribute('rdiTxCount')

	@property
	def RdiTxState(self):
		"""(read only) The rdi tx state.

		Returns:
			str
		"""
		return self._get_attribute('rdiTxState')

	@property
	def ReceivedIfaceTlvDefect(self):
		"""(read only) If true, interface TLV defect errors have been received.

		Returns:
			bool
		"""
		return self._get_attribute('receivedIfaceTlvDefect')

	@property
	def ReceivedPortTlvDefect(self):
		"""(read only) If true, port TLV defect errors have been received.

		Returns:
			bool
		"""
		return self._get_attribute('receivedPortTlvDefect')

	@property
	def ReceivedRdi(self):
		"""(read only) If true, RDI defect error messages have been receved.

		Returns:
			bool
		"""
		return self._get_attribute('receivedRdi')

	@property
	def RemoteMacAddress(self):
		"""(read only) The remote MAC address for the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('remoteMacAddress')

	@property
	def RemoteMepDefectCount(self):
		"""(read only) The number of RMEP defect errors received.

		Returns:
			number
		"""
		return self._get_attribute('remoteMepDefectCount')

	@property
	def RemoteMepId(self):
		"""(read only) The RMEP identifier for the CCM.

		Returns:
			str
		"""
		return self._get_attribute('remoteMepId')

	@property
	def RmepCcmDefect(self):
		"""(read only) If true, RMEP CCM defect errors have been received.

		Returns:
			bool
		"""
		return self._get_attribute('rmepCcmDefect')

	@property
	def ShortMaName(self):
		"""(read only) The Short MA name for the CCM.

		Returns:
			str
		"""
		return self._get_attribute('shortMaName')

	@property
	def ShortMaNameFormat(self):
		"""(read only) The Short MA name format for the CCM.

		Returns:
			number
		"""
		return self._get_attribute('shortMaNameFormat')

	@property
	def SrcMacAddress(self):
		"""(read only) The source MAC address for the CCM.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def SrcMepId(self):
		"""(read only) The source MEP identifier for the CCM.

		Returns:
			number
		"""
		return self._get_attribute('srcMepId')

	def find(self, BVlan=None, CciInterval=None, ErrCcmDefect=None, ErrCcmDefectCount=None, IfaceTlvDefectCount=None, MdLevel=None, MdName=None, MdNameFormat=None, OutOfSequenceCcmCount=None, PortTlvDefectCount=None, RdiRxCount=None, RdiRxState=None, RdiTxCount=None, RdiTxState=None, ReceivedIfaceTlvDefect=None, ReceivedPortTlvDefect=None, ReceivedRdi=None, RemoteMacAddress=None, RemoteMepDefectCount=None, RemoteMepId=None, RmepCcmDefect=None, ShortMaName=None, ShortMaNameFormat=None, SrcMacAddress=None, SrcMepId=None):
		"""Finds and retrieves pbbTeCcmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTeCcmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTeCcmLearnedInfo data from the server.

		Args:
			BVlan (str): (read only) The VLAN identifier for the CCM message.
			CciInterval (str): (read only) The continuity check message interval, in seconds.
			ErrCcmDefect (bool): (read only) If true, CCM defect errors have been detected.
			ErrCcmDefectCount (number): (read only) The number of CCM defect errors received.
			IfaceTlvDefectCount (number): (read only) The number of interface TLV defects received.
			MdLevel (number): (read only) The MD level for the CCM message.
			MdName (str): (read only) The MD name for the CCM message.
			MdNameFormat (number): (read only) The MD name format for the CCM message.
			OutOfSequenceCcmCount (number): (read only) The number of out of sequence CCM messages received.
			PortTlvDefectCount (number): (read only) The number of port TLV defect errors received.
			RdiRxCount (number): (read only) The rdi rx count.
			RdiRxState (str): (read only) The rdi rx state.
			RdiTxCount (number): (read only) The rdi tx count.
			RdiTxState (str): (read only) The rdi tx state.
			ReceivedIfaceTlvDefect (bool): (read only) If true, interface TLV defect errors have been received.
			ReceivedPortTlvDefect (bool): (read only) If true, port TLV defect errors have been received.
			ReceivedRdi (bool): (read only) If true, RDI defect error messages have been receved.
			RemoteMacAddress (str): (read only) The remote MAC address for the CCM message.
			RemoteMepDefectCount (number): (read only) The number of RMEP defect errors received.
			RemoteMepId (str): (read only) The RMEP identifier for the CCM.
			RmepCcmDefect (bool): (read only) If true, RMEP CCM defect errors have been received.
			ShortMaName (str): (read only) The Short MA name for the CCM.
			ShortMaNameFormat (number): (read only) The Short MA name format for the CCM.
			SrcMacAddress (str): (read only) The source MAC address for the CCM.
			SrcMepId (number): (read only) The source MEP identifier for the CCM.

		Returns:
			self: This instance with matching pbbTeCcmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTeCcmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTeCcmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
