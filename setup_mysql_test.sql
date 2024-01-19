-- Database creation
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
USE hbnb_test_db;

-- User creation
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant privileges
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
