FROM fedora:36

WORKDIR /soundations

RUN dnf module install -y nodejs:16
RUN dnf install -y python3-pip
RUN pip install poetry
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY ./pyproject.toml ./poetry.lock /soundations/
RUN poetry install --only dev

ENTRYPOINT [ "/bin/bash", "-c" ]
