from uuid import UUID


def validate_uuid(uuid_string):
    """
   function to validate uuid string.
    :param uuid_string: string of uuid
    :return: returns True if uuid_string is valid else False
    """
    try:
        UUID(uuid_string)
    except ValueError:
        return False
    return True
