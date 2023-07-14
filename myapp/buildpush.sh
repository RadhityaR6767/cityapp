#!/bin/bash


FP=$1

(
set -e
docker build -t cityapp:v$1 .
docker tag cityapp:v$1 rchronic/cityapp:v$1
docker push rchronic/cityapp:v$1
)
