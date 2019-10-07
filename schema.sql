CREATE TABLE IF NOT EXISTS `users` (
    `id` integer AUTO_INCREMENT PRIMARY KEY,
    `email` varchar(255),
    `name` varchar(255),
    `photo` varchar(255),
    `is_host` integer,
    `about` varchar(255),
    `telegram` varchar(255),
    `insta` varchar(255),
    `community` varchar(255));

CREATE TABLE IF NOT EXISTS `communities` (
    `id` int(11) AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `chat_id` BIGINT UNIQUE NOT NULL);
