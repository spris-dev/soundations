FROM python:3.11.0-slim

ARG USER_ID
ARG GROUP_ID

RUN  pip install 'poetry==1.2.2' \
  && apt-get update -y \
  && apt-get install -y curl \
  && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
  && apt-get install -y nodejs

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

WORKDIR /soundations

ENTRYPOINT [ "/bin/bash", "-c" ]
