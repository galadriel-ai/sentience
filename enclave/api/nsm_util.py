"""
This file is modified based on donkersgoed's repository (https://github.com/donkersgoed/nitropepper-enclave-app)
"""

import base64
from dataclasses import dataclass
from typing import Optional

import libnsm


class NSMUtil:
    """NSM util class."""

    def __init__(self):
        """Construct a new NSMUtil instance."""
        # Initialize the Rust NSM Library
        self._nsm_fd = libnsm.nsm_lib_init()  # pylint:disable=c-extension-no-member
        # Create a new random function `nsm_rand_func`, which
        # utilizes the NSM module.
        self.nsm_rand_func = lambda num_bytes: libnsm.nsm_get_random(
            # pylint:disable=c-extension-no-member
            self._nsm_fd,
            num_bytes,
        )

    def get_attestation_doc(self, public_key: bytes):
        """Get the attestation document from /dev/nsm."""
        libnsm_att_doc_cose_signed = libnsm.nsm_get_attestation_doc(
            # pylint:disable=c-extension-no-member
            self._nsm_fd,
            public_key,
            len(public_key),
        )
        return libnsm_att_doc_cose_signed

    def decrypt(self, ciphertext):
        """
        Decrypt ciphertext using private key
        """

        # TODO: is this needed?
        cipher = PKCS1_OAEP.new(self._rsa_key)
        plaintext = cipher.decrypt(ciphertext)

        return plaintext.decode()
