import nacl from 'tweetnacl';

// Given values
// TODO: change to your values
const hash = "c847e98b1abf528f988c0253840616405a014ef2494e7a1b6c8d35e90413dd0a";
const signature = "68603b802f1e293dbf21bb1004bd08bca272fc70b6d00556f2a06b35949319533ad527c614c063836601aa00c8ca960dc600cad990df1ff8ff18079a09561d07";
const publicKey = "835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68";

// Decode the public key from hex
const publicKeyBytes = Buffer.from(publicKey, 'hex');

// Decode the message (hash) and signature from hex
const messageBytes = Buffer.from(hash, 'hex');
const signatureBytes = Buffer.from(signature, 'hex');

// Verify the signature
const isValid = nacl.sign.detached.verify(messageBytes, signatureBytes, publicKeyBytes);

if (isValid) {
  console.log("Signature is valid!");
} else {
  console.log("Signature is invalid!");
}