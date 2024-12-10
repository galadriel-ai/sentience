import cbor2
import cose
import base64
import json

from cose import EC2, CoseAlgorithms, CoseEllipticCurves
from Crypto.Util.number import long_to_bytes
from OpenSSL import crypto

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def verify_attestation_doc(attestation_doc, pcrs=[], root_cert_pem=None):
    """
    Verify the attestation document
    If invalid, raise an exception
    """
    # Decode CBOR attestation document
    data = cbor2.loads(attestation_doc)

    # Load and decode document payload
    doc = data[2]
    doc_obj = cbor2.loads(doc)

    # Get PCRs from attestation document
    document_pcrs_arr = doc_obj['pcrs']

    # Part 1: Validating PCRs
    for index, pcr in enumerate(pcrs):
        # Attestation document doesn't have specified PCR, raise exception
        if index not in document_pcrs_arr or document_pcrs_arr[index] is None:
            raise Exception("Wrong PCR%s" % index)

        # Get PCR hexcode
        doc_pcr = document_pcrs_arr[index].hex()

        # Check if PCR match
        if pcr != doc_pcr:
            raise Exception("Wrong PCR%s" % index)

    # Part 2: Validating signature

    # Get signing certificate from attestation document
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, doc_obj['certificate'])

    # Get the key parameters from the cert public key
    cert_public_numbers = cert.get_pubkey().to_cryptography_key().public_numbers()
    x = cert_public_numbers.x
    y = cert_public_numbers.y
    curve = cert_public_numbers.curve

    x = long_to_bytes(x)
    y = long_to_bytes(y)

    # Create the EC2 key from public key parameters
    key = EC2(alg=CoseAlgorithms.ES384, x=x, y=y, crv=CoseEllipticCurves.P_384)

    # Get the protected header from attestation document
    phdr = cbor2.loads(data[0])

    # Construct the Sign1 message
    msg = cose.Sign1Message(phdr=phdr, uhdr=data[1], payload=doc)
    msg.signature = data[3]

    # Verify the signature using the EC2 key
    if not msg.verify_signature(key):
        raise Exception("Wrong signature")

    # Part 3: Validating signing certificate PKI
    if root_cert_pem is not None:
        # Create an X509Store object for the CA bundles
        store = crypto.X509Store()

        # Create the CA cert object from PEM string, and store into X509Store
        _cert = crypto.load_certificate(crypto.FILETYPE_PEM, root_cert_pem)
        store.add_cert(_cert)

        # Get the CA bundle from attestation document and store into X509Store
        # Except the first certificate, which is the root certificate
        for _cert_binary in doc_obj['cabundle'][1:]:
            _cert = crypto.load_certificate(crypto.FILETYPE_ASN1, _cert_binary)
            store.add_cert(_cert)

        # Get the X509Store context
        store_ctx = crypto.X509StoreContext(store, cert)

        # Validate the certificate
        # If the cert is invalid, it will raise exception
        store_ctx.verify_certificate()
    return


def encrypt(attestation_doc, plaintext):
    """
    Encrypt message using public key in attestation document
    """

    # Decode CBOR attestation document
    data = cbor2.loads(attestation_doc)

    # Load and decode document payload
    doc = data[2]
    doc_obj = cbor2.loads(doc)

    # Get the public key from attestation document
    public_key_byte = doc_obj['public_key']
    public_key = RSA.import_key(public_key_byte)

    # Encrypt the plaintext with the public key and encode the cipher text in base64
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(str.encode(plaintext))

    return base64.b64encode(ciphertext).decode()


def get_public_key(attestation_doc):
    data = cbor2.loads(attestation_doc)

    # Load and decode document payload
    doc = data[2]
    doc_obj = cbor2.loads(doc)

    # Get the public key from attestation document
    public_key_byte = doc_obj['public_key']
    return public_key_byte


def decode_public_key(public_key):
    try:
        public_key = serialization.load_der_public_key(
            public_key,
            backend=default_backend()
        )
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode()
    except ValueError as e:
        print(f"Error decoding data: {e}")
