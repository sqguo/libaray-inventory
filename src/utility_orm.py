import constants
from utility_db import fetch_data_dictionary, insert_data, insert_data_many

# constructs a single sql query to find recommanded books
def make_recommandation(userID):
    # 5400,
    algorithm = " WITH mylikedISBNs AS (SELECT ISBN13 FROM BooksUserRatings WHERE userID = {} AND rating >= 4), "
    algorithm = algorithm + "mylikedISBNsDups AS (SELECT ISBN13 FROM Books WHERE LOWER(title) IN (SELECT LOWER(title) FROM mylikedISBNs LEFT JOIN Books USING(ISBN13))), "
    algorithm = algorithm + "mydislikedISBNs AS (SELECT ISBN13 FROM BooksUserRatings WHERE userID = {} AND rating <= 3),"
    algorithm = algorithm + "mydislikedISBNsDups AS (SELECT ISBN13 FROM Books WHERE LOWER(title) IN (SELECT LOWER(title) FROM mydislikedISBNs LEFT JOIN Books USING(ISBN13))), "
    algorithm = algorithm + "otherUsersWhoLikedmy AS (SELECT userID, COUNT(*) AS userSimilarity FROM mylikedISBNsDups LEFT JOIN BooksUserRatings USING(ISBN13) WHERE userID != {} AND rating >=4 GROUP BY userID), "
    algorithm = algorithm + "topOtherUsersWhoLikedmy AS (SELECT * FROM otherUsersWhoLikedmy ORDER BY userSimilarity DESC LIMIT 20),"
    algorithm = algorithm + "similarISBNs AS (SELECT ISBN13, (SUM(userSimilarity)) AS overlapscore FROM topOtherUsersWhoLikedmy LEFT JOIN BooksUserRatings USING(userID) WHERE rating >=4 and ISBN13 NOT IN (SELECT * FROM mylikedISBNsDups) and ISBN13 NOT IN (SELECT * FROM mydislikedISBNsDups) GROUP BY ISBN13), "
    algorithm = algorithm + "ISBNsToRecommand AS (SELECT MIN(ISBN13) AS defISBN13, LOWER(title), MAX(overlapscore) as aggScore FROM similarISBNs LEFT JOIN Books USING(ISBN13) GROUP BY LOWER(title)), "
    algorithm = algorithm + "ISBNsUniqueReomand AS (SELECT defISBN13 AS ISBN13, aggScore FROM ISBNsToRecommand ORDER BY aggScore DESC LIMIT 20) "
    algorithm = algorithm + "SELECT * FROM ISBNsUniqueReomand LEFT JOIN Books USING (ISBN13) LEFT JOIN Authors USING(authorID) LEFT JOIN Publishers USING(publisherID) LEFT JOIN BooksRatingsSummary USING(ISBN13)"
    rows = fetch_data_dictionary(algorithm.format(userID, userID, userID))
    return list(rows)

# select books based on [none, multiple] conditions
def do_select_books(selection=[], conditions=[], conditions_specials=[]):
    book_cluster_sqls = dict()
    for table in constants.BOOKS_CLUSTER_DESIGN:
        book_cluster_sqls[table] = selector_single_table(table, conditions=conditions, conditions_specials=conditions_specials)
    book_cluster_filtered_sqls = dict()
    for table, sql in book_cluster_sqls.items():
        if not sql == None:
            book_cluster_filtered_sqls[table] = sql
    # create the with clause mapping and assign unique identifiers
    with_clause, with_clause_name_mapping = make_common_expression(book_cluster_filtered_sqls)
    no_book_cluster = len(book_cluster_filtered_sqls) == 0
    book_cluster_name_mapping = dict()
    for table in constants.BOOKS_CLUSTER_DESIGN:
        if with_clause_name_mapping.get(table):
            book_cluster_name_mapping[table] = with_clause_name_mapping[table]
        else:
            book_cluster_name_mapping[table] = table
    # create join expression depending on whether the idenfier is used in the with clause
    join_statement = make_inner_join_expression(book_cluster_name_mapping)
    final_statement = " ".join([with_clause, join_statement, "LIMIT 10"])
    rows = fetch_data_dictionary(final_statement)
    return list(rows)

