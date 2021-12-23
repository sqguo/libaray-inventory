-- 10304 [1]       - 1
-- 16923 [2, 3]     - 2
-- 11428 [4, 5]      - 3
-- 15989 [6, 10]      - 4
-- 13869 [11, 20]      - 5
-- 13433 [21, 50]      - 6
-- 12178 [51, INF]     - 7

WITH 
CheckoutFrequency AS (SELECT bibNum, COUNT(*) AS frequency FROM BibNumBarCodes LEFT JOIN LibraryCheckouts USING(ItemBarcode) WHERE checkoutDate > DATE('2015-01-01') AND checkoutDate < DATE('2018-01-01') GROUP BY bibNum),
pairs AS (SELECT * FROM CheckoutFrequency INNER JOIN BibNumRatingSummary USING(bibNum)),

data1_1 AS (SELECT count(*) AS data1_1 FROM pairs WHERE frequency <= 1 AND bibNumRating <= 2), 
data1_2 AS (SELECT count(*) AS data1_2 FROM pairs WHERE frequency <= 1 AND bibNumRating > 2 AND bibNumRating <= 3), 
data1_3 AS (SELECT count(*) AS data1_3 FROM pairs WHERE frequency <= 1 AND bibNumRating > 3 AND bibNumRating <= 4), 
data1_4 AS (SELECT count(*) AS data1_4 FROM pairs WHERE frequency <= 1 AND bibNumRating > 4 AND bibNumRating <= 5), 

data2_1 AS (SELECT count(*) AS data2_1 FROM pairs WHERE frequency >= 2 AND frequency <= 3 AND bibNumRating <= 2), 
data2_2 AS (SELECT count(*) AS data2_2 FROM pairs WHERE frequency >= 2 AND frequency <= 3 AND bibNumRating > 2 AND bibNumRating <= 3), 
data2_3 AS (SELECT count(*) AS data2_3 FROM pairs WHERE frequency >= 2 AND frequency <= 3 AND bibNumRating > 3 AND bibNumRating <= 4), 
data2_4 AS (SELECT count(*) AS data2_4 FROM pairs WHERE frequency >= 2 AND frequency <= 3 AND bibNumRating > 4 AND bibNumRating <= 5), 

data3_1 AS (SELECT count(*) AS data3_1 FROM pairs WHERE frequency >= 4 AND frequency <= 5 AND bibNumRating <= 2), 
data3_2 AS (SELECT count(*) AS data3_2 FROM pairs WHERE frequency >= 4 AND frequency <= 5 AND bibNumRating > 2 AND bibNumRating <= 3), 
data3_3 AS (SELECT count(*) AS data3_3 FROM pairs WHERE frequency >= 4 AND frequency <= 5 AND bibNumRating > 3 AND bibNumRating <= 4), 
data3_4 AS (SELECT count(*) AS data3_4 FROM pairs WHERE frequency >= 4 AND frequency <= 5 AND bibNumRating > 4 AND bibNumRating <= 5), 

data4_1 AS (SELECT count(*) AS data4_1 FROM pairs WHERE frequency >= 6 AND frequency <= 10 AND bibNumRating <= 2), 
data4_2 AS (SELECT count(*) AS data4_2 FROM pairs WHERE frequency >= 6 AND frequency <= 10 AND bibNumRating > 2 AND bibNumRating <= 3), 
data4_3 AS (SELECT count(*) AS data4_3 FROM pairs WHERE frequency >= 6 AND frequency <= 10 AND bibNumRating > 3 AND bibNumRating <= 4), 
data4_4 AS (SELECT count(*) AS data4_4 FROM pairs WHERE frequency >= 6 AND frequency <= 10 AND bibNumRating > 4 AND bibNumRating <= 5), 

data5_1 AS (SELECT count(*) AS data5_1 FROM pairs WHERE frequency >= 11 AND frequency <= 20 AND bibNumRating <= 2), 
data5_2 AS (SELECT count(*) AS data5_2 FROM pairs WHERE frequency >= 11 AND frequency <= 20 AND bibNumRating > 2 AND bibNumRating <= 3), 
data5_3 AS (SELECT count(*) AS data5_3 FROM pairs WHERE frequency >= 11 AND frequency <= 20 AND bibNumRating > 3 AND bibNumRating <= 4), 
data5_4 AS (SELECT count(*) AS data5_4 FROM pairs WHERE frequency >= 11 AND frequency <= 20 AND bibNumRating > 4 AND bibNumRating <= 5), 

data6_1 AS (SELECT count(*) AS data6_1 FROM pairs WHERE frequency >= 21 AND frequency <= 50 AND bibNumRating <= 2), 
data6_2 AS (SELECT count(*) AS data6_2 FROM pairs WHERE frequency >= 21 AND frequency <= 50 AND bibNumRating > 2 AND bibNumRating <= 3), 
data6_3 AS (SELECT count(*) AS data6_3 FROM pairs WHERE frequency >= 21 AND frequency <= 50 AND bibNumRating > 3 AND bibNumRating <= 4), 
data6_4 AS (SELECT count(*) AS data6_4 FROM pairs WHERE frequency >= 21 AND frequency <= 50 AND bibNumRating > 4 AND bibNumRating <= 5), 

data7_1 AS (SELECT count(*) AS data7_1 FROM pairs WHERE frequency >= 51 AND bibNumRating <= 2), 
data7_2 AS (SELECT count(*) AS data7_2 FROM pairs WHERE frequency >= 51 AND bibNumRating > 2 AND bibNumRating <= 3), 
data7_3 AS (SELECT count(*) AS data7_3 FROM pairs WHERE frequency >= 51 AND bibNumRating > 3 AND bibNumRating <= 4), 
data7_4 AS (SELECT count(*) AS data7_4 FROM pairs WHERE frequency >= 51 AND bibNumRating > 4 AND bibNumRating <= 5)

SELECT * FROM data1_1 JOIN data1_2 JOIN data1_3 JOIN data1_4 
JOIN data2_1 JOIN data2_2 JOIN data2_3 JOIN data2_4 
JOIN data3_1 JOIN data3_2 JOIN data3_3 JOIN data3_4 
JOIN data4_1 JOIN data4_2 JOIN data4_3 JOIN data4_4  
JOIN data5_1 JOIN data5_2 JOIN data5_3 JOIN data5_4  
JOIN data6_1 JOIN data6_2 JOIN data6_3 JOIN data6_4 
JOIN data7_1 JOIN data7_2 JOIN data7_3 JOIN data7_4;