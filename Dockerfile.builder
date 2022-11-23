FROM python:3.11.0-slim

RUN  pip install 'poetry==1.2.2' \
  && apt-get update -y \
  && apt-get install -y curl \
  && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
  && apt-get install -y nodejs

WORKDIR /soundations

ENTRYPOINT [ "/bin/bash", "-c" ]
