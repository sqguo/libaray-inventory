from utility_common import santitize_isbn13

def validate_string(raw, max_len=255):
    if len(raw) == 0 or len(raw) > max_len:
        return None
    return raw

def validate_int(raw, lower=1, upper=None):
    try:
        num = int(raw)
        if num < lower: return None
        if upper != None and num > upper: return None
        return num
    except:
        return None

def validate_review_aggscore(raw):
    try:
        score = float(raw)
        if score < 0.0 or score > 5.0:
            return None
        return score
    except:
        return None

def validate_isbn(raw):
    return santitize_isbn13(raw)

def validate_book_name(raw):
    return validate_string(raw, max_len=1250)

def validate_year(raw):
    return validate_int(raw, lower=1700, upper=2030)

def validate_month(raw):
    return validate_int(raw, lower=1, upper=12)

def validate_day(raw):
    return validate_int(raw, lower=1, upper=31)

def validate_language(raw):
    return validate_string(raw, max_len=13)

def validate_numpages(raw):
    return validate_int(raw, lower=0)
