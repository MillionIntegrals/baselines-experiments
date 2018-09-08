FROM python:3.6 as builder
MAINTAINER Jerry Tworek

ARG vel_checkout

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN git clone https://github.com/MillionIntegrals/vel.git
WORKDIR "vel"
RUN git checkout $vel_checkout
RUN python setup.py bdist_wheel

FROM anibali/pytorch:cuda-9.2
MAINTAINER Jerry Tworek

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install some basic utilities
RUN sudo apt-get update && sudo apt-get install -y gcc && sudo rm -rf /var/lib/apt/lists/*

RUN pip install -U pip cython
COPY --from=builder /vel/dist/vel-0.1.1-py3-none-any.whl .
COPY .velproject.yaml .
