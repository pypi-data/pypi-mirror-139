from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate, X509, X509Name, PKey, TYPE_RSA, X509Req, dump_privatekey, X509Extension)
import sys
import os


def create_self_signed_cert(dump_directory, CN, O, OU, L, ST, C, email):
    """
    Set the serial number of the certificate.

    :param dump_directory: path where keys should be stored
    :type string: :py:class:`str`
    :param CN: fqdn of your site.
    :type string: :py:class:`str`
    :param O: Organization name.
    :type string: :py:class:`str`
    :param OU: Department (Organizational Unit).
    :type string: :py:class:`str`
    :param L: City.
    :type string: :py:class:`str`
     :param ST: State.
    :type string: :py:class:`str`
    :param C: Country.
    :type string: :py:class:`str`
     :param email: Your email.
    :type string: :py:class:`str`

    :return: :py:data`None`
    """
    os.chdir(sys.path[0])
    # private_key_path = re.sub(r".(pem|crt)$", ".key", cert_file_path, flags=re.IGNORECASE)
    private_key_path = (os.path.join(dump_directory, "auth-key.pem"))
    cert_file_path = (os.path.join(dump_directory, "auth-cert.pem"))
    # create public/private key
    key = PKey()
    key.generate_key(TYPE_RSA, 4096)

    # Self-signed cert
    cert = X509()

    # subject = X509Name(cert.get_subject())
    subject = cert.get_subject()
    subject.CN = CN
    subject.O = O
    subject.OU = OU
    subject.L = L
    subject.ST = ST
    subject.C = C
    subject.emailAddress = email

    cert.set_version(2)
    cert.set_issuer(subject)
    cert.set_subject(subject)
    cert.set_serial_number(int.from_bytes(os.urandom(16), byteorder="big"))
    # cert.set_serial_number(int(rand.bytes(16).encode('hex'), 16))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    with open(cert_file_path, 'wb+') as f:
        f.write(dump_certificate(FILETYPE_PEM, cert))
    with open(private_key_path, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))


if __name__ == "__main__":
    file_name = "example-cert.pem"
    CN = 'localhost'
    O = 'XYZ Widgets Inc'
    OU = 'IT Department'
    L = 'Seattle'
    ST = 'Washington'
    C = 'US'
    emailAddress = 'e@example.com'

    create_self_signed_cert(file_name, CN, O, OU, L, ST, C, emailAddress)