-- Initialize prescription database
-- This file is optional as SQLAlchemy will create the schema

-- Set character set
ALTER DATABASE prescription_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges (redundant with docker-compose setup but ensures permissions)
GRANT ALL PRIVILEGES ON prescription_db.* TO 'prescription_user'@'%';
FLUSH PRIVILEGES;

