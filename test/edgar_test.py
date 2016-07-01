from edgar import *
import unittest
import os
import inspect


files_to_clean = ['README.txt' ,'master_1993_1.gz','/tmp/readme.txt','company_1993_1.gz']
files_to_clean.extend(['form_1993_1.gz','master_1993_1.Z','company_1993_1.zip'])

def clean_files(files_to_clean):
	for file_name in files_to_clean:
			if file_name in os.listdir(os.getcwd()):
				os.remove(file_name)

class TestEdgar(unittest.TestCase):

	def setUp(self):
		"""
		create EDGAR login
		Remove all of the files that are created during the testing
		"""
		self.myedgar = EDGAR()
		self.myedgar.login()
		clean_files(files_to_clean)

	def tearDown(self):
		"""
		Close EDGAR Connection
		Remove all of the files that are created during the testing
		"""
		self.myedgar.close()
		clean_files(files_to_clean)

	def test_login(self):
		"""
		To test the login method, this creates it's own EDGAR connection
		and closes the same
		"""
		myedgar = EDGAR()
		result = myedgar.login()
		errmsg = "Connection to edgar is not successful"
		self.assertTrue('230-Anonymous access granted' in result,msg=errmsg)
		myedgar.close()

	def test_get_file_to_local_directoy(self):
		"""
		To test get_file method with minimum inputs
		ftp the file to local directory
		"""
		file_name = 'README.txt'
		self.myedgar.get_file(file_name,file_name)
		errmsg = "README.txt file is not ftpd"
		self.assertTrue(os.path.exists(file_name),msg=errmsg)

	def test_get_file_with_target_location(self):
		"""
		To test get_file method with optional target_file_name
		"""
		file_name = 'README.txt'
		self.myedgar.get_file(file_name,"/tmp/readme.txt")
		errmsg = "readme.txt file is not ftpd to /tmp directory"
		self.assertTrue(os.path.exists("/tmp/readme.txt"),msg=errmsg)

	def test_get_file_with_overwrite_true_w_target_file(self):
		"""
		To test get_file with optional overwrite setting to True
		target file name provided
		"""
		file_name = 'README.txt'
		fh = open("readtest.txt","wb")
		fh.write("This is a test readme\n")
		fh.close()
		file_last_mod_time_before_ftp = os.stat("readtest.txt").st_mtime
		self.myedgar.get_file(file_name,"readtest.txt",overwrite=True)
		errmsg = "readtest.txt file has not been overwritten with overwrite as True"
		file_last_mod_time_after_ftp = os.stat("readtest.txt").st_mtime
		self.assertTrue(file_last_mod_time_before_ftp != file_last_mod_time_after_ftp,msg=errmsg)

	def test_get_file_with_overwrite_true_wout_target_file(self):
		"""
		To test get_file with optional overwrite setting to True
		target file name not provided
		"""
		file_name = 'README.txt'
		if (os.path.exists(file_name)):
			os.remove(file_name)
		self.myedgar.get_file(file_name,overwrite=True)
		errmsg = "readtest.txt file has not been ftpd"
		self.assertTrue(os.path.exists(file_name),msg=errmsg)

	def test_get_file_with_overwrite_false(self):
		"""
		To test get_file with optional overwrite setting to False
		target file name provided
		"""
		file_name = 'README.txt'
		fh = open("readtest1.txt","wb")
		fh.write("This is a test readme\n")
		fh.close()
		file_last_mod_time_before_ftp = os.stat("readtest1.txt").st_mtime
		self.myedgar.get_file(file_name,"readtest1.txt",overwrite=False)
		errmsg = "readtest.txt file has been overwritten with overwrite as False"
		file_last_mod_time_after_ftp = os.stat("readtest1.txt").st_mtime
		self.assertTrue(file_last_mod_time_before_ftp == file_last_mod_time_after_ftp,msg=errmsg)

	def test_get_quarterly_index_baseinput(self):
		#self.myedgar.login()
		file_name = "master_1993_1.gz"
		self.myedgar.get_quarterly_index(1993,1)
		errmsg = "master_1993_1.gz file is not ftpd"
		self.assertTrue(file_name in os.listdir(os.getcwd()),msg=errmsg)

	def test_get_quarterly_index_company_input(self):
		#self.myedgar.login()
		file_name = "company_1993_1.gz"
		self.myedgar.get_quarterly_index(1993,1,file_type='company',file_extension='gz')
		errmsg = "company_1993_1.gz file is not ftpd"
		self.assertTrue(file_name in os.listdir(os.getcwd()),msg=errmsg)

	def test_get_quarterly_index_form_input(self):
		#self.myedgar.login()
		file_name = "form_1993_1.gz"
		self.myedgar.get_quarterly_index(1993,1,file_type='form',file_extension='gz')
		errmsg = "form_1993_1.gz file is not ftpd"
		self.assertTrue(file_name in os.listdir(os.getcwd()),msg=errmsg)

	def test_get_quarterly_index_z_extension(self):
		#self.myedgar.login()
		file_name = "master_1993_1.Z"
		self.myedgar.get_quarterly_index(1993,1,file_extension='Z')
		errmsg = "master_1993_1.Z file is not ftpd"
		self.assertTrue(file_name in os.listdir(os.getcwd()),msg=errmsg)

	def test_get_quarterly_index_zip_extension(self):
		#self.myedgar.login()
		file_name = "company_1993_1.zip"
		self.myedgar.get_quarterly_index(1993,1,file_type='company',file_extension='zip')
		errmsg = "company_1993_1.Z file is not ftpd"
		self.assertTrue(file_name in os.listdir(os.getcwd()),msg=errmsg)

	def test_get_quarterly_index_invalid_file_type(self):
		#self.myedgar.login()
		file_name = "comp_1993_1.zip"
		self.myedgar.get_quarterly_index(1993,1,file_type='comp',file_extension='zip')
		errmsg = "Invalid file comp_1993_1.zip is present"
		self.assertFalse(file_name in os.listdir(os.getcwd()),msg=errmsg)

if __name__ == '__main__' :
	unittest.main()