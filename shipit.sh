#!/bin/sh

REGION=eu-north-1
VERSION=$1
AWS_PATH=$2

docker build . -f Dockerfile_singeinstance -t dagster/dagit_service:$VERSION

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_PATH

docker tag dagster/dagit_service:$VERSION $AWS_PATH/dagster/dagit_service:$VERSION

docker push $AWS_PATH/dagster/dagit_service:$VERSION