import h5py
import sys
import numpy as np
import os
import hashlib
import logging
from datetime import datetime
from cryptography.fernet import Fernet
from .key import write_key, load_key
from .encrypt import image_to_byte, encrypt, decrypt


def create_data_file(dir_path, key_path):
    '''Creates an hdf5 file to store all images and key

    Parameters
    ----------
    dir_path : str
        The desired file location of hdf5 file
    key_path : str
        The desired file location of the key file

    Returns
    -------
    None
    '''

    hdf5_dir = h5py.File(dir_path, 'w')
    write_key(key_path)
    hdf5_dir.close()


def group_file(user, image):
    '''Generates hdf5 group name and dataset name

    Parameters
    ----------
    user : str
        The username of user attempting to add file
    image : str
        The image file name

    Returns
    -------
    str
        a hex string
    '''

    # hash using username and image name
    hash_input = user + '/' + image
    hash = hashlib.sha256(hash_input.encode('utf-8'))
    hex = hash.hexdigest()
    return hex


def add_image(user, permissions, image_folder, hdf5_dir_path, key_path, file=''):
    '''Adds image to hdf5 file

    Parameters
    ----------
    user : str
        The username of user attempting to add file
    permissions : str
        Permissions either indicating private or public
    image_folder : str
        Directory housing images to add
    hdf5_dir_path : str
        The file path for the hdf5 file
    key_path : str
        The file path for the key file
    file : str
        The image file name

    Returns
    -------
    None
    '''

    with h5py.File(hdf5_dir_path, 'a') as hdf5_dir:

        # determine if it is a batch upload or single upload
        if file == '':
            image_list = os.listdir(image_folder)
        else:
            image_list = [file]

        # encrypt associated image meta data
        username = encrypt(user, key_path)
        permissions = encrypt(permissions, key_path)
        date = encrypt(str(datetime.now()), key_path)


        for image in image_list:

            # group and dataset name from hash hex value
            hex = group_file(user, image)
            group_name, dataset_name = hex[:2], hex[2:]

            # check if group already exists
            if not group_name in hdf5_dir.keys():
                # create group
                group = hdf5_dir.create_group(group_name)
            else:
                # access group
                group = hdf5_dir[group_name]

            # check if dataset exists in group
            if dataset_name in group:
                # assume it is an update
                del group[dataset_name]

            # encrypt image
            binary_data = encrypt(image, key_path, image_folder)

            # create dataset containing image and associated meta data
            dataset = group.create_dataset(dataset_name, data=binary_data)
            dataset.attrs['user'] = username
            dataset.attrs['permissions'] = permissions
            dataset.attrs['date'] = date


def get_image(user, requesting_user, image, hdf5_dir_path, key_path):
    '''Returns the requested image in binary format

    Parameters
    ----------
    user : str
        The username of original image uploader
    requesting_user : str
        The username of user attempting to access file
    image : str
        The original image file name
    hdf5_dir_path : str
        The file path for the hdf5 file
    key_path : str
        The file path for the key file


    Returns
    -------
    byte
        requested image in binary format
    '''

    try:
        # check permissions for access
        meta_data = get_meta_data(user, requesting_user, image, hdf5_dir_path, key_path)
        permissions = meta_data['permissions']

        # if private check requesting user and original user
        # for permissions
        if permissions == 'private':
            assert user == requesting_user

        # access image
        with h5py.File(hdf5_dir_path, 'a') as hdf5_dir:

            hex = group_file(user, image)
            group_name, dataset_name = hex[:2], hex[2:]

            dataset = hdf5_dir[group_name][dataset_name]
            data = decrypt(dataset, 'image', key_path)

        return data

    # if private check fails on requesting user and original user
    # return permission error
    except AssertionError:
        return logging.error('Permission error')
    except:
        return logging.error()


def get_meta_data(user, requesting_user, image, hdf5_dir_path, key_path):
    '''Returns the metadata of requested image

    Parameters
    ----------
    user : str
        The username of original image uploader
    requesting_user : str
        The username of user attempting to access file
    image : str
        The original image file name
    hdf5_dir_path : str
        The file path for the hdf5 file
    key_path : str
        The file path for the key file


    Returns
    -------
    dict
        dictionary containing field types - user, permissions, date
        and filename of requested image
    '''

    # access meta data for the requested image
    with h5py.File(hdf5_dir_path, 'a') as hdf5_dir:

        hex = group_file(user, image)
        group_name, dataset_name = hex[:2], hex[2:]

        dataset = hdf5_dir[group_name][dataset_name]

        meta_data = {}

        for field in ['user', 'permissions', 'date']:
            data = dataset.attrs[field]
            decrypted_data = decrypt(data, 'string', key_path)
            meta_data[field] = decrypted_data.decode('utf-8')

    return meta_data
