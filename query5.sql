#Find the number of sellers whose rating is higher than 1000
SELECT COUNT(*) FROM user u, user_item s WHERE u.user_id = s.user_id and u.rating > 1000;