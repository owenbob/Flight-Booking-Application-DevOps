
CREATE USER admin WITH PASSWORD 'root';
CREATE DATABASE flight_app;
GRANT ALL PRIVILEGES ON DATABASE flight_app TO admin;

CREATE DATABASE flight_app_test;
GRANT ALL PRIVILEGES ON DATABASE flight_app TO admin;