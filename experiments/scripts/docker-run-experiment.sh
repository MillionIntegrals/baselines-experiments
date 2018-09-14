#!/usr/bin/env bash

docker run --rm \
    --runtime=nvidia \
    --mount type=bind,source=$(realpath .),target=/experiments \
    millionintegrals/baselines-experiments \
    vel "$@"
