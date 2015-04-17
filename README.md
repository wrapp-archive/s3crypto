# s3Crypto

This module provides a set of functions to encrypt and decrypt data in S3 using an encryption key.

The encryption key is in its turn encrypted using KMS and stored in S3.


## Provided functionality:

* Create a data encryption key using KMS and store it in S3:

    ```create_dek(kek_alias, dek_path)```


* Use a data encryption key to encrypt data already in S3:

    ```encrypt_in_s3(data_path, key_path)```


* Use a data encryption key to store data encrypted in S3:

    ```save_encrypted_to_s3(data, data_path, key_path)```


* Use a data encryption key to decrypt data in S3:

    ```get_decrypted_from_s3(data_path, key_path)```
