from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbmNodeBaseVidRange(Base):
	"""The SpbmNodeBaseVidRange class encapsulates a user managed spbmNodeBaseVidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbmNodeBaseVidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbmNodeBaseVidRange'

	def __init__(self, parent):
		super(SpbmNodeBaseVidRange, self).__init__(parent)

	@property
	def SpbmNodeIsIdRange(self):
		"""An instance of the SpbmNodeIsIdRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodeisidrange.SpbmNodeIsIdRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodeisidrange import SpbmNodeIsIdRange
		return SpbmNodeIsIdRange(self)

	@property
	def BVlanPriority(self):
		"""The user priority of the Base VLAN.

		Returns:
			number
		"""
		return self._get_attribute('bVlanPriority')
	@BVlanPriority.setter
	def BVlanPriority(self, value):
		self._set_attribute('bVlanPriority', value)

	@property
	def BVlanTpId(self):
		"""The tag priority identifier for base VLAN.

		Returns:
			number
		"""
		return self._get_attribute('bVlanTpId')
	@BVlanTpId.setter
	def BVlanTpId(self, value):
		self._set_attribute('bVlanTpId', value)

	@property
	def BaseVid(self):
		"""The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('baseVid')
	@BaseVid.setter
	def BaseVid(self, value):
		self._set_attribute('baseVid', value)

	@property
	def EctAlgorithm(self):
		"""The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.

		Returns:
			number
		"""
		return self._get_attribute('ectAlgorithm')
	@EctAlgorithm.setter
	def EctAlgorithm(self, value):
		self._set_attribute('ectAlgorithm', value)

	@property
	def UseFlag(self):
		"""Set to true to activate the user flag.

		Returns:
			bool
		"""
		return self._get_attribute('useFlag')
	@UseFlag.setter
	def UseFlag(self, value):
		self._set_attribute('useFlag', value)

	def add(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
		"""Adds a new spbmNodeBaseVidRange node on the server and retrieves it in this instance.

		Args:
			BVlanPriority (number): The user priority of the Base VLAN.
			BVlanTpId (number): The tag priority identifier for base VLAN.
			BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
			EctAlgorithm (number): The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.
			UseFlag (bool): Set to true to activate the user flag.

		Returns:
			self: This instance with all currently retrieved spbmNodeBaseVidRange data using find and the newly added spbmNodeBaseVidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbmNodeBaseVidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
		"""Finds and retrieves spbmNodeBaseVidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbmNodeBaseVidRange data from the server.
		By default the find method takes no parameters and will retrieve all spbmNodeBaseVidRange data from the server.

		Args:
			BVlanPriority (number): The user priority of the Base VLAN.
			BVlanTpId (number): The tag priority identifier for base VLAN.
			BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
			EctAlgorithm (number): The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.
			UseFlag (bool): Set to true to activate the user flag.

		Returns:
			self: This instance with matching spbmNodeBaseVidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbmNodeBaseVidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbmNodeBaseVidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
