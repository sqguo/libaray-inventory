import mysql.connector
from utility_common import log_error, csvDBReader, dictDBReader, log_warning, parse_lib_author, parse_lib_date, parse_lib_floating_item, parse_lib_publisher, parse_lib_subjects, santitize_author_name, parse_lib_isbns
from utility_db import close_db, connect_db, load_data, load_script
from utility_deduper import dedupe_bibnum, dedupe_isbns, dedupe_priming_codes, dupe_collection_code, dupe_location_code, dupe_type_code
from utility_mapper import map_author_id, map_publisher_id, map_subject_id
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
INVENTORY_FILE_PATH = './data/Library_Collection_Inventory.csv'
INVENTORY_SQL_SCRIPT_PATH = './scripts/create_inventory_tables.sql'

COLUMN_GOODREADS_ISBN = 'isbn'
COLUMN_GOODREADS_AUTHOR = 'authors'
COLUMN_GOODREADS_PUBLISHER = 'publisher'

COLUMN_BIBNUM = 0
COLUMN_TITLE = 1
COLUMN_AUTHOR = 2
COLUMN_ISBN = 3
COLUMN_PUBLICATION_YEAR = 4
COLUMN_PUBLISHER = 5
COLUMN_SUBJECTS = 6
COLUMN_ITEM_TYPE = 7
COLUMN_ITEM_COLLECTION = 8
COLUMN_FLOATING = 9
COLUMN_ITEM_LOCATION = 10
COLUMN_REPORT_DATE = 11
COLUMN_ITEM_COUNT = 12

MIN_SQL_OPERATION_ROW_INDEX = 32000
SPACING_SQL_OPERATION = 1000
NO_INSERTION_BEFORE_INDEX = 471626

# state variables
row_counter = 0
completed_rows = 0
actual_insertions = 0
rows_ignored = 0


rows_authors = []
rows_publishers = []
rows_subjects = []

rows_inventory = []
rows_bibnumIsbns = []
rows_bibnumSubjects = []

def log_current_status():
    print("ROWS PARSED: ", row_counter)
    print("ROWS INSERTED: ", actual_insertions)
    print("ROWS IGNORED: ", rows_ignored)
    print("ROWS COMPLETED: ", completed_rows)

def signal_handler(sig, frame):
    log_current_status()
    print('...exiting gracefully')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


sql_author = ("INSERT INTO Authors (authorID, authorName) VALUES (%s, %s)")
sql_publisher = ("INSERT INTO Publishers (publisherID, publisherName) VALUES (%s, %s)")
sql_subjects = ("INSERT INTO Subjects (subjectID, subjectName) VALUES (%s, %s) ")
sql_inventory = ("INSERT INTO LibraryInventory (bibNum, itemType, itemCollection, floatingItem, itemLocation, reportDate, itemCount) VALUES (%s, %s, %s, %s, %s, %s, %s) ")
sql_bibnumisbn = ("INSERT INTO BibNumISBNs (ISBN13, bibNum) VALUES (%s, %s) ")
sql_bibnumsubjects = ("INSERT INTO BibNumSubjects (subjectID, bibNum) VALUES (%s, %s) ")

def flush(force=False):
    global rows_authors
    global rows_publishers
    global rows_subjects
    global rows_inventory
    global rows_bibnumIsbns
    global rows_bibnumSubjects
    global completed_rows
    if not force and row_counter % SPACING_SQL_OPERATION != 0:
        return
    if row_counter > MIN_SQL_OPERATION_ROW_INDEX:
        s1 = load_data(sql_author, rows_authors, "AUTH_"+str(row_counter), defer_commit=True)
        s2 = load_data(sql_publisher, rows_publishers, "PUBL_"+str(row_counter), defer_commit=True)
        s3 = load_data(sql_subjects, rows_subjects, "SUBJ_"+str(row_counter), defer_commit=True)
        s4 = load_data(sql_inventory, rows_inventory, "INVE_"+str(row_counter), defer_commit=True)
        s5 = load_data(sql_bibnumisbn, rows_bibnumIsbns, "BIIS_"+str(row_counter), defer_commit=True)
        s6 = load_data(sql_bibnumsubjects, rows_bibnumSubjects, "BISU_"+str(row_counter))
        if not s1 or not s2 or not s3 or not s4 or not s5 or not s6:
            log_warning("WARNING_STOPPED_AT_"+str(row_counter))
            log_current_status()
            sys.exit(0)
        pass
    rows_authors = []
    rows_publishers = []
    rows_subjects = []
    rows_inventory = []
    rows_bibnumIsbns = []
    rows_bibnumSubjects = []
    completed_rows = row_counter
    if (completed_rows % 50000 == 0):
        print("~~ loader heartbeat ~~~")


