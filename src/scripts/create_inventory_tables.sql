-- Create the library inventory tables
-- DROP TABLE IF EXISTS LibraryCheckouts;
-- DROP TABLE IF EXISTS BibNumBarCodes;
-- DROP TABLE IF EXISTS BibNumSubjects;
-- DROP TABLE IF EXISTS BibNumISBNs;
-- DROP TABLE IF EXISTS LibraryInventory;

-- backfill
-- ALTER TABLE Authors MODIFY COLUMN authorName varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;
-- ALTER TABLE Publishers MODIFY COLUMN publisherName varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE NOT NULL;
-- ALTER TABLE Subjects MODIFY COLUMN subjectName varchar(255) NOT NULL UNIQUE;
-- ALTER TABLE LibraryInventory MODIFY COLUMN itemCount MEDIUMINT UNSIGNED NOT NULL DEFAULT 0;
-- ALTER TABLE Books MODIFY COLUMN title varchar(1250) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;

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

CREATE INDEX idx3_call_number ON BibNumBarCodes(callNumber);
