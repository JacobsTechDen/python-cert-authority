from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
import sys
import datetime

script_name = sys.argv[0]

if len(sys.argv) != 2:
    print("Usage: {} <common_name> <org_name> <town_name> <state_name> <country_initials>".format(script_name))
    sys.exit(1)

common_name = sys.argv[1]
org_name = sys.argv[2]
town_name = sys.argv[3]
state_name = sys.argv[4]
country_initials = sys.argv[5]

ca_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

ca_name = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, country_initials),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
    x509.NameAttribute(NameOID.LOCALITY_NAME, town_name),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
])

ca_cert = x509.CertificateBuilder().subject_name(
    ca_name
).issuer_name(
    ca_name
).public_key(
    ca_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.BasicConstraints(ca=True, path_length=None),
    critical=True,
).sign(
    private_key=ca_key,
    algorithm=hashes.SHA256(),
)

with open("ca_cert.pem", "wb") as f:
    f.write(ca_cert.public_bytes(Encoding.PEM))

with open("ca_key.pem", "wb") as f:
    f.write(ca_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))

with open("ca_cert.crt", "wb") as f:
    f.write(ca_cert.public_bytes(Encoding.PEM))

print("CA certificate and key generated.")
