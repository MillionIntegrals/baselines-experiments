#!/usr/bin/env bash

docker run --rm -it \
    --runtime=nvidia \
    --mount type=bind,source=/experiments,target=/experiments \
    millionintegrals/baselines-experiments bash
