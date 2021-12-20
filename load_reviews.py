import mysql.connector
from utility_common import dictDBReader, log_warning, log_error, csvDBReader, santitize_isbn13, santitize_userID
from utility_db import close_db, connect_db, load_data, load_script
from utility_deduper import dedupe_isbn
from utility_mapper import map_title_ISBN
import signal
import sys

# environment constants
GOODREADS_FILE_PATH = ['./data/book1-100k.csv',
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
REVIEWS_FILE_PATH = ['./data/user_rating_0_to_1000.csv',
                     './data/user_rating_1000_to_2000.csv',
                     './data/user_rating_2000_to_3000.csv',
                     './data/user_rating_3000_to_4000.csv',
                     './data/user_rating_4000_to_5000.csv',
                     './data/user_rating_5000_to_6000.csv',
                     './data/user_rating_6000_to_11000.csv']
REVIEWS_SQL_SCRIPT_PATH = './scripts/create_reviews_tables.sql'

MIN_SQL_OPERATION_ROW_INDEX = 0

COLUMN_USER_ID = 0
COLUMN_REVIEWED_TITLE = 1
COLUMN_USER_RATING = 2

COLUMN_GOODREADS_NAME = 'name'
COLUMN_GOODREADS_ISBN = 'isbn'

REVIEW_TYPES = {
    "This user doesn't have any rating": None,
    'did not like it': 1, 
    'it was ok': 2,
    'liked it': 3, 
    'really liked it': 4,
    'it was amazing': 5
}

SPACING_SQL_OPERATION = 5000

row_counter = 0
completed_rows = 0

rows_ratings = []

def log_current_status():
    print("ROWS PARSED: ", row_counter)
    print("ROWS COMPLETED: ", completed_rows)

def signal_handler(sig, frame):
    log_current_status()
    print('...exiting gracefully')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


sql_ratings = ("INSERT INTO BooksUserRatings (bookID, userID, rating) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE rating = VALUES(rating)")

def flush(force=False):
    global rows_ratings
    global completed_rows
    if not force and row_counter % SPACING_SQL_OPERATION != 0:
        return
    elif row_counter > MIN_SQL_OPERATION_ROW_INDEX:
        s1 = load_data(sql_ratings, rows_ratings, "RATI_"+str(row_counter))
        if not s1:
            log_warning("WARNING_STOPPED_AT_"+str(row_counter))
            sys.exit(0)
    rows_ratings = []
    completed_rows = row_counter
    if (completed_rows % 50000 == 0):
        print("~~ loader heartbeat ~~~")

    
def preload_goodreads_keys():
    for csvfile in GOODREADS_FILE_PATH:
        with open(csvfile, newline='', encoding='utf-8') as book_file:
            csvreader = dictDBReader(book_file)
            for row in csvreader:
                isbn = None
                # an ISBN and title is required
                if row[COLUMN_GOODREADS_ISBN]:
                    isbn = santitize_isbn13(row[COLUMN_GOODREADS_ISBN])
                if not isbn or not row[COLUMN_GOODREADS_NAME]:
                    continue
                # ensure isbn key is unique
                isunique1 = dedupe_isbn(isbn)
                if not isunique1:
                    continue
                map_title_ISBN(row[COLUMN_GOODREADS_NAME], isbn)
    print("...mapped GoodReads keys")


def load_reviews():
    global row_counter
    global rows_ratings
    for csvfile in REVIEWS_FILE_PATH:
        with open(csvfile, newline='', encoding='utf-8') as review_file:
            csvreader = csvDBReader(review_file)
            next(csvreader, None)
            for row in csvreader:
                row_counter+=1
                if row[COLUMN_USER_RATING] and row[COLUMN_USER_ID]:
                    rating = REVIEW_TYPES.get(row[COLUMN_USER_RATING])
                    isbnset = map_title_ISBN(row[COLUMN_REVIEWED_TITLE])
                    userID = santitize_userID(row[COLUMN_USER_ID])
                    if rating and userID:
                        for isbn in isbnset:
                            rows_ratings.append((
                                isbn,
                                userID,
                                rating
                            ))
                flush()
                # end of for each record
        # end of for each file
    flush(force=True)



# initialization
connect_db()

# create the tables
load_script(REVIEWS_SQL_SCRIPT_PATH)

# load mappings
preload_goodreads_keys()

# load records
load_reviews()

# cleanup
close_db()
print("...done")
log_current_status()
