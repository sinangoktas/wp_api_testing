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
    email = email_prefix + '_' +\
            ''.join(random.choices(string.ascii_lowercase, k=email_length)) +\
            '@' + domain

    password_length = 10
    password = ''.join(random.choices(string.ascii_letters, k=password_length))

    user_info = {'email': email, 'password': password}
    logger.debug(f"Randomly generated email and password: {user_info}")

    return user_info