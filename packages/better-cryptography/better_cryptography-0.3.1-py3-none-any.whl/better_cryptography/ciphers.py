"Script for encrypting/decrypting files and folders."

import os
import rsa
import string
import secrets
import hashlib as hash
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Protocol.KDF import PBKDF2
from cryptography.fernet import Fernet
from random import randbytes, shuffle


def hash_(StringToHash=str, hash_code = str, return_type = "hex") -> str:
    """
    Miscellenious function for implementing hash algorithms.

    currently supported hashes are:
    
    SHA 224 / CODE = SHA224
    
    SHA 256 / CODE = SHA256
    
    SHA 512 / CODE = SHA512
    
    MD5 / CODE = MD5
    """
    if hash_code == "SHA224":
        hash_obj = hash.sha224(StringToHash.encode())
        if return_type == "bytes":
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    if hash_code == "SHA256":
        hash_obj = hash.sha256(StringToHash.encode())
        if return_type == "bytes":
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    if hash_code == "SHA512":
        hash_obj = hash.sha512(StringToHash.encode())
        if return_type == "bytes":
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    if hash_code == "MD5":
        hash_obj = hash.md5(StringToHash.encode())
        if return_type == "bytes":
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()


def random_choice(list):
    chosen = secrets.choice(list)
    return chosen


def compare_hashes(hash_1=str, hash_2=str):
    """
    hash comparision function. 

    Takes 2 strings and compares them to see if they are the same.
    returns a boolean value in such a way to reduce timing attack efficacy.
    """
    result = secrets.compare_digest(hash_1, hash_2)
    return result


def token_generation(size=int, return_type = str):
    """
    Simplifed method for interfacing with the secrets module.

    return_type: What is being returned. modes are 'URL', 'HEX', and 'BYTES'
    
    size: the number of bytes in the token to be generated.
    """
    if return_type == "HEX":
        token = secrets.token_hex(size)
        return token
    if return_type == "BYTES":
        token = secrets.token_bytes(size)
        return token
    if return_type == "URL":
        token = secrets.token_urlsafe(size)
        return token


def gen_random_password(length=int):
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    shuffle(characters)
    password = []
    for i in range(length):
        password.append(secrets.choice(characters))
    shuffle(password)
    final_password = "".join(password)
    return final_password


def sec_delete(file_path, random_fill = True, null_fill = True, passes = 35) -> int:
    """
    Secure file deletion function with overwriting and null filling.

    It is best practice to combine this with another secure file deletion protocol.
    """
    if "/home/" not in file_path or "/." in file_path:
        return 1
    else:
        with open (file_path, "wb") as file:
            data = file.read()
        length = len(data)
        if random_fill is True:
            for _ in passes:
                with open(file_path, "wb") as file:
                    file.write(randbytes(length))
        if null_fill is True:
            for _ in passes:
                with open (file_path, "wb") as file:
                    file.write("\x00" * length)
        return 0


def delete(path):
    """
    File deletion function.
    """
    if '/home/' not in path or "/." in path:
        return 1
    else:
        os.system("rm {}".format(path))


