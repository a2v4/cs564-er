--Find the number of users from New York
SELECT COUNT(*) FROM user u, location l WHERE l.location = "New York" AND u.location_id = l.location_id;
