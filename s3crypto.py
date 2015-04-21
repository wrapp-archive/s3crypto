import os
from boto.s3 import connect_to_region as connect_to_s3
from boto.kms import connect_to_region as connect_to_kms
from boto.s3.key import Key
import nacl.utils
import nacl.secret


REGION = os.environ.get('AWS_REGION', 'eu-west-1')


def bucket_and_key_from_path(s3_path):
    from urlparse import urlparse

    parts = urlparse(s3_path)
    assert parts.scheme == 's3', 'Only S3 paths supported (starting with s3://)'
    bucket = parts.netloc
    key = parts.path[1:]
    return bucket, key


def generate_encrypted_dek(kek_alias):
    ''' Generate a DEK with KMS using the KEK with kek_alias '''
    dek_data = connect_to_kms(REGION).generate_data_key_without_plaintext(kek_alias, key_spec='AES_256')
    return dek_data['CiphertextBlob']


def get_decrypted_with_kms(path):
    ''' Get data at path and decrypt it with KMS '''
    enc_dek = get_from_s3(path)
    dek = connect_to_kms(REGION).decrypt(enc_dek)['Plaintext']
    return dek


def encrypt_with_key(data, key):
    ''' Encrypt data with key using nacl '''
    box = nacl.secret.SecretBox(key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    return box.encrypt(data, nonce)


def decrypt_with_key(data, key):
    ''' Decrypt data with key using nacl '''
    box = nacl.secret.SecretBox(key)
    return box.decrypt(data)


def get_from_s3(s3_path):
    ''' Get data at s3_path '''
    bucket, key = bucket_and_key_from_path(s3_path)
    b = connect_to_s3(REGION).get_bucket(bucket)
    data = b.get_key(key).get_contents_as_string()
    return data


def save_to_s3(s3_path, data):
    ''' Save data at s3_path '''
    bucket, key = bucket_and_key_from_path(s3_path)
    b = connect_to_s3(REGION).get_bucket(bucket)
    k = Key(b)
    k.key = key
    k.set_contents_from_string(data)


def create_dek(kek_alias, s3_path):
    ''' Generate a new DEK with KMS using the KEK with kek_alias and store it at s3_path '''
    enc_dek = generate_encrypted_dek(kek_alias)
    save_to_s3(s3_path, enc_dek)


def get_decrypted_from_s3(s3_data_path, s3_key_path):
    ''' Get data at s3_data_path and decrypt it using DEK at s3_key_path '''
    key = get_decrypted_with_kms(s3_key_path)
    enc_data = get_from_s3(s3_data_path)
    data = decrypt_with_key(enc_data, key)
    return data


def save_encrypted_to_s3(data, s3_data_path, s3_key_path):
    ''' Save data at s3_data_path encrypted with DEK at s3_key_path '''
    key = get_decrypted_with_kms(s3_key_path)
    enc_data = encrypt_with_key(data, key)
    save_to_s3(s3_data_path, enc_data)


def encrypt_in_s3(s3_data_path, s3_key_path):
    ''' Get data at s3_data_path, encrypt it with DEK at s3_key_path,
        and store it at s3_data_path.enc '''
    data = get_from_s3(s3_data_path)
    enc_data_path = s3_data_path + ".enc"
    save_encrypted_to_s3(data, enc_data_path, s3_key_path)
