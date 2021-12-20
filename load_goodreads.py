import mysql.connector
from utility_common import dictDBReader, log_warning, santitize_isbn13, log_error, csvDBReader, santitize_author_name, santitize_ratings, santitize_year, santitize_month, santitize_day
from utility_db import close_db, connect_db, load_data, load_script
from utility_deduper import dedupe_isbn, dupe_language_code
from utility_mapper import map_author_id, map_publisher_id
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

MIN_SQL_OPERATION_ROW_INDEX = 1098000
SPACING_SQL_OPERATION = 1000



row_counter = 0
completed_rows = 0

rows_languages = []
rows_authors = []
rows_publishers = []

rows_review = []
rows_books = []

def log_current_status():
    print("ROWS PARSED: ", row_counter)
    print("ROWS COMPLETED: ", completed_rows)

def signal_handler(sig, frame):
    log_current_status()
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



sql_language = ("INSERT INTO Languages (languageCode) VALUES (%s)")
sql_author = ("INSERT INTO Authors (authorID, authorName) VALUES (%s, %s)")
sql_publisher = ("INSERT INTO Publishers (publisherID, publisherName) VALUES (%s, %s)")
sql_books = ("INSERT INTO Books (ISBN13, title, authorID, publisherID, publicationYear, publicationMonth, publicationDay, numPages, languageCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
sql_reviews = ("INSERT INTO BooksRatings (ISBN13, ratingDist1, ratingDist2, ratingDist3, ratingDist4, ratingDist5, countsOfTextReview) VALUES (%s, %s, %s, %s, %s, %s, %s)")

def flush(force=False):
    global rows_languages
    global rows_authors
    global rows_publishers
    global rows_review
    global rows_books
    global completed_rows
    if not force and row_counter % SPACING_SQL_OPERATION != 0:
        return
    if row_counter > MIN_SQL_OPERATION_ROW_INDEX:
        print(".", end="", flush=True)
        s1 = load_data(sql_language, rows_languages, "LANG_"+str(row_counter), defer_commit=True)
        s2 = load_data(sql_author, rows_authors, "AUTH_"+str(row_counter), defer_commit=True)
        s3 = load_data(sql_publisher, rows_publishers, "PUBL_"+str(row_counter), defer_commit=True)
        s4 = load_data(sql_books, rows_books, "BOOK_"+str(row_counter), defer_commit=True)
        s5 = load_data(sql_reviews, rows_review, "REVI_"+str(row_counter))
        if not s1 or not s2 or not s3 or not s4 or not s5:
            log_current_status()
            log_warning("WARNING_STOPPED_AT_"+str(row_counter))
            sys.exit(0)
        print(".", end="", flush=True)
    rows_languages = []
    rows_authors = []
    rows_publishers = []
    rows_review = []
    rows_books = []
    completed_rows = row_counter
    if (completed_rows % 10000 == 0):
        print("..ok", end="\r\n", flush=True)
    if (completed_rows % 50000 == 0):
        print("~~ loader heartbeat ~~~")


  

def load_goodreads():
    global row_counter
    global rows_languages
    global rows_authors
    global rows_publishers
    global rows_review
    global rows_books
    for csvfile in INVENTORY_FILE_PATH:
        special_column_const_swap(csvfile)
        with open(csvfile, newline='', encoding='utf-8') as book_file:
            csvreader = dictDBReader(book_file)
            for row in csvreader:
                row_counter+=1
                isbn = None
                authorID = None
                publisherID = None
                review_count = 0
                language_code = None
                # an ISBN and title is required
                if row[COLUMN_ISBN]:
                    isbn = santitize_isbn13(row[COLUMN_ISBN])
                if not isbn or not row[COLUMN_NAME]:
                    continue
                # ensure isbn key is unique
                notdupe1 = dedupe_isbn(isbn)
                if not notdupe1:
                    continue
                if row[COLUMN_AUTHOR]:
                    author_name = santitize_author_name(row[COLUMN_AUTHOR])
                    authorID = map_author_id(author_name, rows_authors)
                if row[COLUMN_PUBLISHER]:
                    publisherID = map_publisher_id(row[COLUMN_PUBLISHER], rows_publishers)
                if row[COLUMN_LANGUAGE]:
                    language_code = dupe_language_code(row[COLUMN_LANGUAGE], rows_languages)
                if row[COLUMN_REVIEWCOUNT]:
                    review_count = row[COLUMN_REVIEWCOUNT]
                # cleanup data errors
                rating1 = santitize_ratings(row[COLUMN_RATING_DIST1])
                rating2 = santitize_ratings(row[COLUMN_RATING_DIST2])
                rating3 = santitize_ratings(row[COLUMN_RATING_DIST3])
                rating4 = santitize_ratings(row[COLUMN_RATING_DIST4])
                rating5 = santitize_ratings(row[COLUMN_RATING_DIST5])
                year = santitize_year(row[COLUMN_PUBLISH_YEAR])
                month = santitize_month(row[COLUMN_PUBLISH_MONTH]) 
                day = santitize_day(row[COLUMN_PUBLISH_DAY])
                # more rows to insert
                rows_books.append((
                    isbn, 
                    row[COLUMN_NAME], 
                    authorID, 
                    publisherID, 
                    year, 
                    month, 
                    day,
                    row[COLUMN_PAGENUM], 
                    language_code
                ))
                rows_review.append((
                    isbn, 
                    rating1,
                    rating2,
                    rating3,
                    rating4,
                    rating5,
                    review_count
                ))
                flush()
    flush(force=True)
    print("...loaded Goodreads records")


# initialization
connect_db()

# create the tables
load_script(BOOKS_SQL_SCRIPT_PATH)

# load goodreads records
load_goodreads()

# cleanup
close_db()
print("...done")
log_current_status()
