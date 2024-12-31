//const Sentience = require('../src/sentience');
const Sentience = require('../sentience.min.js');

const EXAMPLE_VALID = {
    hash: '5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc7',
    public_key: '835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68',
    signature: '819218f6ad5a8ec86091afc1dfbecc5d21384d62f1df0c649ab0c351e515e825fda72d124091418b3cc4a3be35b20dd471b8f8447a448712315b19ecaef34206',
}

const EXAMPLE_INVALID_HASH = {
    hash: '5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc8',
    public_key: '835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68',
    signature: '819218f6ad5a8ec86091afc1dfbecc5d21384d62f1df0c649ab0c351e515e825fda72d124091418b3cc4a3be35b20dd471b8f8447a448712315b19ecaef34206',
}

const EXAMPLE_INVALID_PUBLIC_KEY = {
    hash: '5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc7',
    public_key: '835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e69',
    signature: '819218f6ad5a8ec86091afc1dfbecc5d21384d62f1df0c649ab0c351e515e825fda72d124091418b3cc4a3be35b20dd471b8f8447a448712315b19ecaef34206',
}

const EXAMPLE_INVALID_SIGNATURE = {
    hash: '5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc7',
    public_key: '835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68',
    signature: '819218f6ad5a8ec86091afc1dfbecc5d21384d62f1df0c649ab0c351e515e825fda72d124091418b3cc4a3be35b20dd471b8f8447a448712315b19ecaef34207',
}

describe('verifySignature', () => {
    it('returns false for empty', () => {
        expect(Sentience.verifySignature("")).toBe(false);
    })
    it('returns false for random', () => {
        expect(Sentience.verifySignature("abc")).toBe(false);
    })
    it('returns false for a dict', () => {
        expect(Sentience.verifySignature({"abc": "def"})).toBe(false);
    })
    it('returns false for invalid hash', () => {
        expect(Sentience.verifySignature(EXAMPLE_INVALID_HASH)).toBe(false);
    })
    it('returns false for invalid public key', () => {
        expect(Sentience.verifySignature(EXAMPLE_INVALID_PUBLIC_KEY)).toBe(false);
    })
    it('returns false for invalid signature', () => {
        expect(Sentience.verifySignature(EXAMPLE_INVALID_SIGNATURE)).toBe(false);
    })
    it('returns true for valid', () => {
        expect(Sentience.verifySignature(EXAMPLE_VALID)).toBe(true);
    })
});