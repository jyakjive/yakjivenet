CREATE TABLE article_attachment_${ID} (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    article_id INT UNSIGNED NOT NULL,
    attachment_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(id),
    INDEX(article_id),
    FOREIGN KEY(article_id) REFERENCES article_${ID}(id) 
        ON DELETE CASCADE,
    INDEX(attachment_id),
    FOREIGN KEY(attachment_id) REFERENCES attachment_${ID}(id) 
        ON DELETE CASCADE) 
    ENGINE = INNODB;