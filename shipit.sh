#!/bin/sh

REGION=eu-north-1
VERSION=$1
PATH_TO_AWS=$2

docker build . -f Dockerfile_singleinstance -t dagster/dagit_service:$VERSION

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $PATH_TO_AWS

docker tag dagster/dagit_service:$VERSION $PATH_TO_AWS/dagster/dagit_service:$VERSION

docker push $PATH_TO_AWS/dagster/dagit_service:$VERSION
