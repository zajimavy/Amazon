import pyodbc
import teradata
import os

class SQL:
	def upload(self, query):
		connection_str = """Connection STRING"""
		cnxn = pyodbc.connect(connection_str)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)

	def runQuery(self, query):
		connection_str = """ Connection STRING """
		cnxn = pyodbc.connect(connection_str)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)	
		results = cursor.fetchall()
		return results
		
	def executeScriptsFromFile(self,filename):
		connection_str = """Connection STRING """
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
		connection_str = """ Connection STRING """
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
		connection_str = """ Connection STRING""" % os.getenv('username')
		cnxn = pyodbc.connect(connection_str, autocommit=True)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)	
		results = cursor.fetchall()
		return results
		
	def upload(self, query):
		connection_str = """ Connection STRING""" % os.getenv('username')
		cnxn = pyodbc.connect(connection_str, autocommit=True)
		cnxn.autocommit = True
		cursor = cnxn.cursor()
		cursor.execute(query)
		
		
	
	            
if __name__ == "__main__": #this is what runs at the cmd line
	 result = executeScriptsFromFile("FILE PATH\\sql_test_files.sql")
	 print type(result)
	 print result
	 
