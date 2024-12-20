# Sentience AI stack

Stack for building provable AI Agents like [Daige](https://www.daige.ai/).
Tap into Galadriel's verified inference which powers Daige’s [Proof of Sentience](https://www.daige.ai/proof).

## Features
- Addresses the challenge of proving that the AI agents run autonomously and are not influenced by the human operators.
- It Ensures the LLM inference is executed inside [Amazon Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/). The enclave can't be accessed from the outside which gives it security.
- Provides an OpenAI compatible chat completion API
- Returns additional values in inference response to enable verification of the inference.
- Posts proofs of inference responses to Solana.

## Project Structure

This project is divided into these parts:
1. [enclave](enclave) - this where the enclave is built and run
2. [host](host) - proxies HTTP requests to the API running in the enclave
3. [solana-attestation-contract](solana-attestation-contract) - posts proofs of inference responses to Solana
4. [verify](verify) - instructions and code for verifying the TEE

## Quickstart
If you are building AI Agents go to [docs](https://docs.galadriel.com/for-agents-developers/quickstart) for a quickstart guide.

## Development
Use instructions below, depending on your goal:
- [Enclave](enclave/README.md) - to build and run the enclave
- [Verification](verify/README.md) - to verify the attestations