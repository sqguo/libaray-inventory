import constants
from datetime import datetime

from utility_ui import print_dash_border

ROW_FORMAT_1 = "{0:<15.15}{1:<50.48}{2:<20.18}{3:<20.18}{4:<8.8}{5:<10.10}{6:<10.10}{7:<15.15}"
ROW_HEADER_1 = ["ISBN13", "Title","Author","Publisher","Score","Language","Pages","Publication Date"]
ROW_FORMAT_2 = "{0:<20.20}{1:<15.15}{2:<50}"
ROW_HEADER_2 = ["ISBN13", "Your Rating", "Title"]
ROW_FORMAT_3 = "{0:<20.20}{1:<20.18}{2:<12.10}{3:<12.10}{4:<12.10}{5:<20.18}{6:<10}"
ROW_HEADER_3 = ["BibNumber", "Description", "Type", "Collection", "Location", "Report Date", "Count"]
ROW_FORMAT_4 = "{0:<20.20}{1:<30.28}{2:<12.10}{3:<12.10}{4:<12.10}{5:<20.18}{6:<10}"
ROW_HEADER_4 = ["BibNumber", "WHERE TO FIND IT", "Type", "Collection", "Location", "Report Date", "Count"]
ROW_FORMAT_5 = "{0:<30.30}{1:<30}"
ROW_HEADER_5 = ["Barcode", "Last Checkout Time"]

def pretty_print_none_values(row):
    return [str(col) if col else "???" for col in row]

def pretty_print_date(year, month, day):
    if year:
        result = datetime.strptime(str(year), '%Y')
        if month: 
            result = result.replace(month=month)
            if day:
                result = result.replace(day=day)
                return result.strftime('%d %b %Y')
            return result.strftime('%b %Y')
        return result.strftime('%Y')
    return None


def pretty_print_books(rows):
    print_dash_border()
    header = ROW_FORMAT_1.format(*ROW_HEADER_1)
    print(header)
    for row in rows:
        content = ROW_FORMAT_1.format(*pretty_print_none_values([
            row[constants.COLUMN_BOOKS_ISBN13],
            row[constants.COLUMN_BOOKS_TITLE],
            row[constants.COLUMN_AUTHORS_AUTHORNAME],
            row[constants.COLUMN_PUBLISHERS_PUBLISHERNAME],
            row[constants.COLUMN_BOOKSRATINGSSUMMARY_AVERAGERATINGS],
            row[constants.COLUMN_BOOKS_LANGUAGECODE],
            row[constants.COLUMN_BOOKS_NUMPAGES],
            pretty_print_date(
                row[constants.COLUMN_BOOKS_PUBLICATIONYEAR],
                row[constants.COLUMN_BOOKS_PUBLICATIONMONTH],
                row[constants.COLUMN_BOOKS_PUBLICATIONDAY]
            )
        ]))
        print(content)
    print_dash_border()
    return

def pretty_print_user_ratings(rows):
    print_dash_border()
    header = ROW_FORMAT_2.format(*ROW_HEADER_2)
    print(header)
    for row in rows:
        content = ROW_FORMAT_2.format(*pretty_print_none_values([
            row[constants.COLUMN_BOOKS_ISBN13],
            row[constants.COLUMN_BOOKSUSERRATINGS_RATING],
            row[constants.COLUMN_BOOKS_TITLE]
        ]))
        print(content)
    print_dash_border()
    return

def pretty_print_inventory(rows):
    print_dash_border()
    header = ROW_FORMAT_3.format(*ROW_HEADER_3)
    print(header)
    for row in rows:
        content = ROW_FORMAT_3.format(*pretty_print_none_values([
            row[constants.COLUMN_LIBRARYINVENTORY_BIBNUM],
            row["description"],
            row[constants.COLUMN_LIBRARYINVENTORY_ITEMTYPE],
            row[constants.COLUMN_LIBRARYINVENTORY_ITEMCOLLECTION],
            row[constants.COLUMN_LIBRARYINVENTORY_ITEMLOCATION],
            row[constants.COLUMN_LIBRARYINVENTORY_REPORTDATE],
            row[constants.COLUMN_LIBRARYINVENTORY_ITEMCOUNT]
        ]))
        print(content)
    print_dash_border()
    return

def pretty_print_inventory_with_Barcodes(row):
    print_dash_border()
    header = ROW_FORMAT_4.format(*ROW_HEADER_4)
    print(header)
    content = ROW_FORMAT_4.format(*pretty_print_none_values([
        row[constants.COLUMN_LIBRARYINVENTORY_BIBNUM],
        row["description"],
        row[constants.COLUMN_LIBRARYINVENTORY_ITEMTYPE],
        row[constants.COLUMN_LIBRARYINVENTORY_ITEMCOLLECTION],
        row[constants.COLUMN_LIBRARYINVENTORY_ITEMLOCATION],
        row[constants.COLUMN_LIBRARYINVENTORY_REPORTDATE],
        row[constants.COLUMN_LIBRARYINVENTORY_ITEMCOUNT]
    ]))
    print(content)
    print_dash_border()
    return

def pretty_print_Barcodes(rows):
    print_dash_border()
    header = ROW_FORMAT_5.format(*ROW_HEADER_5)
    print(header)
    for row in rows:
        content = ROW_FORMAT_5.format(*pretty_print_none_values([
            row[constants.COLUMN_LIBRARYCHECKOUTS_ITEMBARCODE],
            row["mostRecentCheckoutDate"]
        ]))
        print(content)
    print_dash_border()
    return
