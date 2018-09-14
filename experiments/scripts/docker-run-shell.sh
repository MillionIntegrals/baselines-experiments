#!/usr/bin/env bash

docker run --rm -it \
    --runtime=nvidia \
    --mount type=bind,source=$(realpath .),target=/experiments \
    millionintegrals/baselines-experiments bash
