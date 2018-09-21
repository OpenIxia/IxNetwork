from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CcmLearnedInfo(Base):
	"""The CcmLearnedInfo class encapsulates a system managed ccmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CcmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ccmLearnedInfo'

	def __init__(self, parent):
		super(CcmLearnedInfo, self).__init__(parent)

	@property
	def AllRmepDead(self):
		"""(read only) If true, indicates this MEP is receiving none of the remote MEPs' CCMs.

		Returns:
			bool
		"""
		return self._get_attribute('allRmepDead')

	@property
	def CVlan(self):
		"""(read only) The stacked VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def CciInterval(self):
		"""(read only) The Continuity Check interval.

		Returns:
			str
		"""
		return self._get_attribute('cciInterval')

	@property
	def ErrCcmDefect(self):
		"""(read only) If true, a CCM defect error has been detected.

		Returns:
			bool
		"""
		return self._get_attribute('errCcmDefect')

	@property
	def ErrCcmDefectCount(self):
		"""The total number of CCM defect error that has been detected.

		Returns:
			number
		"""
		return self._get_attribute('errCcmDefectCount')

	@property
	def IfaceTlvDefectCount(self):
		"""The total number of iface Tlv defect error that has been detected.

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
		"""(read only) The MD name associated with the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('mdName')

	@property
	def MdNameFormat(self):
		"""(read only) The MD Name Format of the CCM message.

		Returns:
			number
		"""
		return self._get_attribute('mdNameFormat')

	@property
	def MepId(self):
		"""(read only) The MEP identifier of the CCM message.

		Returns:
			number
		"""
		return self._get_attribute('mepId')

	@property
	def MepMacAddress(self):
		"""(read only) The MEP MAC address of the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('mepMacAddress')

	@property
	def OutOfSequenceCcmCount(self):
		"""(read only) The number of Out of Sequence CCM messages received.

		Returns:
			number
		"""
		return self._get_attribute('outOfSequenceCcmCount')

	@property
	def PortTlvDefectCount(self):
		"""The total number of Port Tlv defect error that has been detected.

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
	def ReceivedAis(self):
		"""(read only) If true, AIS messages have been detected.

		Returns:
			bool
		"""
		return self._get_attribute('receivedAis')

	@property
	def ReceivedIfaceTlvDefect(self):
		"""(read only) If true, interface TLV defect messages have been detected.

		Returns:
			bool
		"""
		return self._get_attribute('receivedIfaceTlvDefect')

	@property
	def ReceivedPortTlvDefect(self):
		"""(read only) If true, port TLV defect messages have been detected.

		Returns:
			bool
		"""
		return self._get_attribute('receivedPortTlvDefect')

	@property
	def ReceivedRdi(self):
		"""(read only) If true, RDI messages have been detected.

		Returns:
			bool
		"""
		return self._get_attribute('receivedRdi')

	@property
	def RemoteMepDefectCount(self):
		"""The total number of remote Mep defect error that has been detected.

		Returns:
			number
		"""
		return self._get_attribute('remoteMepDefectCount')

	@property
	def RmepCcmDefect(self):
		"""(read only) If true, remote MEP CCM defect messages have been detected.

		Returns:
			bool
		"""
		return self._get_attribute('rmepCcmDefect')

	@property
	def SVlan(self):
		"""(read only) The single VLAN associated with the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def ShortMaName(self):
		"""(read only) The Short MA Name associated with the CCM message.

		Returns:
			str
		"""
		return self._get_attribute('shortMaName')

	@property
	def ShortMaNameFormat(self):
		"""(read only) The Short MA Name format associated with the CCM message.

		Returns:
			number
		"""
		return self._get_attribute('shortMaNameFormat')

	@property
	def SomeRmepDefect(self):
		"""(read only) Indicates the aggregate state of the Remote MEP State Machines. If true, at least one of the Remote MEP State Machines is not receiving valid CCMs from its remote MEPs. If false, all Remote MEP State Machines are receiving valid CCMs.

		Returns:
			bool
		"""
		return self._get_attribute('someRmepDefect')

	def find(self, AllRmepDead=None, CVlan=None, CciInterval=None, ErrCcmDefect=None, ErrCcmDefectCount=None, IfaceTlvDefectCount=None, MdLevel=None, MdName=None, MdNameFormat=None, MepId=None, MepMacAddress=None, OutOfSequenceCcmCount=None, PortTlvDefectCount=None, RdiRxCount=None, RdiRxState=None, ReceivedAis=None, ReceivedIfaceTlvDefect=None, ReceivedPortTlvDefect=None, ReceivedRdi=None, RemoteMepDefectCount=None, RmepCcmDefect=None, SVlan=None, ShortMaName=None, ShortMaNameFormat=None, SomeRmepDefect=None):
		"""Finds and retrieves ccmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ccmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all ccmLearnedInfo data from the server.

		Args:
			AllRmepDead (bool): (read only) If true, indicates this MEP is receiving none of the remote MEPs' CCMs.
			CVlan (str): (read only) The stacked VLAN identifier.
			CciInterval (str): (read only) The Continuity Check interval.
			ErrCcmDefect (bool): (read only) If true, a CCM defect error has been detected.
			ErrCcmDefectCount (number): The total number of CCM defect error that has been detected.
			IfaceTlvDefectCount (number): The total number of iface Tlv defect error that has been detected.
			MdLevel (number): (read only) The MD level for the CCM message.
			MdName (str): (read only) The MD name associated with the CCM message.
			MdNameFormat (number): (read only) The MD Name Format of the CCM message.
			MepId (number): (read only) The MEP identifier of the CCM message.
			MepMacAddress (str): (read only) The MEP MAC address of the CCM message.
			OutOfSequenceCcmCount (number): (read only) The number of Out of Sequence CCM messages received.
			PortTlvDefectCount (number): The total number of Port Tlv defect error that has been detected.
			RdiRxCount (number): (read only) The rdi rx count.
			RdiRxState (str): (read only) The rdi rx state.
			ReceivedAis (bool): (read only) If true, AIS messages have been detected.
			ReceivedIfaceTlvDefect (bool): (read only) If true, interface TLV defect messages have been detected.
			ReceivedPortTlvDefect (bool): (read only) If true, port TLV defect messages have been detected.
			ReceivedRdi (bool): (read only) If true, RDI messages have been detected.
			RemoteMepDefectCount (number): The total number of remote Mep defect error that has been detected.
			RmepCcmDefect (bool): (read only) If true, remote MEP CCM defect messages have been detected.
			SVlan (str): (read only) The single VLAN associated with the CCM message.
			ShortMaName (str): (read only) The Short MA Name associated with the CCM message.
			ShortMaNameFormat (number): (read only) The Short MA Name format associated with the CCM message.
			SomeRmepDefect (bool): (read only) Indicates the aggregate state of the Remote MEP State Machines. If true, at least one of the Remote MEP State Machines is not receiving valid CCMs from its remote MEPs. If false, all Remote MEP State Machines are receiving valid CCMs.

		Returns:
			self: This instance with matching ccmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ccmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ccmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
