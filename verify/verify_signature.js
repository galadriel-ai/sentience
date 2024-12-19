import nacl from 'tweetnacl';
import bs58 from 'bs58';

// Given values
// TODO: fix with your values
const hashHex = "ce855e4a2c6fc713c3c5b629ada24cf119f8ed37cce719c8b51ef1841206b020";
const signatureHex = "afb7252df102fd4fd15e2791fe5170dad4b9d775eb5ac31cc6a9c040d62bb673e0e481128f5c4e0a1f8c031298278e57710525222a4f8029270f4e10017c6901";
const publicKeyBase58 = "Dp2k554Ebsij5RjuhjsZujVW2bJnQzfb43VYZSQ4NZo1";

// Decode the public key from Base58
const publicKeyBytes = bs58.decode(publicKeyBase58);

// Decode the message (hash) and signature from hex
const messageBytes = Buffer.from(hashHex, 'hex');
const signatureBytes = Buffer.from(signatureHex, 'hex');

// Verify the signature
const isValid = nacl.sign.detached.verify(messageBytes, signatureBytes, publicKeyBytes);

if (isValid) {
  console.log("Signature is valid!");
} else {
  console.log("Signature is invalid!");
}