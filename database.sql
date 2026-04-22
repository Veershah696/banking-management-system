-- Create Database
CREATE DATABASE bank_db;
USE bank_db;

-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO users (username, password) VALUES
('admin', '1234'),
('rahul', '1111'),
('priya', '2222'),
('amit', '3333'),
('neha', '4444'),
('rohit', '5555');

-- ACCOUNTS TABLE
CREATE TABLE accounts (
    acc_no BIGINT PRIMARY KEY,
    name VARCHAR(100),
    balance DOUBLE
);

INSERT INTO accounts VALUES
(1234567890, 'Veer Shah', 50000),
(9876543210, 'Rahul Sharma', 75000),
(8765432109, 'Priya Mehta', 62000),
(7654321098, 'Amit Patel', 88000),
(6543210987, 'Neha Verma', 43000),
(5432109876, 'Rohit Singh', 99000);
