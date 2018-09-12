#!/usr/bin/env bash

shift
docker run --rm -it \
    --runtime=nvidia \
    --mount type=bind,source=/experiments,target=/experiments \
    millionintegrals/baselines-experiments \
    vel atari/a2c/breakout_a2c.yaml train "$@"
