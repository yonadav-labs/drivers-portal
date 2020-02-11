import hashlib


def create_hash(field=''):
    # keep size same as MD5
    return hashlib.blake2b(field.encode("utf-8"), digest_size=16).hexdigest()
