from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologySpbNodeBaseVidRange(Base):
	"""The CustomTopologySpbNodeBaseVidRange class encapsulates a user managed customTopologySpbNodeBaseVidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologySpbNodeBaseVidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologySpbNodeBaseVidRange'

	def __init__(self, parent):
		super(CustomTopologySpbNodeBaseVidRange, self).__init__(parent)

	@property
	def CustomTopologySpbNodeIsidRange(self):
		"""An instance of the CustomTopologySpbNodeIsidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopologyspbnodeisidrange.CustomTopologySpbNodeIsidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopologyspbnodeisidrange import CustomTopologySpbNodeIsidRange
		return CustomTopologySpbNodeIsidRange(self)

	@property
	def BVlanPriority(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('bVlanPriority')
	@BVlanPriority.setter
	def BVlanPriority(self, value):
		self._set_attribute('bVlanPriority', value)

	@property
	def BVlanTpId(self):
		"""NOT DEFINED

		Returns:
			str(33024|37120|37376|34987)
		"""
		return self._get_attribute('bVlanTpId')
	@BVlanTpId.setter
	def BVlanTpId(self, value):
		self._set_attribute('bVlanTpId', value)

	@property
	def BaseVid(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('baseVid')
	@BaseVid.setter
	def BaseVid(self, value):
		self._set_attribute('baseVid', value)

	@property
	def EctAlgorithm(self):
		"""NOT DEFINED

		Returns:
			str(00-80-C2-01|00-80-C2-02|00-80-C2-03|00-80-C2-04|00-80-C2-05|00-80-C2-06|00-80-C2-07|00-80-C2-08|00-80-C2-09|00-80-C2-0A|00-80-C2-0B|00-80-C2-0C|00-80-C2-0D|00-80-C2-0E|00-80-C2-0F|00-80-C2-10)
		"""
		return self._get_attribute('ectAlgorithm')
	@EctAlgorithm.setter
	def EctAlgorithm(self, value):
		self._set_attribute('ectAlgorithm', value)

	@property
	def UseFlag(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('useFlag')
	@UseFlag.setter
	def UseFlag(self, value):
		self._set_attribute('useFlag', value)

	def add(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
		"""Adds a new customTopologySpbNodeBaseVidRange node on the server and retrieves it in this instance.

		Args:
			BVlanPriority (number): NOT DEFINED
			BVlanTpId (str(33024|37120|37376|34987)): NOT DEFINED
			BaseVid (number): NOT DEFINED
			EctAlgorithm (str(00-80-C2-01|00-80-C2-02|00-80-C2-03|00-80-C2-04|00-80-C2-05|00-80-C2-06|00-80-C2-07|00-80-C2-08|00-80-C2-09|00-80-C2-0A|00-80-C2-0B|00-80-C2-0C|00-80-C2-0D|00-80-C2-0E|00-80-C2-0F|00-80-C2-10)): NOT DEFINED
			UseFlag (bool): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologySpbNodeBaseVidRange data using find and the newly added customTopologySpbNodeBaseVidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologySpbNodeBaseVidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
		"""Finds and retrieves customTopologySpbNodeBaseVidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologySpbNodeBaseVidRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologySpbNodeBaseVidRange data from the server.

		Args:
			BVlanPriority (number): NOT DEFINED
			BVlanTpId (str(33024|37120|37376|34987)): NOT DEFINED
			BaseVid (number): NOT DEFINED
			EctAlgorithm (str(00-80-C2-01|00-80-C2-02|00-80-C2-03|00-80-C2-04|00-80-C2-05|00-80-C2-06|00-80-C2-07|00-80-C2-08|00-80-C2-09|00-80-C2-0A|00-80-C2-0B|00-80-C2-0C|00-80-C2-0D|00-80-C2-0E|00-80-C2-0F|00-80-C2-10)): NOT DEFINED
			UseFlag (bool): NOT DEFINED

		Returns:
			self: This instance with matching customTopologySpbNodeBaseVidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologySpbNodeBaseVidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologySpbNodeBaseVidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
