def verify_device(db_obj, query_obj, device) -> bool:
    """
    Checks to see if a device has the same id as that recorded within the
    db
    :param db_obj:
    :param query_obj:
    :return: boolean
    """
    result = db_obj.read_one(query_obj.verify_device(device))

    if result:
        return True
    else:
        return False


def get_device_id(location, db_obj, query_obj):
    """
    Checks to see if a device has the same id as that recorded within the
    db
    :param query_obj:
    :param db_obj:
    :param location:
    :return: device_id
    """
    result = db_obj.read_one(query_obj.device_id(location))

    if result:
        return result['device_id']
    else:
        return None
