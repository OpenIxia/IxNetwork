from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInfo(Base):
	"""The LearnedInfo class encapsulates a system managed learnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedInfo'

	def __init__(self, parent):
		super(LearnedInfo, self).__init__(parent)

	@property
	def ActorCollectingFlag(self):
		"""(read only) The learned Actor Collecting Flag status, either True of False. If True, the Collecting Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('actorCollectingFlag')

	@property
	def ActorDefaultedFlag(self):
		"""(read only) The learned Actor Defaulted Flag status, either True of False. If True, the Defaulted Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('actorDefaultedFlag')

	@property
	def ActorDistributingFlag(self):
		"""(read only) The learned Actor Distributing Flag status, either True of False. If True, the Distributing Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('actorDistributingFlag')

	@property
	def ActorExpiredFlag(self):
		"""(read only) The learned Actor Expired Flag status, either True of False. If True, the Expired Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('actorExpiredFlag')

	@property
	def ActorLacpActivity(self):
		"""(read only) The learned Actor LACP activity mode, either Passive or Active

		Returns:
			str(passive|active)
		"""
		return self._get_attribute('actorLacpActivity')

	@property
	def ActorLacpTimeout(self):
		"""(read only) The learned Actor LACPDU timeout mode, either Long or Short.

		Returns:
			str(long|short)
		"""
		return self._get_attribute('actorLacpTimeout')

	@property
	def ActorLinkAggregationStatus(self):
		"""(read only) The learned link aggregation status of the actor, either Aggregated or Not Aggregated.

		Returns:
			str(individual|aggregatable)
		"""
		return self._get_attribute('actorLinkAggregationStatus')

	@property
	def ActorOperationalKey(self):
		"""(read only) The learned Actor operation key, in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('actorOperationalKey')

	@property
	def ActorPortNumber(self):
		"""(read only) The learned Actor port number in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('actorPortNumber')

	@property
	def ActorPortPriority(self):
		"""(read only) The learned Actor port priority, in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('actorPortPriority')

	@property
	def ActorSyncFlag(self):
		"""(read only) The learned Actor synchronized status, either OUT_OF_SYNC/IN_SYNC.

		Returns:
			str(inSync|outOfSync)
		"""
		return self._get_attribute('actorSyncFlag')

	@property
	def ActorSystemId(self):
		"""(read only) The learned Actor system identifier, in 6 byte format.

		Returns:
			str
		"""
		return self._get_attribute('actorSystemId')

	@property
	def ActorSystemPriority(self):
		"""(read only) The learned Actor system priority, in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('actorSystemPriority')

	@property
	def AdministrativeKey(self):
		"""(read only) This field controls the aggregation of ports of the same system with similar Actor Key.

		Returns:
			number
		"""
		return self._get_attribute('administrativeKey')

	@property
	def EnabledAggregation(self):
		"""(read only) The learned Actor aggregation status (whether the port is Individual or Aggregated).

		Returns:
			bool
		"""
		return self._get_attribute('enabledAggregation')

	@property
	def OtherLagMemberCount(self):
		"""(read only) The total number of ports,excluding the individual port that are a part of the LAG

		Returns:
			number
		"""
		return self._get_attribute('otherLagMemberCount')

	@property
	def OtherLagMemberDetails(self):
		"""(read only) The detailed information of the other member ports of the same LAG, visible in card:port format.

		Returns:
			str
		"""
		return self._get_attribute('otherLagMemberDetails')

	@property
	def PartnerCollectingFlag(self):
		"""(read only) The learned Partner Collecting Flag status, either True of False. If True, the Collecting Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('partnerCollectingFlag')

	@property
	def PartnerCollectorMaxDelay(self):
		"""(read only) The learned maximum Collection Delay for the partner, in microseconds.

		Returns:
			number
		"""
		return self._get_attribute('partnerCollectorMaxDelay')

	@property
	def PartnerDefaultedFlag(self):
		"""(read only) The learned Partner Defaulted Flag status, either True of False. If True, the Defaulted Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('partnerDefaultedFlag')

	@property
	def PartnerDistributingFlag(self):
		"""(read only) The learned Partner Distributing Flag status, either True of False. If True, the Distributing Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('partnerDistributingFlag')

	@property
	def PartnerExpiredFlag(self):
		"""(read only) The learned Partner Expired Flag status, either True of False. If True, the Expired Flag is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('partnerExpiredFlag')

	@property
	def PartnerLacpActivity(self):
		"""(read only) The learned Partner LACP activity mode, either Passive or Active

		Returns:
			str(passive|active)
		"""
		return self._get_attribute('partnerLacpActivity')

	@property
	def PartnerLacpTimeout(self):
		"""(read only) The learned Partner LACPDU timeout mode, either Long or Short.

		Returns:
			str(long|short)
		"""
		return self._get_attribute('partnerLacpTimeout')

	@property
	def PartnerLinkAggregationStatus(self):
		"""(read only) The learned link aggregation status of the partner, either Aggregated or Not Aggregated.

		Returns:
			str(individual|aggregatable)
		"""
		return self._get_attribute('partnerLinkAggregationStatus')

	@property
	def PartnerOperationalKey(self):
		"""(read only) The learned Partner operation key, in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('partnerOperationalKey')

	@property
	def PartnerPortNumber(self):
		"""(read only) The learned Partner port number in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('partnerPortNumber')

	@property
	def PartnerPortPriority(self):
		"""(read only) The learned Partner port priority, in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('partnerPortPriority')

	@property
	def PartnerSyncFlag(self):
		"""(read only) The learned Partner synchronized status, either OUT_OF_SYNC/IN_SYNC.

		Returns:
			str(inSync|outOfSync)
		"""
		return self._get_attribute('partnerSyncFlag')

	@property
	def PartnerSystemId(self):
		"""(read only) The learned Partner system identifier, in 6 byte format.

		Returns:
			str
		"""
		return self._get_attribute('partnerSystemId')

	@property
	def PartnerSystemPriority(self):
		"""(read only) The learned Partner system priority, in hexadecimal format.

		Returns:
			number
		"""
		return self._get_attribute('partnerSystemPriority')

	def find(self, ActorCollectingFlag=None, ActorDefaultedFlag=None, ActorDistributingFlag=None, ActorExpiredFlag=None, ActorLacpActivity=None, ActorLacpTimeout=None, ActorLinkAggregationStatus=None, ActorOperationalKey=None, ActorPortNumber=None, ActorPortPriority=None, ActorSyncFlag=None, ActorSystemId=None, ActorSystemPriority=None, AdministrativeKey=None, EnabledAggregation=None, OtherLagMemberCount=None, OtherLagMemberDetails=None, PartnerCollectingFlag=None, PartnerCollectorMaxDelay=None, PartnerDefaultedFlag=None, PartnerDistributingFlag=None, PartnerExpiredFlag=None, PartnerLacpActivity=None, PartnerLacpTimeout=None, PartnerLinkAggregationStatus=None, PartnerOperationalKey=None, PartnerPortNumber=None, PartnerPortPriority=None, PartnerSyncFlag=None, PartnerSystemId=None, PartnerSystemPriority=None):
		"""Finds and retrieves learnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedInfo data from the server.

		Args:
			ActorCollectingFlag (bool): (read only) The learned Actor Collecting Flag status, either True of False. If True, the Collecting Flag is enabled.
			ActorDefaultedFlag (bool): (read only) The learned Actor Defaulted Flag status, either True of False. If True, the Defaulted Flag is enabled.
			ActorDistributingFlag (bool): (read only) The learned Actor Distributing Flag status, either True of False. If True, the Distributing Flag is enabled.
			ActorExpiredFlag (bool): (read only) The learned Actor Expired Flag status, either True of False. If True, the Expired Flag is enabled.
			ActorLacpActivity (str(passive|active)): (read only) The learned Actor LACP activity mode, either Passive or Active
			ActorLacpTimeout (str(long|short)): (read only) The learned Actor LACPDU timeout mode, either Long or Short.
			ActorLinkAggregationStatus (str(individual|aggregatable)): (read only) The learned link aggregation status of the actor, either Aggregated or Not Aggregated.
			ActorOperationalKey (number): (read only) The learned Actor operation key, in hexadecimal format.
			ActorPortNumber (number): (read only) The learned Actor port number in hexadecimal format.
			ActorPortPriority (number): (read only) The learned Actor port priority, in hexadecimal format.
			ActorSyncFlag (str(inSync|outOfSync)): (read only) The learned Actor synchronized status, either OUT_OF_SYNC/IN_SYNC.
			ActorSystemId (str): (read only) The learned Actor system identifier, in 6 byte format.
			ActorSystemPriority (number): (read only) The learned Actor system priority, in hexadecimal format.
			AdministrativeKey (number): (read only) This field controls the aggregation of ports of the same system with similar Actor Key.
			EnabledAggregation (bool): (read only) The learned Actor aggregation status (whether the port is Individual or Aggregated).
			OtherLagMemberCount (number): (read only) The total number of ports,excluding the individual port that are a part of the LAG
			OtherLagMemberDetails (str): (read only) The detailed information of the other member ports of the same LAG, visible in card:port format.
			PartnerCollectingFlag (bool): (read only) The learned Partner Collecting Flag status, either True of False. If True, the Collecting Flag is enabled.
			PartnerCollectorMaxDelay (number): (read only) The learned maximum Collection Delay for the partner, in microseconds.
			PartnerDefaultedFlag (bool): (read only) The learned Partner Defaulted Flag status, either True of False. If True, the Defaulted Flag is enabled.
			PartnerDistributingFlag (bool): (read only) The learned Partner Distributing Flag status, either True of False. If True, the Distributing Flag is enabled.
			PartnerExpiredFlag (bool): (read only) The learned Partner Expired Flag status, either True of False. If True, the Expired Flag is enabled.
			PartnerLacpActivity (str(passive|active)): (read only) The learned Partner LACP activity mode, either Passive or Active
			PartnerLacpTimeout (str(long|short)): (read only) The learned Partner LACPDU timeout mode, either Long or Short.
			PartnerLinkAggregationStatus (str(individual|aggregatable)): (read only) The learned link aggregation status of the partner, either Aggregated or Not Aggregated.
			PartnerOperationalKey (number): (read only) The learned Partner operation key, in hexadecimal format.
			PartnerPortNumber (number): (read only) The learned Partner port number in hexadecimal format.
			PartnerPortPriority (number): (read only) The learned Partner port priority, in hexadecimal format.
			PartnerSyncFlag (str(inSync|outOfSync)): (read only) The learned Partner synchronized status, either OUT_OF_SYNC/IN_SYNC.
			PartnerSystemId (str): (read only) The learned Partner system identifier, in 6 byte format.
			PartnerSystemPriority (number): (read only) The learned Partner system priority, in hexadecimal format.

		Returns:
			self: This instance with matching learnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
