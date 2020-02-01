"""
Encrypts file found at path on command line using, prints out string
"""
import sys
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from getpass import getpass
from typing import Union
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pathlib import Path

def crypto_setup(username: str, password: str, salt: str) -> str:
    kdf = Scrypt(
        salt=salt.encode("utf-8"),
        length=32,
        n=2**16,
        r=8,
        p=1,
        backend=default_backend(),
    )
    key = urlsafe_b64encode(
        kdf.derive(
            f"{username}{password}".encode("utf-8")
        )
    )
    f = Fernet(key)
    def encode(string: str) -> str:
        return f.encrypt(
            string.encode("utf-8")
        ).decode("utf-8")
    def decode(string: str) -> str:
        return f.decrypt(
            string.encode("utf-8")
        ).decode("utf-8")
    f.encode = encode
    f.decode = decode
    return f

def main(args: Namespace) -> None:
    path = args.path
    username = getpass(prompt="Username: ")
    password = getpass(prompt="Password: ")
    salt     = getpass(prompt="Salt:     ")
    f = crypto_setup(username, password, salt)
    if args.encrypt:
        print(f.encode(path.read_text()))
    else:
        print(f.decode(path.read_text()))

if __name__ == "__main__":
    parser = ArgumentParser(description="Encrypt or decrypt a file")
    def non_empty_file(path: str) -> Path:
        path = Path(path)
        if path.exists() and path.stat().st_size > 0:
            return path
        else:
            raise ArgumentTypeError("PATH needs to be a file with text")
    parser.add_argument("path", type=non_empty_file, help="The path to a file with text to be encrypted or decrypted")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--decrypt", action="store_true")
    group.add_argument("-e", "--encrypt", action="store_true")
    main(parser.parse_args())