def antiflush():
    global rows_authors
    global rows_publishers
    global rows_subjects
    global rows_inventory
    global rows_bibnumIsbns
    global rows_bibnumSubjects
    if actual_insertions <= NO_INSERTION_BEFORE_INDEX:
        rows_authors = []
        rows_publishers = []
        rows_subjects = []
        rows_inventory = []
        rows_bibnumIsbns = []
        rows_bibnumSubjects = []
    else:
        print(row_counter)
        sys.exit(0)



def preload_goodreads_keys():
    dedupe_priming_codes()
    for csvfile in GOODREADS_FILE_PATH:
        with open(csvfile, newline='', encoding='utf-8') as book_file:
            csvreader = dictDBReader(book_file)
            for row in csvreader:
                if row[COLUMN_GOODREADS_AUTHOR]:
                    map_author_id(santitize_author_name(row[COLUMN_GOODREADS_AUTHOR]))
                if row[COLUMN_GOODREADS_PUBLISHER]:
                    map_publisher_id(row[COLUMN_GOODREADS_PUBLISHER])  
    print("...mapped GoodReads keys")




def load_inventory():
    global row_counter, rows_ignored, actual_insertions
    global rows_authors
    global rows_publishers
    global rows_subjects
    global rows_inventory
    global rows_bibnumIsbns
    global rows_bibnumSubjects
    with open(INVENTORY_FILE_PATH, newline='', encoding='utf-8') as inven_file:
        csvreader = csvDBReader(inven_file)
        next(csvreader, None)
        for row in csvreader:
            row_counter+=1
            isbnset = set()
            subjectset = []
            subjectIDs = set()
            authorID = None
            publisherID = None
            itemType = None
            itemCollection = None
            itemLocation = None
            isFloating = False
            itemCount = 0
            reportDate = None
            notdupe1 = True
            notdupe2 = True
            if row[COLUMN_BIBNUM]:
                notdupe1 = dedupe_bibnum(row[COLUMN_BIBNUM])
            if row[COLUMN_ISBN]:
                isbnset = parse_lib_isbns(row[COLUMN_ISBN])
                notdupe2 = dedupe_isbns(isbnset)
            # make sure the record is unique
            if not notdupe1 or not notdupe2:
                rows_ignored += 1
                continue
            if row[COLUMN_SUBJECTS]:
                subjectset = parse_lib_subjects(row[COLUMN_SUBJECTS])
            if row[COLUMN_ITEM_COLLECTION]:
                itemCollection = dupe_collection_code(row[COLUMN_ITEM_COLLECTION])
            if row[COLUMN_ITEM_TYPE]:
                itemType = dupe_type_code(row[COLUMN_ITEM_TYPE])
            if row[COLUMN_ITEM_LOCATION]:
                itemLocation = dupe_location_code(row[COLUMN_ITEM_LOCATION])
            if row[COLUMN_ITEM_COUNT]:
                itemCount = row[COLUMN_ITEM_COUNT]
            if row[COLUMN_FLOATING]:
                isFloating = parse_lib_floating_item(row[COLUMN_FLOATING])
            if row[COLUMN_AUTHOR]:
                authorName = parse_lib_author(row[COLUMN_AUTHOR])
                authorID = map_author_id(authorName, rows_authors)
            if row[COLUMN_PUBLISHER]:
                publisherName = parse_lib_publisher(row[COLUMN_PUBLISHER])
                publisherID = map_publisher_id(publisherName, rows_publishers)
            if row[COLUMN_REPORT_DATE]:
                reportDate = parse_lib_date(row[COLUMN_REPORT_DATE])
            for subject in subjectset:
                subjectID = map_subject_id(subject, rows_subjects)
                subjectIDs.add(subjectID)
            for subjectID in subjectIDs:
                rows_bibnumSubjects.append((subjectID, row[COLUMN_BIBNUM]))
            for isbn in isbnset:
                rows_bibnumIsbns.append((isbn, row[COLUMN_BIBNUM]))
            actual_insertions += 1
            rows_inventory.append((
                row[COLUMN_BIBNUM],
                itemType,
                itemCollection,
                isFloating,
                itemLocation,
                reportDate,
                itemCount
            ))
            flush()
        flush(force=True)
    print("...loaded library inventory")

# LIBNUM -> ISBN
# LIBNUM -> ISBN -> EDITION
#           ISBN
#                -> EDITION
        
# if there is no match, add a new book edition* libnum->editon
# if there is one to one match, great, libnum->editon
# if there is one edition in record, the library has multiple isbns editions libnum->editon, editon->isbn, libnum->isbn, libnum->isbn
# if there are two editions on record, the library has multiple isbns, libnum->editon libnum->editon


# initialization
connect_db()

# create the tables
load_script(INVENTORY_SQL_SCRIPT_PATH)

# preload mappings
preload_goodreads_keys()

# load library inventory
load_inventory()


# cleanup
close_db()
print("...done")
log_current_status()