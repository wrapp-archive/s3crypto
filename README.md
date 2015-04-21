# s3Crypto

This module provides a set of functions to encrypt and decrypt data in S3 using a Data Encryption Key (DEK).
The encryption key is in its turn encrypted using KMS and stored in S3.
S3_paths must include s3 scheme, t.ex. ```s3://bukect/key```.

## Provided functionality:

* Generate a new DEK with KMS using the KEK with kek_alias and store it at s3_path:

    ```create_dek(kek_alias, s3_path)```


* Get data at s3_data_path, encrypt it with DEK at s3_key_path, and store it at s3_data_path.enc:

    ```encrypt_in_s3(s3_data_path, s3_key_path)```


* Save data at s3_data_path encrypted with DEK at s3_key_path:

    ```save_encrypted_to_s3(data, s3_data_path, s3_key_path)```


* Get data at s3_data_path and decrypt it using DEK at s3_key_path:

    ```get_decrypted_from_s3(s3_data_path, s3_key_path)```
