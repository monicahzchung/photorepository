import numpy as np
from cryptography.fernet import Fernet
from .key import write_key, load_key


def image_to_byte(image, image_folder):
    '''Returns image in binary format

    Parameters
    ----------
    image : str
        The original image file name
    image_folder : str
        Directory housing images to add


    Returns
    -------
    byte
        image in binary format
    '''

    with open(image_folder + image, 'rb') as file:
        binary_image = file.read()
    return binary_image


def encrypt(item, key_path, image_folder=''):
    '''Encrypts item

    Parameters
    ----------
    item : str
        The image to be added or meta data associated with image
        - user, permissions, date, filename
    key_path : str
        The file path for the key file
    image_folder : str
        Directory housing images to add or default empty string


    Returns
    -------
    bytes
        encrypted bytes data of image meta data

    or

    numpy.ndarray
        encrypted numpy array of binary image data
    '''

    # load key
    key = load_key(key_path)
    f = Fernet(key)

    # check if item is image or meta data and encrypt
    if image_folder != '':
        binary_image = image_to_byte(item, image_folder)
        encrypted_data = f.encrypt(binary_image)
        encrypted = np.asarray(encrypted_data)

    else:
        # encrypt data
        item_bytes = bytes(item,'utf-8')
        encrypted = f.encrypt(item_bytes)

    return encrypted


def decrypt(item, type, key_path):
    '''Decrypts item

    Parameters
    ----------
    item : str
        The image to be added or meta data associated with image
        - user, permissions, date, filename
    type : str
        Type of item, being image or its associated meta data
    key_path : str
        The file path for the key file


    Returns
    -------
    bytes
        decrypted bytes of image or its meta data
    '''

    # load key
    key = load_key(key_path)
    f = Fernet(key)

    # check if item is image or meta data and decrypt
    if type == 'image':
        decrypted_array = np.asarray(item)
        decrypted_bytes = decrypted_array.tobytes(order='C')
        decrypted = f.decrypt(decrypted_bytes)

    else:
        item_bytes = bytes(item, 'utf-8')
        decrypted = f.decrypt(item_bytes)

    return decrypted