def do_select_user_ratings(userid):
    sql_statement1 = "WITH myratings AS (SELECT * FROM BooksUserRatings WHERE userID = {})".format(userid)
    sql_statement2 = "SELECT ISBN13, title, rating FROM myratings LEFT JOIN Books USING(ISBN13) LIMIT 10"
    final_statement = " ".join([sql_statement1, sql_statement2])
    rows = fetch_data_dictionary(final_statement)
    return list(rows)

def do_select_user_ratings_good(userid):
    sql_statement1 = "WITH myratings AS (SELECT * FROM BooksUserRatings WHERE userID = {} and rating >= 4)".format(userid)
    sql_statement2 = "SELECT ISBN13, title, rating FROM myratings LEFT JOIN Books USING(ISBN13) LIMIT 10"
    final_statement = " ".join([sql_statement1, sql_statement2])
    rows = fetch_data_dictionary(final_statement)
    return list(rows)

def do_insert_user_rating(userid, isbn13, rating):
    sql_statement = "INSERT INTO BooksUserRatings (ISBN13, userID, rating) VALUES ({}, {}, {}) ON DUPLICATE KEY UPDATE rating = VALUES(rating)"
    final_statement = sql_statement.format(isbn13, userid, rating)
    success = insert_data(final_statement)
    return success

