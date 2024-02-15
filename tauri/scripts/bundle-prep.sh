#!/bin/bash

pushd $(dirname $0)/..

mkdir -p ./src-tauri/assets
cp ../docker-compose.yml ./src-tauri/assets/docker-compose.yml
popd