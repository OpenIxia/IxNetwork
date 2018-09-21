from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Group(Base):
	"""The Group class encapsulates a user managed group node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Group property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'group'

	def __init__(self, parent):
		super(Group, self).__init__(parent)

	@property
	def Source(self):
		"""An instance of the Source class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.host.group.source.source.Source)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.host.group.source.source import Source
		return Source(self)

	@property
	def EnablePacking(self):
		"""If enabled, this option controls how many multicast records and sources will be included in each listener report for this group range.

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def Enabled(self):
		"""Enables the use of the group range in the IGMP simulation.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GroupCount(self):
		"""Specifies the set of IPv4 multicast addresses in the group range.

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupFrom(self):
		"""The IP address of the first member of the group (multicast address).

		Returns:
			str
		"""
		return self._get_attribute('groupFrom')
	@GroupFrom.setter
	def GroupFrom(self, value):
		self._set_attribute('groupFrom', value)

	@property
	def IncrementStep(self):
		"""The value used to increment the IP address for each additional member of the group.

		Returns:
			number
		"""
		return self._get_attribute('incrementStep')
	@IncrementStep.setter
	def IncrementStep(self, value):
		self._set_attribute('incrementStep', value)

	@property
	def RecordsPerFrame(self):
		"""If the user wants a specified number of records to be sent in each frame, packing should be enabled (enablePacking is true), and the number of records indicated with the recordsPerFrame option.

		Returns:
			number
		"""
		return self._get_attribute('recordsPerFrame')
	@RecordsPerFrame.setter
	def RecordsPerFrame(self, value):
		self._set_attribute('recordsPerFrame', value)

	@property
	def SourceMode(self):
		"""Indicates whether the associated source range is a set of IP addresses to be included or excluded.

		Returns:
			str(include|exclude)
		"""
		return self._get_attribute('sourceMode')
	@SourceMode.setter
	def SourceMode(self, value):
		self._set_attribute('sourceMode', value)

	@property
	def SourcesPerRecord(self):
		"""The number of multicast sources that will be included in each listener report for this group range.

		Returns:
			number
		"""
		return self._get_attribute('sourcesPerRecord')
	@SourcesPerRecord.setter
	def SourcesPerRecord(self, value):
		self._set_attribute('sourcesPerRecord', value)

	@property
	def UpdateRequired(self):
		"""Notifies the user that the changes made to the IGMP configuration of the source IP addresses for this group range need to be reflected.

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')
	@UpdateRequired.setter
	def UpdateRequired(self, value):
		self._set_attribute('updateRequired', value)

	def add(self, EnablePacking=None, Enabled=None, GroupCount=None, GroupFrom=None, IncrementStep=None, RecordsPerFrame=None, SourceMode=None, SourcesPerRecord=None, UpdateRequired=None):
		"""Adds a new group node on the server and retrieves it in this instance.

		Args:
			EnablePacking (bool): If enabled, this option controls how many multicast records and sources will be included in each listener report for this group range.
			Enabled (bool): Enables the use of the group range in the IGMP simulation.
			GroupCount (number): Specifies the set of IPv4 multicast addresses in the group range.
			GroupFrom (str): The IP address of the first member of the group (multicast address).
			IncrementStep (number): The value used to increment the IP address for each additional member of the group.
			RecordsPerFrame (number): If the user wants a specified number of records to be sent in each frame, packing should be enabled (enablePacking is true), and the number of records indicated with the recordsPerFrame option.
			SourceMode (str(include|exclude)): Indicates whether the associated source range is a set of IP addresses to be included or excluded.
			SourcesPerRecord (number): The number of multicast sources that will be included in each listener report for this group range.
			UpdateRequired (bool): Notifies the user that the changes made to the IGMP configuration of the source IP addresses for this group range need to be reflected.

		Returns:
			self: This instance with all currently retrieved group data using find and the newly added group data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the group data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnablePacking=None, Enabled=None, GroupCount=None, GroupFrom=None, IncrementStep=None, RecordsPerFrame=None, SourceMode=None, SourcesPerRecord=None, UpdateRequired=None):
		"""Finds and retrieves group data from the server.

		All named parameters support regex and can be used to selectively retrieve group data from the server.
		By default the find method takes no parameters and will retrieve all group data from the server.

		Args:
			EnablePacking (bool): If enabled, this option controls how many multicast records and sources will be included in each listener report for this group range.
			Enabled (bool): Enables the use of the group range in the IGMP simulation.
			GroupCount (number): Specifies the set of IPv4 multicast addresses in the group range.
			GroupFrom (str): The IP address of the first member of the group (multicast address).
			IncrementStep (number): The value used to increment the IP address for each additional member of the group.
			RecordsPerFrame (number): If the user wants a specified number of records to be sent in each frame, packing should be enabled (enablePacking is true), and the number of records indicated with the recordsPerFrame option.
			SourceMode (str(include|exclude)): Indicates whether the associated source range is a set of IP addresses to be included or excluded.
			SourcesPerRecord (number): The number of multicast sources that will be included in each listener report for this group range.
			UpdateRequired (bool): Notifies the user that the changes made to the IGMP configuration of the source IP addresses for this group range need to be reflected.

		Returns:
			self: This instance with matching group data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of group data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the group data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateSources(self):
		"""Executes the updateSources operation on the server.

		This command is used to update the host group source information for IGMP.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=group)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateSources', payload=locals(), response_object=None)
