CREATE TABLE newspage_article_${ID} (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    article_id INT UNSIGNED NOT NULL,
    newspage_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id),
    INDEX(article_id),
    FOREIGN KEY(article_id) REFERENCES article_${ID}(id) 
        ON DELETE CASCADE) 
    ENGINE = INNODB;