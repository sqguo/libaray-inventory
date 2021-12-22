import mysql.connector
from utility_common import log_error, csvDBReader
from utility_db import close_db, connect_db, load_data, load_script


# environment constants
ILS_FILE_PATH = './data/Integrated_Library_System__ILS__Data_Dictionary.csv'
ILS_SQL_SCRIPT_PATH = './scripts/create_ils_tables.sql'

COLUMN_CODE = 0
COLUMN_DESCRIPTION = 1
COLUMN_CODE_TYPE = 2
COLUMN_FORMAT = 3
COLUMN_SUB_FORMAT = 4
COLUMN_CATEGORY = 5
COLUMN_SUB_CATEGORY = 6

TYPE_COLLECTION = 'ItemCollection'
TYPE_LOCATION = 'ItemLocation'
TYPE_TYPE = 'ItemType'

CODE_UNKNOWN = 'unk'
CODE_LOC_1 = 'spa'
CATEGORY_REFERENCE = 'Reference'

# special treatment for data consistency
def special_code_treatment():
    data_dictionary.append((CODE_UNKNOWN, 'Unknown type for item creation'))
    data_dictionary.append((CODE_LOC_1, 'South Park, 8604 8TH AV S'))
    data_row_location.append((CODE_LOC_1,))
    data_row_location.append((CODE_UNKNOWN,))

# initialization
connect_db()
format_set = set()
sub_format_set = set()
category_set = set()
sub_category_set = set()
data_format = []
data_sub_format = []
data_category = []
data_sub_category  = []
data_dictionary = []
data_row_location = []
data_row_category = []
data_row_type = []

# create the tables
load_script(ILS_SQL_SCRIPT_PATH)
print("...created ils tables")

# compute the data
special_code_treatment()
with open(ILS_FILE_PATH, newline='', encoding='utf-8') as ils_file:
    csvreader = csvDBReader(ils_file)
    next(csvreader, None)
    for row in csvreader:
        if row[COLUMN_FORMAT]:
            format_set.add(row[COLUMN_FORMAT])
        if row[COLUMN_SUB_FORMAT]:
            sub_format_set.add(row[COLUMN_SUB_FORMAT])
        if row[COLUMN_CATEGORY]:
            category_set.add(row[COLUMN_CATEGORY])
        if row[COLUMN_SUB_CATEGORY]:
            sub_category_set.add(row[COLUMN_SUB_CATEGORY])
        code_code = row[COLUMN_CODE]
        code_type = row[COLUMN_CODE_TYPE]
        if code_code == CODE_LOC_1:
            continue
        if code_code != CODE_UNKNOWN:
            data_dictionary.append((code_code, row[COLUMN_DESCRIPTION]))
        if code_type == TYPE_TYPE:
            is_reference = row[COLUMN_CATEGORY] == CATEGORY_REFERENCE
            data_row_type.append((code_code, row[COLUMN_FORMAT], row[COLUMN_SUB_FORMAT], is_reference))
        elif code_type == TYPE_COLLECTION:
            data_row_category.append((code_code, row[COLUMN_FORMAT], row[COLUMN_SUB_FORMAT], row[COLUMN_CATEGORY], row[COLUMN_SUB_CATEGORY]))
        elif code_type == TYPE_LOCATION:
            data_row_location.append((code_code, ))
        else:
            log_error("unknown code type: "+ code_type)

# insert the data
sql_format = ("INSERT INTO FormatGroups (formatName) VALUES (%s)")
sql_sub_format = ("INSERT INTO FormatSubGroups (subFormatName) VALUES (%s)")
sql_category = ("INSERT INTO CategoryGroups (categoryName) VALUES (%s)")
sql_sub_category = ("INSERT INTO CategorySubGroups (subCategoryName) VALUES (%s)")
data_format = list([(item,) for item in format_set])
data_sub_format = list([(item,) for item in sub_format_set])
data_category = list([(item,) for item in category_set])
data_sub_category = list([(item,) for item in sub_category_set])
load_data(sql_format, data_format)
load_data(sql_sub_format, data_sub_format)
load_data(sql_category, data_category)
load_data(sql_sub_category, data_sub_category)
print("...loaded constants")

sql_dictionary = ("INSERT INTO CodeDictionary (code, description) VALUES (%s, %s)")
sql_itype = ("INSERT INTO ItemTypes (itemTypeCode, formatName, subFormatName, isReference) VALUES (%s, %s, %s, %s)")
sql_icat = ("INSERT INTO ItemCollections (itemCollectionsCode, formatName, subFormatName, categoryName, subCategoryName) VALUES (%s, %s, %s, %s, %s)")
sql_iloc = ("INSERT INTO ItemLocations (itemLocationCode) VALUES (%s)")
load_data(sql_dictionary, data_dictionary)
print("...loaded dictionary")
load_data(sql_itype, data_row_type)
print("...loaded types")
load_data(sql_icat, data_row_category)
print("...loaded categories")
load_data(sql_iloc, data_row_location)
print("...loaded locations")

# cleanup
close_db()
print("...done")



