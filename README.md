# Fall 2022 - Shopify Data Engineer Intern Challenge Question

## Description
This project is built to demonstrate a potential backend functionality of an image repository. It supports single/bulk uploads, private/public permissions, and secure storage.

### Design Overview
Hierarchical Data Format version 5 (HDF5) is a compressed file format designed to support big data. It also offers self-describing object types, Groups and Datasets. Groups act as folder-like entities, while Datasets are comparable to files. Additionally, some highlighted features include its ability to support complex, heterogenous data, as well as data slicing to prevent complete reading of large files.

#### Repository Initiation
To start, the hdf5 file and the encryption key must be initialized with the create_data_file function in sample/photorepo.py. The function takes the desired file path for each of the listed files as parameters and writes them accordingly.

![Upload](/assets/Upload.svg)
![Retrieve](/assets/Retrieve.svg)

#### Add Image
After the hdf5 file and the encryption key are initialized, we can start adding images. This current prototype supports single and batch uploads with the add_image function in sample/photorepo.py. In order to upload to the photo repository, the username, file path, file name (optional), permissions, hdf5 file path and the encryption key path must be defined as parameters for the function.

#### Hashing Based Distribution
The hdf5 image repository structure is based on hashing. A hash is generated using the concatenation of the user and file name, with the first two characters dictating the Group name in which the image will be saved. The rest of the hash is reserved for the Dataset name. This method was chosen to mitigate an unbalanced distribution of Groups and Datasets, as well as to promote the quick lookup and subsequent retrieval of images.

![Hashing](/assets/Hashing.svg)

#### Encrytion at Rest
Following the Group and Dataset name designations, the image and its associated metadata is encrypted at rest using Fernet. After encryption, the image is saved as a Dataset, while the metadata is embedded within it.


#### Unit tests
1. Batch upload with public permissions
   - Retrieval from user that uploaded image
   - Retrieval from user that did not upload image

2. Batch upload with private permissions
   - Retrieval from user that uploaded image
   - Retrieval from user that did not upload image

3. Batch upload with public permissions
   - Retrieval from user that uploaded image
   - Retrieval from user that did not upload image

4. Batch upload with private permissions
   - Retrieval from user that uploaded image
   - Retrieval from user that did not upload image


### Roadmap
#### Hash Value Collision
Current implementation assumes that collisions are an update from the same user. In other words, it will look to "update" a previously uploaded file. However, in future implementations, will have to look mitigate possible collisions between different users as to not overwrite saved files.

#### Encryption
Improve on current encryption capabilities. Some possible directions include generating keys for each Dataset, as well as storing keys in a secure location.

#### HTTPS over TLS, HTTPS over SSL
Support secure upload of images and associated data from client to web server.

## Getting Started
The entire pipeline was built using python, leveraging the HDF5 software library. The HDF5 file format was chosen for its efficient processing and storage capabilities.

### Dependencies
- python3.10
- hdf5

For MacOS and Linux users, run the following command to download the HDF5 library.
```
brew install hdf5
```

For other OS users, visit https://www.hdfgroup.org/downloads/hdf5/ for HDF5 download and configuration.

In order to download all the required python packages, run the following command.
```
pip install -r requirements.txt
```

### Installation
```
git clone https://github.com/monicahzchung/photorepository
```
