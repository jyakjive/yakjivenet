CREATE TABLE article_${ID} ( 
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    hide_address BOOLEAN NOT NULL DEFAULT 0,
    published BOOLEAN NOT NULL DEFAULT 0,
    expired BOOLEAN NOT NULL DEFAULT 0,
    latitude FLOAT ZEROFILL,
    longitude FLOAT ZEROFILL,
    altitude FLOAT ZEROFILL,
    street VARCHAR(255),
    street2 VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(255),
    country VARCHAR(255),
    phone VARCHAR(255),
    keywords VARCHAR(255),
    category VARCHAR(255),
    source_name VARCHAR(255),
    source_url VARCHAR(255),
    language VARCHAR(255),              -- for future use
    published_date DATETIME NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_date DATETIME NOT NULL,
    modified_by VARCHAR(255),
    modified_date DATETIME,
    PRIMARY KEY(id)) ENGINE = INNODB;