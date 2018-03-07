
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
#print today.strftime("%Y-%m-%d")
#exit()
AccessKeyID = 'AKIAII7SIICRLNY4DX4A'
SecretKey = '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'


merchant_id = 'A1X4G4EP9W5CW1'
marketplaceId = 'ATVPDKIKX0DER'


conn = MWSConnection(AccessKeyID,SecretKey)
conn.SellerId = 'A1X4G4EP9W5CW1'
conn.Merchant = 'Fanzz Sports'
conn.MarketplaceId = 'ATVPDKIKX0DER' #https://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html


variants = tera.runQuery("select * from fanzz_labs.js_top_sellers   where sales >= '1000' ") #where upc = '190528763607'

#print variants

#variants = [190528763294, 190528763379]

print type(variants)
x=0
records = len(variants)
for variant in variants:
    SKU = [variant[0]]
    print '--------------------------------------------'
    print SKU
    time.sleep(.1)
    try:
    	result = conn.get_matching_product_for_id(MarketplaceId=marketplaceId,IdType="UPC",IdList=SKU)
    	#print result
    	asin =  result.GetMatchingProductForIdResult[0].Products.Product[0].Identifiers.MarketplaceASIN.ASIN
    #	print asin
    	#print '1 Row Uploaded: ' + UPC  + '|' + SKU[0]
    	try:
    		sql = "insert into fanzz_labs.m_amazon_upc values ('%s','%s')" %(SKU[0], asin)
    		tera.upload(sql) 
    	except:
    		print "Duplicate Error"
    #	print sql
    	
    except:
    	print 'No Amazon Match: ', SKU[0]
    	asin = 'NULL'
    	try:
    		sql = "insert into fanzz_labs.m_amazon_upc values ('%s',%s)" %(SKU[0], asin)
    	 	tera.upload(sql) 
    	except:
    		print "Duplicate"
    	
    x = x + 1
    print str(x) + ' of ' + str(records)    



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