-- Create the ILS tables
-- DROP TABLE IF EXISTS ItemTypes;
-- DROP TABLE IF EXISTS ItemCollections;
-- DROP TABLE IF EXISTS ItemLocations;
-- DROP TABLE IF EXISTS CodeDictionary;
-- DROP TABLE IF EXISTS CodeTypes;
-- DROP TABLE IF EXISTS FormatGroups;
-- DROP TABLE IF EXISTS FormatSubGroups;
-- DROP TABLE IF EXISTS CategoryGroups;
-- DROP TABLE IF EXISTS CategorySubGroups;

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
