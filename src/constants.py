
# table names
TABLE_AUTHORS = 'Authors'
TABLE_PUBLISHERS = 'Publishers'
TABLE_SUBJECTS = 'Subjects'
TABLE_LANGUAGES = 'Languages'
TABLE_BOOKS = 'Books'
TABLE_BOOKSRATINGS = 'BooksRatings'
TABLE_BOOKSUSERRATINGS = 'BooksUserRatings'
TABLE_LIBRARYINVENTORY = 'LibraryInventory'
TABLE_BIBNUMISBNS = 'BibNumISBNs'
TABLE_BIBNUMSUBJECTS = 'BibNumSubjects'
TABLE_BIBNUMBARCODES = 'BibNumBarCodes'
TABLE_LIBRARYCHECKOUTS = 'LibraryCheckouts'

# view names
VIEW_BOOKSRATINGSSUMMARY = 'BooksRatingsSummary'


# table columns
COLUMN_AUTHORS_AUTHORID = 'authorID'
COLUMN_AUTHORS_AUTHORNAME = 'authorName'
COLUMN_AUTHORS_BIRTHYEAR = 'birthYear'
COLUMN_PUBLISHERS_PUBLISHERID = 'publisherID'
COLUMN_PUBLISHERS_PUBLISHERNAME = 'publisherName'
COLUMN_SUBJECTS_SUBJECTID = 'subjectID'
COLUMN_SUBJECTS_SUBJECTNAME = 'subjectName'
COLUMN_LANGUAGES_LANGUAGECODE = 'languageCode'
COLUMN_BOOKS_ISBN13 = 'ISBN13'
COLUMN_BOOKS_TITLE = 'title'
COLUMN_BOOKS_AUTHORID = 'authorID'
COLUMN_BOOKS_PUBLISHERID = 'publisherID'
COLUMN_BOOKS_PUBLICATIONYEAR = 'publicationYear'
COLUMN_BOOKS_PUBLICATIONMONTH = 'publicationMonth'
COLUMN_BOOKS_PUBLICATIONDAY = 'publicationDay'
COLUMN_BOOKS_NUMPAGES = 'numPages'
COLUMN_BOOKS_LANGUAGECODE = 'languageCode'
COLUMN_BOOKSRATINGS_ISBN13 = 'ISBN13'
COLUMN_BOOKSRATINGS_RATINGDIST1 = 'ratingDist1'
COLUMN_BOOKSRATINGS_RATINGDIST2 = 'ratingDist2'
COLUMN_BOOKSRATINGS_RATINGDIST3 = 'ratingDist3'
COLUMN_BOOKSRATINGS_RATINGDIST4 = 'ratingDist4'
COLUMN_BOOKSRATINGS_RATINGDIST5 = 'ratingDist5'
COLUMN_BOOKSRATINGS_COUNTSOFTEXTREVIEW = 'countsOfTextReview'
COLUMN_BOOKSUSERRATINGS_ISBN13 = 'ISBN13'
COLUMN_BOOKSUSERRATINGS_USERID = 'userID'
COLUMN_BOOKSUSERRATINGS_RATING = 'rating'
COLUMN_LIBRARYINVENTORY_BIBNUM = 'bibNum'
COLUMN_LIBRARYINVENTORY_ITEMTYPE = 'itemType'
COLUMN_LIBRARYINVENTORY_ITEMCOLLECTION = 'itemCollection'
COLUMN_LIBRARYINVENTORY_FLOATINGITEM = 'floatingItem'
COLUMN_LIBRARYINVENTORY_ITEMLOCATION = 'itemLocation'
COLUMN_LIBRARYINVENTORY_REPORTDATE = 'reportDate'
COLUMN_LIBRARYINVENTORY_ITEMCOUNT = 'itemCount'
COLUMN_BIBNUMISBNS_ISBN13 = 'ISBN13'
COLUMN_BIBNUMISBNS_BIBNUM = 'bibNum'
COLUMN_BIBNUMSUBJECTS_SUBJECTID = 'subjectID'
COLUMN_BIBNUMSUBJECTS_BIBNUM = 'bibNum'
COLUMN_BIBNUMBARCODES_ITEMBARCODE = 'ItemBarcode'
COLUMN_BIBNUMBARCODES_BIBNUM = 'bibNum'
COLUMN_BIBNUMBARCODES_CALLNUMBER = 'callNumber'
COLUMN_LIBRARYCHECKOUTS_ITEMBARCODE = 'ItemBarcode'
COLUMN_LIBRARYCHECKOUTS_CHECKOUTDATE = 'checkoutDate'
COLUMN_BOOKSRATINGSSUMMARY_ISBN13 = 'ISBN13'
COLUMN_BOOKSRATINGSSUMMARY_AVERAGERATINGS = 'averageRating'
COLUMN_BOOKSRATINGSSUMMARY_NUMRATINGS = 'numRatings'
COLUMN_BOOKSRATINGSSUMMARY_COUTSOFTEXTREVIEW = 'countsOfTextReview'

