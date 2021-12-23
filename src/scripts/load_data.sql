tee final-project-outfile.txt;

-- DROP VIEW IF EXISTS RecentLibraryCheckouts;
-- DROP TABLE IF EXISTS LibraryCheckouts;
-- DROP TABLE IF EXISTS BibNumBarCodes;
-- DROP TABLE IF EXISTS BibNumSubjects;
-- DROP TABLE IF EXISTS BibNumISBNs;
-- DROP TABLE IF EXISTS LibraryInventory;

-- DROP TABLE IF EXISTS BooksUserRatings;
-- DROP VIEW IF EXISTS BooksRatingsSummary;

-- DROP TABLE IF EXISTS BooksRatings;
-- DROP TABLE IF EXISTS BooksSubjects;
-- DROP TABLE IF EXISTS Books;
-- DROP TABLE IF EXISTS Authors;
-- DROP TABLE IF EXISTS Publishers;
-- DROP TABLE IF EXISTS Subjects;
-- DROP TABLE IF EXISTS Languages;

-- DROP TABLE IF EXISTS ItemTypes;
-- DROP TABLE IF EXISTS ItemCollections;
-- DROP TABLE IF EXISTS ItemLocations;
-- DROP TABLE IF EXISTS CodeDictionary;
-- DROP TABLE IF EXISTS CodeTypes;
-- DROP TABLE IF EXISTS FormatGroups;
-- DROP TABLE IF EXISTS FormatSubGroups;
-- DROP TABLE IF EXISTS CategoryGroups;
-- DROP TABLE IF EXISTS CategorySubGroups;

-- SELECT '----------- DROPPED TABLES' as '';




CREATE TABLE IF NOT EXISTS FormatGroups (
    formatName char(16),
    PRIMARY KEY (formatName)
);

CREATE TABLE IF NOT EXISTS FormatSubGroups (
    subFormatName char(16),
    PRIMARY KEY (subFormatName)
);

CREATE TABLE IF NOT EXISTS CategoryGroups (
    categoryName char(16),
    PRIMARY KEY (categoryName)
);

CREATE TABLE IF NOT EXISTS CategorySubGroups (
    subCategoryName char(16),
    PRIMARY KEY (subCategoryName)
);

CREATE TABLE IF NOT EXISTS CodeDictionary (
    code char(7),
    description varchar(120),
    PRIMARY KEY (code)
);

CREATE TABLE IF NOT EXISTS ItemTypes (
    itemTypeCode char(7),
    formatName char(16),
    subFormatName char(16),
    isReference boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (itemTypeCode),
    FOREIGN KEY (itemTypeCode) REFERENCES CodeDictionary(code),
    FOREIGN KEY (formatName) REFERENCES FormatGroups(formatName),
    FOREIGN KEY (subFormatName) REFERENCES FormatSubGroups(subFormatName)
);

CREATE TABLE IF NOT EXISTS ItemCollections (
    itemCollectionsCode char(7),
    formatName char(16),
    subFormatName char(16),
    categoryName char(16),
    subCategoryName char(16),
    PRIMARY KEY (itemCollectionsCode),
    FOREIGN KEY (itemCollectionsCode) REFERENCES CodeDictionary(code),
    FOREIGN KEY (formatName) REFERENCES FormatGroups(formatName),
    FOREIGN KEY (subFormatName) REFERENCES FormatSubGroups(subFormatName),
    FOREIGN KEY (categoryName) REFERENCES CategoryGroups(categoryName),
    FOREIGN KEY (subCategoryName) REFERENCES CategorySubGroups(subCategoryName)
);

CREATE TABLE IF NOT EXISTS ItemLocations (
    itemLocationCode char(7),
    PRIMARY KEY (itemLocationCode),
    FOREIGN KEY (itemLocationCode) REFERENCES CodeDictionary(code)
);

