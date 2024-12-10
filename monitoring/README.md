# Enclave Monitoring Service

This service is a FastAPI application that provides system metrics from an enclave environment, exposed via a REST API. The service can be managed using two simple shell scripts to start and stop the server.

## Installation

```bash
cd monitoring
pip3 install -r requirements.txt
```

## Running the service

```bash
./run_monitoring_service.sh
```

## Stopping the service

```bash
./stop_monitoring_service.sh
```


## Usage

Once the service is running, you can access the metrics at:

```bash
http://localhost:9101/metrics
```

This endpoint will provide system metrics in Prometheus format, which can be used for monitoring and alerting purposes.