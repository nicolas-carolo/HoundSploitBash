CREATE DATABASE IF NOT EXISTS HOUNDSPLOIT CHARACTER SET utf32;
CREATE USER IF NOT EXISTS 'hound-user'@'localhost' IDENTIFIED BY 'Hound-password9';
GRANT ALTER, CREATE, DELETE, INSERT, REFERENCES, SELECT, UPDATE ON `HOUNDSPLOIT`.* TO 'hound-user'@'localhost';
