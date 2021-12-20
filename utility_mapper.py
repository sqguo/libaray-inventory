

# mappings of name to ID
all_authors = dict()
all_publishers = dict()
all_subjects = dict()

# total number of objects
num_authors = 0
num_publishers = 0
num_subjects = 0


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