def do_insert_book(isbn13, title, authorName, publisherName, numPages, languageCode, publicationYear, publicationMonth, publicationDay):
    sql_statement0 = "SELECT * FROM Books WHERE ISBN13 = {}"
    sql_statement1 = ("INSERT INTO Books (ISBN13, title, authorID, publisherID, publicationYear, publicationMonth, publicationDay, numPages, languageCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    book_rows = fetch_data_dictionary(sql_statement0.format(isbn13))
    if len(list(book_rows)) > 0: return (False, False)
    authorID = None
    publisherID = None
    # ensure the publisher and author exists, if not add them
    if authorName is not None:
        authorID = do_fetch_author_id(authorName)
        if authorID == None: authorID = do_insert_author(authorName)
    if publisherName is not None:
        publisherID = do_fetch_publisher_id(publisherName)
        if publisherID == None: publisherID = do_insert_publisher(publisherName)
    do_insert_language_code(languageCode)
    success = insert_data_many(sql_statement1, [(
        isbn13, 
        title, 
        authorID, 
        publisherID, 
        publicationYear, 
        publicationMonth, 
        publicationDay, 
        numPages, 
        languageCode
    )])
    return (True, success)


def do_fetch_author_id(authorName):
    sql_statement1 = "SELECT * FROM Authors WHERE LOWER(authorName) = LOWER({})"
    author_rows = list(fetch_data_dictionary(sql_statement1.format(make_quotes(authorName))))
    if len(author_rows) > 0: return author_rows[0][constants.COLUMN_AUTHORS_AUTHORID]
    else: return None

def do_insert_author(authorName):
    sql_statement1 = ("INSERT INTO Authors (authorName) VALUES (%s)")
    insert_data_many(sql_statement1, [(authorName,)])
    return do_fetch_author_id(authorName)

def do_fetch_publisher_id(publisherName):
    sql_statement2 = "SELECT * FROM Publishers WHERE LOWER(publisherName) = LOWER({})"
    publisher_rows = list(fetch_data_dictionary(sql_statement2.format(make_quotes(publisherName))))
    if len(publisher_rows) > 0: return publisher_rows[0][constants.COLUMN_PUBLISHERS_PUBLISHERID]
    else: return None

def do_insert_publisher(publisherName):
    sql_statement1 = ("INSERT INTO Publishers (publisherName) VALUES (%s)")
    insert_data_many(sql_statement1, [(publisherName,)])
    return do_fetch_publisher_id(publisherName)

def do_insert_language_code(languageCode):
    sql_statement1 = ("INSERT INTO Languages (languageCode) VALUES (%s) ON DUPLICATE KEY UPDATE languageCode = VALUES(languageCode)")
    return insert_data_many(sql_statement1, [(languageCode.upper(),)])
    

def do_select_inventory(bibnumber):
    sql_statement1 = "WITH my AS (SELECT * FROM LibraryInventory WHERE bibNum = {}) SELECT * FROM my LEFT JOIN CodeDictionary AS ty ON (my.itemLocation = ty.code)"
    inventory_rows = list(fetch_data_dictionary(sql_statement1.format(bibnumber)))
    if len(inventory_rows) == 0:
        return (None, None)
    sql_statement1 = "WITH mybarcodes AS (SELECT * FROM BibNumBarCodes WHERE bibNum = {}) SELECT ItemBarcode, MAX(checkoutDate) AS mostRecentCheckoutDate FROM mybarcodes INNER JOIN LibraryCheckouts USING(ItemBarcode) GROUP BY ItemBarcode"
    barcode_rows = list(fetch_data_dictionary(sql_statement1.format(bibnumber)))
    return (inventory_rows[0], barcode_rows)

def do_select_inventory_with_isbn(isbn13):
    sql_statement1 = "WITH my AS (SELECT * FROM LibraryInventory WHERE bibNum IN (SELECT DISTINCT(bibNum) FROM BibNumISBNs WHERE ISBN13 = {})) SELECT * FROM my LEFT JOIN CodeDictionary AS ty ON (my.itemType = ty.code) LEFT JOIN CodeDictionary AS co ON (my.itemCollection = co.code)"
    return list(fetch_data_dictionary(sql_statement1.format(isbn13)))


def do_select_barcode(barcode):
    sql_statement1 = "SELECT * FROM BibNumBarCodes WHERE ItemBarcode = {} LIMIT 2"
    return list(fetch_data_dictionary(sql_statement1.format(barcode)))

def do_insert_checkout(barcode):
    sql_statement1 = ("INSERT INTO LibraryCheckouts (ItemBarcode, checkoutDate) VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE ItemBarcode = VALUES(ItemBarcode)")
    return insert_data_many(sql_statement1, [(barcode,)])



def selector_single_table(table, selection=[], conditions={}, conditions_specials={}):
    # contructs the select and where clause of a single table
    available_cols = set(constants.DATABASE_DESIGN[table])
    filtered_selections = available_cols.intersection(set(selection))
    filtered_conditions = [cond for cond in conditions if (cond in available_cols)]
    if len(filtered_conditions) == 0:
        return None
    filtered_condition_strings = []
    # create where clause and append
    for filtered_cond in filtered_conditions:
        col_and_cond = (filtered_cond, conditions[filtered_cond])
        where_string = make_where_default(col_and_cond) if conditions_specials.get(filtered_cond) == None else conditions_specials[filtered_cond](col_and_cond)
        filtered_condition_strings.append(where_string)

    return selector_method(table, filtered_selections, filtered_condition_strings)
    

def selector_method(table, selection=[], conditionstings=[]):
    selection_statement = "*"
    if len(selection) > 0:
        selection_statement = ",".join(selection)
    where_statement = ""
    if len(conditionstings) > 0:
        where_statement = "WHERE "
        where_statement = where_statement+" AND ".join(conditionstings)
    return " ".join(["SELECT", selection_statement, "FROM", table, where_statement])


def make_inner_join_expression(name_mappings):
    statement1 = "SELECT * FROM "
    skip_first_row = True
    using_statements = ""
    for table, name in name_mappings.items():
        if skip_first_row:
            using_statements = name
        else:
            if table == name: using_statements = using_statements+" LEFT JOIN "
            else: using_statements = using_statements+" INNER JOIN "
            using_statements = using_statements+" "+" ".join([name, "USING", "(", constants.BOOKS_CLUSTER_FOREIGN_KEY_DESIGN[table], ")"])
        skip_first_row = False
    return statement1+using_statements

def make_common_expression(sqls={}):
    result_seq = []
    name_mapping = dict()
    counter = 0
    for table, sql in sqls.items():
        new_name = table+str(counter)
        name_mapping[table] = new_name
        result_seq.append(" ".join([new_name, "AS", "(", sql, ")"]))
    if len(sqls) > 0:
        return ("WITH "+",\n".join(result_seq), name_mapping)
    return ""

def make_where_greater_float(cond):
    return " ".join([cond[0], ">", str(cond[1])])

def make_where_like_string(cond):
    return " ".join(["LOWER("+cond[0]+")", "LIKE", "\"%"+str(cond[1]).lower()+"%\""])

def make_where_default(cond):
    return " ".join(["LOWER("+cond[0]+")", "=", "\""+str(cond[1]).lower()+"\""])

def make_quotes(text):
    return "\""+str(text)+"\""

