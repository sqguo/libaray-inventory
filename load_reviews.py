import mysql.connector
from load_goodreads import MIN_SQL_OPERATION_ROW_INDEX
from utility_common import dictDBReader, log_warning, log_error, csvDBReader, santitize_userID
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
REVIEWS_FILE_PATH = ['./data/user_rating_0_to_1000.csv',
                     './data/user_rating_1000_to_2000.csv',
                     './data/user_rating_2000_to_3000.csv',
                     './data/user_rating_3000_to_4000.csv',
                     './data/user_rating_4000_to_5000.csv',
                     './data/user_rating_5000_to_6000.csv',
                     './data/user_rating_6000_to_11000.csv']
REVIEWS_SQL_SCRIPT_PATH = './scripts/create_reviews_tables.sql'



COLUMN_NAME = 'name'
COLUMN_USER_ID = 0
COLUMN_REVIEWED_TITLE = 1
COLUMN_USER_RATING = 2

REVIEW_TYPES = {
    "This user doesn't have any rating": 0,
    'did not like it': 1, 
    'it was ok': 2,
    'liked it': 3, 
    'really liked it': 4,
    'it was amazing': 5
}

SPACING_SQL_OPERATION = 5000



# initialization
connect_db()

# create the tables
load_script(REVIEWS_SQL_SCRIPT_PATH)
print("...created reviews tables")

row_counter = 0
completed_rows = 0

all_titles = dict()
rows_ratings = []



def signal_handler(sig, frame):
    print("ROWS PARSED: ", row_counter)
    print("ROWS COMPLETED: ", completed_rows)
    print('...exiting gracefully')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def handle_title(column_title):
    title_key = column_title.lower()
    bookID = all_titles.get(title_key)
    if not bookID:
        all_titles[title_key] = row_counter


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

    


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for csvfile in INVENTORY_FILE_PATH:
    with open(csvfile, newline='', encoding='utf-8') as book_file:
        csvreader = dictDBReader(book_file)
        for row in csvreader:
            row_counter+=1
            if row[COLUMN_NAME]:
                handle_title(row[COLUMN_NAME])
            # end of for each record
    # end of for each file
print("...mapped all titles")
row_counter = 0
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


rows_added = 0
for csvfile in REVIEWS_FILE_PATH:
    with open(csvfile, newline='', encoding='utf-8') as review_file:
        csvreader = csvDBReader(review_file)
        next(csvreader, None)
        for row in csvreader:
            row_counter+=1
            if row[COLUMN_USER_RATING] and row[COLUMN_USER_ID]:
                rating = REVIEW_TYPES.get(row[COLUMN_USER_RATING])
                bookID = all_titles.get(row[COLUMN_REVIEWED_TITLE].lower())
                userID = santitize_userID(row[COLUMN_USER_ID])
                if rating > 0 and bookID and userID:
                    rows_ratings.append((
                        bookID,
                        userID,
                        rating
                    ))
                    rows_added+=1
            flush()
            # end of for each record
    # end of for each file
flush(force=True)

# cleanup
close_db()
print("...done")
print("NEW ROWS: ", rows_added)
print("ROWS COMPLETED: ", completed_rows, "/", row_counter)
