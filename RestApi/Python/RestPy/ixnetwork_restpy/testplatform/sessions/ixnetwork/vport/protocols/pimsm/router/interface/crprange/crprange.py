from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CrpRange(Base):
	"""The CrpRange class encapsulates a user managed crpRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CrpRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'crpRange'

	def __init__(self, parent):
		super(CrpRange, self).__init__(parent)

	@property
	def AdvertisementHoldTime(self):
		"""The time interval (in seconds) between two consecutive Candidate RP advertisements.

		Returns:
			number
		"""
		return self._get_attribute('advertisementHoldTime')
	@AdvertisementHoldTime.setter
	def AdvertisementHoldTime(self, value):
		self._set_attribute('advertisementHoldTime', value)

	@property
	def BackOffInterval(self):
		"""The back off time interval for the C-RP-Adv messages.

		Returns:
			number
		"""
		return self._get_attribute('backOffInterval')
	@BackOffInterval.setter
	def BackOffInterval(self, value):
		self._set_attribute('backOffInterval', value)

	@property
	def CrpAddress(self):
		"""Start address of the set of candidate RPs to be simulated.

		Returns:
			str
		"""
		return self._get_attribute('crpAddress')
	@CrpAddress.setter
	def CrpAddress(self, value):
		self._set_attribute('crpAddress', value)

	@property
	def Enabled(self):
		"""Enables/disables a Candidate RP range on the fly. The default is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GroupAddress(self):
		"""Starting group address of the group range for which the candidate RP will advertise candidacy.

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')
	@GroupAddress.setter
	def GroupAddress(self, value):
		self._set_attribute('groupAddress', value)

	@property
	def GroupCount(self):
		"""Number of groups in the range.

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupMaskLen(self):
		"""Mask width (prefix length in bits) for the group range.

		Returns:
			number
		"""
		return self._get_attribute('groupMaskLen')
	@GroupMaskLen.setter
	def GroupMaskLen(self, value):
		self._set_attribute('groupMaskLen', value)

	@property
	def MeshingType(self):
		"""It indicates if the mappings for groups and RP addresses are Fully-Meshed or One-To-One.

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('meshingType')
	@MeshingType.setter
	def MeshingType(self, value):
		self._set_attribute('meshingType', value)

	@property
	def PeriodicAdvertisementInterval(self):
		"""Rate controlling variable indicating how many C-RP-Adv messages can be sent in the specified time interval.

		Returns:
			number
		"""
		return self._get_attribute('periodicAdvertisementInterval')
	@PeriodicAdvertisementInterval.setter
	def PeriodicAdvertisementInterval(self, value):
		self._set_attribute('periodicAdvertisementInterval', value)

	@property
	def PriorityChangeInterval(self):
		"""Time interval after which priority of all the RPs get changed, if priority type is incremental or random.

		Returns:
			number
		"""
		return self._get_attribute('priorityChangeInterval')
	@PriorityChangeInterval.setter
	def PriorityChangeInterval(self, value):
		self._set_attribute('priorityChangeInterval', value)

	@property
	def PriorityType(self):
		"""It indicates the type of priority to be held by the candidate RPs (CRPs). The options are Same, Incremental, and Random.

		Returns:
			str(same|incremental|random)
		"""
		return self._get_attribute('priorityType')
	@PriorityType.setter
	def PriorityType(self, value):
		self._set_attribute('priorityType', value)

	@property
	def PriorityValue(self):
		"""Value of priority field sent in candidate RP advertisement messages.

		Returns:
			number
		"""
		return self._get_attribute('priorityValue')
	@PriorityValue.setter
	def PriorityValue(self, value):
		self._set_attribute('priorityValue', value)

	@property
	def RouterCount(self):
		"""Total number of candidate RPs to be simulated starting from C-RP Address. A contiguous address range is used for this RP range simulation.

		Returns:
			number
		"""
		return self._get_attribute('routerCount')
	@RouterCount.setter
	def RouterCount(self, value):
		self._set_attribute('routerCount', value)

	@property
	def TriggeredCrpMessageCount(self):
		"""The number of times CRP advertisements is sent to the newly elected Bootstrap Router.

		Returns:
			number
		"""
		return self._get_attribute('triggeredCrpMessageCount')
	@TriggeredCrpMessageCount.setter
	def TriggeredCrpMessageCount(self, value):
		self._set_attribute('triggeredCrpMessageCount', value)

	def add(self, AdvertisementHoldTime=None, BackOffInterval=None, CrpAddress=None, Enabled=None, GroupAddress=None, GroupCount=None, GroupMaskLen=None, MeshingType=None, PeriodicAdvertisementInterval=None, PriorityChangeInterval=None, PriorityType=None, PriorityValue=None, RouterCount=None, TriggeredCrpMessageCount=None):
		"""Adds a new crpRange node on the server and retrieves it in this instance.

		Args:
			AdvertisementHoldTime (number): The time interval (in seconds) between two consecutive Candidate RP advertisements.
			BackOffInterval (number): The back off time interval for the C-RP-Adv messages.
			CrpAddress (str): Start address of the set of candidate RPs to be simulated.
			Enabled (bool): Enables/disables a Candidate RP range on the fly. The default is disabled.
			GroupAddress (str): Starting group address of the group range for which the candidate RP will advertise candidacy.
			GroupCount (number): Number of groups in the range.
			GroupMaskLen (number): Mask width (prefix length in bits) for the group range.
			MeshingType (str(fullyMeshed|oneToOne)): It indicates if the mappings for groups and RP addresses are Fully-Meshed or One-To-One.
			PeriodicAdvertisementInterval (number): Rate controlling variable indicating how many C-RP-Adv messages can be sent in the specified time interval.
			PriorityChangeInterval (number): Time interval after which priority of all the RPs get changed, if priority type is incremental or random.
			PriorityType (str(same|incremental|random)): It indicates the type of priority to be held by the candidate RPs (CRPs). The options are Same, Incremental, and Random.
			PriorityValue (number): Value of priority field sent in candidate RP advertisement messages.
			RouterCount (number): Total number of candidate RPs to be simulated starting from C-RP Address. A contiguous address range is used for this RP range simulation.
			TriggeredCrpMessageCount (number): The number of times CRP advertisements is sent to the newly elected Bootstrap Router.

		Returns:
			self: This instance with all currently retrieved crpRange data using find and the newly added crpRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the crpRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertisementHoldTime=None, BackOffInterval=None, CrpAddress=None, Enabled=None, GroupAddress=None, GroupCount=None, GroupMaskLen=None, MeshingType=None, PeriodicAdvertisementInterval=None, PriorityChangeInterval=None, PriorityType=None, PriorityValue=None, RouterCount=None, TriggeredCrpMessageCount=None):
		"""Finds and retrieves crpRange data from the server.

		All named parameters support regex and can be used to selectively retrieve crpRange data from the server.
		By default the find method takes no parameters and will retrieve all crpRange data from the server.

		Args:
			AdvertisementHoldTime (number): The time interval (in seconds) between two consecutive Candidate RP advertisements.
			BackOffInterval (number): The back off time interval for the C-RP-Adv messages.
			CrpAddress (str): Start address of the set of candidate RPs to be simulated.
			Enabled (bool): Enables/disables a Candidate RP range on the fly. The default is disabled.
			GroupAddress (str): Starting group address of the group range for which the candidate RP will advertise candidacy.
			GroupCount (number): Number of groups in the range.
			GroupMaskLen (number): Mask width (prefix length in bits) for the group range.
			MeshingType (str(fullyMeshed|oneToOne)): It indicates if the mappings for groups and RP addresses are Fully-Meshed or One-To-One.
			PeriodicAdvertisementInterval (number): Rate controlling variable indicating how many C-RP-Adv messages can be sent in the specified time interval.
			PriorityChangeInterval (number): Time interval after which priority of all the RPs get changed, if priority type is incremental or random.
			PriorityType (str(same|incremental|random)): It indicates the type of priority to be held by the candidate RPs (CRPs). The options are Same, Incremental, and Random.
			PriorityValue (number): Value of priority field sent in candidate RP advertisement messages.
			RouterCount (number): Total number of candidate RPs to be simulated starting from C-RP Address. A contiguous address range is used for this RP range simulation.
			TriggeredCrpMessageCount (number): The number of times CRP advertisements is sent to the newly elected Bootstrap Router.

		Returns:
			self: This instance with matching crpRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of crpRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the crpRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
