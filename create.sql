--This is a user table where it includes all sellers and all bidders. 
--It saves the information of the users such as rating and location id. 
DROP TABLE IF EXISTS user;
CREATE TABLE user (user_id CHAR(256) NOT NULL UNIQUE,
	rating INT NOT NULL,
	location_id CHAR(256),
	PRIMARY KEY(user_id),
	FOREIGN KEY(location_id) REFERENCES location(location_id));

--This is a location table where it saves information on location and the country id.
DROP TABLE IF EXISTS location;
CREATE TABLE location (location_id CHAR(256) NOT NULL UNIQUE,
	location CHAR(256),
	country_id CHAR(256),
	PRIMARY KEY(location_id),
	FOREIGN KEY(country_id) REFERENCES country(country_id));

--This is a country table where it saves information regarding all the countries present. 
DROP TABLE IF EXISTS country;
CREATE TABLE country (country_id CHAR(256) NOT NULL UNIQUE,
	country CHAR(256),
	PRIMARY KEY(country_id));

--This is an item table where it saves the information per item. 
--It saves information such as name, currently, buy_price, first_bid 
DROP TABLE IF EXISTS item;
CREATE TABLE item (item_id CHAR(256) NOT NULL UNIQUE,
	name CHAR(256),
	currently CHAR(256),
	buy_price CHAR(256),
	first_bid CHAR(256),
	number_of_bids INT,
	started CHAR(256),
	ends CHAR(256),
	seller_id CHAR(256),
	description CHAR(1000),
	PRIMARY KEY (item_id),
	FOREIGN KEY(first_bid) REFERENCES bids(bid_id),
	FOREIGN KEY(seller_id) REFERENCES user(user_id));

--This is the category table which saves information about category id and category. 
DROP TABLE IF EXISTS category;
CREATE TABLE category (category_id CHAR(256) NOT NULL UNIQUE,
	category CHAR(256) NOT NULL,
	PRIMARY KEY(category_id));

--This is the ctegory_item table which saves the all of the categories from each item. 
DROP TABLE IF EXISTS category_item;
CREATE TABLE category_item (item_id CHAR(256),
	category_id CHAR(256),
	PRIMARY KEY(item_id, category_id));

--This is the bids table that saves all of the information from one bid. 
DROP TABLE IF EXISTS item_bids;
CREATE TABLE bids (item_id CHAR(256) NOT NULL,
	bids_id CHAR(256),
	PRIMARY KEY(item_id, bids_id),
	FOREIGN KEY(bids_id) REFERENCES bids(bids_id),
	FOREIGN KEY(item_id) REFERENCES item(item_id));




