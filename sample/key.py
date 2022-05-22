from cryptography.fernet import Fernet

def write_key(key_path):
    '''Writes key

    Parameters
    ----------
    key_path : str
        The file path for the key file


    Returns
    -------
    None
    '''

    key = Fernet.generate_key()

    with open(key_path + 'key.key', 'wb') as key_file:
        key_file.write(key)


def load_key(key_path):
    '''Loads key

    Parameters
    ----------
    key_path : str
        The file path for the key file


    Returns
    -------
    bytes
        key data in binary format
    '''
    with open(key_path + 'key.key', 'rb') as key_file:
        key = key_file.read()

    return key
