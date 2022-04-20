import sys
from json import loads
from re import sub

COLUMN_SEPARATOR = "|"
USER_DATA_DICT = {}
CATEGORY_DATA_DICT = {}
COUNTRY_DATA_DICT = {}
LOCATION_DATA_DICT = {}
BIDDERS_DATA_ARRAY = []
BID_ITEM_DATA_ARRAY = []
ITEM_TABLE_DATA_ARRAY = []
ITEM_CATEGORY_DATA_ARRAY = []
USER_ITEM_DATA_ARRAY = []
USER_BID_DATA_ARRAY = []


# Dictionary of months used for date transformation
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


def isJson(f):
    """
    Returns true if a file ends in .json
    """
    return len(f) > 5 and f[-5:] == '.json'


def transformMonth(mon):
    """
    Converts month to a number, e.g. 'Dec' to '12'
    """
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


def transformDttm(dttm):
    """
    Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
    """
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


def transformDollar(money):
    """
    Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
    """
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def parseJson(json_file):
    """
    Parses a single json file. Currently, there's a loop that iterates over each
    item in the data set. Your job is to extend this functionality to create all
    of the necessary SQL tables for your database.
    """
    with open(json_file, 'r') as f:
        # creates a Python dictionary of Items for the supplied json file
        items = loads(f.read())['Items']
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])
            locations_parser(item)
            users_parser(item)
            category_parser(item)
            item_table_parser(item)
            bids_parser(item)


def instance_checker(data, expected_datatype) -> bool:
    """
    Check to make sure that the given element is the correct
    type. If not, raise an exception to inform the user.
    """
    if data != None and not isinstance(data, expected_datatype):
        raise Exception("Given data is not what was expected.")
        return False
    return True


def escape_quotes(string) -> str:
    """
    Escape quotes within given string to allow SQL to parse correctly

    Parameters:
            string (str): the string to manipulate
    Returns:
            str: parsed string with escape quotes if found
    """
    return sub(r'"+', '""', string)


def users_parser(item) -> None:
    """
    Parse users data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    curr_seller = item['Seller']
    instance_checker(curr_seller, dict)

    if is_user_parsed_already(curr_seller) == False:
        # {"UserID": "captwhiz", "Rating": "1054"}
        '''
        "Seller": {
                                "description": "Attributes give the seller's UserID and rating.", 
                                "type": "object",
                                "properties": {
                                        "UserID": {
                                                "description": "unique id for a user across all users",
                                                "type": "string"
                                        },
                                        "Rating": {
                                                "description": "Users's rating",
                                                "type": "number"
                                        }
                                },
                                "required": ["UserID", "Rating"]
                        },
        '''
        USER_DATA_DICT[curr_seller['UserID']] = curr_seller['Rating'] + \
            COLUMN_SEPARATOR + "NULL"
    if item.get("Bids") != None:
        instance_checker(item['Bids'], list)
        for bid in item['Bids']:
            # bid -> dict_keys(['Bid'])
            instance_checker(bid, dict)

            curr_bid = bid['Bid']
            # curr_bid -> dict_keys(['Bidder', 'Time', 'Amount'])
            instance_checker(curr_bid, dict)

            curr_bidder = curr_bid['Bidder']
            # curr_bidder -> dict_keys(['UserID', 'Rating', 'Location', 'Country'])
            instance_checker(curr_bidder, dict)

            # Some bidders info does not have a location/country as it is not required
            # So this is a safe guard
            location = curr_bidder.get('Location')
            location_data_item = LOCATION_DATA_DICT.get(location)
            location_entry = "NULL"
            if location_data_item != None:
                location_entry = location_data_item[0]

            USER_DATA_DICT[curr_bidder['UserID']] = COLUMN_SEPARATOR.join(
                [escape_quotes(str(x)) for x in [curr_bidder['Rating'], location_entry]])


def is_user_parsed_already(seller) -> None:
    """
    Check whether a user has already been parsed

    Parameters:
            seller (dict): data to grab UserID from to check against
    Returns:
            True/False
    """
    instance_checker(seller, dict)
    # seller.keys() -> dict_keys(['UserID', 'Rating'])

    curr_seller = seller.get("UserID")
    if curr_seller not in (None, "NULL") and curr_seller in USER_DATA_DICT:
        return True
    return False


def locations_parser(item) -> None:
    """
    Parse location data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    curr_location = escape_quotes(item.get("Location", "NULL"))
    curr_country = escape_quotes(item.get("Country", "NULL"))
    curr_bids = item.get("Bids")
    instance_checker(curr_bids, list)

    if curr_location not in (None, "NULL") and curr_country not in (None, "NULL") and curr_location not in LOCATION_DATA_DICT:
        if curr_country not in COUNTRY_DATA_DICT:
            COUNTRY_DATA_DICT[curr_country] = len(COUNTRY_DATA_DICT) + 1
        LOCATION_DATA_DICT[curr_location] = (
            len(LOCATION_DATA_DICT) + 1, COUNTRY_DATA_DICT[curr_country])
    if curr_bids != None:
        for bid in curr_bids:
            instance_checker(bid, dict)
            # bid -> dict_keys(['Bid'])
            curr_bid = bid['Bid']
            # curr_bid -> dict_keys(['Bidder', 'Time', 'Amount'])
            curr_bidder = curr_bid['Bidder']
            instance_checker(curr_bid, dict)
            check_country(curr_bidder)
            check_location(curr_bidder)