SELECT '----------- CREATED ILS TABLES' as '';


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
    ISBN13 decimal(13) ZEROFILL,
    title varchar(1250) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    authorID MEDIUMINT UNSIGNED,
    publisherID MEDIUMINT UNSIGNED,
    publicationYear decimal(4),
    publicationMonth decimal(2),
    publicationDay decimal(2),
    numPages MEDIUMINT UNSIGNED,
    languageCode char(13),
    PRIMARY KEY (ISBN13),
    FOREIGN KEY (authorID) REFERENCES Authors(authorID),
    FOREIGN KEY (publisherID) REFERENCES Publishers(publisherID),
    FOREIGN KEY (languageCode) REFERENCES Languages(languageCode),
    CHECK(ISBN13 >= 0),
    CHECK(publicationYear >= 0 AND publicationYear <= 9999),
    CHECK(publicationMonth > 0 AND publicationMonth <= 12),
    CHECK(publicationDay > 0 AND publicationDay <= 31)
);

CREATE TABLE IF NOT EXISTS BooksRatings (
    ISBN13 decimal(13) ZEROFILL,
    ratingDist1 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist2 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist3 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist4 INT UNSIGNED NOT NULL DEFAULT 0,
    ratingDist5 INT UNSIGNED NOT NULL DEFAULT 0,
    countsOfTextReview INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (ISBN13),
    FOREIGN KEY (ISBN13) REFERENCES Books(ISBN13)
);

CREATE TABLE IF NOT EXISTS BooksUserRatings (
    ISBN13 decimal(13) ZEROFILL,
    userID decimal(6),
    rating TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (ISBN13, userID),
    FOREIGN KEY (ISBN13) REFERENCES Books(ISBN13),
    CHECK(rating >= 1 AND rating <= 5),
    CHECK(userID >= 1)
);

CREATE OR REPLACE VIEW BooksRatingsSummary AS
    SELECT 
        ISBN13, 
        ROUND(CAST((ratingDist1*1 + ratingDist2*2 + ratingDist3*3 + ratingDist4*4 + ratingDist5*5) AS float) / CAST((ratingDist1 + ratingDist2 + ratingDist3 + ratingDist4 + ratingDist5) AS float), 2) AS averageRating,
        (ratingDist1 + ratingDist2 + ratingDist3 + ratingDist4 + ratingDist5) AS numRatings,
        countsOfTextReview
    FROM BooksRatings;

SELECT '----------- CREATED BOOKS TABLES' as '';

CREATE TABLE IF NOT EXISTS LibraryInventory (
    bibNum decimal(7),
    itemType char(7) NOT NULL,
    itemCollection char(7) NOT NULL,
    floatingItem boolean NOT NULL DEFAULT 0,
    itemLocation char(7) NOT NULL,
    reportDate DATE NOT NULL,
    itemCount MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (bibNum),
    FOREIGN KEY (itemType) REFERENCES ItemTypes(itemTypeCode),
    FOREIGN KEY (itemCollection) REFERENCES ItemCollections(itemCollectionsCode),
    FOREIGN KEY (itemLocation) REFERENCES ItemLocations(itemLocationCode),
    CHECK(bibNum >= 0)
);

CREATE TABLE IF NOT EXISTS BibNumISBNs (
    ISBN13 decimal(13) ZEROFILL,
    bibNum decimal(7) NOT NULL,
    PRIMARY KEY (ISBN13, bibNum),
    FOREIGN KEY (bibNum) REFERENCES LibraryInventory(bibNum),
    CHECK(ISBN13 >= 0)
);

CREATE TABLE IF NOT EXISTS BibNumSubjects (
    subjectID MEDIUMINT UNSIGNED,
    bibNum decimal(7),
    PRIMARY KEY (bibNum, subjectID),
    FOREIGN KEY (subjectID) REFERENCES Subjects(subjectID),
    FOREIGN KEY (bibNum) REFERENCES LibraryInventory(bibNum)
);

