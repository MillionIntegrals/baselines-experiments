FROM millionintegrals/vel
MAINTAINER Jerry Tworek

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

USER user

VOLUME /experiments
WORKDIR /experiments