def check_location(item) -> None:
    """
    Parse location data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    curr_location = escape_quotes(item.get("Location", "NULL"))
    curr_country = escape_quotes(item.get("Country", "NULL"))
    if curr_location not in (None, "NULL") and curr_country not in (None, "NULL") and curr_location not in LOCATION_DATA_DICT:
        LOCATION_DATA_DICT[curr_location] = (
            len(LOCATION_DATA_DICT) + 1, COUNTRY_DATA_DICT[curr_country])


def check_country(item) -> None:
    """
    Parse country data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    curr_country = escape_quotes(item.get("Country", "NULL"))
    if curr_country not in (None, "NULL") and curr_country not in COUNTRY_DATA_DICT:
        COUNTRY_DATA_DICT[curr_country] = len(COUNTRY_DATA_DICT) + 1


def bids_parser(item) -> None:
    """
    Parse bid data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    bids = item.get("Bids")
    if bids == None:
        return
    instance_checker(bids, list)

    for bid in bids:
        instance_checker(bid, dict)
        # bid -> dict_keys(['Bid'])
        curr_bid = bid['Bid']
        # curr_bid -> dict_keys(['Bidder', 'Time', 'Amount'])
        curr_bidder = curr_bid['Bidder']
        # curr_bidder -> dict_keys(['UserID', 'Rating', 'Location', 'Country'])
        instance_checker(curr_bid, dict)
        bids_id = len(BIDDERS_DATA_ARRAY) + 1
        bid_amount = curr_bid['Amount']
        bid_time = transformDttm(curr_bid['Time'])
        bid_user_id = curr_bidder['UserID']
        bid_item_id = item['ItemID']
        BIDDERS_DATA_ARRAY.append(COLUMN_SEPARATOR.join([escape_quotes(str(x)) for x in
                                                         [bids_id, bid_amount, bid_time, bid_user_id, bid_item_id]]))
        BID_ITEM_DATA_ARRAY.append(
            COLUMN_SEPARATOR.join([escape_quotes(str(x)) for x in [bid_item_id, bids_id]]))
        USER_BID_DATA_ARRAY.append(COLUMN_SEPARATOR.join(
            [escape_quotes(str(x)) for x in [bid_user_id, bids_id]]))


def category_parser(item) -> None:
    """
    Parse category data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    categories = item.get("Category")
    instance_checker(categories, list)

    for category in categories:
        if category not in CATEGORY_DATA_DICT:
            CATEGORY_DATA_DICT[category] = len(CATEGORY_DATA_DICT) + 1


