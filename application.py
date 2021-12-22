import signal
import sys

import constants
from colorama import init
from utility_db import close_db, connect_db
from utility_orm import do_insert_book, do_insert_checkout, do_insert_user_rating, do_select_barcode, do_select_inventory, do_select_inventory_with_isbn, do_select_user_ratings, make_where_greater_float, make_where_like_string, do_select_books, selector_single_table
from utility_pretty_print import pretty_print_Barcodes, pretty_print_books, pretty_print_inventory, pretty_print_inventory_with_Barcodes, pretty_print_user_ratings

from utility_ui import error_occured, force_choice, force_valid_response, print_success, print_warning, request_multiple_selection_and_validate_response, print_centered, print_new_page, yes_or_no
from utility_validator import validate_book_name, validate_day, validate_int, validate_isbn, validate_language, validate_month, validate_numpages, validate_review_aggscore, validate_string, validate_year


selected_books = []
userid = None
selected_bibnumber = None
selected_barcode = None

def signal_handler(sig, frame):
    exit()

def exit():
    close_db()
    print_new_page("~~ Goodbye ~~")
    sys.exit(0)

def homepage():
    print_new_page("~~ Homepage ~~")
    next_location = force_choice([
        ("f", "lookup a book", lookup_book_page),
        ("b", "borrow a book", borrow_book_page),
        ("p", "publish a book", publish_book_page),
        ("r", "review a book", review_book_page),
        ("c", "checkout a book", checkout_page),
        ("q", "exit", exit)
    ])
    return next_location

def main():
    print_new_page("~~ Seattle Library Client Started ~~")
    next_location = homepage
    while(True):
        if next_location == None: exit()
        next_location = next_location()
    return

def lookup_book_page(nextpage=None, findone=False):
    global selected_books
    print_new_page("~~ Lookup Page ~~")
    selected_books = []
    do_look_up = True
    while do_look_up or (findone and len(selected_books) != 1):
        print("define your search criterias:")
        specifications = request_multiple_selection_and_validate_response([
            # ("b", "library Bibnumber", constants.COLUMN_LIBRARYINVENTORY_BIBNUM, validate_int),
            ("i", "ISBN number", constants.COLUMN_BOOKS_ISBN13, validate_isbn),
            ("t", "book title", constants.COLUMN_BOOKS_TITLE, validate_book_name),
            ("n", "author full name", constants.COLUMN_AUTHORS_AUTHORNAME, validate_string),
            ("p", "publisher name", constants.COLUMN_PUBLISHERS_PUBLISHERNAME, validate_string),
            ("y", "publication year", constants.COLUMN_BOOKS_PUBLICATIONYEAR, validate_year),
            ("m", "publication month", constants.COLUMN_BOOKS_PUBLICATIONMONTH, validate_month),
            ("d", "publication day", constants.COLUMN_BOOKS_PUBLICATIONDAY, validate_day),
            ("u", "language code", constants.COLUMN_LANGUAGES_LANGUAGECODE, validate_language),
            ("c", "MIN number of pages", constants.COLUMN_BOOKS_NUMPAGES, validate_numpages),
            # ("s", "subject name", constants.COLUMN_SUBJECTS_SUBJECTNAME, validate_string),
            # ("e", "item type", constants.COLUMN_LIBRARYINVENTORY_ITEMTYPE, validate_string),
            # ("o", "item collection", constants.COLUMN_LIBRARYINVENTORY_ITEMCOLLECTION, validate_string),
            ("r", "MIN average score", constants.COLUMN_BOOKSRATINGSSUMMARY_AVERAGERATINGS, validate_review_aggscore)
        ])
        # search with the criterias
        specials = {
            constants.COLUMN_BOOKS_TITLE: make_where_like_string,
            constants.COLUMN_SUBJECTS_SUBJECTNAME: make_where_like_string,
            constants.COLUMN_BOOKSRATINGSSUMMARY_AVERAGERATINGS: make_where_greater_float,
            constants.COLUMN_BOOKS_NUMPAGES: make_where_greater_float
        }
        selected_books = do_select_books(selection=[], conditions=specifications, conditions_specials=specials)
        if len(selected_books) == 0: 
            print_warning("zero results found :(")
            if not findone: do_look_up = yes_or_no("try searching again?")
        else:
            pretty_print_books(selected_books)
            if findone and len(selected_books) != 1: print_warning("multiple results, please narrow your search down one ISBNs edition")
            elif len(selected_books) >= 10: print_warning("too many results, showing the first 10 matches...")
            do_look_up = False
        print()
    if nextpage: 
        return nextpage
    return homepage

