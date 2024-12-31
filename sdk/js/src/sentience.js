import nacl from 'tweetnacl';

export default class Sentience {

    static verifySignature(completion) {
        // Check if required fields are present
        if (!_isInputWithAllFields(completion)) {
            return false;
        }

        // Decode the public key from hex
        const publicKeyBytes = _getPublicKey(completion);
        if (!publicKeyBytes) {
            return false;
        }

        // Decode the hash (message) and signature from hex
        const messageBytes = Buffer.from(completion.hash, 'hex');
        const signatureBytes = Buffer.from(completion.signature, 'hex');

        try {
            // tweetnacl's sign.detached.verify returns a boolean
            // indicating whether the signature is valid.
            return nacl.sign.detached.verify(messageBytes, signatureBytes, publicKeyBytes);
        } catch (error) {
            // If any error occurs, treat it as a failed verification
            return false;
        }
    }
}

/**
 * Checks whether the completion object has the required fields.
 *
 * @param {Object} completion
 * @returns {boolean}
 */
function _isInputWithAllFields(completion) {
    try {
        return completion.public_key && completion.hash && completion.signature;
    } catch (error) {
        return false;
    }
}

/**
 * Decodes the public key from hex.
 *
 * @param {Object} completion
 * @returns {Uint8Array|null}
 */
function _getPublicKey(completion) {
    try {
        return Buffer.from(completion.public_key, 'hex');
    } catch (error) {
        return null;
    }
}