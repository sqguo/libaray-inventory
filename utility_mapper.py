

# mappings of name to ID
all_authors = dict()
all_publishers = dict()
all_subjects = dict()

# total number of objects
num_authors = 0
num_publishers = 0
num_subjects = 0

# maps objects to isbnset
all_bibISBNs = dict()
all_titleISBNs = dict()

# maps objects to bibnum
all_barcodeBibnums = dict()


def map_author_id(author_name, rows_authors=[]):
    global num_authors
    global all_authors
    author_name_key = author_name.lower()
    authorID = all_authors.get(author_name_key)
    if authorID == None:
        num_authors+=1
        all_authors[author_name_key] = num_authors
        authorID = num_authors
        rows_authors.append((authorID, author_name))
    return authorID


def map_publisher_id(publisher_name, rows_publishers=[]):
    global num_publishers
    global all_publishers
    publisher_name_key = publisher_name.lower()
    publisherID = all_publishers.get(publisher_name_key)
    if publisherID == None:
        num_publishers+=1
        all_publishers[publisher_name_key] = num_publishers
        publisherID = num_publishers
        rows_publishers.append((publisherID, publisher_name))
    return publisherID

def map_subject_id(subject_name, rows_subjects=[]):
    global num_subjects
    global all_subjects
    subject_name_key = subject_name.lower()
    subjectID = all_subjects.get(subject_name_key)
    if subjectID == None:
        num_subjects+=1
        all_subjects[subject_name_key] = num_subjects
        subjectID = num_subjects
        rows_subjects.append((subjectID, subject_name))
    return subjectID

def map_bib_ISBN(bibnum, new_isbnset, rows_bibISBN=[]):
    global all_bibISBNs
    old_isbnset = all_bibISBNs.get(bibnum)
    extra_isbnset = set()
    if old_isbnset == None:
        all_bibISBNs[bibnum] = new_isbnset
        extra_isbnset = new_isbnset
    else:
        extra_isbnset = new_isbnset - old_isbnset
        all_bibISBNs[bibnum] = extra_isbnset.union(old_isbnset)
    for isbn in extra_isbnset:
        rows_bibISBN.append((isbn, bibnum))
    return extra_isbnset

def map_title_ISBN(title, isbn=None):
    global all_titleISBNs
    title_key = title.lower()
    isbnset = all_titleISBNs.get(title_key)
    if isbn:
        if not isbnset:
            isbnset = set([isbn])
            all_titleISBNs[title_key] = isbnset
        else:
            isbnset.add(isbn)
            all_titleISBNs[title_key] = isbnset
    return isbnset

def map_barcode_bibnum(barcode, bibnum, callNumber, rows_bibBarcodes=[]):
    global all_barcodeBibnums
    old_bibnum = all_barcodeBibnums.get(barcode)
    if not old_bibnum:
        all_barcodeBibnums[barcode] = bibnum
        rows_bibBarcodes.append((barcode, bibnum, callNumber))
        return True
    elif old_bibnum == bibnum:
        return True
    return False
    
    

    

