import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode, b64encode, b64decode

# dfile = 'advance-file-arranger'

app_current_folder = os.path.abspath(".")

class Ecyper():
    def __init__(self, passphrase= b"m9999999oftware@@@$%^%$##$%^^", salt=b"m767788alt03odoee3", keyname= 'dkey.key'):
        self.keyname = keyname
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(passphrase)
        # Base64-encode the key in URL-safe format
        key_b64 = urlsafe_b64encode(key)
        # Create a Fernet instance with the key_b64
        self.fernet = Fernet(key_b64)
        # Generate a random encryption key to encrypt the data

    def create_key(self):
        # Save the encrypted key to a file
        # os.path.join(app_current_folder,  dfile + "-health.key")
        # create the raw file
        if not os.path.exists(self.keyname):
            encryption_key = Fernet.generate_key()
            # Encrypt the encryption key using the passphrase-derived key
            encryptedkey = self.fernet.encrypt(encryption_key)
        
            with open(self.keyname, "wb") as key_file:
                key_file.write(encryptedkey)
            
        return True
        
    def read_key(self):
        encrypt_code, decrypted_key = '', ''
        # Load the encrypted key from the file
        with open(self.keyname, "rb") as key_file:
            encrypt_code = key_file.read()
        
        if encrypt_code:
            # Decrypt the encryption key using the passphrase-derived key
            decrypted_key = self.fernet.decrypt(encrypt_code)
        return decrypted_key
    
    def enc(self, rawfile, newfile=""):
        if os.path.exists(rawfile):
            raw_content = b''
            with open(rawfile, "rb") as raw:
                raw_content = raw.read()
                
            if raw_content:
                # get new name
                if not newfile:
                    nfile, ext = os.path.splitext(rawfile)
                    newfile = nfile + '-raws.key'
                    
                encrypted_script = self.fernet.encrypt(raw_content)
                with open(newfile, 'wb') as file:
                    file.write(encrypted_script)
                    
        return newfile
    
    def enc_read(self, encdodedfile):
        if os.path.exists(encdodedfile):
            raw_content = ''
            with open(encdodedfile, "rb") as raw:
                raw_content = raw.read()
                
            decrypted_script = self.fernet.decrypt(raw_content).decode()
            # print(decrypted_script)
            # print(type(decrypted_script))

            # exec(decrypted_script)
            return decrypted_script