DATABASE_DESIGN = {
    TABLE_AUTHORS: [
        COLUMN_AUTHORS_AUTHORID,
        COLUMN_AUTHORS_AUTHORNAME,
        COLUMN_AUTHORS_BIRTHYEAR,
    ],
    TABLE_PUBLISHERS: [
        COLUMN_PUBLISHERS_PUBLISHERID,
        COLUMN_PUBLISHERS_PUBLISHERNAME
    ],
    TABLE_SUBJECTS: [
        COLUMN_SUBJECTS_SUBJECTID,
        COLUMN_SUBJECTS_SUBJECTNAME,
    ],
    TABLE_LANGUAGES: [
        COLUMN_LANGUAGES_LANGUAGECODE
    ],
    TABLE_BOOKS: [
        COLUMN_BOOKS_ISBN13,
        COLUMN_BOOKS_TITLE,
        COLUMN_BOOKS_AUTHORID,
        COLUMN_BOOKS_PUBLISHERID,
        COLUMN_BOOKS_PUBLICATIONYEAR,
        COLUMN_BOOKS_PUBLICATIONMONTH,
        COLUMN_BOOKS_PUBLICATIONDAY,
        COLUMN_BOOKS_NUMPAGES,
        COLUMN_BOOKS_LANGUAGECODE
    ],
    TABLE_BOOKSRATINGS: [
        COLUMN_BOOKSRATINGS_ISBN13,
        COLUMN_BOOKSRATINGS_RATINGDIST1,
        COLUMN_BOOKSRATINGS_RATINGDIST2,
        COLUMN_BOOKSRATINGS_RATINGDIST3,
        COLUMN_BOOKSRATINGS_RATINGDIST4,
        COLUMN_BOOKSRATINGS_RATINGDIST5,
        COLUMN_BOOKSRATINGS_COUNTSOFTEXTREVIEW
    ],
    TABLE_BOOKSUSERRATINGS: [
        COLUMN_BOOKSUSERRATINGS_ISBN13,
        COLUMN_BOOKSUSERRATINGS_USERID,
        COLUMN_BOOKSUSERRATINGS_RATING
    ],
    TABLE_LIBRARYINVENTORY: [
        COLUMN_LIBRARYINVENTORY_BIBNUM,
        COLUMN_LIBRARYINVENTORY_ITEMTYPE,
        COLUMN_LIBRARYINVENTORY_ITEMCOLLECTION,
        COLUMN_LIBRARYINVENTORY_FLOATINGITEM,
        COLUMN_LIBRARYINVENTORY_ITEMLOCATION,
        COLUMN_LIBRARYINVENTORY_REPORTDATE,
        COLUMN_LIBRARYINVENTORY_ITEMCOUNT
    ],
    TABLE_BIBNUMISBNS: [
        COLUMN_BIBNUMISBNS_ISBN13,
        COLUMN_BIBNUMISBNS_BIBNUM
    ],
    TABLE_BIBNUMSUBJECTS: [
        COLUMN_BIBNUMSUBJECTS_SUBJECTID,
        COLUMN_BIBNUMSUBJECTS_BIBNUM
    ],
    TABLE_BIBNUMBARCODES: [
        COLUMN_BIBNUMBARCODES_BIBNUM,
        COLUMN_BIBNUMBARCODES_CALLNUMBER
    ],
    TABLE_LIBRARYCHECKOUTS: [
        COLUMN_LIBRARYCHECKOUTS_ITEMBARCODE,
        COLUMN_LIBRARYCHECKOUTS_CHECKOUTDATE
    ],
    VIEW_BOOKSRATINGSSUMMARY: [
        COLUMN_BOOKSRATINGSSUMMARY_AVERAGERATINGS,
        COLUMN_BOOKSRATINGSSUMMARY_NUMRATINGS,
        COLUMN_BOOKSRATINGSSUMMARY_COUTSOFTEXTREVIEW
    ]
}

BOOKS_CLUSTER_DESIGN = [
    TABLE_BOOKS,
    TABLE_AUTHORS,
    TABLE_PUBLISHERS,
    VIEW_BOOKSRATINGSSUMMARY
]

BOOKS_CLUSTER_FOREIGN_KEY_DESIGN = {
    TABLE_BOOKS: COLUMN_BOOKS_ISBN13,
    TABLE_AUTHORS: COLUMN_AUTHORS_AUTHORID,
    TABLE_PUBLISHERS: COLUMN_PUBLISHERS_PUBLISHERID,
    VIEW_BOOKSRATINGSSUMMARY: COLUMN_BOOKS_ISBN13
}


