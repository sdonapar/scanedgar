import gzip
import numpy as np
import pandas as pd
from datetime import date, datetime


class MasterFile():
	"""This class is to process the master file """
	def __init__(self,file_name,file_extension='gz',format='delimited',delimiter="|"):
		self.file_name = file_name
		self.file_extension = file_extension # allowed values '.zip', '.gz','.idx'
		self.format = format # allowed values 'delimited' or 'fixed-width'
		self.delimiter = delimiter
		self.field_position = [0,62,74,86,98]
		self.read_data() 

	def _get_file_handle(self):
		"""
		This function returns a file handle based on the mode
		mode can be 'gz' or 'idx'
		"""
		file_handle = None
		if (self.file_extension=="gz"):
			file_handle = gzip.open(self.file_name,"rb")
		elif (mode=='idx'):
			file_handle = open(self.file_name,"rb")
		else:
			print "Error:Invalid mode %s"%s(self.file_name)
		return file_handle

	def read_data(self):
		"""
		This functions reads a file and retunrs the header and rows in a tuple
		First 10 rows are not part of the file, 8th row is the header
		"""
		file_handle = self._get_file_handle()
		skip_rows = [0,1,2,3,4,5,6,7,9]
		delimiter = "|"
		col_index = ['cik','company_name','form_type','form_date','file_name']
		col_types = {'cik':str,'company_name':str,'form_type':str,'form_date':pd.datetime,'form_type':str}
		dataframe = pd.read_csv(file_handle,skiprows=skip_rows,delimiter="|",
			header=0,parse_dates=[3],names=col_index,dtype=col_types)
		self.dataframe = dataframe

	def find_by_name(self,company,filing_date=None,form_type=None):
		df = self.dataframe
		condition1 = df["company_name"].apply(lambda x: company in str(x))
		final_condition = condition1
		if (filing_date):
			condition2 = df["form_date"] == datetime.strptime(filing_date,"%Y-%m-%d")
			final_condition  = condition2 & final_condition
		if (form_type):
			condition3 = df["form_type"] == form_type
			final_condition  = condition3 & final_condition
		return df[final_condition]

	def find_by_cik(self,cik,filing_date=None,form_type=None):
		df = self.dataframe
		condition1 = df["cik"] == cik
		final_condition = condition1
		if (filing_date):
			condition2 = df["form_date"] == datetime.strptime(filing_date,"%Y-%m-%d")
			final_condition  = condition2 & final_condition
		if (form_type):
			condition3 = df["form_type"] == form_type
			final_condition  = condition3 & final_condition
		return df[final_condition]

	def _sort_data(self,df):
		sort_columns = ['form_date','form_type','file_name']
		df = df.sort_values(by=sort_columns,ascending=False,inplace=False)
		return df

	def find_latest_by_name(self,company,filing_date=None,form_type=None):
		df = self.find_by_name(company,filing_date=filing_date,form_type=form_type)
		df = self._sort_data(df)
		if df is not None:
			return df.iloc[0].to_dict()
		else:
			return None

	def find_latest_by_cik(self,company,filing_date=None,form_type=None):
		df = self.find_by_cik(company,filing_date=filing_date,form_type=form_type)
		df = self._sort_data(df)
		if df is not None:
			return df.iloc[0].to_dict()
		else:
			return None

if __name__ == '__main__':
	master_file = MasterFile("master_2016_1.gz")
	df = master_file.dataframe
	print df.columns
	print df.dtypes