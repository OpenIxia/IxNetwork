from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DmLearnedInfo(Base):
	"""The DmLearnedInfo class encapsulates a system managed dmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'dmLearnedInfo'

	def __init__(self, parent):
		super(DmLearnedInfo, self).__init__(parent)

	@property
	def AverageLooseRtt(self):
		"""This signifies the average loose RTT.

		Returns:
			str
		"""
		return self._get_attribute('averageLooseRtt')

	@property
	def AverageLooseRttVariation(self):
		"""This signifies the average loose RTT variation.

		Returns:
			str
		"""
		return self._get_attribute('averageLooseRttVariation')

	@property
	def AverageStrictRtt(self):
		"""This signifies the average strict RTT.

		Returns:
			str
		"""
		return self._get_attribute('averageStrictRtt')

	@property
	def AverageStrictRttVariation(self):
		"""This signifies the average strict RTT variation.

		Returns:
			str
		"""
		return self._get_attribute('averageStrictRttVariation')

	@property
	def DmQueriesSent(self):
		"""This signifies the number of DM queries sent.

		Returns:
			number
		"""
		return self._get_attribute('dmQueriesSent')

	@property
	def DmResponsesReceived(self):
		"""This signifies the total number of DM responses received.

		Returns:
			number
		"""
		return self._get_attribute('dmResponsesReceived')

	@property
	def IncomingLabelOuterInner(self):
		"""This signifies the incoming label information.

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def MaxLooseRtt(self):
		"""This signifies the maximum loose RTT.

		Returns:
			str
		"""
		return self._get_attribute('maxLooseRtt')

	@property
	def MaxStrictRtt(self):
		"""This signifies the maximum strict RTT.

		Returns:
			str
		"""
		return self._get_attribute('maxStrictRtt')

	@property
	def MinLooseRtt(self):
		"""This signifies the minimum loose RTT.

		Returns:
			str
		"""
		return self._get_attribute('minLooseRtt')

	@property
	def MinStrictRtt(self):
		"""This signifies the minimum strict RTT.

		Returns:
			str
		"""
		return self._get_attribute('minStrictRtt')

	@property
	def OutgoingLabelOuterInner(self):
		"""This signifies the Outgoing Label information.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def Type(self):
		"""This signifies the type of the learned information.

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, AverageLooseRtt=None, AverageLooseRttVariation=None, AverageStrictRtt=None, AverageStrictRttVariation=None, DmQueriesSent=None, DmResponsesReceived=None, IncomingLabelOuterInner=None, MaxLooseRtt=None, MaxStrictRtt=None, MinLooseRtt=None, MinStrictRtt=None, OutgoingLabelOuterInner=None, Type=None):
		"""Finds and retrieves dmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve dmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all dmLearnedInfo data from the server.

		Args:
			AverageLooseRtt (str): This signifies the average loose RTT.
			AverageLooseRttVariation (str): This signifies the average loose RTT variation.
			AverageStrictRtt (str): This signifies the average strict RTT.
			AverageStrictRttVariation (str): This signifies the average strict RTT variation.
			DmQueriesSent (number): This signifies the number of DM queries sent.
			DmResponsesReceived (number): This signifies the total number of DM responses received.
			IncomingLabelOuterInner (str): This signifies the incoming label information.
			MaxLooseRtt (str): This signifies the maximum loose RTT.
			MaxStrictRtt (str): This signifies the maximum strict RTT.
			MinLooseRtt (str): This signifies the minimum loose RTT.
			MinStrictRtt (str): This signifies the minimum strict RTT.
			OutgoingLabelOuterInner (str): This signifies the Outgoing Label information.
			Type (str): This signifies the type of the learned information.

		Returns:
			self: This instance with matching dmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
