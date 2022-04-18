#Find the ID(s) of action(s) with the highest current price
SELECT user_id FROM bids ORDER BY amount DESC LIMIT 1;