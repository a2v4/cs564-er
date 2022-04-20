--Find the number of users who are both sellers and bidders
SELECT COUNT(DISTINCT s.user_id) FROM user_item s, user_bid b WHERE s.user_id = b.user_id;