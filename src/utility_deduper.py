

# unique objects
from utility_db import fetch_data


CODE_UNKNOWN = 'unk'
unique_isbns = set()
unique_bibnums = set()
unique_location_codes = set()
unique_collection_codes = set()
unique_type_codes = set()
unique_language_codes = set()

def dedupe_bibnum(bibnum):
    global unique_bibnums
    if bibnum in unique_bibnums:
        return False
    unique_bibnums.add(bibnum)
    return True

def has_bibnum(bibnum):
    if bibnum in unique_bibnums:
        return True
    return False

def dedupe_isbn(isbn):
    global unique_isbns
    if isbn in unique_isbns:
        return False
    unique_isbns.add(isbn)
    return True

def dedupe_priming_codes():
    global unique_location_codes
    global unique_collection_codes
    global unique_type_codes
    sql_locations = "SELECT itemLocationCode FROM ItemLocations"
    sql_collections = "SELECT itemCollectionsCode FROM ItemCollections"
    sql_types = "SELECT itemTypeCode FROM ItemTypes"
    unique_location_codes = set([dup[0] for dup in fetch_data(sql_locations)])
    unique_collection_codes= set([dup[0] for dup in fetch_data(sql_collections)])
    unique_type_codes = set([dup[0] for dup in fetch_data(sql_types)])
    print("...primed ILS codes")

def dupe_location_code(code):
    if code in unique_location_codes:
        return code
    return CODE_UNKNOWN

def dupe_collection_code(code):
    if code in unique_collection_codes:
        return code
    return CODE_UNKNOWN

def dupe_type_code(code):
    if code in unique_type_codes:
        return code
    return CODE_UNKNOWN

def dupe_language_code(code, rows_languages=[]):
    global unique_language_codes
    language_key = code.upper()
    if not language_key in unique_language_codes:
        unique_language_codes.add(language_key)
        rows_languages.append((language_key,))
    return language_key


    
