
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

today = datetime.datetime.now()
print today.strftime("%Y-%m-%d")

AccessKeyID = 'ACCESS KEY'
merchant_id = 'MERCHANT ID'
SecretKey = 'SECRET KEY'
conn = MWSConnection(AccessKeyID,SecretKey)
conn.SellerId = 'SELLER ID'
conn.Merchant = 'MERCHANT NAME'
conn.MarketplaceId = 'MARKETPLACE ID'
marketplaceId = 'MARKETPLACE ID'


result = conn.list_inventory_supply(QueryStartDateTime='2017-07-01') #Gets First Page
r = result.ListInventorySupplyResult.InventorySupplyList
inventory = []
for item in r:
	print item
	#exit()
	oh_units =  item.InStockSupplyQuantity
	ttl_units =  item.TotalSupplyQuantity
	ASIN = item.ASIN
	Variant = item.SellerSKU
	inventory.append([ASIN, Variant, oh_units,ttl_units])
    

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
	tera.upload('delete from BACKUP TABLE')
	tera.upload("""insert into INSERT PROD TABLE INTO BACKUP TABLE""")
	print 'Table Backed up'
except:
	print "backup failed"



for item in inventory:
	try:
		sql = "insert into PROD TABLE values('%s','%s','%s','%s','%s')" %(item[0],item[1],item[2],item[2],today.strftime("%Y-%m-%d"))
		#print sql
		tera.upload(sql)
	except:
		print "upload failed"

print 'records uploaded'

###################################
#Set up an email
###################################

fr = 'FROM EMAIL'
to = [
"MY OLD EMAIL HERE"
]

cc = [
"CO WORKERS EMAIL"

]

subject = 'Weekly Store Capacity'
server = 'mail.lhmsports.com'
file_name = "test.xlsx"
file_path = "FILE PATH\\%s" % file_name
data_sheet_name = "Data"

#Re-write if sending message
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