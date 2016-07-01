from processing import *
import unittest
import os
import inspect


master_file_name = os.path.dirname(inspect.getfile(MasterFile)) + "/test/data/master_1994_1.gz"


class TestProcessing(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_find_by_name(self):
		master_file = MasterFile(master_file_name)
		company_name = "3COM CORP"
		errmsg = "Did not find company {}".format(company_name)
		df = master_file.find_by_name(company_name)
		self.assertTrue(len(df) == 5,msg=errmsg)

	def test_find_by_cik(self):
		master_file = MasterFile(master_file_name)
		cik = "738076"
		company_name = "3COM CORP"
		errmsg = "Did not find cik {}".format(cik)
		df = master_file.find_by_cik(cik)
		self.assertTrue(len(df) == 5,msg=errmsg)

	def test_find_by_name_w_form_type(self):
		master_file = MasterFile(master_file_name)
		company_name = "3COM CORP"
		form_type = "10-Q"
		expected_form_date = "1994-01-14"
		errmsg = "Number of records for company {} does not match".format(company_name)
		df = master_file.find_by_name(company_name,form_type=form_type)
		self.assertTrue(len(df) == 1,msg=errmsg)
		errmsg = "form date for company {} does not match with {}".format(company_name,expected_form_date)
		self.assertTrue(df['form_date'].iloc[0] == pd.to_datetime(expected_form_date),msg=errmsg)

	def test_find_by_cik_w_form_type(self):
		master_file = MasterFile(master_file_name)
		cik = "738076"
		company_name = "3COM CORP"
		form_type = "10-Q"
		expected_form_date = "1994-01-14"
		errmsg = "Number of records for cik {} does not match".format(cik)
		df = master_file.find_by_cik(cik,form_type=form_type)
		self.assertTrue(len(df) == 1,msg=errmsg)
		errmsg = "form date for cik {} does not match with {}".format(cik,expected_form_date)
		self.assertTrue(df['form_date'].iloc[0] == pd.to_datetime(expected_form_date),msg=errmsg)

	def test_find_latest_by_name_top(self):
		master_file = MasterFile(master_file_name)
		company_name = "ACORN INVESTMENT TRUST"
		expected_form_date = "1994-02-14"
		doc = master_file.find_latest_by_name(company_name)
		errmsg = "latest date for company {} does not match with {}".format(company_name,expected_form_date)
		self.assertTrue(doc['form_date'] == pd.to_datetime(expected_form_date),msg=errmsg)

	def test_find_latest_by_cik_top(self):
		master_file = MasterFile(master_file_name)
		cik = "2110"
		company_name = "ACORN INVESTMENT TRUST"
		expected_form_date = "1994-02-14"
		doc = master_file.find_latest_by_cik(cik)
		errmsg = "latest date for cik {} does not match with {}".format(cik,expected_form_date)
		self.assertTrue(doc['form_date'] == pd.to_datetime(expected_form_date),msg=errmsg)

	def test_find_latest_by_name_form(self):
		master_file = MasterFile(master_file_name)
		company_name = "ACORN INVESTMENT TRUST"
		form_type = "SC 13G/A"
		expected_file_name = "edgar/data/2110/0000899657-94-000051.txt"

		doc = master_file.find_latest_by_name(company_name,form_type=form_type)
		errmsg = "file name for comppany {} does not match with {}".format(company_name,expected_file_name)
		self.assertTrue(doc['file_name'] == expected_file_name,msg=errmsg)

	def test_find_latest_by_cik_form(self):
		master_file = MasterFile(master_file_name)
		cik = "2110"
		form_type = "SC 13G/A"
		form_date = "1994-02-11"
		expected_file_name = "edgar/data/2110/0000899657-94-000037.txt"

		doc = master_file.find_latest_by_cik(cik,form_type=form_type,filing_date=form_date)
		errmsg = "file name for cik {} does not match with {}".format(cik,expected_file_name)
		self.assertTrue(doc['file_name'] == expected_file_name,msg=errmsg)

	

	def test_find_latest_by_name_form_date(self):
		master_file = MasterFile(master_file_name)
		company_name = "ADVANCED MICRO DEVICES INC"
		form_type = "8-K"
		expected_form_date = "1994-03-23"

		doc = master_file.find_latest_by_name(company_name,form_type=form_type)
		errmsg = "latest date for company {} does not match with {}".format(company_name,expected_form_date)
		self.assertTrue(doc['form_date'] == pd.to_datetime(expected_form_date),msg=errmsg)

	def test_find_latest_by_cik_form_date(self):
		master_file = MasterFile(master_file_name)
		cik = "2488"
		form_type = "8-K"
		expected_form_date = "1994-03-23"

		doc = master_file.find_latest_by_cik(cik,form_type=form_type)
		errmsg = "latest date for cik {} does not match with {}".format(cik,expected_form_date)
		self.assertTrue(doc['form_date'] == pd.to_datetime(expected_form_date),msg=errmsg)


	def test_find_latest_by_name_form_multiple(self):
		master_file = MasterFile(master_file_name)

		company_name = "ACORN INVESTMENT TRUST"
		form_type = "SC 13G/A"
		expected_file_name = "edgar/data/2110/0000899657-94-000051.txt"

		doc = master_file.find_latest_by_name(company_name,form_type=form_type)
		errmsg = "file name for company {} does not match with {}".format(company_name,expected_file_name)
		self.assertTrue(doc['file_name'] == expected_file_name,msg=errmsg)

	def test_find_latest_by_cik_form_multiple(self):
		master_file = MasterFile(master_file_name)

		cik = "2110"
		form_type = "SC 13G/A"
		expected_file_name = "edgar/data/2110/0000899657-94-000051.txt"

		doc = master_file.find_latest_by_cik(cik,form_type=form_type)
		errmsg = "file name for company {} does not match with {}".format(cik,expected_file_name)
		self.assertTrue(doc['file_name'] == expected_file_name,msg=errmsg)

	def test_find_latest_by_name_form_type_date(self):
		master_file = MasterFile(master_file_name)
		company_name = "ACORN INVESTMENT TRUST"
		form_type = "SC 13G/A"
		form_date = "1994-02-11"
		expected_file_name = "edgar/data/2110/0000899657-94-000037.txt"

		doc = master_file.find_latest_by_name(company_name,form_type=form_type,filing_date=form_date)
		errmsg = "file name for company {} does not match with {}".format(company_name,expected_file_name)
		self.assertTrue(doc['file_name'] == expected_file_name,msg=errmsg)	

	def test_find_latest_by_cik_form_type_date(self):
		master_file = MasterFile(master_file_name)
		cik = "2110"
		form_type = "SC 13G/A"
		form_date = "1994-02-11"
		expected_file_name = "edgar/data/2110/0000899657-94-000037.txt"

		doc = master_file.find_latest_by_cik(cik,form_type=form_type,filing_date=form_date)
		errmsg = "file name for cik {} does not match with {}".format(cik,expected_file_name)
		self.assertTrue(doc['file_name'] == expected_file_name,msg=errmsg)
		
if __name__ == '__main__' :
	unittest.main()