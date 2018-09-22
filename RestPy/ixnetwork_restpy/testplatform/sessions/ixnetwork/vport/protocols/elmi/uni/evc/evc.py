from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Evc(Base):
	"""The Evc class encapsulates a user managed evc node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Evc property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'evc'

	def __init__(self, parent):
		super(Evc, self).__init__(parent)

	@property
	def BwProfile(self):
		"""An instance of the BwProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.bwprofile.bwprofile.BwProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.bwprofile.bwprofile import BwProfile
		return BwProfile(self)

	@property
	def CeVlanIdRange(self):
		"""An instance of the CeVlanIdRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.cevlanidrange.cevlanidrange.CeVlanIdRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.cevlanidrange.cevlanidrange import CeVlanIdRange
		return CeVlanIdRange(self)

	@property
	def DefaultEvc(self):
		"""If enabled, default EVC bit is set to 1. It indicates that all CE-VLAN IDs that are not specified in this or other CE-VLAN ID/EVC Map IEs are mapped to this EVC. At most one EVC can be identified as a Default EVC on the UNI. The 'Default EVC' bit has significance only if CE-VLAN ID/EVC Map Type is equal to 'Bundling' (see UNI Status information element octet 3). It must be set to 0 when it is not significant. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('defaultEvc')
	@DefaultEvc.setter
	def DefaultEvc(self, value):
		self._set_attribute('defaultEvc', value)

	@property
	def Enabled(self):
		"""If enabled, the EVC is in effect.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EvcIdentifier(self):
		"""It signifies the content of EVC ID. The length is determined by EVC ID Length. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('evcIdentifier')
	@EvcIdentifier.setter
	def EvcIdentifier(self, value):
		self._set_attribute('evcIdentifier', value)

	@property
	def EvcIdentifierLength(self):
		"""It signifies one octet and indicates the length of EVC ID content. Default is 1. Min is 1 and Max is 100.

		Returns:
			number
		"""
		return self._get_attribute('evcIdentifierLength')
	@EvcIdentifierLength.setter
	def EvcIdentifierLength(self, value):
		self._set_attribute('evcIdentifierLength', value)

	@property
	def EvcStatus(self):
		"""Default is New and Active.

		Returns:
			str(notActive|newAndNotActive|active|newAndActive|partiallyActive|newAndPartiallyActive)
		"""
		return self._get_attribute('evcStatus')
	@EvcStatus.setter
	def EvcStatus(self, value):
		self._set_attribute('evcStatus', value)

	@property
	def EvcType(self):
		"""It is a drop down of Point-to-Point which is 0 and Multipoint-to-Multipoint which is 1. Default is Point-to-Point.

		Returns:
			str(pointToPoint|multipointToMultipoint)
		"""
		return self._get_attribute('evcType')
	@EvcType.setter
	def EvcType(self, value):
		self._set_attribute('evcType', value)

	@property
	def ReferenceId(self):
		"""Default value is 1. Max two octet maximum value, Min 1.

		Returns:
			number
		"""
		return self._get_attribute('referenceId')
	@ReferenceId.setter
	def ReferenceId(self, value):
		self._set_attribute('referenceId', value)

	@property
	def UntaggedPriorityTagged(self):
		"""If enabled, Untagged/Priority Tagged bit is set to 1. It indicates that this EVC Map Entry identifies the CE VLAN ID for Untagged/Priority Service Frames. The 'Untagged/Priority Tagged' bit has significance only if CE-VLAN ID/EVC Map Type is not equal to 'All to one Bundling' (see UNI Status information element octet 3). It must be set to 0 when it is not significant. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('untaggedPriorityTagged')
	@UntaggedPriorityTagged.setter
	def UntaggedPriorityTagged(self, value):
		self._set_attribute('untaggedPriorityTagged', value)

	def add(self, DefaultEvc=None, Enabled=None, EvcIdentifier=None, EvcIdentifierLength=None, EvcStatus=None, EvcType=None, ReferenceId=None, UntaggedPriorityTagged=None):
		"""Adds a new evc node on the server and retrieves it in this instance.

		Args:
			DefaultEvc (bool): If enabled, default EVC bit is set to 1. It indicates that all CE-VLAN IDs that are not specified in this or other CE-VLAN ID/EVC Map IEs are mapped to this EVC. At most one EVC can be identified as a Default EVC on the UNI. The 'Default EVC' bit has significance only if CE-VLAN ID/EVC Map Type is equal to 'Bundling' (see UNI Status information element octet 3). It must be set to 0 when it is not significant. Default is 0.
			Enabled (bool): If enabled, the EVC is in effect.
			EvcIdentifier (str): It signifies the content of EVC ID. The length is determined by EVC ID Length. Default is 0.
			EvcIdentifierLength (number): It signifies one octet and indicates the length of EVC ID content. Default is 1. Min is 1 and Max is 100.
			EvcStatus (str(notActive|newAndNotActive|active|newAndActive|partiallyActive|newAndPartiallyActive)): Default is New and Active.
			EvcType (str(pointToPoint|multipointToMultipoint)): It is a drop down of Point-to-Point which is 0 and Multipoint-to-Multipoint which is 1. Default is Point-to-Point.
			ReferenceId (number): Default value is 1. Max two octet maximum value, Min 1.
			UntaggedPriorityTagged (bool): If enabled, Untagged/Priority Tagged bit is set to 1. It indicates that this EVC Map Entry identifies the CE VLAN ID for Untagged/Priority Service Frames. The 'Untagged/Priority Tagged' bit has significance only if CE-VLAN ID/EVC Map Type is not equal to 'All to one Bundling' (see UNI Status information element octet 3). It must be set to 0 when it is not significant. Default is 0.

		Returns:
			self: This instance with all currently retrieved evc data using find and the newly added evc data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the evc data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DefaultEvc=None, Enabled=None, EvcIdentifier=None, EvcIdentifierLength=None, EvcStatus=None, EvcType=None, ReferenceId=None, UntaggedPriorityTagged=None):
		"""Finds and retrieves evc data from the server.

		All named parameters support regex and can be used to selectively retrieve evc data from the server.
		By default the find method takes no parameters and will retrieve all evc data from the server.

		Args:
			DefaultEvc (bool): If enabled, default EVC bit is set to 1. It indicates that all CE-VLAN IDs that are not specified in this or other CE-VLAN ID/EVC Map IEs are mapped to this EVC. At most one EVC can be identified as a Default EVC on the UNI. The 'Default EVC' bit has significance only if CE-VLAN ID/EVC Map Type is equal to 'Bundling' (see UNI Status information element octet 3). It must be set to 0 when it is not significant. Default is 0.
			Enabled (bool): If enabled, the EVC is in effect.
			EvcIdentifier (str): It signifies the content of EVC ID. The length is determined by EVC ID Length. Default is 0.
			EvcIdentifierLength (number): It signifies one octet and indicates the length of EVC ID content. Default is 1. Min is 1 and Max is 100.
			EvcStatus (str(notActive|newAndNotActive|active|newAndActive|partiallyActive|newAndPartiallyActive)): Default is New and Active.
			EvcType (str(pointToPoint|multipointToMultipoint)): It is a drop down of Point-to-Point which is 0 and Multipoint-to-Multipoint which is 1. Default is Point-to-Point.
			ReferenceId (number): Default value is 1. Max two octet maximum value, Min 1.
			UntaggedPriorityTagged (bool): If enabled, Untagged/Priority Tagged bit is set to 1. It indicates that this EVC Map Entry identifies the CE VLAN ID for Untagged/Priority Service Frames. The 'Untagged/Priority Tagged' bit has significance only if CE-VLAN ID/EVC Map Type is not equal to 'All to one Bundling' (see UNI Status information element octet 3). It must be set to 0 when it is not significant. Default is 0.

		Returns:
			self: This instance with matching evc data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evc data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evc data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
