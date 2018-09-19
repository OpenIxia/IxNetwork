import os


class Files(object):
	def __init__(self, file_path, local_file=True):
		"""Wraps access to /api/v1/sessions/<id>/ixnetwork/files functionality

		Use this class when a generated class has an method parameter with a type of (obj[Files]).

		Args:
			file_path (str): the name of the file and path if the file is local
			local_file (bool default[True]): 
				If True then the file_name will be uploaded to the server to its default file storage location 
				and will overwrite any existing file in that location.

		"""
		self._file_path = file_path
		self._file_name = os.path.basename(file_path)
		self._local_file = local_file
	
	@property
	def is_local_file(self):
		return self._local_file

	@property
	def file_path(self):
		return self._file_path

	@property
	def file_name(self):
		return self._file_name
