"Script for encrypting/decrypting files and folders."

import os
import rsa
from log import Log
import datetime as dt
import hashlib as hash
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Protocol.KDF import PBKDF2


class Ciphers:
    """
    A class for ciphering/deciphering operations.

    Linux native.

    Parameters:
        Username: The Linux username of the user who is logging in.
        Password: The password of the user.
    """


    def __init__(self, password=str, username=str) -> None:
        self.password = password
        self.username = username
        self.marker  = b"E1m%nj2i$bhilj"
        self.logger = Log(self.username)


    # misc functions


    def check_path_validity(self, path=str or None, decrypting=bool, type_=str) -> int:
        """
        A guard clause for file operations.

        Return codes:
            0: File path is good.
            1: File path is None.
            2: File path is invalid.
            3: App does not have permission to access file.
            4: File is hidden.
            5: File is part of root filesystem and not accessing chromeos.
            6: File encryption marker detected during encryption.
            7: File encryption marker not detected during decryption.
            8: File was encrypted with a different algorithm.
        """
        if path is None:
            return 1
        # checking if file is hidden
        if "/." in path:
            return 4
        # checking if file is part of the root filesystem and not a part of ChromeOS for linux in Chromebooks
        if "/home/" not in path and "/mnt/chromeos/MyFiles" not in path:
            return 5
        # checking if decrypt is cancelleD
        try:
            if os.path.isfile(path) is True:
                with open (path, "rb") as file:
                    type_of_file = file.read(3)
                    file_marker = file.read(14)
            elif os.path.isdir(path) is True:
                return 0
        # checking if file exists
        except FileNotFoundError:
            return 2
        # checking if application has permission
        except PermissionError:
            return 3
        # checking if there is a file encryption marker during encryption
        if file_marker == self.marker and decrypting is False:
            return 6
        # checking if there is not a file encryption marker during decryption
        elif file_marker != self.marker and decrypting is True:
            return 7
        if decrypting is True:
            if str(type_of_file) != type_:
                return 8
            else:
                return 0
        else:
            return 0


    def hash(self, StringToHash=str) -> str:
        # miscellaneous function for creating hashes.
        hash_obj = hash.sha256(StringToHash.encode())
        hash_ = hash_obj.hexdigest()
        return hash_

    
    def change_encrypting_password(self, old_password = str, new_password = str):
        if self.password == old_password:
            self.password = new_password


    # RSA functions 


    def generate_RSA_keys(self):
        "method to generate a public/private key pair for RSA encryption."
        public_key, private_key = rsa.newkeys(4096)
        return (public_key, private_key)


    def RSA_encrypt_str(self, public_key, str_=str):
        "method to encrypt a string with a RSA public key."
        encrypted_string = rsa.encrypt(str_.encode(), public_key)
        return encrypted_string


    def RSA_decrypt_str(self, private_key, encrypted_str):
        "Method to decrypt a string with a RSA private key."
        decrypted_string = rsa.decrypt(encrypted_str, private_key).decode()
        pass


        # AES functions


    def generate_symmetric_key(self, salt) -> 'tuple[bytes, bytes]':
        if salt is None:
            salt_ = os.urandom(32)
            key = PBKDF2(self.password, salt_, dkLen=32)
            return key, salt
        else:
            key = PBKDF2(self.password, salt, dkLen=32)
            return key


    def AESencrypt_file(self, path=str) -> int:
        """
        A method for encrypting a file/folder object.

        Takes only a file path as an argument.

        Return codes:
            0: File encrypt successful.
            1: Path is None.
            2: Path is invalid.
            3: App does not have permissions required to access file.
            4: File is hidden.
            5: File is part of root filesystem and not part of ChromeOS.
            6: File encryption marker detected during encryption.
        """
        return_code = self.check_path_validity(path, decrypting=False, type_="AES")
        if return_code != 0:
            return return_code
        salt = os.urandom(32)
        iv = os.urandom(16)
        key = PBKDF2(self.password, salt, dkLen=32)
        key_hash = hash.sha256(key); key_signature = key_hash.digest()
        if os.path.isfile(path) is True:
            with open (path, "rb") as file:
                data = file.read()
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            ciphered_data = cipher.encrypt(data)
            with open(path, "wb") as file:
                file.write(b"AES")
                file.write(self.marker)
                file.write(iv)
                file.write(salt)
                file.write(key_signature)
                file.write(ciphered_data)
            self.log("File : {} was encrypted at {}.".format(path, str(dt.datetime.utcnow)))
            return 0
        elif os.path.isdir(path) is True:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(file_name, decrypting=False, type_='AES')
                    if return_code != 0:
                        continue
                    with open (file_name, "rb") as file:
                        data = file.read()
                    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                    ciphered_data = cipher.encrypt(data)
                    with open(file_name, "wb") as file:
                        file.write(self.marker)
                        file.write(iv)
                        file.write(salt)
                        file.write(key_signature)
                        file.write(ciphered_data)
            self.log("Folder : {} was encrypted at {}.".format(path, str(dt.datetime.utcnow)))
            return 0


    def AESdecrypt_file(self, path=str) -> int:
        """
        A method for decrypting an encrypted file.

        Takes only a file path as an argument.

        return codes:
            0: File decrypt successful.
            1: Path is None.
            2: File path is invalid.
            3: App does not have permissions required to access file.
            4: File is hidden.
            5: File is part of root filesystem and not part of ChromeOS.
            6: File was encrypted with a different key.
            7: File was not encrypted.
            8: File was encrypted using a different alogorithm.
        """
        return_code = self.check_path_validity(path, decrypting=True, type_="AES")
        if return_code != 0:
            return return_code
        if os.path.isfile(path) is True:
            with open (path, "rb") as file:
                file.read(3)
                file.read(14)
                iv = file.read(16)
                salt = file.read(32)
                file_signature = file.read(32)
                ciphered_data = file.read()
            key = PBKDF2(self.password, salt, dkLen=32)
            key_hash = hash.sha256(key); key_signature = key_hash.digest()
            if file_signature != key_signature:
                return 6
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            original_data = cipher.decrypt(ciphered_data)
            with open(path, "wb") as file:
                file.write(original_data)
            return 0
        elif os.path.isdir(path) is True:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(file_name, decrypting=True)
                    if return_code != 0:
                        continue
                    with open (file_name, "rb") as file:
                        file.read(14)
                        iv = file.read(16)
                        salt = file.read(32)
                        file_signature = file.read(32)
                        ciphered_data = file.read()
                    key = PBKDF2(self.password, salt, dkLen=32)
                    key_hash = hash.sha256(key); key_signature = key_hash.digest()
                    if key_signature != file_signature:
                        continue
                    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                    original_data = cipher.decrypt(ciphered_data)
                    with open (file_name, "wb") as file:
                        file.write(original_data)
            return 0
        

        self.log()
        pass


    # Blowfish functions


    def BLOencrypt_file(self, path=str):
        """
        A method for encrypting a file using the Blowfish encryption algorithm.
        """
        return_code = self.check_path_validity(path, decrypting=False, type_="BLO")
        if return_code != 0:
            return return_code
        iv = os.urandom(8)
        keySalt = self.generate_symmetric_key(salt=None)
        key = keySalt[0]; salt = keySalt[1]
        key_hash = hash.sha256(key) ; key_signature = key_hash.hexdigest()
        if os.path.isfile(path) is True:
            with open (path, "rb") as file:
                data = file.read()
            cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
            ciphered_data = cipher.encrypt(data)
            with open (path, "wb") as file:
                file.write(b"BLO")
                file.write(self.marker)
                file.write(iv)
                file.write(salt)
                file.write(key_signature)
                file.write(ciphered_data)
        elif os.path.isdir(path) is True:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(path, decrypting=False, type_="BLO")
                    if return_code != 0:
                        continue
                    with open(file_name, "rb") as file:
                        data = file.read()
                    cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
                    ciphered_data = cipher.encrypt(data)
                    with open(file_name, "rb") as file:
                        file.write(b"BLO")
                        file.write(self.marker)
                        file.write(iv)
                        file.write(salt)
                        file.write(key_signature)
                        file.write(ciphered_data)


    def BLOdecrypt_file(self, path=str):
        return_code = self.check_path_validity(path, decrypting=True, type_="BLO")
        if return_code != 0:
            return return_code
        if os.path.isfile(path) is True:
            with open (path, "rb") as file:
                file.read(3)
                file.read(14)
                iv = file.read(8)
                salt = file.read(32)
                file_signature = file.read(32)
                ciphered_data = file.read()
                key = self.generate_symmetric_key(salt=salt)
                key_hash = hash.sha256(key); key_signature = key_hash.hexdigest()
                if key_signature != file_signature:
                    return 6
                cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
                original_data = cipher.decrypt(ciphered_data)
                with open (path, 'wb') as file:
                    file.write(original_data)
        elif os.path.isdir(path) is True:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(file_name, decrypting=True, type_="BLO")
                    if return_code != 0:
                        continue
                    with open (file_name) as file:
                        file.read(3)
                        file.read(14)
                        iv = file.read(8)
                        salt = file.read(32)
                        file_signature = file.read(32)
                        ciphered_data = file.read()
                    key = self.generate_symmetric_key(salt)
                    key_hash = hash.sha256(key); key_signature = key_hash.hexdigest()
                    if key_signature != file_signature:
                        continue
                    cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
                    original_data = cipher.decrypt(ciphered_data)
                    with open (file_name, "wb") as file:
                        file.write(original_data)