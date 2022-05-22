from context import sample
from sample.photorepo import add_image, get_image, get_meta_data, image_to_byte, create_data_file
import unittest
import logging
import sys

# users
user1, user2 = 'bob123', 'tom123'

# permissions
public_permissions, private_permissions = 'public', 'private'

# folders
public_batch_folder = sys.path[0] + '/tests/photos/batch/public/'
private_batch_folder = sys.path[0] + '/tests/photos/batch/private/'
single_folder = sys.path[0] + '/tests/photos/single/'

# images
batch_image_public = '._chris-barbalis--nYBR0LFTvQ-unsplash.jpg'
batch_image_private = '._matt-duncan-IUY_3DvM__w-unsplash.jpg'
single_image_public = 'jakob-owens-1_0KyvVdtP4-unsplash.jpg'
single_image_private = 'photo-1489389944381-3471b5b30f04.jpeg'

# database file path
hdf5_dir_path = sys.path[0] + '/tests/hdf5/photo.hdf5'

# key file path
key_path = sys.path[0] + '/tests/key/'


class TestPhotoRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create database
        create_data_file(hdf5_dir_path, key_path)

        # add batch public
        add_image(user1, public_permissions,
            public_batch_folder, hdf5_dir_path, key_path)

        # add batch private
        add_image(user2, private_permissions,
            private_batch_folder, hdf5_dir_path, key_path)

        # add single public
        add_image(user2, public_permissions,
            single_folder, hdf5_dir_path, key_path, single_image_public)

        # add single private
        add_image(user1, private_permissions,
            single_folder, hdf5_dir_path, key_path, single_image_private)


    def test_batch_public(self):
        # same user
        self.assertEqual(get_image(user1, user2, batch_image_public, hdf5_dir_path, key_path),
            image_to_byte(batch_image_public, public_batch_folder))
        # another user
        self.assertEqual(get_image(user1, user2, batch_image_public, hdf5_dir_path, key_path),
            image_to_byte(batch_image_public, public_batch_folder))

    def test_batch_private(self):
        # same user
        self.assertEqual(get_image(user2, user2, batch_image_private, hdf5_dir_path, key_path),
            image_to_byte(batch_image_private, private_batch_folder))
        # another user
        self.assertEqual(get_image(user2, user1, batch_image_private, hdf5_dir_path, key_path),
            logging.error('Permission error'))

    def test_single_public(self):
        # same user
        self.assertEqual(get_image(user2, user2, single_image_public, hdf5_dir_path, key_path),
            image_to_byte(single_image_public, single_folder))
        # another user
        self.assertEqual(get_image(user2, user1, single_image_public, hdf5_dir_path, key_path),
            image_to_byte(single_image_public, single_folder))

    def test_single_private(self):
        # same user
        self.assertEqual(get_image(user1, user1, single_image_private, hdf5_dir_path, key_path),
            image_to_byte(single_image_private, single_folder))
        # another user
        self.assertEqual(get_image(user1, user2, single_image_private, hdf5_dir_path, key_path),
            logging.error('Permission error'))


if __name__ == '__main__':
    unittest.main()
