# Attestation Verification

This directory contains instructions and code for verifying the TEE.

Here's a high-level diagram of the steps needed to fully verify the oracle:

![](/verification-diagram2.png)

1. Verify that the code was converted to the docker image correctly. Docker image building can be non deterministic that can introduce errors.
2. Verify that the docker image was converted into the enclave image correctly. Enclave image is always created with a hash (PCR0) that proves that the code from step 1 is now inside the enclave image.
3. Verify TEE attestation that you got from a verified inference request and checking that it is indeed correctly signed by AWS, and that it corresponds to the enclave image hash.

We explain below how to execute both verification steps below. 

### 0. Prerequisites

System requirements:

* An AWS EC2 instance with Nitro Enclave support (we have tested on `m5.xlarge` EC2 instance).
    * You must enable the "Nitro Enclave enabled" option when creating the instance
    * Amazon Linux (tested on `Amazon Linux 2023 AMI 2023.3.20240312.0 x86_64 HVM kernel-6.1`)
    * x86_64 architecture CPU
    * It is easiest to use an EC2 image with Docker and `nitro-cli` installed
    * If you want to support a different linux distro, you need additional configuration
    * If the Nitro Enclave kernel driver is not included on chosen linux kernel, it needs to be installed manually. See more [here](https://github.com/aws/aws-nitro-enclaves-cli/blob/main/docs/ubuntu_20.04_how_to_install_nitro_cli_from_github_sources.md)


For Amazon Linux:

```shell
sudo yum update -y
sudo dnf install aws-nitro-enclaves-cli -y
sudo dnf install aws-nitro-enclaves-cli-devel -y
sudo systemctl enable --now nitro-enclaves-allocator.service
sudo usermod -aG ne $USER

sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker $(whoami)

sudo yum install python-pip -y

sudo reboot
```

### 1. Create the docker image (Optional)

This step can be non deterministic in certain scenarios. To make sure that you are working with exactly the same docker image you can also pull it from the docker hub.

```shell
cd ../enclave
docker build -t aws_enclave .
```

### 2. Create the enclave image

```shell
cd ../verify
nitro-cli build-enclave --docker-uri "ghcr.io/galadriel-ai/aws_enclave:v0.0.2" --output-file "galadriel.eif"
```

You need to get exactly the same hashes:

```shell
Enclave Image successfully created.
{
  "Measurements": {
    "HashAlgorithm": "Sha384 { ... }",
    "PCR0": "b3a233e8a1d2682455777643d5a793c9d231754ebd89e8ffc14b07a21da0de07920763e87f8cc6eb3a6d362beeb4f541",
    "PCR1": "52b919754e1643f4027eeee8ec39cc4a2cb931723de0c93ce5cc8d407467dc4302e86490c01c0d755acfe10dbf657546",
    "PCR2": "3bf7565751ec5865be41221c62fc7e69429a0d9a219a91ba858fd4b2fa31fac6cc416d5eca29cc9405a83749c896e494"
  }
}
```

### Setup Python

```shell
pip install -r requirements.txt
```

### 3. Verify attestation

Optionally, you can download the root.pem from Amazon and verify it is the same 
as the `root.pem` in this repo: https://aws-nitro-enclaves.amazonaws.com/AWS_NitroEnclaves_Root-G1.zip

**Verify with pcr0 hash**  
This uses the `attestation_doc_b64.txt` file
```shell
# The argument is the PCR0 from the enclave image build step.
python3 verify.py --pcr0_hash b3a233e8a1d2682455777643d5a793c9d231754ebd89e8ffc14b07a21da0de07920763e87f8cc6eb3a6d362beeb4f541
```

Congratulations! You have now successfully verified the attestation. This means that the code inside the TEE is exactly the same as in ../enclave sub folder and will be executed exactly as intended without any way for Galadriel to interfere.

All LLM inferences coming out of the TEE are signed by the private key inside the enclave. The corresponding public key is exported together with attestation and signed by AWS. If the public key is known you can now easily verify the LLM response signatures.

# Verify Signatures

In Python:
```shell
# Edit the verify_signature.py variables (hash, signature, publick_key)
python verify_signature.py
```

In Javascript:
```shell
# Edit the verify_signature.js variables (hash, signature, publick_key)
node verify_signature.js
```