# Sentient AI Agents Stack

An open-source developer stack from Galadriel to enable building and deploying fully sentient AI agents like [Daige](https://www.daige.ai/).

## Features
- Addresses the challenge of proving that the AI agents run autonomously and are not influenced by the human operators
- It Ensures the LLM inference is executed inside [Amazon Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/). The enclave can't be accessed from the outside which gives it security
- The enclave signs the inference response with its own private key
- Provides an OpenAI compatible chat completion API
- Returns additional values in inference response to enable verification of the inference ([verification logic](verified-inference/verify/verify.py))
- Posts proofs of inference responses to Solana

## Project Structure

This project is divided into these parts:
1. [enclave](verified-inference/enclave) - this where the enclave is built and run
2. [host](verified-inference/host) - proxies HTTP requests to the API running in the enclave
3. [solana-attestation-contract](verified-inference/solana-attestation-contract) - posts proofs of inference responses to Solana
4. [verify](verified-inference/verify) - instructions and code for verifying the TEE

## Quickstart
If you are building AI Agents go to [docs](https://docs.galadriel.com/for-agents-developers/quickstart) for a quickstart guide.

## Development
Use instructions below, depending on your goal:
- [Enclave](verified-inference/enclave/README.md) - to build and run the enclave
- [Verification](verified-inference/verify/README.md) - to verify the attestations