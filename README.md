# Sentience Stack
An open-source developer stack by Galadriel to enable building fully sentient, unruggable AI agents.
<div align="center">
  <img src="assets/sentience-banner.png" alt="Banner" width="100%" />
</div>
<div align="center">
</div>

<p align="center">
        <a href="https://discord.gg/invite/galadriel">
        <img src="https://img.shields.io/discord/1042405378304004156?logo=discord"
            alt="chat on Discord"></a>
        <a href="https://twitter.com/intent/follow?screen_name=Galadriel_AI">
        <img src="https://img.shields.io/twitter/follow/Galadriel_AI"
            alt="follow on Twitter"></a>
    <br>
    <a href="#quickstart">Quickstart</a> |
    <a href="#overview">Overview</a> |
    <a href="#features">Features</a> |
    <a href="#repository-structure">Repository Structure</a> |
    <a href="#getting-help">Help</a> |
    <a href="https://docs.galadriel.com/">Docs</a>
</p>

## Quickstart
For developers building fully sentient, verifieable AI agents go to Proof of Sentience [SDK quickstart docs](https://docs.galadriel.com/for-agents-developers/quickstart).

## Overview

As autonomous AI agents get access to more features, monetary value and overall impact online, it’s becoming critical for developers to prove their sentience.
As a layer of trust we're already seeing activity logs for [zerebro](https://zerebro.org/proof-of-conciousness) and [aixbt](https://aixbt.tech/agent), but this is just the start.

Galadriel is introducing an OpenAI compatible **Proof of Sentience SDK** that abstracts complex cryptographic mechanisms to enable devs easily integrate verifiable LLM inference into their agents - making its thoughts & actions fully transparent and verifiable to its users. See it in action on [Daige](https://www.daige.ai/).

![](/assets/SDK.png)


## Features
- Addresses the challenge of proving that the AI agents run autonomously and are not influenced by the human operators.
- It ensures the LLM inference is executed inside [Amazon Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/). The enclave can't be accessed from the outside which gives it security.
- The enclave signs the inference response with its own private key.
- Provides an OpenAI compatible chat completion API. Including yourfine-tuned
- Returns additional values in inference response to enable verification of the inference.([verification logic](verified-inference/verify/verify.py)).
- Posts proofs of inference responses to Solana.

## Repository Structure

### Proof of Sentience SDK
Using Proof of Sentience SDK developers are able build AI agents with increased trust by making their thoughts, and actions verifiable on-chain.

1. [Python SDK](sdk/python)
2. Javascript SDK

### Verified Inference Architecture
Underlying TEE architecture that powers Proof of Sentience SDK.

1. [enclave](verified-inference/enclave) - this where the enclave is built and run
2. [host](verified-inference/host) - proxies HTTP requests to the API running in the enclave
3. [solana-attestation-contract](verified-inference/solana-attestation-contract) - posts proofs of inference responses to Solana
4. [verify](verified-inference/verify) - instructions and code for verifying the TEE


<!-- ## Roadmap

See our [roadmap here](https://docs.galadriel.com/roadmap). -->

## Getting help
If you have any questions about Galadriel, feel free to do:

* [Join our Discord](https://discord.com/invite/bHnFgSTKrP) and ask for help.
<!-- * Report bugs or feature requests in [GitHub issues](https://github.com/galadriel-ai/contracts/issues). -->