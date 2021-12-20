from utility_common import csvDBReader, log_warning, parse_checkout_datetime
from utility_db import connect_db, close_db, load_data
from utility_mapper import map_barcode_bibnum
import signal
import sys


# environment constants
CHECKOUTS_FILE_PATH = ['./data/Checkouts_By_Title_Data_Lens_2017.csv',
                       './data/Checkouts_By_Title_Data_Lens_2016.csv',
                       './data/Checkouts_By_Title_Data_Lens_2015.csv',
                       './data/Checkouts_By_Title_Data_Lens_2014.csv',
                       './data/Checkouts_By_Title_Data_Lens_2013.csv',
                       './data/Checkouts_By_Title_Data_Lens_2012.csv',
                       './data/Checkouts_By_Title_Data_Lens_2011.csv',
                       './data/Checkouts_By_Title_Data_Lens_2010.csv',
                       './data/Checkouts_By_Title_Data_Lens_2009.csv',
                       './data/Checkouts_By_Title_Data_Lens_2008.csv',
                       './data/Checkouts_By_Title_Data_Lens_2007.csv',
                       './data/Checkouts_By_Title_Data_Lens_2005.csv',
                       './data/Checkouts_By_Title_Data_Lens_2006.csv',
                       './data/Checkouts_By_Title_Data_Lens_2005.csv']
INVENTORY_FILE_PATH = './data/Library_Collection_Inventory.csv'

SPACING_SQL_OPERATION = 1000
MIN_SQL_OPERATION_ROW_INDEX = 0

COLUMN_BIBNUM = 0
COLUMN_BARCODE = 1
COLUMN_CALLNUM = 4
COLUMN_CHECKOUT_DATE = 5

row_counter = 0
completed_rows = 0
debug_counter = 0

rows_checkouts = []
rows_bibNum_barcodes = []

def log_current_status():
    print("DEBUG: ", debug_counter)
    print("ROWS PARSED: ", row_counter)
    print("ROWS COMPLETED: ", completed_rows)

def signal_handler(sig, frame):
    log_current_status()
    print('...exiting gracefully')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


sql_bibBarcodes = ("INSERT INTO BibNumBarCodes (ItemBarcode, bibNum, callNumber) VALUES (%s, %s, %s) ")
sql_checkouts = ("INSERT INTO LibraryCheckouts (ItemBarcode, checkoutDate) VALUES (%s, %s) ")

def flush(force=False):
    global rows_bibNum_barcodes
    global rows_checkouts
    global completed_rows
    global debug_counter
    if not force and row_counter % SPACING_SQL_OPERATION != 0:
        return
    if row_counter > MIN_SQL_OPERATION_ROW_INDEX:
        print(".", end="", flush=True)
        # s1 = load_data(sql_bibBarcodes, rows_bibNum_barcodes, "BBAR_"+str(row_counter), defer_commit=True)
        # s2 = load_data(sql_checkouts, rows_checkouts, "CHEK_"+str(row_counter))
        # if not s1 or not s2:
        #     log_warning("WARNING_STOPPED_AT_"+str(row_counter))
        #     log_current_status()
        #     sys.exit(0)
        print(".", end="", flush=True)
    rows_checkouts = []
    rows_bibNum_barcodes = []
    completed_rows = row_counter
    if (completed_rows % 20000 == 0):
        print("..ok", end="\r\n", flush=True)
    if (completed_rows % 100000 == 0):
        print("~~ loader heartbeat ~~~")


def load_checkouts():
    global row_counter
    global debug_counter
    for csvfile in CHECKOUTS_FILE_PATH:
        with open(csvfile, newline='', encoding='utf-8') as checkout_file:
            csvreader = csvDBReader(checkout_file)
            next(csvreader, None)
            for row in csvreader:
                row_counter += 1
                if not row[COLUMN_BIBNUM] or not row[COLUMN_BARCODE]:
                    continue
                is_valid = map_barcode_bibnum(row[COLUMN_BARCODE], row[COLUMN_BIBNUM], row[COLUMN_CALLNUM], rows_bibNum_barcodes)
                if not is_valid:
                    continue
                date = parse_checkout_datetime(row[COLUMN_CHECKOUT_DATE])
                rows_checkouts.append((row[COLUMN_BARCODE], date))
                flush()
        print(csvfile)
    flush(force=True)
    print("...loaded checkout records")


print("started...")
# initialization
connect_db()

# load the records
load_checkouts()

# cleanup
close_db()
print("...done")
log_current_status()
