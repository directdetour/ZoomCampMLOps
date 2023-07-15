#!/usr/bin/env bash

docker-compose up -d

sleep 5

# setup envs
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://localhost:4566"

# create localstack bucket
aws --endpoint-url="${S3_ENDPOINT_URL}" s3 mb s3://nyc-duration

# run tests
pipenv run python integration_test.py

ERRORCODE=$?

if [ ${ERRORCODE} != 0 ]; then
    docker-compose logs    
fi

docker-compose down
echo "Tests Successful"
exit ${ERRORCODE}
