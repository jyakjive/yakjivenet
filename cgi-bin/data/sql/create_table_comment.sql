CREATE TABLE comment_${ID} (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    article_id INT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    hide_address BOOLEAN NOT NULL DEFAULT 1,
    created_date DATETIME NOT NULL,
    PRIMARY KEY(id),
    INDEX(article_id),
    FOREIGN KEY(article_id) REFERENCES article_${ID}(id) 
        ON DELETE CASCADE)
    ENGINE = INNODB;