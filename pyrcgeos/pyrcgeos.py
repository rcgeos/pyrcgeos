"""Main module."""

import random
import string

def generate_random_string(length=10, upper=False, digits=False, punctuation=False):
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_lowercase
    if digits:
        letters += string.digits
    if punctuation:
        letters += string.punctuation
    #print(letters)
    return ''.join(random.choice(letters) for i in range(length))

def generate_lucky_number(length=1):
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)