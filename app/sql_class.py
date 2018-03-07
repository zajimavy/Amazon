import pyodbc
import teradata
import os

class SQL:
	def upload(self, query):
		connection_str = """ Driver={SQL Server Native Client 11.0}; Server=FNZBISQL01\DAX_SQL_BI; Database=dw; Trusted_Connection=yes; """
		cnxn = pyodbc.connect(connection_str)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)

	def runQuery(self, query):
		connection_str = """ Driver={SQL Server Native Client 11.0}; Server=FNZBISQL01\DAX_SQL_BI; Database=dw; Trusted_Connection=yes; """
		cnxn = pyodbc.connect(connection_str)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)	
		results = cursor.fetchall()
		return results
		
	def executeScriptsFromFile(self,filename):
		connection_str = """ Driver={SQL Server Native Client 11.0}; Server=FNZBISQL01\DAX_SQL_BI; Database=dw; Trusted_Connection=yes; """
		cnxn = pyodbc.connect(connection_str)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		
		fd = open(filename, 'r')
		sqlFile = fd.read()
		fd.close()
		sqlCommands = sqlFile.split(';')
		
		cursor.execute(sqlFile)
		results = cursor.fetchall()
	
		return results

	def executeScriptsFromFileNoResults(self,filename):
		connection_str = """ Driver={SQL Server Native Client 11.0}; Server=FNZBISQL01\DAX_SQL_BI; Database=dw; Trusted_Connection=yes; """
		cnxn = pyodbc.connect(connection_str)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		
		fd = open(filename, 'r')
		sqlFile = fd.read()
		fd.close()
		sqlCommands = sqlFile.split(';')
		
		cursor.execute(sqlFile)

class Teradata:
	def runQuery(self, query):
		connection_str = """ Driver={Teradata}; dbcname=141.206.21.20; dsn = vm; authentication = TD2; uid={%s}; pwd={$tdwallet(pass_win)};""" % os.getenv('username')
		cnxn = pyodbc.connect(connection_str, autocommit=True)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)	
		results = cursor.fetchall()
		return results
		
	def upload(self, query):
		connection_str = """ Driver={Teradata}; dbcname=141.206.21.20; dsn = vm; authentication = TD2; uid={%s}; pwd={$tdwallet(pass_win)};""" % os.getenv('username')
		cnxn = pyodbc.connect(connection_str, autocommit=True)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)
		
		
	
	            
if __name__ == "__main__": #this is what runs at the cmd line
	 result = executeScriptsFromFile("N:\Planning\John\SQL Queries\Python Queries\\sql_test_files.sql")
	 print type(result)
	 print result
	 