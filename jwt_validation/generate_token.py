import numbers
import random
import string

def generate_token():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters + string.digits) for i in range(16))
    return result_str
    print("Random string of length", length, "is:", result_str)