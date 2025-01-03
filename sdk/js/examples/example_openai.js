const OpenAI = require('openai');

const client = new OpenAI({
    apiKey: process.env['GALADRIEL_API_KEY'], // This is the default and can be omitted
    baseURL: "https://api.galadriel.com/v1/verified",
});

async function main() {
    const chatCompletion = await client.chat.completions.create({
        messages: [{role: 'user', content: 'Say this is a test'}],
        model: 'gpt-4o',
    });
    console.log("chatCompletion:", chatCompletion)
}

main();