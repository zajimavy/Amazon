
###################################
#Basic Imports
###################################

from app import email, sql, excel, tera

from boto.mws.connection import MWSConnection
import time
import datetime

###################################
#Return a result set
###################################

#results = sql.executeScriptsFromFile('N:\Planning\John\SQL Queries\Python Queries\\sql_test_files.sql')
#print "hello world"

today = datetime.datetime.now()
print today.strftime("%Y-%m-%d")
#exit()
AccessKeyID = 'AKIAII7SIICRLNY4DX4A'
merchant_id = 'A1X4G4EP9W5CW1'
SecretKey = '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'
conn = MWSConnection(AccessKeyID,SecretKey)
conn.SellerId = 'A1X4G4EP9W5CW1'
conn.Merchant = 'Fanzz Sports'
conn.MarketplaceId = 'ATVPDKIKX0DER '
marketplaceId = 'ATVPDKIKX0DER '


result = conn.list_inventory_supply(QueryStartDateTime='2017-07-01') #Gets First Page
r = result.ListInventorySupplyResult.InventorySupplyList
inventory = []
for item in r:
	print item
	oh_units =  item.InStockSupplyQuantity
	ttl_units =  item.TotalSupplyQuantity
	ASIN = item.ASIN
	Variant = item.SellerSKU
	inventory.append([ASIN, Variant, oh_units,ttl_units])
    
#print inventory
print len(inventory)


try:
	NextToken = result.ListInventorySupplyResult.NextToken
except:
	NextToken = 0
print result    
while NextToken <> 0:
	result = conn.list_inventory_supply_by_next_token(NextToken = NextToken)
	r =  result.ListInventorySupplyByNextTokenResult.InventorySupplyList
	for item in r:
		oh_units =  item.InStockSupplyQuantity
		ttl_units =  item.TotalSupplyQuantity
		ASIN = item.ASIN
		Variant = item.SellerSKU
		inventory.append([ASIN, Variant, oh_units,ttl_units])
		try:
			NextToken = result.ListInventorySupplyByNextTokenResult.NextToken
		except:
			NextToken = 0



try:
	tera.upload('delete from fanzz_labs.m_fba_inv_backup')
	tera.upload("""insert into fanzz_labs.m_fba_inv_backup
								select * from fanzz_labs.m_fba_inv""")
	print 'Table Backed up'
except:
	print "backup failed"



for item in inventory:
	try:
		sql = "insert into fanzz_labs.m_fba_inv values('%s','%s','%s','%s','%s')" %(item[0],item[1],item[2],item[2],today.strftime("%Y-%m-%d"))
		#print sql
		tera.upload(sql)
	except:
		print "upload failed"

print 'records uploaded'

###################################
#Set up an email
###################################

fr = 'John.Stockinger@lhmsports.com'
to = [
 "John.Stockinger@lhmsports.com"
#, "Steven.Scalzi@lhmsports.com"
]

cc = [
#"Scott.Nelson@lhmsports.com"
#, "Justin.Trujillo@lhmsports.com"
#, "Jered.Tate@lhmsports.com"
#, "John.Stockinger@lhmsports.com"

]

subject = 'Weekly Store Capacity'
server = 'mail.lhmsports.com'
file_name = "test.xlsx"
file_path = "N:\Planning\John\Data\Excel Files\\%s" % file_name
data_sheet_name = "Data"
message = """
Team,
<br><br>
This is a test
<br><br>
Also a test paragraph

<br><br><br> <a href="%s">A test file report</a>""" % file_path


###################################
#Save and format an excel file 
#then email it
###################################
#excel.saveData(results, file_path, data_sheet_name) #you can denote columns to format with [8,9,10,11,14,15]
#email.emailAttachment(fr, to, subject, message, server, file_path, cc)