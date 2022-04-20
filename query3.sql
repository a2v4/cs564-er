--Find the number of auctions belonging to exactly four categories
SELECT COUNT(*) FROM (SELECT * FROM item i, category_item c WHERE i.item_id = c.item_id 
GROUP BY c.category_id HAVING COUNT(*) = 4);
