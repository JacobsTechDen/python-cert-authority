from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import sys
import datetime

script_name = sys.argv[0]

# Check if a domain name argument is provided
if len(sys.argv) != 2:
    print("Usage: {} <domain_name>".format(script_name))
    sys.exit(1)

domain_name = sys.argv[1]

# Load the CA certificate and key
with open("ca_cert.pem", "rb") as f:
    ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())

with open("ca_key.pem", "rb") as f:
    ca_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

# Generate a private key for the server
server_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Create a certificate signing request (CSR) for the server
server_name = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, domain_name),
])

csr = x509.CertificateSigningRequestBuilder().subject_name(
    server_name
).sign(
    private_key=server_key,
    algorithm=hashes.SHA256(),
)

# Sign the CSR with the CA to generate the server certificate
server_cert = x509.CertificateBuilder().subject_name(
    csr.subject
).issuer_name(
    ca_cert.subject
).public_key(
    csr.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).sign(
    private_key=ca_key,
    algorithm=hashes.SHA256(),
)

# Save the server certificate and private key
with open(domain_name+".pem", "wb") as f:
    f.write(server_cert.public_bytes(Encoding.PEM))

with open(domain_name+"_key.pem", "wb") as f:
    f.write(server_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))

# Save the certificate and key as .crt files
with open(domain_name+".crt", "wb") as f:
    f.write(server_cert.public_bytes(Encoding.PEM))

print("Server certificate and key generated.")
