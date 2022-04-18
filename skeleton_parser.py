
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"
user = {}
category = {}
country = {}
location = {}
bidders = []
bid_item = []
itemtable = []
item_category = []
user_item = []
user_bid = []



# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            location(item)
            users(item)
            category(item)
            item_table(item)
            bids(item)

def users(item):
	if (CheckUser(item['Seller']) == False): 
		use = item['Seller']
		users[use['UserID']] = use['Rating'] + columnSeparator + "null"
	else if item['Bids'] is not null:
		for bid in item['Bids']['Bid']:
			use = bid['Bidder']
			users[use['UserID']] = use['Rating'] + columnSeparator + location[use['Location']][0]

def CheckUser(seller):
	if (seller['UserID'] is in user):
		return True
	return False

def location(item):
	if item['Location'] not in location:
		if item['Country'] not in country:
			country[item['Country']] = len(country) + 1
		location[item['Location']] = (len(location) + 1, country[item['Country']])
	else if item['Bids'] is not null:
		for bid in item['Bids']['Bid']:
			use = bid['Bidder']
			CheckCountry(use)
			CheckLocation(use)

def CheckLocation(item):
	if item['Location'] not in location:
		location[item['Location']] = (len(location) + 1, country[item['Country']])

def CheckCountry(item):
	if item['Country'] not in country:
		country[item['Country']] = len(country) + 1		

def bids(item):
	if item['Bids'] is null:
		pass
	for bid in item['Bids']['Bid']:
		bidder = bid['Bidder']
		bids_id = len(bidders) + 1
		amount = bid['Amount']
		time = transformDttm(bid['Time'])
		user_id = bidder['UserID']
		item_id = item['ItemID']
		bidders.append(bids_id + columnSeparator + amount + columnSeparator + time + columnSeparator + user_id + columnSeparator + item_id)
		bid_item.append(item_id + columnSeparator + bids_id)
		user_bid.append(user_id + columnSeparator + bids_id)


def category(item):
	for cat in item['Category']:
		if cat not in category:
			category[cat] = len(category) + 1

def item_table(item):
	item_id = item['ItemID']
	name = item['Name'].replace('"','""')
	currently = transformDollar(item['Currently'])
	first_bid = transformDollar(item['First_Bid'])
	number_of_bids = item['Number_of_Bids']
	started = transformDttm(item['Started'])
	ends = transformDttm(item['ends'])
	user_id = item['Seller']['UserID']
	buyprice = item['Buy_Price']
	desc = item['Description'].replace('"','""')
	user_id = item['Seller']['UserID']
	itemtable.append(item_id + columnSeparator + '"' +  name + '"' + columnSeparator + currently+ columnSeparator + buyprice
		+ columnSeparator + first_bid + columnSeparator + number_of_bids + columnSeparator + started + columnSeparator + ends
		+ columnSeparator + user_id + columnSeparator + '"' + desc + '"')
	user_item.append(user_id + columnSeparator + item_id)
	for cat in item['Category']:
		item_category.append(item_id + columnSeparator + category[cat])


def generate_files():
	with open('user.dat', 'w') as f:
		f.write('\n'.join(str(user_id) + columnSeparator + rateloc for user_id, rateloc in users.iteritems()))
	with open('location.dat', 'w') as f:
		f.write()
	with open('country.dat', 'w') as f:
		f.write('\n'.join(country_id + columnSeparator + str(country_name) for country_name, countryid in country.iteritems()))
	with open('item.dat', 'w') as f:
		f.write('\n'.join(itemtable))
	with open('category.dat', 'w') as f:
		f.write('\n'.join(category_id + columnSeparator + str(category_name) for category_name, categoryid in category.iteritems()))
	with open('category_item.dat', 'w') as f:
		f.write('\n'.join(item_category))
	with open('bids.dat', 'w') as f:
		f.write('\n'.join(bidders))
	with open('item_bids.dat', 'w') as f:
		f.write('\n'.join(bid_item))
	with open('user_item.dat', 'w') as f:
		f.write('\n'.join(user_item))
	with open('user_bid.dat', 'w') as f:
		f.write('\n'.join(user_bid))

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f
    generate_files()
if __name__ == '__main__':
    main(sys.argv)
