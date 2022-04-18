#Find the number of users from New York
SELECT COUNT(*) FROM user, location WHERE location.location = "New York" and user.location_id = location.location_id;
