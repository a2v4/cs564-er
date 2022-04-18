#Find the number of categories that include at least one item with a bid of more than 1000
SELECT COUNT(DISTINCT c.category_id) FROM item i, category_item c 
WHERE i.number_of_bids >= 1 AND i.currently > 1000.0 AND i.item_id = c.item_id;