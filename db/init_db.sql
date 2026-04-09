CREATE DATABASE IF NOT EXISTS threat_dashboard;

USE threat_dashboard;

CREATE TABLE IF NOT EXISTS phishing_urls (
    phish_id VARCHAR(100) PRIMARY KEY,
    url TEXT NOT NULL,
    online VARCHAR(20),
    target VARCHAR(100),
    source VARCHAR(50),
    threat_category VARCHAR(100),
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_url (url(255))
);

