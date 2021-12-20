-- DROP TABLE IF EXISTS BooksISBN;
-- DROP TABLE IF EXISTS BooksRatings;
-- DROP TABLE IF EXISTS BooksSubjects;
-- DROP TABLE IF EXISTS Books;
-- DROP TABLE IF EXISTS Authors;
-- DROP TABLE IF EXISTS Publishers;
-- DROP TABLE IF EXISTS Subjects;
-- DROP TABLE IF EXISTS Languages;

CREATE TABLE IF NOT EXISTS Authors (
    authorID MEDIUMINT UNSIGNED AUTO_INCREMENT,
    authorName varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    birthYear decimal(4),
    PRIMARY KEY (authorID),
    UNIQUE (authorName, birthYear),
    CHECK(birthYear >= 0 AND birthYear <= 9999)
);

CREATE TABLE IF NOT EXISTS Publishers (
    publisherID MEDIUMINT UNSIGNED AUTO_INCREMENT,
    publisherName varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE NOT NULL,
    PRIMARY KEY (publisherID)
);

CREATE TABLE IF NOT EXISTS Subjects (
    subjectID MEDIUMINT UNSIGNED AUTO_INCREMENT,
    subjectName varchar(255) NOT NULL UNIQUE,
    PRIMARY KEY (subjectID)
);

CREATE TABLE IF NOT EXISTS Languages (
    languageCode char(13),
    PRIMARY KEY (languageCode)
);

CREATE TABLE IF NOT EXISTS Books (
    bookID MEDIUMINT UNSIGNED AUTO_INCREMENT,
    title varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    authorID MEDIUMINT UNSIGNED,
    publisherID MEDIUMINT UNSIGNED,
    publicationYear decimal(4),
    publicationMonth decimal(2),
    publicationDay decimal(2),
    numPages MEDIUMINT UNSIGNED,
    languageCode char(13),
    PRIMARY KEY (bookID),
    FOREIGN KEY (authorID) REFERENCES Authors(authorID),
    FOREIGN KEY (publisherID) REFERENCES Publishers(publisherID),
    FOREIGN KEY (languageCode) REFERENCES Languages(languageCode),
    CHECK(publicationYear >= 0 AND publicationYear <= 9999),
    CHECK(publicationMonth > 0 AND publicationMonth <= 12),
    CHECK(publicationDay > 0 AND publicationDay <= 31)
);

CREATE TABLE IF NOT EXISTS BooksISBN (
    ISBN13 decimal(13) ZEROFILL UNIQUE,
    bookID MEDIUMINT UNSIGNED NOT NULL UNIQUE,
    PRIMARY KEY (ISBN13),
    FOREIGN KEY (bookID) REFERENCES Books(bookID),
    CHECK(ISBN13 >= 0)
);

CREATE TABLE IF NOT EXISTS BooksRatings (
    bookID MEDIUMINT UNSIGNED,
    ratingDist1 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist2 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist3 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist4 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist5 INT UNSIGNED NOT NULL DEFAULT 0,
    countsOfTextReview INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (bookID),
    FOREIGN KEY (bookID) REFERENCES Books(bookID)
);

-- Backfill
-- ALTER TABLE BooksISBN ADD UNIQUE(bookID);

