
import csv
import isbnlib
from datetime import datetime

# derived from 
# https://stackoverflow.com/questions/11379300/csv-reader-behavior-with-none-and-empty-string
# to convert '' data to null for easy parsing
class csvDBReader():
    def __init__(self, csvfile, *args, **kwrags):
        self.reader = csv.reader(csvfile, *args, **kwrags)
    def __iter__(self):
        return self
    def __next__(self):
        return [None if not val else val for val in next(self.reader)]
    next = __next__  # Python2.x compatibility.

class dictDBReader():
    def __init__(self, csvfile, *args, **kwrags):
        self.reader = csv.DictReader(csvfile, *args, **kwrags)
        self.reader.fieldnames = [name.strip().lower() for name in self.reader.fieldnames]
    def __iter__(self):
        return self
    def __next__(self):
        return {key: (None if not val else val) for key, val in next(self.reader).items()}
    next = __next__  # Python2.x compatibility.

def log_error(msg):
    f = open("./temp/error.txt", "a")
    print("ERROR: {}".format(msg))
    f.write("{}\n".format(msg))
    f.close()

def log_warning(msg):
    f = open("./temp/warning.txt", "a")
    print("WARNING: {}".format(msg))
    f.write("{}\n".format(msg))
    f.close()


def santitize_author_name(name):
    newname = name
    if '(' in name:
        newname = name[:name.index('(')]
    return " ".join(newname.split())

def santitize_isbn13(isbn):
    if isbnlib.is_isbn10(isbn):
        return isbnlib.to_isbn13(isbn)
    elif isbnlib.is_isbn13(isbn):
        return isbnlib.to_isbn13(isbn)
    return None

def santitize_ratings(rating):
    if rating and ':' in rating:
        try:
            tmp = rating[rating.index(':')+1:]
            ratingint = int(tmp)
            if ratingint >= 0:
                return ratingint
            return 0
        except:
            return 0
    return 0

def santitize_year(year):
    try:
        newyear = int(year)
        if newyear >= 0 and newyear < 9999:
            return newyear
        return None
    except:
        return None

def santitize_month(month):
    try:
        newmonth = int(month)
        if newmonth > 0 and newmonth <= 12:
            return newmonth
        return None
    except:
        return None

def santitize_day(day):
    try:
        newday = int(day)
        if newday > 0 and newday <= 31:
            return newday
        return None
    except:
        return None

def santitize_userID(userid):
    try:
        intid = int(userid)
        if intid > 0 and intid < 999999:
            return intid
        return None 
    except:
        return None

def santitize_title(title):
    newntitle = title
    if '/' in title:
        newntitle = title[:title.index('/')]
    return " ".join(newntitle.split())

def parse_lib_subjects(subjects):
    list = [subj.strip() for subj in subjects.split(',')]
    return set(list)

def parse_lib_author(raw):
    sub_vals = [val.strip() for val in raw.split(',')]
    name = santitize_author_name(sub_vals[0])
    if (len(sub_vals) > 1 and not any(char.isdigit() for char in sub_vals[1])):
        name = name + " " + santitize_author_name(sub_vals[1])
    return name

def parse_lib_publisher(raw):
    sub_vals = [val.strip() for val in raw.split(',')]
    return sub_vals[0]

def parse_lib_floating_item(value):
    if value == "Floating":
        return True
    return False

def parse_lib_isbns(isbns):
    isbn13s = set()
    anyisbns = [isbn.strip() for isbn in isbns.split(',')]
    for isbn in anyisbns:
        isbn13 = santitize_isbn13(isbn)
        if isbn13:
            isbn13s.add(isbn13)
    return isbn13s

def parse_lib_date(raw):
    return datetime.strptime(raw, '%m/%d/%Y')

def parse_lib_publication_year(raw):
    nums = raw.split()
    try:
        firstIndex = 0
        for i, c in enumerate(nums[0]):
            if c.isdigit():
                firstIndex = i
                break
        maybeyear = nums[0][firstIndex:firstIndex+4]
        return santitize_year(maybeyear)
    except:
        return None

def parse_checkout_datetime(raw):
    return datetime.strptime(raw, '%m/%d/%Y %H:%M:%S %p')




