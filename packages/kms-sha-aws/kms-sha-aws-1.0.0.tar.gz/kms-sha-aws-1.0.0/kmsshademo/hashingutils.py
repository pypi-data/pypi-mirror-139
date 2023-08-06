import base64
import boto3
import hashlib

class hashingutils:

    def __init__(self):
        pass
    def getkmsEncryptedValue(self,val,keyid):
        session = boto3.session.Session()
        kms = session.client('kms')
        stuff = kms.encrypt(KeyId=keyid, Plaintext=val)
        binary_encrypted = stuff['CiphertextBlob']
        encrypted_password = base64.b64encode(binary_encrypted)
        return encrypted_password

    def getkmsDecryptedValue(self,encryptedValue):
        session = boto3.session.Session()
        kms = session.client('kms')
        binary_data = base64.b64decode(encryptedValue)
        meta = kms.decrypt(CiphertextBlob=binary_data)
        plaintext = meta['Plaintext']
        return plaintext.decode()

    def getSha256Value(self,val):
        result = hashlib.sha256(val.encode())
        return result.hexdigest()