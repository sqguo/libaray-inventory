import mysql.connector
from utility_common import dictDBReader, log_warning, santitize_isbn13, log_error, csvDBReader, santitize_author_name, santitize_ratings, santitize_year, santitize_month, santitize_day
from utility_db import close_db, connect_db, load_data, load_script
import signal
import sys

# environment constants
INVENTORY_FILE_PATH = ['./data/book1-100k.csv',
                       './data/book100k-200k.csv',
                       './data/book200k-300k.csv',
                       './data/book300k-400k.csv',
                       './data/book400k-500k.csv',
                       './data/book500k-600k.csv',
                       './data/book600k-700k.csv',
                       './data/book700k-800k.csv',
                       './data/book800k-900k.csv',
                       './data/book900k-1000k.csv',
                       './data/book1000k-1100k.csv',
                       './data/book1100k-1200k.csv',
                       './data/book1200k-1300k.csv',
                       './data/book1300k-1400k.csv',
                       './data/book1400k-1500k.csv',
                       './data/book1500k-1600k.csv',
                       './data/book1600k-1700k.csv',
                       './data/book1700k-1800k.csv',
                       './data/book1800k-1900k.csv',
                       './data/book1900k-2000k.csv',
                       './data/book2000k-3000k.csv',
                       './data/book3000k-4000k.csv',
                       './data/book4000k-5000k.csv',]
BOOKS_SQL_SCRIPT_PATH = './scripts/create_books_tables.sql'

COLUMN_NAME = 'name'
COLUMN_ISBN = 'isbn'
COLUMN_AUTHOR = 'authors'
COLUMN_PUBLISHER = 'publisher'
COLUMN_PUBLISH_YEAR = 'publishyear'
COLUMN_PUBLISH_MONTH = 'publishmonth'
COLUMN_PUBLISH_DAY = 'publishday'
COLUMN_PAGENUM = 'pagesnumber'
COLUMN_LANGUAGE = 'language'
COLUMN_RATING_DIST1 = 'ratingdist1'
COLUMN_RATING_DIST2 = 'ratingdist2'
COLUMN_RATING_DIST3 = 'ratingdist3'
COLUMN_RATING_DIST4 = 'ratingdist4'
COLUMN_RATING_DIST5 = 'ratingdist5'
COLUMN_REVIEWCOUNT = 'countsofreview'

MIN_SQL_OPERATION_ROW_INDEX = 0
SPACING_SQL_OPERATION = 1000



# initialization
connect_db()

# create the tables
load_script(BOOKS_SQL_SCRIPT_PATH)
print("...created books tables")


row_counter = 0
completed_rows = 0

all_authors = dict()
all_publishers = dict()
all_languages = set()
all_isbns = set()

num_authors = 0
num_publishers = 0

rows_languages = []
rows_authors = []
rows_publishers = []
rows_isbn = []
rows_review = []
rows_books = []


def signal_handler(sig, frame):
    print("ROWS PARSED: ", row_counter)
    print("ROWS COMPLETED: ", completed_rows)
    print('...exiting gracefully')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def special_column_const_swap(current_file):
    global COLUMN_PUBLISH_MONTH
    global COLUMN_PUBLISH_DAY
    if current_file == INVENTORY_FILE_PATH[0]:
        COLUMN_PUBLISH_MONTH = 'publishday'
        COLUMN_PUBLISH_DAY = 'publishmonth'
    elif current_file == INVENTORY_FILE_PATH[18]:
        COLUMN_PUBLISH_MONTH = 'publishmonth'
        COLUMN_PUBLISH_DAY = 'publishday'
    return

def get_author_id(author_column):
    global num_authors
    global rows_authors
    global all_authors
    author_name = santitize_author_name(author_column)
    author_name_key = author_name.lower()
    authorID = all_authors.get(author_name_key)
    if authorID == None:
        num_authors+=1
        all_authors[author_name_key] = num_authors
        authorID = num_authors
        rows_authors.append((authorID, author_name))
    return authorID

def get_publisher_id(publisher_column):
    global num_publishers
    global rows_publishers
    global all_publishers
    publisher_name = publisher_column
    publisher_name_key = publisher_name.lower()
    publisherID = all_publishers.get(publisher_name_key)
    if publisherID == None:
        num_publishers+=1
        all_publishers[publisher_name_key] = num_publishers
        publisherID = num_publishers
        rows_publishers.append((publisherID, publisher_name))
    return publisherID

def handle_isbn(isbn_column, bookId):
    isbn13 = santitize_isbn13(isbn_column)
    if isbn13 in all_isbns:
        return False
    if isbn13:
        rows_isbn.append((isbn13, bookId))
        all_isbns.add(isbn13)
    else:
        log_error("INVALID ISBN: "+str(row_counter))
    return True

def get_language_code(language_column):
    global all_languages
    global rows_languages
    language_key = language_column.upper()
    if language_key not in all_languages:
        all_languages.add(language_key)
        rows_languages.append((language_key,))
    return language_key