def publish_book_page():
    print_new_page("~~ Book Creation Page ~~")
    print("lets start by entering some required information for your book...")
    isbn13 = force_valid_response("ISBN13 (or ISBN10)", validate_isbn)
    title = force_valid_response("book title", validate_string)
    authorName = force_valid_response("author name", validate_string, isSkippable=True)
    publisherName = force_valid_response("publisher name", validate_string, isSkippable=True)
    numPages = force_valid_response("number of pages", validate_numpages)
    languageCode = force_valid_response("language code (eg. ENG)", validate_language)
    publicationYear = force_valid_response("publication year", validate_year)
    publicationMonth = force_valid_response("publication month", validate_month, isSkippable=True)
    publicationDay = force_valid_response("publication day", validate_day, isSkippable=True)
    do_insert = yes_or_no("are you sure you want to publish the book {} ?".format(title))
    if not do_insert: return homepage
    can_insert, success = do_insert_book(isbn13, title, authorName, publisherName, numPages, languageCode, publicationYear, publicationMonth, publicationDay)
    if not can_insert: print_warning("sorry, there is already a book in our database with the same ISBN13")
    elif not success: error_occured()
    else: print_success("you book has been added to the database")
    return homepage

def borrow_book_page():
    print_new_page("~~ Borrow A Book Page ~~")
    bibnumber = None
    know_bibnum = yes_or_no("Do you know the Library BibNumber of the Book You want to Borrow?")
    if not know_bibnum:
        print("Lets check if the book you want to borrow is in our collection...")
        isbn13 = force_valid_response("ISBN13 (or ISBN10)", validate_isbn)
        inventory_rows = do_select_inventory_with_isbn(isbn13)
        if len(inventory_rows) == 0:
            print_warning("looks like our library doesn't have the book yet, sorry")
            return homepage
        elif len(inventory_rows) == 1:
            bibnumber = inventory_rows[0][constants.COLUMN_LIBRARYINVENTORY_BIBNUM]
            print()
            print_success("the library BibNumber is {}".format(bibnumber))
        else:
            print_success("we found several results in our inventory, please choose")
            pretty_print_inventory(inventory_rows)
            bibnumber = force_valid_response("BibNumber", validate_int)
    else:
        bibnumber = force_valid_response("BibNumber", validate_int)
    a_inventory_row, barcode_rows = do_select_inventory(bibnumber)
    if a_inventory_row is None:
        print()
        print_warning("looks like our library no longer has the book, sorry")
        return homepage
    pretty_print_inventory_with_Barcodes(a_inventory_row)
    if len(barcode_rows) == 0:
        print()
        print_warning("looks like we don't have any item barcodes on record, check with you librarian instead")
        return homepage
    pretty_print_Barcodes(barcode_rows)
    return checkout_page

def checkout_page():
    print_new_page("~~ Checkout Page ~~")
    print("lets continue with the checkout by scanning the barcode")
    barcode = force_valid_response("Item Barcode", validate_int)
    barcode_rows = do_select_barcode(barcode)
    if len(barcode_rows) == 0:
        print_warning("the item barcode you entered in invalid")
        return homepage
    success = do_insert_checkout(barcode)
    if not success: error_occured()
    print()
    print_success("success, a new checkout record is added to our database")
    return homepage

def review_book_page():
    global userid
    print_new_page("~~ Review Page ~~")
    print("you may (re-)rate a book here")
    print("to personalize your experience, you must have a user ID (suggested user ID: 10986)")
    userid = force_valid_response("your userId", validate_int)
    ratings = do_select_user_ratings(userid)
    if len(ratings) > 0: pretty_print_user_ratings(ratings)
    else: print("you current don't have any ratings, add one now")
    if len(ratings) >= 10: print("showing only the first 10 ratings...")
    print("first find the book you want to review, redirecting to Lookup Page...")
    print()
    return lookup_book_page(nextpage=add_review_page, findone=True)

def add_review_page():
    print_new_page("~~ Add A Rating ~~")
    if len(selected_books) != 1 or userid == None:
        error_occured()
        return None
    print("How do you feel about \"{}\" ?".format(selected_books[0][constants.COLUMN_BOOKS_TITLE]))
    ISBN13 = selected_books[0][constants.COLUMN_BOOKS_ISBN13]
    newrating = force_choice([
        ("1", "did not like it", 1),
        ("2", "it was ok", 2),
        ("3", "liked it", 3),
        ("4", "really liked it", 4),
        ("5", "it was amazing", 5)
    ], prompt="Enter your rating")
    success = do_insert_user_rating(userid, ISBN13, newrating)
    if success: print_success("your rating has been added")
    else: error_occured()
    return homepage



# Starts the application
init()
signal.signal(signal.SIGINT, signal_handler)
connect_db()
main()
