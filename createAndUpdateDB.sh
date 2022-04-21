sqlite3 ebay < create.sql;
sqlite3 ebay < load.txt;

## USED FOR TESTING LOCALLY
# sqlite3 ebay < create.sql;
# cd ./parsed_ebay_data;
# sqlite3 ../ebay < ../load.txt;