class Ciphers:
    """
    A class for ciphering/deciphering operations.

    Linux native.

    Parameters:
        Username: The Linux username of the user who is logging in.
        Password: The password of the user.
    """


    def __init__(self, password=str) -> None:
        self.password = password
        self.marker  = b"E1m%nj2i$bhilj"


    # misc methods


    def generate_symmetric_key(self, salt) -> 'tuple[bytes, bytes]':
        "Method for generating keys. Will return tuple (key, salt) if salt is not provided."
        if salt is None:
            salt_ = os.urandom(32)
            key = PBKDF2(self.password, salt_, dkLen=32)
            return key, salt
        else:
            key = PBKDF2(self.password, salt, dkLen=32)
            return key


    def generate_FerNet_key():
        key = Fernet.generate_key()
        return key


    def check_path_validity(self, path=str or None, decrypting=bool, type_=str) -> int:
        """
        A guard clause for file operations.

        Return codes:
            0: File path is suitable.
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

    
    def change_encrypting_password(self, old_password = str, new_password = str):
        if self.password == old_password:
            self.password = new_password


    # RSA methods 


    def generate_RSA_keys(self):
        "method to generate a public/private key pair for RSA encryption."
        public_key, private_key = rsa.newkeys(4096)
        return (public_key, private_key)


    def RSA_encrypt_str(self, public_key, str_=str):
        "method to encrypt a string with a RSA public key."
        encrypted_string = rsa.encrypt(str_.encode(), public_key)
        return encrypted_string


    def RSA_decrypt_str(self, private_key, encrypted_str=str):
        "Method to decrypt a string with a RSA private key."
        decrypted_string = rsa.decrypt(encrypted_str, private_key).decode()
        return decrypted_string


        # AES methods


    def AES_encrypt_file(self, path=str) -> int:
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
        # encryption for single file
        if os.path.isfile(path) is True:
            # checking if the file path is ok
            return_code = self.check_path_validity(path, decrypting=False, type_="AES")
            if return_code != 0:
                return return_code
                # generating a key and key signature
            salt = os.urandom(32)
            iv = os.urandom(16)
            key_and_salt = self.generate_symmetric_key(salt=None)
            key = key_and_salt[0]; salt = key_and_salt[1]
            key_hash = hash.sha256(key); key_signature = key_hash.digest()
            # getting the data and setting a cipher (using CFB to avoid padding.)
            with open (path, "rb") as file:
                data = file.read()
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            # ciphering and writing
            ciphered_data = cipher.encrypt(data)
            with open(path, "wb") as file:
                file.write(b"AES")
                file.write(self.marker)
                file.write(iv)
                file.write(salt)
                file.write(key_signature)
                file.write(ciphered_data)
            return 0
        # encryption for directory.
        elif os.path.isdir(path) is True:
            # looping through files in dir
            for root, dirs, files in os.walk(path):
                for file in files:
                    # checking if each file is suitable for encryption
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(file_name, decrypting=False, type_='AES')
                    if return_code != 0:
                        continue
                    salt = os.urandom(32)
                    iv = os.urandom(16)
                    key_and_salt = self.generate_symmetric_key(salt=None)
                    key = key_and_salt[0]; salt = key_and_salt[1]
                    key_hash = hash.sha256(key); key_signature = key_hash.digest()
                    # getting data and setting cipher
                    with open (file_name, "rb") as file:
                        data = file.read()
                    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                    # ciphering and writing.
                    ciphered_data = cipher.encrypt(data)
                    with open(file_name, "wb") as file:
                        file.write(self.marker)
                        file.write(iv)
                        file.write(salt)
                        file.write(key_signature)
                        file.write(ciphered_data)
            return 0


    def AES_decrypt_file(self, path=str) -> int:
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
        # decryption for single file
        if os.path.isfile(path) is True:
            # checking if file is suitable
            return_code = self.check_path_validity(path, decrypting=True, type_="AES")
            if return_code != 0:
                return return_code
                # gathering needed data
            with open (path, "rb") as file:
                file.read(3)
                file.read(14)
                iv = file.read(16)
                salt = file.read(32)
                file_signature = file.read(32)
                ciphered_data = file.read()
                # building key and key hash, then comparing key hash to file signature
            key = self.generate_symmetric_key(salt=salt)
            key_hash = hash.sha256(key); key_signature = key_hash.digest()
            if file_signature != key_signature:
                return 6
            # setting cipher and decrypting the data
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            original_data = cipher.decrypt(ciphered_data)
            # writing
            with open(path, "wb") as file:
                file.write(original_data)
            return 0
        # directory decryption
        elif os.path.isdir(path) is True:
            # looping through files
            for root, dirs, files in os.walk(path):
                for file in files:
                    # checking if file is suitable
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(file_name, decrypting=True)
                    if return_code != 0:
                        continue
                    # gathering needed data
                    with open (file_name, "rb") as file:
                        file.read(14)
                        iv = file.read(16)
                        salt = file.read(32)
                        file_signature = file.read(32)
                        ciphered_data = file.read()
                    # building key/key hash and comparing to file signature
                    key = self.generate_symmetric_key(salt=salt)
                    key_hash = hash.sha256(key); key_signature = key_hash.digest()
                    if key_signature != file_signature:
                        continue
                    # building the cipher and decrypting the data
                    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                    original_data = cipher.decrypt(ciphered_data)
                    # decrypting
                    with open (file_name, "wb") as file:
                        file.write(original_data)
            return 0
        

    def AES_encrypt_string():
        pass


    def AES_decrypt_string():
        pass


    # Blowfish methods


    def BLO_encrypt_file(self, path=str):
        """
        A method for encrypting a file using the Blowfish encryption algorithm.
        """
        # file encryption
        if os.path.isfile(path) is True:
            # checking if file is suitable
            return_code = self.check_path_validity(path, decrypting=False, type_="BLO")
            if return_code != 0:
                return return_code
            # generating a key, salt, and key signature
            key_and_salt = self.generate_symmetric_key(salt=None)
            key = key_and_salt[0]; salt = key_and_salt[1]
            key_hash = hash.sha256(key); key_signature = key_hash.digest()
            iv = os.urandom(8) # generating IV (blowfish only takes 8)
            # getting data and setting the cipher
            with open (path, "rb") as file:
                data = file.read()
            cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
            # encrypting the data and writing.
            ciphered_data = cipher.encrypt(data)
            with open (path, "wb") as file:
                file.write(b"BLO")
                file.write(self.marker)
                file.write(iv)
                file.write(salt)
                file.write(key_signature)
                file.write(ciphered_data)
            return 0
        # directory encryption.
        elif os.path.isdir(path) is True:
            # looping through files in dir
            for root, dirs, files in os.walk(path):
                for file in files:
                    # checking if files are suitable
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(path, decrypting=False, type_="BLO")
                    if return_code != 0:
                        continue
                    # getting data from file
                    with open(file_name, "rb") as file:
                        data = file.read()
                    # generating a key and building a key signature
                    key_and_salt = self.generate_symmetric_key(salt=None)
                    key = key_and_salt[0]
                    salt = key_and_salt[1]
                    key_hash = hash.sha256(key); key_signature = key_hash.digest()
                    iv = os.urandom(8) # IV for cipher
                    # setting cipher and encrypting data
                    cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
                    ciphered_data = cipher.encrypt(data)
                    # writing
                    with open(file_name, "rb") as file:
                        file.write(b"BLO")
                        file.write(self.marker)
                        file.write(iv)
                        file.write(salt)
                        file.write(key_signature)
                        file.write(ciphered_data)


    def BLO_decrypt_file(self, path=str):
        """
        method for decrypting a file encrypted with the Blowfish encryption alogrithm
        """
        # file decryption
        if os.path.isfile(path) is True:
            # checking if file is suitable
            return_code = self.check_path_validity(path, decrypting=True, type_="BLO")
            if return_code != 0:
                return return_code
            # getting needed data
            with open (path, "rb") as file:
                file.read(3)
                file.read(14)
                iv = file.read(8)
                salt = file.read(32)
                file_signature = file.read(32)
                ciphered_data = file.read()
                # rebuilding the key and getting its signature
            key = self.generate_symmetric_key(salt=salt)
            key_hash = hash.sha256(key); key_signature = key_hash.hexdigest()
            if key_signature != file_signature:
                return 6
            # setting cipher and decrypting data
            cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
            # writing
            original_data = cipher.decrypt(ciphered_data)
            with open (path, 'wb') as file:
                file.write(original_data)
            return 0
        # directory decryption
        elif os.path.isdir(path) is True:
            # looping through files
            for root, dirs, files in os.walk(path):
                for file in files:
                    # checking if file is suitable
                    file_name = os.path.join(root, file)
                    return_code = self.check_path_validity(file_name, decrypting=True, type_="BLO")
                    if return_code != 0:
                        continue
                    # getting data
                    with open (file_name) as file:
                        file.read(3)
                        file.read(14)
                        iv = file.read(8)
                        salt = file.read(32)
                        file_signature = file.read(32)
                        ciphered_data = file.read()
                    # building key and key signature
                    key = self.generate_symmetric_key(salt)
                    key_hash = hash.sha256(key); key_signature = key_hash.hexdigest()
                    if key_signature != file_signature:
                        continue
                    # setting the cipher and decrypting
                    cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
                    original_data = cipher.decrypt(ciphered_data)
                    # writing the data
                    with open (file_name, "wb") as file:
                        file.write(original_data)


    def BLO_encrypt_string(self, key=bytes or None, string_=str):
        """
        Method for encrypting strings using the Blowfish encryption alogrithm.
        returns a tuple of (ciphered_string, iv, salt)
        """
        if key is None:
            salt = os.urandom(32)
            key = self.generate_symmetric_key(salt)
        iv = os.urandom(8)
        cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
        ciphered_string = cipher.encrypt(string_)
        return (ciphered_string, iv, key)


    def BLO_decrypt_string(self, encrypted_string=str, key=bytes, iv=bytes):
        """
        Method for encrypting strings using the Blowfish encryption alogrithm.
        returns a tuple of (ciphered_string, iv, salt)
        """
        if key is None:
            return 1
        cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv=iv)
        decrypted_string = cipher.decrypt(encrypted_string)
        return (decrypted_string)

    # FerNet methods


    def FerNet_encrypt_file(self, path=str, key = str or None):
        if os.path.isfile(path) is True:
            return_code = self.check_path_validity(path, decrypting=False, type_="FER")
            if return_code != 0:
                return return_code
            if key is None:
                key = self.generate_FerNet_key()
            f = Fernet(key)
            with open(path, "rb") as file:
                data = file.read()
            encrypted_data = f.encrypt(data)
            with open (path, "wb") as file:
                file.write(b"FER")
                file.write(self.marker)
                file.write(encrypted_data)
            return 0
        if os.path.isdir(path) is True:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    return_code = self.check_path_validity(file_path, decrypting=False, type_="FER")
                    if key is None:
                        key = self.generate_FerNet_key()
                    f = Fernet(key)
                    with open (file_path, "rb") as file:
                        data = file.read()
                    encrypted_data = f.encrypt(data)
                    with open(path, "wb") as file:
                        file.write(b"FER")
                        file.write(self.marker)
                        file.write(encrypted_data)
            return 0
    

    def FerNet_decrypt_file(self, path=str, key=bytes):
        if os.path.isfile(path) is True:
            return_code = self.check_path_validity(path, decrypting=True, type_="FER")
            if return_code != 0:
                return return_code
            f = Fernet(key)
            with open(path, "rb") as file:
                file.read(3)
                file.read(14)
                ciphered_data = file.read()
            decrypted_data = f.decrypt(ciphered_data)
            with open(path, 'wb') as file:
                file.write(decrypted_data)
            return 0
        if os.path.isdir(path) is True:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    return_code = self.check_path_validity(file_path, decrypting=True, type_="FER")
                    if return_code != 0:
                        return return_code
                    f = Fernet(key)
                    with open(file_path, "rb") as file:
                        file.read(3)
                        file.read(14)
                        ciphered_data = file.read()
                    decrypted_data = f.decrypt(ciphered_data)
                    with open(file_path, 'wb') as file:
                        file.write(decrypted_data)
            return 0
    

    def FerNet_encrypt_string(self, key = str or None, bstring=bytes):
        if key is None:
            key = self.generate_FerNet_key()
        f = Fernet(key)
        encrypted_text = f.encrypt(bstring)
        return encrypted_text


    def FerNet_decrypt_string(self, key=bytes, encrypted_string=bytes):
        if key is None:
            return 1
        f = Fernet(key)
        decrypted_text = f.encrypt(encrypted_string)
        return decrypted_text