def item_table_parser(item) -> None:
    """
    Parse item data based on data given

    Parameters:
            item (dict): dictionary to grab data from
    Returns:
            None
    """
    instance_checker(item, dict)
    # item.keys() -> dict_keys(['ItemID', 'Name', 'Category', 'Currently', 'First_Bid', 'Number_of_Bids', 'Bids', 'Location', 'Country', 'Started', 'Ends', 'Seller', 'Description'])

    item_id = item.get('ItemID', 'NULL')
    name = item.get('Name', 'NULL')
    currently = transformDollar(item.get('Currently', 'NULL'))
    first_bid = transformDollar(item.get('First_Bid', 'NULL'))
    number_of_bids = item.get('Number_of_Bids', 'NULL')
    started = transformDttm(item.get('Started', 'NULL'))
    ends = transformDttm(item.get('Ends', 'NULL'))
    user_id = item.get('Seller', {}).get('UserID', 'NULL')
    buy_price = item.get('Buy_Price', "NULL")
    # some descriptions are None, so the 'or' will replace it with a 'NULL'
    desc = item.get('Description', 'NULL') or 'NULL'

    ITEM_TABLE_DATA_ARRAY.append(COLUMN_SEPARATOR.join([escape_quotes(str(x)) for x in
                                                        [item_id, f'"{name}"', currently, buy_price, first_bid, number_of_bids, started, ends, user_id, f'"{desc}"']]))
    USER_ITEM_DATA_ARRAY.append(COLUMN_SEPARATOR.join(
        [escape_quotes(str(x)) for x in [user_id, item_id]]))

    categories = item.get("Category")
    instance_checker(categories, list)

    for category in categories:
        ITEM_CATEGORY_DATA_ARRAY.append(
            COLUMN_SEPARATOR.join([escape_quotes(str(x)) for x in [item_id, CATEGORY_DATA_DICT[category]]]))


def generate_files():
    """
    Generate and write to output files (.dat) for SQL import

    Parameters:
            None
    Returns:
            None
    """
    with open('user.dat', 'w') as f:
        f.write('\n'.join(str(user_id) + COLUMN_SEPARATOR +
                str(rateloc) for user_id, rateloc in USER_DATA_DICT.items()))
    with open('location.dat', 'w') as f:
        f.write('\n'.join(str(location_data[0]) + COLUMN_SEPARATOR + str(location)
                          for location, location_data in LOCATION_DATA_DICT.items()))
    with open('country.dat', 'w') as f:
        f.write('\n'.join(str(country_id) + COLUMN_SEPARATOR + str(country_name)
                for country_name, country_id in COUNTRY_DATA_DICT.items()))
    with open('item.dat', 'w') as f:
        f.write('\n'.join(ITEM_TABLE_DATA_ARRAY))
    with open('category.dat', 'w') as f:
        f.write('\n'.join(str(category_id) + COLUMN_SEPARATOR + str(category_name)
                for category_name, category_id in CATEGORY_DATA_DICT.items()))
    with open('category_item.dat', 'w') as f:
        f.write('\n'.join(ITEM_CATEGORY_DATA_ARRAY))
    with open('bids.dat', 'w') as f:
        f.write('\n'.join(BIDDERS_DATA_ARRAY))
    with open('item_bids.dat', 'w') as f:
        f.write('\n'.join(BID_ITEM_DATA_ARRAY))
    with open('user_item.dat', 'w') as f:
        f.write('\n'.join(USER_ITEM_DATA_ARRAY))
    with open('user_bid.dat', 'w') as f:
        f.write('\n'.join(USER_BID_DATA_ARRAY))


def main(argv):
    """
    Loops through each json files provided on the command line and passes each file
    to the parser
    """
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files')
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)
    generate_files()


if __name__ == '__main__':
    main(sys.argv)
