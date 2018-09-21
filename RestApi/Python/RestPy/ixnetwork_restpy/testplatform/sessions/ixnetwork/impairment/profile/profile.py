from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Profile(Base):
	"""The Profile class encapsulates a user managed profile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Profile property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'profile'

	def __init__(self, parent):
		super(Profile, self).__init__(parent)

	@property
	def AccumulateAndBurst(self):
		"""An instance of the AccumulateAndBurst class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.accumulateandburst.accumulateandburst.AccumulateAndBurst)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.accumulateandburst.accumulateandburst import AccumulateAndBurst
		return AccumulateAndBurst(self)._select()

	@property
	def BitError(self):
		"""An instance of the BitError class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.biterror.biterror.BitError)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.biterror.biterror import BitError
		return BitError(self)._select()

	@property
	def Checksums(self):
		"""An instance of the Checksums class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.checksums.checksums.Checksums)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.checksums.checksums import Checksums
		return Checksums(self)._select()

	@property
	def CustomDelayVariation(self):
		"""An instance of the CustomDelayVariation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.customdelayvariation.customdelayvariation.CustomDelayVariation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.customdelayvariation.customdelayvariation import CustomDelayVariation
		return CustomDelayVariation(self)._select()

	@property
	def Delay(self):
		"""An instance of the Delay class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.delay.delay.Delay)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.delay.delay import Delay
		return Delay(self)._select()

	@property
	def DelayVariation(self):
		"""An instance of the DelayVariation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.delayvariation.delayvariation.DelayVariation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.delayvariation.delayvariation import DelayVariation
		return DelayVariation(self)._select()

	@property
	def Drop(self):
		"""An instance of the Drop class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.drop.drop.Drop)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.drop.drop import Drop
		return Drop(self)._select()

	@property
	def Duplicate(self):
		"""An instance of the Duplicate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.duplicate.duplicate.Duplicate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.duplicate.duplicate import Duplicate
		return Duplicate(self)._select()

	@property
	def FixedClassifier(self):
		"""An instance of the FixedClassifier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.fixedclassifier.fixedclassifier.FixedClassifier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.fixedclassifier.fixedclassifier import FixedClassifier
		return FixedClassifier(self)

	@property
	def Modifier(self):
		"""An instance of the Modifier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.modifier.modifier.Modifier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.modifier.modifier import Modifier
		return Modifier(self)

	@property
	def Reorder(self):
		"""An instance of the Reorder class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.reorder.reorder.Reorder)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.reorder.reorder import Reorder
		return Reorder(self)._select()

	@property
	def RxRateLimit(self):
		"""An instance of the RxRateLimit class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.rxratelimit.rxratelimit.RxRateLimit)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.rxratelimit.rxratelimit import RxRateLimit
		return RxRateLimit(self)._select()

	@property
	def __links__(self):
		"""List of references to impairment links.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/impairment?deepchild=link])
		"""
		return self._get_attribute('__links__')
	@__links__.setter
	def __links__(self, value):
		self._set_attribute('__links__', value)

	@property
	def AllLinks(self):
		"""If true, apply the profile to all impairment links. If not, only apply the profile to packets on selected links.

		Returns:
			bool
		"""
		return self._get_attribute('allLinks')
	@AllLinks.setter
	def AllLinks(self, value):
		self._set_attribute('allLinks', value)

	@property
	def Enabled(self):
		"""If true, enables the profile.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Name(self):
		"""The name of the profile.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def Priority(self):
		"""Profile priority. 1 is highest.

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def ProfileId(self):
		"""A unique identifier for the profile. Read-only.

		Returns:
			number
		"""
		return self._get_attribute('profileId')

	def add(self, __links__=None, AllLinks=None, Enabled=None, Name=None, Priority=None):
		"""Adds a new profile node on the server and retrieves it in this instance.

		Args:
			__links__ (list(str[None|/api/v1/sessions/1/ixnetwork/impairment?deepchild=link])): List of references to impairment links.
			AllLinks (bool): If true, apply the profile to all impairment links. If not, only apply the profile to packets on selected links.
			Enabled (bool): If true, enables the profile.
			Name (str): The name of the profile.
			Priority (number): Profile priority. 1 is highest.

		Returns:
			self: This instance with all currently retrieved profile data using find and the newly added profile data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the profile data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, __links__=None, AllLinks=None, Enabled=None, Name=None, Priority=None, ProfileId=None):
		"""Finds and retrieves profile data from the server.

		All named parameters support regex and can be used to selectively retrieve profile data from the server.
		By default the find method takes no parameters and will retrieve all profile data from the server.

		Args:
			__links__ (list(str[None|/api/v1/sessions/1/ixnetwork/impairment?deepchild=link])): List of references to impairment links.
			AllLinks (bool): If true, apply the profile to all impairment links. If not, only apply the profile to packets on selected links.
			Enabled (bool): If true, enables the profile.
			Name (str): The name of the profile.
			Priority (number): Profile priority. 1 is highest.
			ProfileId (number): A unique identifier for the profile. Read-only.

		Returns:
			self: This instance with matching profile data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of profile data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the profile data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
