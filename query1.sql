#Find the number of users in the database
SELECT COUNT(*) FROM users;

#Find the number of users from New York
SELECT COUNT(*) FROM user, location WHERE location.location = "New York" and user.location_id = location.location_id;

#Find the number of auctions belonging to exactly four categories


#Find the ID(s) of action(s) with the highest current price


#Find the number of sellers whose rating is higher than 1000
SELECT COUNT(*) FROM user u, user_item s WHERE u.user_id = s.user_id and u.rating > 1000;


#Find the number of users who are both sellers and bidders
SELECT COUNT(DISTINCT s.user_id) FROM user_item s, user_bid b WHERE s.user_id = b.user_id;



#Find the number of categories that include at least one item with a bid of more than 1000

