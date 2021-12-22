from colorama import Fore, Style

def print_centered(text):
    print(text.center(65))

def print_new_page(page):
    print()
    print_centered(page)
    print_centered("...")

def print_warning(message):
    print(Fore.RED+"<!> ", end="")
    print(Style.RESET_ALL+message)

def print_success(message):
    print(Fore.GREEN+":) ", end="")
    print(Style.RESET_ALL+message)

def print_question(message):
    print(Fore.CYAN+"(?) ", end="")
    print(Style.RESET_ALL+message)

def try_again(thing="response"):
    print_centered("-- stop --")
    print_warning("your "+thing+" is not valid, try again")

def error_occured():
    print_centered("-- sorry --")
    print("an error has occurred, returning to homepage")

def print_dash_border():
    print("--------------------------------------------------------------------------------------------------------------------------")

# (option, description, method)
def make_choice(choices, prompt="Enter command"):
    for choice in choices:
        print(f"{choice[1]:30}", choice[0])
    print()
    chosen = input(prompt+": ").lower()
    for choice in choices:
        if choice[0] == chosen:
            return choice[2]
    return None

# (option, description, method)
def force_choice(choices, prompt="Enter command"):
    result = make_choice(choices, prompt)
    while(result == None):
        try_again()
        result = make_choice(choices, prompt)
    return result

# (description, validation_method)
def force_valid_response(descriptor, validation_method, isSkippable=False):
    mydescriptor = descriptor
    if isSkippable:
        mydescriptor = descriptor+"(or enter nothing to skip)"
    usercolumn = input("Enter "+mydescriptor+": ")
    if isSkippable and len(usercolumn) == 0:
        return None
    result = validation_method(usercolumn)
    while(result == None):
        try_again(descriptor)
        usercolumn = input("Enter "+descriptor+" again: ")
        if isSkippable and len(usercolumn) == 0:
            return None
        result = validation_method(usercolumn)
    return result

# (description)
def yes_or_no(question):
    answer = input(question+" (y/n): ")
    if answer.lower() == "y": return True
    elif answer.lower() == "n": return False
    try_again()
    return yes_or_no(question)

# (option, description, column_name, validation_method)
def request_selection_and_validate_response(choices):
    first_choices = [(choice[0], choice[1], (choice[1], choice[2], choice[3])) for choice in choices]
    first_choices.append(("x", "complete criteria selection", (None, None, None)))
    column_description, column_name, validation_method = force_choice(first_choices, prompt="Select criteria")
    if column_name == None:
        return None
    result = force_valid_response(column_description, validation_method)
    return (column_name, result)

# (option, description, column_name, validation_method)
def request_multiple_selection_and_validate_response(choices):
    result = dict()
    sub_result = request_selection_and_validate_response(choices)
    while(sub_result == None):
        print_warning("sorry, you must select at least one criteria")
        sub_result = request_selection_and_validate_response(choices)
    result[sub_result[0]] = sub_result[1]
    print()
    print_question("ok, criteria added, continue?")
    sub_result = request_selection_and_validate_response(choices)
    while(sub_result != None):
        print()
        print_question("ok, criteria added, continue?")
        result[sub_result[0]] = sub_result[1]
        sub_result = request_selection_and_validate_response(choices)
    return result


    