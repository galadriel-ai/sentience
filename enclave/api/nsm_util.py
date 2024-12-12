"""
This file is modified based on donkersgoed's repository (https://github.com/donkersgoed/nitropepper-enclave-app)
"""

from dataclasses import dataclass

try:
    import libnsm
except ImportError:
    print("NSMUtil not found, mocking attestation")


class NSMUtil:
    """NSM util class."""

    def __init__(self):
        """Construct a new NSMUtil instance."""
        # Initialize the Rust NSM Library
        try:
            self._nsm_fd = libnsm.nsm_lib_init()  # pylint:disable=c-extension-no-member
            # Create a new random function `nsm_rand_func`, which
            # utilizes the NSM module.
            self.nsm_rand_func = lambda num_bytes: libnsm.nsm_get_random(
                # pylint:disable=c-extension-no-member
                self._nsm_fd,
                num_bytes,
            )
        except NameError:
            print("NSMUtil not found, mocking attestation")

    def get_attestation_doc(self, public_key: bytes) -> bytes:
        """Get the attestation document from /dev/nsm."""
        try:
            libnsm_att_doc_cose_signed = libnsm.nsm_get_attestation_doc(
                # pylint:disable=c-extension-no-member
                self._nsm_fd,
                public_key,
                len(public_key),
            )
            return libnsm_att_doc_cose_signed
        except NameError:
            print("NSMUtil not found, mocking attestation")
            return b"mocked_attestation_doc"
