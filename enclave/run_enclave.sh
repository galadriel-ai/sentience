ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
[ "$ENCLAVE_ID" != "null" ] && nitro-cli terminate-enclave --enclave-id ${ENCLAVE_ID}

docker build \
  --label "org.opencontainers.image.source=https://github.com/galadriel-ai/aws-enclave" \
  --label "org.opencontainers.image.description=AWS Enclave Image" \
  --label "org.opencontainers.image.licenses=MIT" \
  ./ -t "galadriel:latest" --no-cache
rm galadriel.eif
nitro-cli build-enclave --docker-uri "galadriel:latest" --output-file "galadriel.eif"
nitro-cli run-enclave --cpu-count 2 --memory 7000 --eif-path galadriel.eif
#nitro-cli describe-enclaves
