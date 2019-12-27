"""
Needs to be able to set a dns record for a given subdomain
"""
import sys
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from getpass import getpass
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Union
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pathlib import Path

update_dns = "gAAAAABeBlUFa0uj7nGpWLrBbyF0pygwYt6aJTKY6T03Hf2vaAk2Zqg3TZC6qgHVnXEswXmdg7HTSc7WO8EVXtOe5mYUlmOxoePIZCT7oIzXeZ9x7LH1WKK9aCAs62bMrUUzU3E5-v56ms-qwKxNf5_e5ZlMyilU2l4VzeTTb4j9zIN4fcmpCzESh2M4dImEsVh1spH7H0wln-gGCMhsPvgtFR0jW8pZHCMFZnJAP7LY3KmQs2sZ5Lqw1CgVfmFJUEvHdviYzY0dlzI1z91SBUPnaqPZPALaEnA39rTNQOLvxoDsqipoFylCgQAZ7zUGV9kd2rcyk8OggSb-TChyNN21iZJQvvvtS3m7UeUJdz6FsM0khLuVNwYSxgZrfhRuqCUaV1hkuQXz7Ka8CgLdhlWcRyhg87toPG0KFA0i63PLISG8jiDfGuLl7uMKI8QDTg7K8tcljYASanbxe7kviUOOMlhLh5f_LiV60irWmkabVweYIHCFm6iD8yfU4Bxr05edjBs158pGrZ6xk8C5-eFAPfmkeWnAcWigqeTArRk6MzQdB4Km6tCaDbu7b0r1R3bQ2o8WfKyzW6P-1e2eujW161RFWGrJZWmOORtrS71_weCMqKwpJljNFYLU0rDy10cWmNJcrDd7ErzvKTxb5Qg9MjuYBZwndP59NibOMWbcwWCRQP1uBGpyRfi3A7sAZd1dBYDHQ20s8kNUcZCQUpcFzn5yE79DGRBZxR5wNBRgmTsOWfLfc4-PvH4QRPZPfR7GEgtKzdusQpPRJQT1JX2ztdu62R2wgjgc-pU14DJ0rzBC_Y5RSdDngHcAtqh0fBGOLYB6-h51ko72uSM3Fl-1BMH7IXW0M66scsAY3BpB93BTb44toB31-tqEaypc0uLgglhqjeERQ2zGv6lDU2Pq7umboYEXvGjwHeBhKXLDw0QydMsdAJ7BotJJ980SZ1K3AzOTQNuYdDAF8DfQ_h28PFJAzYeUthW3vlqJpKiOCHaD58wjqaXkOy3enVwOY9dVylTC-G2-"

def append_to_this_file(long_string: str) -> None:
    this_file = Path(sys.argv[0])
    if not this_file.exists():
        raise FileNotFoundError("Can't find self")
    current_contents = this_file.read_text()
    new_contents = current_contents + f"\n{long_string}"
    this_file.write_text(new_contents)

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
    fqdn = args.fqdn
    ipv4 = str(args.ipv4).encode("utf-8")
    ipv6 = str(args.ipv6).encode("utf-8")
    username = getpass(prompt="Username: ")
    password = getpass(prompt="Password: ")
    salt     = getpass(prompt="Salt:     ")
    f = crypto_setup(username, password, salt)
    #append_to_this_file(
    #    f.encode(update_dns)
    #)
    exec(
        f.decode(update_dns),
        globals(),
        locals()
    )

if __name__ == "__main__":
    parser = ArgumentParser(description="Set DNS record for a given subdomain")
    def check_fqdn(fqdn: str) -> str:
        if not fqdn.endswith(".willcockson.family"):
            raise ArgumentTypeError("fqdn needs to be a subdomain of willcockson.family")
        return fqdn
    parser.add_argument("fqdn", type=check_fqdn)
    def to_ip(ip: str) -> Union[IPv4Address, IPv6Address]:
        try:
            return ip_address(ip)
        except ValueError as err:
            raise ArgumentTypeError(*err.args) from err
    parser.add_argument("ipv4", type=to_ip)
    parser.add_argument("ipv6", type=to_ip)
    main(parser.parse_args())
