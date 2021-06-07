def update_dict(result, keys_to_remove):
    for key in keys_to_remove:
        del result[key]
    return result