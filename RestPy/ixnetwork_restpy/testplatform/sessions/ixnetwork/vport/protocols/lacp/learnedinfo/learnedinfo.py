
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('actorCollectingFlag')

	@property
	def ActorDefaultedFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('actorDefaultedFlag')

	@property
	def ActorDistributingFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('actorDistributingFlag')

	@property
	def ActorExpiredFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('actorExpiredFlag')

	@property
	def ActorLacpActivity(self):
		"""

		Returns:
			str(passive|active)
		"""
		return self._get_attribute('actorLacpActivity')

	@property
	def ActorLacpTimeout(self):
		"""

		Returns:
			str(long|short)
		"""
		return self._get_attribute('actorLacpTimeout')

	@property
	def ActorLinkAggregationStatus(self):
		"""

		Returns:
			str(individual|aggregatable)
		"""
		return self._get_attribute('actorLinkAggregationStatus')

	@property
	def ActorOperationalKey(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorOperationalKey')

	@property
	def ActorPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorPortNumber')

	@property
	def ActorPortPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorPortPriority')

	@property
	def ActorSyncFlag(self):
		"""

		Returns:
			str(inSync|outOfSync)
		"""
		return self._get_attribute('actorSyncFlag')

	@property
	def ActorSystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actorSystemId')

	@property
	def ActorSystemPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorSystemPriority')

	@property
	def AdministrativeKey(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('administrativeKey')

	@property
	def EnabledAggregation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabledAggregation')

	@property
	def OtherLagMemberCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('otherLagMemberCount')

	@property
	def OtherLagMemberDetails(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('otherLagMemberDetails')

	@property
	def PartnerCollectingFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('partnerCollectingFlag')

	@property
	def PartnerCollectorMaxDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('partnerCollectorMaxDelay')

	@property
	def PartnerDefaultedFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('partnerDefaultedFlag')

	@property
	def PartnerDistributingFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('partnerDistributingFlag')

	@property
	def PartnerExpiredFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('partnerExpiredFlag')

	@property
	def PartnerLacpActivity(self):
		"""

		Returns:
			str(passive|active)
		"""
		return self._get_attribute('partnerLacpActivity')

	@property
	def PartnerLacpTimeout(self):
		"""

		Returns:
			str(long|short)
		"""
		return self._get_attribute('partnerLacpTimeout')

	@property
	def PartnerLinkAggregationStatus(self):
		"""

		Returns:
			str(individual|aggregatable)
		"""
		return self._get_attribute('partnerLinkAggregationStatus')

	@property
	def PartnerOperationalKey(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('partnerOperationalKey')

	@property
	def PartnerPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('partnerPortNumber')

	@property
	def PartnerPortPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('partnerPortPriority')

	@property
	def PartnerSyncFlag(self):
		"""

		Returns:
			str(inSync|outOfSync)
		"""
		return self._get_attribute('partnerSyncFlag')

	@property
	def PartnerSystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('partnerSystemId')

	@property
	def PartnerSystemPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('partnerSystemPriority')

	def find(self, ActorCollectingFlag=None, ActorDefaultedFlag=None, ActorDistributingFlag=None, ActorExpiredFlag=None, ActorLacpActivity=None, ActorLacpTimeout=None, ActorLinkAggregationStatus=None, ActorOperationalKey=None, ActorPortNumber=None, ActorPortPriority=None, ActorSyncFlag=None, ActorSystemId=None, ActorSystemPriority=None, AdministrativeKey=None, EnabledAggregation=None, OtherLagMemberCount=None, OtherLagMemberDetails=None, PartnerCollectingFlag=None, PartnerCollectorMaxDelay=None, PartnerDefaultedFlag=None, PartnerDistributingFlag=None, PartnerExpiredFlag=None, PartnerLacpActivity=None, PartnerLacpTimeout=None, PartnerLinkAggregationStatus=None, PartnerOperationalKey=None, PartnerPortNumber=None, PartnerPortPriority=None, PartnerSyncFlag=None, PartnerSystemId=None, PartnerSystemPriority=None):
		"""Finds and retrieves learnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedInfo data from the server.

		Args:
			ActorCollectingFlag (bool): 
			ActorDefaultedFlag (bool): 
			ActorDistributingFlag (bool): 
			ActorExpiredFlag (bool): 
			ActorLacpActivity (str(passive|active)): 
			ActorLacpTimeout (str(long|short)): 
			ActorLinkAggregationStatus (str(individual|aggregatable)): 
			ActorOperationalKey (number): 
			ActorPortNumber (number): 
			ActorPortPriority (number): 
			ActorSyncFlag (str(inSync|outOfSync)): 
			ActorSystemId (str): 
			ActorSystemPriority (number): 
			AdministrativeKey (number): 
			EnabledAggregation (bool): 
			OtherLagMemberCount (number): 
			OtherLagMemberDetails (str): 
			PartnerCollectingFlag (bool): 
			PartnerCollectorMaxDelay (number): 
			PartnerDefaultedFlag (bool): 
			PartnerDistributingFlag (bool): 
			PartnerExpiredFlag (bool): 
			PartnerLacpActivity (str(passive|active)): 
			PartnerLacpTimeout (str(long|short)): 
			PartnerLinkAggregationStatus (str(individual|aggregatable)): 
			PartnerOperationalKey (number): 
			PartnerPortNumber (number): 
			PartnerPortPriority (number): 
			PartnerSyncFlag (str(inSync|outOfSync)): 
			PartnerSystemId (str): 
			PartnerSystemPriority (number): 

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
