"""Main module."""

import random
import string

def generate_random_string(length=10, upper=False, digits=False, punctuation=False):
    """Generate a random string of a given length

    Args:
        length (int, optional): _description_. Defaults to 10.
        upper (bool, optional): _description_. Defaults to False.
        digits (bool, optional): _description_. Defaults to False.
        punctuation (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: The generated string
    """    
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
    """Generate a random string of a given length

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: Digits of a defined length
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)