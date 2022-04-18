# User
This is a user table where it includes all sellers and all bidders. It saves the information of the users such as rating and location id.

||**USER**||
| -------- | ----------- | --------- |
| **PK**   | user_id     | CHAR(256) |
|          | rating      | INT       |
| FK       | location_id | CHAR(256) |

```sql
CREATE TABLE user (user_id CHAR(256) NOT NULL UNIQUE,
			rating INT NOT NULL,
			location_id CHAR(256),
			PRIMARY KEY(user_id),
			FOREIGN KEY(location_id) REFERENCES location(location_id));
```

# Location
This is a location table where it saves information on location and the country id.

|| **LOCATION** ||
| ------------ | ----------- | --------- |
| **PK**       | location_id | CHAR(256) |
|              | location    | CHAR(256) |
| FK           | country_id  | CHAR(256) |

```sql
CREATE TABLE location (location_id CHAR(256) NOT NULL UNIQUE,
			location CHAR(256),
			country_id CHAR(256),
			PRIMARY KEY(location_id),
			FOREIGN KEY(country_id) REFERENCES country(country_id));
```


# Country
This is a country table where it saves information regarding all the countries present.

|| **COUNTRY** ||
| ----------- | ---------- | --------- |
| **PK**      | country_id | CHAR(256) |
|             | country    | CHAR(256) |

```sql
CREATE TABLE country (country_id CHAR(256) NOT NULL UNIQUE,
			country CHAR(256),
			PRIMARY KEY(country_id));
```


# Item
This is an item table where it saves the information per item. It saves information such as name, currently, buy_price, first_bid

|| **ITEM** ||
| -------- | -------------- | ---------- |
| **PK**   | item_id        | CHAR(256)  |
|          | name           | CHAR(256)  |
|          | currently      | CHAR(256)  |
|          | buy_price      | CHAR(256)  |
| FK       | first_bid      | CHAR(256)  |
|          | number_of_bids | INT        |
|          | started        | CHAR(256)  |
|          | ends           | CHAR(256)  |
| FK       | seller_id      | CHAR(256)  |
|          | description    | CHAR(1000) |

```sql
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
```


# Category
This is the category table which saves information about category id and category.

|| **CATEGORY**||
| ------------ | ----------- | --------- |
| **PK**       | category_id | CHAR(256) |
|              | category    | CHAR(256) |
```sql
CREATE TABLE category (category_id CHAR(256) NOT NULL UNIQUE,
			category CHAR(256) NOT NULL,
			PRIMARY KEY(category_id));
```

# Category_Item
This is the ctegory_item table which saves all of the categories from each item.

|| **CATEGORY_ITEM**||
| ----------------- | ----------- | --------- |
| **PK**, FK        | item_id     | CHAR(256) |
| **PK**, FK        | category_id | CHAR(256) |

```sql
CREATE TABLE category_item (item_id CHAR(256),
				category_id CHAR(256),
				PRIMARY KEY(item_id, category_id));
```

# Bids
This is the bids table that saves all of the information from one bid.

|| **BIDS**||
| -------- | ------- | --------- |
| **PK**   | bids_id | CHAR(256) |
|          | amount  | CHAR(256) |
|          | time    | CHAR(256) |
| FK       | user_id | CHAR(256) |
| FK       | item_id | CHAR(256) |

```sql
CREATE TABLE bids (bids_id CHAR(256) NOT NULL UNIQUE,
			amount CHAR(256),
			time CHAR(256),
			user_id CHAR(256),
			item_id CHAR(256),
			PRIMARY KEY(bids_id),
			FOREIGN KEY(user_id) REFERENCES user(user_id),
			FOREIGN KEY(item_id) REFERENCES item(item_id));
```


# Item_Bids
This is the item_bids table that saves all the bids information per item.

|| **ITEM_BIDS** ||
| ---------- | ------- | --------- |
| **PK**, FK | item_id | CHAR(256) |
| **PK**, FK | bids_id | CHAR(256) |

```sql
CREATE TABLE bids (item_id CHAR(256) NOT NULL,
			bids_id CHAR(256),
			PRIMARY KEY(item_id, bids_id),
			FOREIGN KEY(bids_id) REFERENCES bids(bids_id),
			FOREIGN KEY(item_id) REFERENCES item(item_id));
```
