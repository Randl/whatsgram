import phonenumbers  # pip install phonenumbers


def get_prefix(number_string):
    """
    Check if number is valid
    :return: phone number prefix if number is valid, empty string
    """
    try:
        num = phonenumbers.parse(number_string, None)
    except NumberParseException:
        return ''
    if phonenumbers.is_valid_number(num):
        return num.country_code
    return ''
