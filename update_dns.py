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

update_dns = "gAAAAABeNdeXpk07Nx9wAaHlkl0f9SJ6AHWrrkVMoY7K98M_WAEJSpP1odzjQwwXU6a61atBMWtnPlgnzoa2UJYxmSL0fkNNz3G3mWowZPYwcw-B2H0ArsA7xJN9GqufvlJ6xo4EXi6FIZ53u6h7P9raa554Fo1I3GT62bwiSkGYExp3xqfARmdi-NImfiOiKNQskIgYHW9zvpvwMEHxSIbSzdfbhVWBuIbFimz2vwwa8h4Ss65P1W1Es4JOO9q0jb73OAMYTOW2HkBqwqauOnppbgN4B_1RqLhe7wfQrX-tFHiW3DVRjzHhyzsA9JG8LdPowYOGG9MBVXpt10NbPAd0jmSL6rtcw-oQpXpvIOTKJdJFol7d-kuD8Y9bTbWnkya5HljXpzcPU1PRxCiwXilGKd3kBEUkMC15hw67JvC70BeVJTh1IPNWGKNp8A1uPqSUQBOvaCBBy4r0JZalxcD3PfA1akiCSa5YOjfXGYBryCuGGScv-S5ycnlyr7IWdeVCBaUKbfqi-o3hVUbuyAEqPGOG0gy2W-kL9p-FLCa_N7_bEe--7F6id6NogLZkmTzpA6cZQ3YU65LJUzzZUnh-fa2rNUPMxi30Tptq4f3GXOJW3rOFhbAL4dn0FlBvLR6RDejNVXWXqbmucmNfwDSgnoQqd2vx6ltfo4_lk2mv14hccSelBTKNlWeU9jFBB1zuqg4Bv5rTr0KNvrn9PVWjWg0He6UnCp77xiWyGpZk7XlbJn4uJu5QP0gtfCea75DzeC5jGqtD9Xuh-c9ulbBxs1syb4UtbRo2IM0M5zkDmO__uO5oNi-F27Ds0buEbz7x-cTjK5djSeQB4g7gGQtEyjZdFOr0Xi2XCm-D99WXMPlGvVIH8gQr3RN0xoRYdt3zU7eZVOpfMu7iwUR0mNTuqqFKtsur5fVoNQn7o-DdMJjNN1tFQ5zYf1ZQQnQ36XFAUI7kAYTuK-hOarUwc2BBBeOpvrmNqQJl5iCj73-aOB7R1G9XDCaXLgxe4URH-rB_UEGZzWDAbYl5U8KwkknaswjVrrCgkz43Yi1EdyW0pibgn51XLBYl302VhWq9LgUZBcTRF42MOpdvWXswojyz5cMca3qKKxew3bLHdA5_dpWD7xqHBtoL--uTkgbH19agmrCuGfmROu98fMqu0BdjegTM5N3kj1JTIpxXr5qKSBlsIQbFSeeCG7JRU_ALeZSV-aBzlQjEBdBQnHkglfe349f2ZqXDguTQ9uloztvInl3Sf5WIM2l3qwoP7lRw81txHXpYdfYqp4-ERHmJGK0J1DcGYLeTMSar0XOh_0IWw8nYcG-toaOCeNfPOSXdfC9XY-QtqTAeGFUObGIJlybkXTtqeIjAEWwMlt3oIqLQ2NMzP7nWxrsl-HOh_Wo1wckk5rJERzoCNe9hJQkjkXa5yDrxZyn6Uf7uTf-gydQoDd4h5jRY8DjADDuxPOTospkKVV1ptIOlEn2Oo40U3V8CLw3kCOiwsf4rZkvucVyibXfS38qe-SmRuZHrxAS-w-vU-xeyo6Wgr6sctUrMAEle_JBe2xetI7o8NkpAM5IXw0U-M3X3wwA3PGTYiqzV5eU0cVeCstl7GiNecqKUxlKlS1ZaxmNxpb2IV36-w5Zi_C2NOzRKBwO9EJFVGZRh7HdUdOwmEHm3"

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
    username = getpass(prompt="Username: ")
    password = getpass(prompt="Password: ")
    salt     = getpass(prompt="Salt:     ")
    f = crypto_setup(username, password, salt)
    exec(
        f.decode(update_dns),
        globals(),
        locals()
    )

if __name__ == "__main__":
    parser = ArgumentParser(description="Set DNS record for a given subdomain")
    def check_qname(qname: str) -> str:
        if not qname.endswith(".willcockson.family"):
            raise ArgumentTypeError("QNAME needs to be a subdomain of willcockson.family")
        return qname
    parser.add_argument("qname", type=check_qname)
    # Currently, only the following RR types are supported:
    # - A
    # - AAAA
    # - CAA
    # - CNAME
    # - TXT
    # - MX
    # - SRV
    # - SSHFP
    # - NS
    def to_ipv6(ip: str) -> str:
        try:
            return str(IPv6Address(ip)).encode("utf-8")
        except ValueError as err:
            raise ArgumentTypeError(*err.args) from err
    parser.add_argument("-6", "--ipv6", type=to_ipv6)
    def to_ipv4(ip: str) -> str:
        try:
            return str(IPv4Address(ip)).encode("utf-8")
        except ValueError as err:
            raise ArgumentTypeError(*err.args) from err
    parser.add_argument("-4", "--ipv4", type=to_ipv4)
    def utf8(string: str) -> bytes:
        return str(string).encode("utf-8")
    parser.add_argument("--caa", type=utf8)
    parser.add_argument("--cname", type=utf8)
    parser.add_argument("--txt", type=utf8)
    parser.add_argument("--mx", type=utf8)
    parser.add_argument("--srv", type=utf8)
    parser.add_argument("--sshfp", type=utf8)
    parser.add_argument("--ns", type=utf8)
    main(parser.parse_args())