CREATE TABLE IF NOT EXISTS BibNumBarCodes (
    ItemBarcode decimal(13) ZEROFILL,
    bibNum decimal(7),
    callNumber varchar(60),
    PRIMARY KEY (ItemBarcode),
    FOREIGN KEY (bibNum) REFERENCES LibraryInventory(bibNum),
    CHECK(ItemBarcode >= 0)
);

CREATE TABLE IF NOT EXISTS LibraryCheckouts (
    ItemBarcode decimal(13),
    checkoutDate dateTime,
    PRIMARY KEY (ItemBarcode, checkoutDate),
    FOREIGN KEY (ItemBarcode) REFERENCES BibNumBarCodes(ItemBarcode)
);

CREATE OR REPLACE VIEW RecentLibraryCheckouts AS 
    SELECT ItemBarcode, MAX(checkoutDate) AS mostRecentCheckoutDate
    FROM LibraryCheckouts GROUP BY ItemBarcode;

CREATE OR REPLACE VIEW BibNumRatingSummary AS 
    SELECT bibNum, 
        SUM(averageRating*numRatings)/SUM(numRatings) AS bibNumRating 
    FROM BibNumISBNs LEFT JOIN BooksRatingsSummary USING(ISBN13) 
    WHERE averageRating IS NOT NULL AND numRatings > 0
    GROUP BY bibNum;

-- CREATE INDEX idx1_books_title ON Books(title);
CREATE INDEX idx2_books_publicationDate ON Books(publicationYear, publicationMonth, publicationDay);
CREATE INDEX idx3_call_number ON BibNumBarCodes(callNumber);

SELECT '----------- LOADING FormatGroups' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_FormatGroups.csv' IGNORE INTO TABLE FormatGroups FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING FormatSubGroups' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_FormatSubGroups.csv' IGNORE INTO TABLE FormatSubGroups FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING CategoryGroups' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_CategoryGroups.csv' IGNORE INTO TABLE CategoryGroups FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING CategorySubGroups' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_CategorySubGroups.csv' IGNORE INTO TABLE CategorySubGroups FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING CodeDictionary' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_CodeDictionary.csv' IGNORE INTO TABLE CodeDictionary FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING ItemTypes' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_ItemTypes.csv' IGNORE INTO TABLE ItemTypes FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING ItemCollections' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_ItemCollections.csv' IGNORE INTO TABLE ItemCollections FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING ItemLocations' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_ItemLocations.csv' IGNORE INTO TABLE ItemLocations FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING Authors' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/Authors.csv' IGNORE INTO TABLE Authors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING Publishers' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_Publishers.csv' IGNORE INTO TABLE Publishers FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING Subjects' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_Subjects.csv' IGNORE INTO TABLE Subjects FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING Languages' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_Languages.csv' IGNORE INTO TABLE Languages FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING Books' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_Books.csv' IGNORE INTO TABLE Books FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING BooksRatings' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_BooksRatings.csv' IGNORE INTO TABLE BooksRatings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING BooksUserRatings' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_BooksUserRatings.csv' IGNORE INTO TABLE BooksUserRatings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING LibraryInventory' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_LibraryInventory.csv' IGNORE INTO TABLE LibraryInventory FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING BibNumISBNs' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_BibNumISBNs.csv' IGNORE INTO TABLE BibNumISBNs FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING BibNumSubjects' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_BibNumSubjects.csv' IGNORE INTO TABLE BibNumSubjects FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING BibNumBarCodes' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_BibNumBarCodes.csv' IGNORE INTO TABLE BibNumBarCodes FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- LOADING LibraryCheckouts' as '';
LOAD DATA INFILE '/var/lib/mysql-files/Group57/ece356_sqguo_LibraryCheckouts.csv' IGNORE INTO TABLE LibraryCheckouts FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT '----------- ALL DONE' as '';
