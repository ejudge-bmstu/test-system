from uuid import UUID


def validate_uuid(uuid_string):
    try:
        UUID(uuid_string)
    except ValueError:
        return False
    return True