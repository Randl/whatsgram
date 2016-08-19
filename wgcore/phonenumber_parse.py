import logging

import phonenumbers  # pip install phonenumbers

logger = logging.getLogger(__name__)


def get_cc_and_number(number_string):
    """
    Check if number is valid
    :return: list of phone number country code and national number if number is valid, else empty list
    """
    try:
        num = phonenumbers.parse(number_string, None)
    except:
        logger.warning('Unable to parse a number {}'.format(number_string))
        return []
    if phonenumbers.is_valid_number(num):
        return [num.country_code, num.national_number]
    logger.warning('Invalid number {}'.format(number_string))
    return []
