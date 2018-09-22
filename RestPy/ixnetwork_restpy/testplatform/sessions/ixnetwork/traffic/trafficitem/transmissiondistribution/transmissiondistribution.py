from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TransmissionDistribution(Base):
	"""The TransmissionDistribution class encapsulates a system managed transmissionDistribution node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TransmissionDistribution property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'transmissionDistribution'

	def __init__(self, parent):
		super(TransmissionDistribution, self).__init__(parent)

	@property
	def AvailableDistributions(self):
		"""Indicates the available transmission distributions for the traffic streams.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableDistributions')

	@property
	def Distributions(self):
		"""Indicates the predefined size distribution based on size and weight.

		Returns:
			list(str)
		"""
		return self._get_attribute('distributions')
	@Distributions.setter
	def Distributions(self, value):
		self._set_attribute('distributions', value)

	@property
	def DistributionsDisplayNames(self):
		"""Returns user friendly list of distribution fields

		Returns:
			list(str)
		"""
		return self._get_attribute('distributionsDisplayNames')

	def find(self, AvailableDistributions=None, Distributions=None, DistributionsDisplayNames=None):
		"""Finds and retrieves transmissionDistribution data from the server.

		All named parameters support regex and can be used to selectively retrieve transmissionDistribution data from the server.
		By default the find method takes no parameters and will retrieve all transmissionDistribution data from the server.

		Args:
			AvailableDistributions (list(str)): Indicates the available transmission distributions for the traffic streams.
			Distributions (list(str)): Indicates the predefined size distribution based on size and weight.
			DistributionsDisplayNames (list(str)): Returns user friendly list of distribution fields

		Returns:
			self: This instance with matching transmissionDistribution data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of transmissionDistribution data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the transmissionDistribution data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
