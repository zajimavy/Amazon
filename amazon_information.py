
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
AccessKeyID = 'ACCESS KEY'
SecretKey = 'SECRET KEY'


merchant_id = 'MERCHANT ID'
marketplaceId = 'MARKETPLACE ID'


conn = MWSConnection(AccessKeyID,SecretKey)
conn.SellerId = 'SELLER ID'
conn.Merchant = MERCHANT NAME'
conn.MarketplaceId = 'MARKETPLACE' #https://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html


#variants = tera.runQuery("select * from fanzz_labs.js_upc_amazon") #where upc = '190528763607'

#print variants

#variants = [190528763294, 190528763379]
        
ASINLIST = tera.runQuery('''select 


m.amz_asin
, p.retailvariant_id


from UPC TABLE m 
left join PRODUCT TABLE p on p.upc = m.upc

where m.amz_asin is not null
and m.amz_asin not in (select amz_asin from AMAZON LISTING TABLE )
and m.amz_asin <> 'B075TZHPSC'
group by 1,2
 ''' )
#and m.amz_asin = 'B01MQIXH3T'

#print ASINLIST        
x = 0
records = len(ASINLIST)
for item in ASINLIST:
    
    print '----------------------------------------------------'
    print item
    ASIN = [item[0]]
    RetailVariantID = item[1]
    print ASIN[0]
    
    parent = conn.get_matching_product_for_id(MarketplaceId=marketplaceId,IdType="ASIN",IdList=ASIN)
    try:
        parent = parent.GetMatchingProductForIdResult[0].Products.Product[0].Relationships.VariationParent[0].Identifiers
        parent = [parent.MarketplaceASIN.ASIN]
    except:
        parent = ASIN

    print 'Parent ASIN: ' + str(parent[0])

    try:
        slsrank = conn.get_matching_product_for_id(MarketplaceId=marketplaceId,IdType="ASIN",IdList=parent)
        title =  slsrank.GetMatchingProductForIdResult[0].Products.Product[0].AttributeSets.ItemAttributes[0].Title
    except:
        title = 'FAIL'
    try:
        slsrank = slsrank.GetMatchingProductForIdResult[0].Products.Product[0].SalesRankings.SalesRank[0].Rank
        if slsrank =='None':
            slsrank = 9999999
    except:
        slsrank = 9999999
    print 'Sales Rank: ' + str(slsrank)
    try:
        print 'Title: ' + title
    except:
        print 'Title: '

    result = conn.get_lowest_offer_listings_for_asin(MarketplaceId=marketplaceId,ASINList=ASIN)
    
    try:
        channel = result.GetLowestOfferListingsForASINResult[0].Product.LowestOfferListings.LowestOfferListing[0].Qualifiers.FulfillmentChannel
    except:
        channel = 'Unknown'
    
    #print channel
    try:
        result = result.GetLowestOfferListingsForASINResult[0].Product.LowestOfferListings.LowestOfferListing[0].Price
        lowestprice = result.ListingPrice
        shipprice = result.Shipping
    except:
        lowestprice = 0
        shipprice = 0

    result = conn.get_competitive_pricing_for_asin(MarketplaceId=marketplaceId,ASINList = ASIN)
    try:
        listingcount = result.GetCompetitivePricingForASINResult[0].Product.CompetitivePricing[0].OfferListingCount
        listingcount = str(listingcount)
        listingcount = int(listingcount)
    except:
        listingcount = 0
    try:    
        buyboxprice = float(result.GetCompetitivePricingForASINResult[0].Product.CompetitivePricing[0].CompetitivePrices.CompetitivePrice[0].Price.ListingPrice)
    except:
        buyboxprice = 0
    try:
        fanzzinbuybox = result.GetCompetitivePricingForASINResult[0].Product.CompetitivePricing[0].CompetitivePrices.CompetitivePrice[0]['belongsToRequester']
    except:
        fanzzinbuybox = 'False'
    print 'Lowest Price: ' + str(lowestprice)
    print 'Ship Cost: ' + str(shipprice)
    print 'Fufilment Channel: ' + channel
    print 'Listing Count:' + str(listingcount)
    print 'Buy Box Price:' + str(buyboxprice)
    print 'Do we have buy box? ' + fanzzinbuybox
    ASIN = ASIN[0]
    parent = str(parent[0])
    sql = """insert into AMAZON LISTING TABLE values('%s','%s','%s','%s','%s','%s','%s',current_timestamp,'%s','%s','%s','%s')""" % (ASIN,parent,float(lowestprice),float(shipprice),channel,slsrank,title.replace("'", "''"),RetailVariantID ,listingcount,buyboxprice,str(fanzzinbuybox))
    #print str(sql)
    
    tera.upload (sql) 
    x=x+1
    print str(x) + ' of ' + str(len(ASINLIST))
    



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
