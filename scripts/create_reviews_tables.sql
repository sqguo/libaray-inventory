-- DROP TABLE IF EXISTS BooksUserRatings;

CREATE TABLE IF NOT EXISTS BooksUserRatings (
    bookID MEDIUMINT UNSIGNED,
    userID decimal(6),
    rating TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (bookID, userID),
    FOREIGN KEY (bookID) REFERENCES Books(bookID),
    CHECK(rating >= 1 AND rating <= 5),
    CHECK(userID >= 1)
);

-- CREATE OR REPLACE VIEW BooksRatingsSummary AS
--     SELECT 
--         bookID, 
--         ROUND(CAST((ratingDist1*1 + ratingDist2*2 + ratingDist3*3 + ratingDist4*4 + ratingDist5*5) AS float) / CAST((ratingDist1 + ratingDist2 + ratingDist3 + ratingDist4 + ratingDist5) AS float), 2) AS averageRating,
--         (ratingDist1 + ratingDist2 + ratingDist3 + ratingDist4 + ratingDist5) AS numRatings,
--         countsOfTextReview
--     FROM BooksRatings;

-- CREATE OR REPLACE VIEW BooksUserRatingsSummary AS
--     SELECT 
--         userID, 
--         SUM(rating) / count(*) AS averageUserRating,
--         count(*) AS numUserRatings
--     FROM BooksUserRatings
--     GROUP BY userID;
