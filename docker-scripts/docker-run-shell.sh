#!/usr/bin/env bash

docker run --rm -it \
    --runtime=nvidia \
    --mount type=bind,source="$(pwd)"/experiments,target=/experiments \
    millionintegrals/baselines-experiments bash