sql_language = ("INSERT INTO Languages (languageCode) VALUES (%s)")
sql_author = ("INSERT INTO Authors (authorID, authorName) VALUES (%s, %s)")
sql_publisher = ("INSERT INTO Publishers (publisherID, publisherName) VALUES (%s, %s)")
sql_books = ("INSERT INTO Books (bookID, title, authorID, publisherID, publicationYear, publicationMonth, publicationDay, numPages, languageCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
sql_isbn = ("INSERT INTO BooksISBN (ISBN13, bookID) VALUES (%s, %s)")
sql_reviews = ("INSERT INTO BooksRatings (bookID, ratingDist1, ratingDist2, ratingDist3, ratingDist4, ratingDist5, countsOfTextReview) VALUES (%s, %s, %s, %s, %s, %s, %s)")

def flush(force=False):
    global rows_languages
    global rows_authors
    global rows_publishers
    global rows_isbn
    global rows_review
    global rows_books
    global completed_rows
    if not force and row_counter % SPACING_SQL_OPERATION != 0:
        return
    # if row_counter == MIN_SQL_OPERATION_ROW_INDEX:
    #     print("amending....")
    #     s1 = load_data(sql_language, rows_languages, "LANG_"+str(row_counter))
    #     s2 = load_data(sql_author, rows_authors, "AUTH_"+str(row_counter))
    #     s3 = load_data(sql_publisher, rows_publishers, "PUBL_"+str(row_counter))
    #     s4 = load_data(sql_books, rows_books, "BOOK_"+str(row_counter))
    #     s5 = load_data(sql_isbn, rows_isbn, "ISBN_"+str(row_counter))
    #     s6 = load_data(sql_reviews, rows_review, "REVI_"+str(row_counter))
    #     print("....finished")
    #     if not s6:
    #         log_warning("WARNING_STOPPED_AT_"+str(row_counter))
    #         sys.exit(0)
    if row_counter > MIN_SQL_OPERATION_ROW_INDEX:
        s1 = load_data(sql_language, rows_languages, "LANG_"+str(row_counter), defer_commit=True)
        s2 = load_data(sql_author, rows_authors, "AUTH_"+str(row_counter), defer_commit=True)
        s3 = load_data(sql_publisher, rows_publishers, "PUBL_"+str(row_counter), defer_commit=True)
        s4 = load_data(sql_books, rows_books, "BOOK_"+str(row_counter), defer_commit=True)
        s5 = load_data(sql_isbn, rows_isbn, "ISBN_"+str(row_counter), defer_commit=True)
        s6 = load_data(sql_reviews, rows_review, "REVI_"+str(row_counter))
        if not s1 or not s2 or not s3 or not s4 or not s5 or not s6:
            log_warning("WARNING_STOPPED_AT_"+str(row_counter))
            sys.exit(0)
    rows_languages = []
    rows_authors = []
    rows_publishers = []
    rows_isbn = []
    rows_review = []
    rows_books = []
    completed_rows = row_counter
    if (completed_rows % 50000 == 0):
        print("~~ loader heartbeat ~~~")

    



for csvfile in INVENTORY_FILE_PATH:
    special_column_const_swap(csvfile)
    with open(csvfile, newline='', encoding='utf-8') as book_file:
        csvreader = dictDBReader(book_file)
        for row in csvreader:
            row_counter+=1
            bookId = row_counter
            authorID = None
            publisherID = None
            isbn = None
            review_count = 0
            language_code = None
            do_insert = True
            if row[COLUMN_NAME] == None:
                log_error("MISSING TITLE: "+str(row_counter))
                do_insert = False
            if row[COLUMN_AUTHOR]:
                authorID = get_author_id(row[COLUMN_AUTHOR])
            if row[COLUMN_PUBLISHER]:
                publisherID = get_publisher_id(row[COLUMN_PUBLISHER])
            if row[COLUMN_LANGUAGE]:
                language_code = get_language_code(row[COLUMN_LANGUAGE])
            if row[COLUMN_ISBN]:
                notdupISBN = handle_isbn(row[COLUMN_ISBN], bookId=row_counter)
                if not notdupISBN:
                    do_insert = False
            if row[COLUMN_REVIEWCOUNT]:
                review_count = row[COLUMN_REVIEWCOUNT]
            rating1 = santitize_ratings(row[COLUMN_RATING_DIST1])
            rating2 = santitize_ratings(row[COLUMN_RATING_DIST2])
            rating3 = santitize_ratings(row[COLUMN_RATING_DIST3])
            rating4 = santitize_ratings(row[COLUMN_RATING_DIST4])
            rating5 = santitize_ratings(row[COLUMN_RATING_DIST5])
            if do_insert:
                rows_books.append((
                    row_counter, 
                    row[COLUMN_NAME], 
                    authorID, 
                    publisherID, 
                    santitize_year(row[COLUMN_PUBLISH_YEAR]), 
                    santitize_month(row[COLUMN_PUBLISH_MONTH]), 
                    santitize_day(row[COLUMN_PUBLISH_DAY]), 
                    row[COLUMN_PAGENUM], 
                    language_code
                ))
                rows_review.append((
                    row_counter, 
                    rating1,
                    rating2,
                    rating3,
                    rating4,
                    rating5,
                    review_count
                ))
            flush()
            # end of for each record
    # end of for each file
flush(force=True)


# cleanup
close_db()
print("...done")