FROM ubuntu:focal
LABEL maintainer "Delimbetov Kirill <1starfall1@gmail.com>"

# use bash so commands like source work
SHELL ["/bin/bash", "-c"]

# prepare directory
ENV PROJECT_DIR=/project
ENV TMP_DIR=$PROJECT_DIR/tmp
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# get deps
## pillow deps
# RUN apt-get update && apt-get install -y \
#     libjpeg8-dev zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev libopenjp2-7-dev

## python
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3.9-venv \
    python3.9-distutils

## other deps
RUN apt-get install -y curl

## pip
RUN mkdir -p $TMP_DIR
WORKDIR $TMP_DIR
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
WORKDIR $PROJECT_DIR

# init venv
RUN python3.9 -m venv venv
RUN source ./venv/bin/activate

# copy relevant data from build context
COPY ./ $PROJECT_DIR/

# get pip deps
RUN pip3.9 install --upgrade pip
RUN pip3.9 install wheel setuptools
RUN pip3.9 install -r ./requirements.txt

# Run
ENTRYPOINT ["python3.9", "main.py"]
CMD ["api id", "api hash", "bot token"]

