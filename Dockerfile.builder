FROM alpine:20220715

RUN  apk add --no-cache gcc g++ musl-dev \
  && apk add --no-cache bash \
  && apk add --no-cache poetry \
  && apk add --no-cache npm \
  && apk add --no-cache python3-dev && ln -sf python3 /usr/bin/python \
  && find /usr/lib -type d -regex .*__pycache__ | xargs rm -rf

WORKDIR /soundations

ENTRYPOINT [ "/bin/bash", "-c" ]
