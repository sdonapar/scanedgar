import os
from ftplib import FTP,error_perm

class EDGAR():
	"""This is EDGAR base class"""
	def __init__(self,ftp_server='ftp.sec.gov',ftp_mode='binary'):
		self.ftp_server = ftp_server
		self.ftp_mode = 'binary'

	def login(self,default_directory=None):
		"""This creates a connection to the ftp server and changes to the default directory"""
		result = None
		try:
			result = self.connection = FTP(self.ftp_server)
			result = self.connection.login()
		except :
			print("Not able to connect to the ftp server:%s"%self.ftp_server)
			print(result)

		if (default_directory):
			self.set_directory(default_directory)
		return result
		
	def set_ftp_mode(self,ftp_mode):
		"""This is to set the ftp mode either to 'ascii' or 'binary', default is 'binary'"""
		if (ftp_mode in ['ascii','binary']):
			self.ftp_mode = ftp_mode
		else:
			print ("ERROR:invalid FTP mode '%s'"%ftp_mode)

	def set_directory(self,directory):
		"""To change the working directory, path can be either absolute or relative"""
		try:
			self.connection.cwd(directory)
		except error_perm as e:
			print("ERROR:%s"%e)


	def _is_file_already_exists(self,file_name):
		""" checks if the file provided existings in the directory
			if directory is not provided, it takes the current working directory
		"""
		qual_file_name = os.path.abspath(file_name)
		abs_file_name = os.path.basename(qual_file_name) 
		directory = os.path.dirname(qual_file_name)
		return abs_file_name in os.listdir(directory)

	def _ftp_file(self,file_name,target_file_name):
		"""
			ftps fhe tile to the target location
		"""
		result = None
		ftp_string = "RETR " + file_name
		callback = open(target_file_name,"wb").write
		try:	
			if (self.ftp_mode == 'binary'):
				result = self.connection.retrbinary(ftp_string, callback)
			elif (self.ftp_mode == 'ascii'):
				result = ftp_connection.retrlines(ftp_string, callback)
		except error_perm as e:
			print("ERROR:%s"%e)
		return result

	def get_file(self,file_name,target_file_name=None,overwrite=True):
		
		if not (target_file_name):
				target_file_name = os.getcwd() + "/" + os.path.basename(file_name)

		file_exists = self._is_file_already_exists(target_file_name)
		result = None
		if (file_exists):
			if (overwrite):
				result = self._ftp_file(file_name,target_file_name)
			else:
				print("File {} already exists, not ftpd".format(target_file_name))
		else:
			result = self._ftp_file(file_name,target_file_name)
		return result

	def get_quarterly_index(self,year,quarter,file_type='master',file_extension='gz',overwrite=False):
		path = "/edgar/full-index/{year}/QTR{quarter}/".format(year=str(year),quarter=str(quarter))
		inp_file_name = None
		if (file_type in ['master','company','form']):
			inp_file_name = file_type + "." + file_extension
			target_file_name = "{file_type}_{year}_{quarter}.{ext}".format(file_type=str(file_type),year=str(year),quarter=str(quarter),ext=file_extension)
			current_directory = self.connection.pwd()
			self.set_directory(path)
			self.get_file(inp_file_name,target_file_name,overwrite=overwrite)
			self.set_directory(current_directory)
		else:
			print("ERROR: Invalid file type {}".format(file_type))

	def close(self):
		self.connection.close()


if __name__ == '__main__':
	myedgar = EDGAR()
	result = myedgar.login()
	#"edgar/full-index/2016/QTR1"
	#print(result)
	#myedgar.set_directory("dddd")
	myedgar.set_ftp_mode('binary')
	#result = myedgar.get_file('master.zip')
	#print(result)
	myedgar.get_quarterly_index(2016, 1,file_extension='gz')
	myedgar.close()	
