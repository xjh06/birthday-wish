CREATE TABLE IF NOT EXISTS birthday_info (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    recipient_name VARCHAR(80) NOT NULL,
    birthday_date DATE NOT NULL,
    hero_title VARCHAR(160) NOT NULL,
    blessing_title VARCHAR(160) NOT NULL,
    blessing_text VARCHAR(1000) NOT NULL,
    card_salutation VARCHAR(80) NOT NULL,
    card_message VARCHAR(1000) NOT NULL,
    music_url VARCHAR(1000)
);

CREATE TABLE IF NOT EXISTS birthday_message (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sender_name VARCHAR(30) NOT NULL,
    relationship VARCHAR(30) NOT NULL,
    content VARCHAR(500) NOT NULL,
    like_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    visible BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS message_like (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message_id BIGINT NOT NULL,
    visitor_id VARCHAR(80) NOT NULL,
    created_at DATETIME NOT NULL,
    CONSTRAINT uk_message_visitor UNIQUE (message_id, visitor_id)
);

CREATE TABLE IF NOT EXISTS visit_stat (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    visit_date DATE NOT NULL,
    visit_count INT NOT NULL DEFAULT 1,
    CONSTRAINT uk_visit_date UNIQUE (visit_date)
);
