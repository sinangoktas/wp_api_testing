import logging as logger
import random
import string

def generate_random_email_and_password(domain=None, email_prefix=None):
    logger.debug("Generating random email and password.")

    if not domain:
        domain = 'sigsolutions.com'
    if not email_prefix:
        email_prefix = 't_u'

    email_length = 5
    password_length = 10
    email = email_prefix + '_' + ''.join(random.choices(string.ascii_lowercase, k=email_length)) + '@' + domain
    password = ''.join(random.choices(string.ascii_letters, k=password_length))
    user_info = {'email': email, 'password': password}

    logger.debug(f"Randomly generated email and password: {user_info}")
    return user_info


def generate_random_string(length=10, prefix=None, suffix=None):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string = random_string + suffix

    return random_string


def generate_random_coupon_code(suffix=None, length=10):
    code = ''.join(random.choices(string.ascii_uppercase, k=length))

    if suffix:
        code += suffix

    return code