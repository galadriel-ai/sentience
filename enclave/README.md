# Setup

```shell
sudo yum update -y
sudo yum install git python3-pip -y
sudo yum install aws-nitro-enclaves-cli-1.2.2-0.amzn2023 -y
sudo yum install aws-nitro-enclaves-cli-devel-1.2.2-0.amzn2023 -y
sudo yum install docker-24.0.5-1.amzn2023.0.1 -y
sudo systemctl enable --now nitro-enclaves-allocator.service
sudo systemctl enable --now docker

sudo usermod -aG ne $USER
sudo usermod -aG docker $USER
```

Verify that dependencies installed and reboot the machine:

```
nitro-cli --version
docker --version
sudo reboot
```

```shell
sudo systemctl start nitro-enclaves-allocator.service \
  && sudo systemctl enable nitro-enclaves-allocator.service
  
```

# Running

Make sure that submodules have been updated:

```
git submodule update --init --recursive
git submodule update --remote --merge
```