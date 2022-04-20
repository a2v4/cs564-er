sqlite3 ebay < ./create.sql;
cd ./parsed_ebay_data;
sqlite3 ../ebay < ../load.txt;
