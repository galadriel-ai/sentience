FROM amazonlinux:2023.3.20240219.0

# Install python for running the server and net-tools for modifying network config
RUN yum update -y
RUN yum groupinstall "Development Tools" -y
RUN yum install openssl-devel bzip2-devel libffi-devel wget net-tools git iproute dnsmasq -y
# stop DNS service (just in case)
RUN systemctl disable systemd-resolved

WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
RUN tar -xf Python-3.10.4.tgz
RUN cd Python-3.10.4/ && ./configure --enable-optimizations
RUN cd Python-3.10.4/ && make -j $(nproc)
RUN cd Python-3.10.4/ && make altinstall

# TODO: do we need rust?
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# RUN echo export PATH="$HOME/.cargo/bin:$PATH" >> /root/.bashrc

WORKDIR /app

COPY requirements.txt ./
RUN python3.10 -m pip install -r /app/requirements.txt

COPY server.py ./
COPY NsmUtil.py ./
COPY run.sh ./
COPY libnsm.so ./
COPY traffic_forwarder.py ./
COPY settings.py ./
COPY guess_encoding.py ./
COPY oracle_ping_for_funds.py ./
COPY key_manager.py ./
COPY oracles/oracles ./oracles

# TODO: debug only
COPY proxy_checks ./proxy_checks/
COPY check_proxies.py ./

COPY dnsmasq.conf /etc/dnsmasq.conf

RUN chmod +x run.sh

CMD ["/app/run.sh"]
