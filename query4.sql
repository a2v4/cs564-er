#Find the ID(s) of action(s) with the highest current price
SELECT item_id FROM item ORDER BY currently desc LIMIT 1;