DROP TABLE article_attachment_1;
DROP TABLE newspage_article_1;
DROP TABLE comment_1;
DROP TABLE attachment_1;
DROP TABLE article_1;
--DROP TABLE newspage;

CREATE TABLE article_1 ( 
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

CREATE TABLE attachment_1 (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    notes VARCHAR(255),
    align VARCHAR(255),
    image BOOLEAN NOT NULL DEFAULT 0,
    image_height SMALLINT UNSIGNED ZEROFILL,
    image_width SMALLINT UNSIGNED ZEROFILL,
    thumbnail_name VARCHAR(255),
    thumbnail_height SMALLINT UNSIGNED ZEROFILL,
    thumbnail_width SMALLINT UNSIGNED ZEROFILL,
    size INT ZEROFILL,
    created_date DATETIME NOT NULL,
    PRIMARY KEY(id)) ENGINE = INNODB;

CREATE TABLE article_attachment_1 (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    article_id INT UNSIGNED NOT NULL,
    attachment_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(id),
    INDEX(article_id),
    FOREIGN KEY(article_id) REFERENCES article_1(id) 
        ON DELETE CASCADE,
    INDEX(attachment_id),
    FOREIGN KEY(attachment_id) REFERENCES attachment_1(id) 
        ON DELETE CASCADE) 
    ENGINE = INNODB;

CREATE TABLE comment_1 (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    article_id INT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    hide_address BOOLEAN NOT NULL DEFAULT 1,
    created_date DATETIME NOT NULL,
    PRIMARY KEY(id),
    INDEX(article_id),
    FOREIGN KEY(article_id) REFERENCES article_1(id) 
        ON DELETE CASCADE)
    ENGINE = INNODB;

-- This table implemented for a shell only... not yet used
/* CREATE TABLE newspage_1 ( 
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)) ENGINE = INNODB;
*/

-- This table implemented for future functionality.  Note
-- that it is not yet connected to Newspage
CREATE TABLE newspage_article_1 (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    article_id INT UNSIGNED NOT NULL,
    newspage_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id),
    INDEX(article_id),
    FOREIGN KEY(article_id) REFERENCES article_1(id) 
        ON DELETE CASCADE) 
    ENGINE = INNODB;

    