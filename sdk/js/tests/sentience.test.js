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

describe('Sentience.getHistory', () => {
    beforeEach(() => {
        // Mock global fetch before each test
        global.fetch = jest.fn();
    });

    afterEach(() => {
        // Reset all mocks after each test to ensure a clean slate
        jest.resetAllMocks();
    });

    it('should call fetch with limit=100 if limit is undefined', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey);

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            'https://api.galadriel.com/v1/verified/chat/completions?limit=100',
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

    it('should call fetch with limit=100 if limit is 0 or negative', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey, 0);
        await Sentience.getHistory(mockApiKey, -5);

        // Assert
        expect(global.fetch).toHaveBeenNthCalledWith(
            1,
            'https://api.galadriel.com/v1/verified/chat/completions?limit=100',
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
        expect(global.fetch).toHaveBeenNthCalledWith(
            2,
            'https://api.galadriel.com/v1/verified/chat/completions?limit=100',
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

    it('should call fetch with provided limit if limit is a positive number', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        const mockLimit = 50;
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey, mockLimit);

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            `https://api.galadriel.com/v1/verified/chat/completions?limit=${mockLimit}`,
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

    it('should call fetch without invalid filter', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        const mockLimit = 50;
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey, mockLimit, null, "invalidFilter");

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            `https://api.galadriel.com/v1/verified/chat/completions?limit=${mockLimit}`,
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

    it('should call fetch with provided filter mine', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        const mockLimit = 50;
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey, mockLimit, null, "mine");

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            `https://api.galadriel.com/v1/verified/chat/completions?limit=${mockLimit}&filter=mine`,
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

    it('should call fetch with provided filter all', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        const mockLimit = 50;
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey, mockLimit, null, "all");

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            `https://api.galadriel.com/v1/verified/chat/completions?limit=${mockLimit}&filter=all`,
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

    it('should return JSON data when response is ok', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        const mockResponse = {data: ['item1', 'item2']};
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => mockResponse,
        });

        // Act
        const result = await Sentience.getHistory(mockApiKey, 20);

        // Assert
        expect(result).toEqual(mockResponse);
    });

    it('should throw an error when response is not ok', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        global.fetch.mockResolvedValue({
            ok: false,
            status: 404,
            json: async () => ({}),
        });

        // Act & Assert
        await expect(Sentience.getHistory(mockApiKey, 20)).rejects.toThrow(
            'HTTP error! Status: 404'
        );
    });

    it('should call fetch with cursor if cursor is defined', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getHistory(mockApiKey, 100, "mockCursor");

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            'https://api.galadriel.com/v1/verified/chat/completions?limit=100&cursor=mockCursor',
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });

});

describe('Sentience.getByHash', () => {
    beforeEach(() => {
        // Mock global fetch before each test
        global.fetch = jest.fn();
    });

    afterEach(() => {
        // Reset all mocks after each test to ensure a clean slate
        jest.resetAllMocks();
    });

    it('should call fetch with correct url and hash', async () => {
        // Arrange
        const mockApiKey = 'test-api-key';
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({data: []}),
        });

        // Act
        await Sentience.getByHash(mockApiKey, "mockHash");

        // Assert
        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(global.fetch).toHaveBeenCalledWith(
            'https://api.galadriel.com/v1/verified/chat/completions/mockHash',
            expect.objectContaining({
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${mockApiKey}`,
                },
            })
        );
    });
});
