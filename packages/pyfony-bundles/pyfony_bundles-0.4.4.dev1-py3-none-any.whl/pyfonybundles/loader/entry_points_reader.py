import importlib_metadata


def get_by_key(key: str):
    return importlib_metadata.entry_points().select(group=key)
